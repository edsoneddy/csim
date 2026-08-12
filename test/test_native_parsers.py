"""Verify the native (C++) parsers are equivalent to the pure-Python ones.

Speed is not the property under test here: every test asserts that switching
the parser leaves csim's *output* untouched, at each stage of the pipeline
(raw tree -> Normalize -> PruneAndHash -> similarity).
"""

import os

import pytest

from csim import Compare
from csim.native import is_available
from csim.processing.tree_processing import Normalize, PruneAndHash
from csim.utils import group_by_exhaustive_search, report_pairwise_similarity


NATIVE_LANGS = ["java_20", "java_24", "cpp_14"]


JAVA_SAMPLES = {
    "simple": "public class A { void m() { int x = 1; } }",
    "generics": (
        "public class B<T extends Comparable<T>> { java.util.List<T> xs;"
        " T get(int i){ return xs.get(i); } }"
    ),
    "control": (
        "public class C { int f(int n){ if(n<=1) return 1;"
        " for(int i=0;i<n;i++){ n+=i; } while(n>0){ n--; } return n; } }"
    ),
    "nested": (
        "public class D { class E { void p(){ System.out.println(\"x\"); } }"
        " static void main(String[] a){ new D().new E().p(); } }"
    ),
    "lambda": (
        "import java.util.function.*; public class F {"
        " Function<Integer,Integer> f = x -> x*2; void g(){ f.apply(3); } }"
    ),
    "compound_assign": (
        "public class G { void m(){ int x = 1; x += 2; x *= 3; x -= 1; } }"
    ),
}

CPP_SAMPLES = {
    "simple": "int main() { int x = 1; return 0; }",
    "template": (
        "template<typename T> class N { public: T v; N(T x):v(x){} };"
        " int main(){ N<int> n(5); return 0; }"
    ),
    "stl": (
        "#include <vector>\nint main(){ std::vector<int> v;"
        " for(int i=0;i<10;i++) v.push_back(i); return 0; }"
    ),
    "smart_ptr": (
        "#include <memory>\nstruct S{int a;};"
        " int main(){ auto p=std::make_unique<S>(); p->a=1; return 0; }"
    ),
    "compound_assign": "int main(){ int x=1; x += 2; x *= 3; x <<= 1; return x; }",
    "namespace": (
        "namespace ns { int f(int a){ return a*2; } }"
        " int main(){ return ns::f(21); }"
    ),
}

SAMPLES_BY_LANG = {"java_20": JAVA_SAMPLES, "java_24": JAVA_SAMPLES, "cpp_14": CPP_SAMPLES}


def _parse_python_only(file_name, content, lang):
    """Parse forcing the pure-Python path, bypassing the native fast path."""
    os.environ["CSIM_DISABLE_NATIVE"] = "1"
    try:
        # Reload so the loader re-reads the env var and skips the library.
        import importlib

        from csim.native import loader

        loader._handles.clear()
        importlib.reload(loader)
        from csim.language.parser import ANTLR_parse

        return ANTLR_parse(file_name, content, lang)
    finally:
        os.environ.pop("CSIM_DISABLE_NATIVE", None)
        from csim.native import loader as loader_after

        loader_after._handles.clear()


def _parse_native_only(file_name, content, lang):
    """Parse through the native path, skipping the test if it is unavailable."""
    from csim.native import loader

    loader._handles.clear()
    tree = loader.native_parse(content, lang)
    if tree is None:
        pytest.skip(f"native parser unavailable for {lang}")
    return tree


def _flatten(node, relabel_fn=None):
    """Flatten a parse tree to (kind, label, child_count) triples in preorder.

    The node kind is recorded explicitly rather than folded into the label:
    an earlier encoding added a fixed offset to token types, which made EOF
    (token type -1) indistinguishable from a rule index and let a real
    terminal-vs-rule mismatch slip through this comparison.

    relabel_fn, when given (java_24 only -- see csim.utils.get_relabel_fn),
    is applied to every rule node's label. The native bridge bakes its
    relabeling in at parse time (csim/native/src/java_24_bridge.cpp), while
    the pure-Python path only applies it later, in Normalize() -- so a RAW
    tree comparison needs this to compare like with like; without it, an
    assignment-shaped `expression` node native already reports as the
    synthetic id would be compared against the Python side's un-relabeled
    real rule index and fail, even though both sides agree once Normalize()
    runs (see test_normalized_tree_matches_python, the invariant that
    actually matters).
    """
    from antlr4.tree.Tree import TerminalNode

    out = []

    def walk(n):
        if isinstance(n, TerminalNode):
            token = n.symbol
            out.append(("terminal", token.type if token else None, 0))
            return
        children = list(n.getChildren())
        label = n.getRuleIndex()
        if relabel_fn is not None:
            label = relabel_fn(n) or label
        out.append(("rule", label, len(children)))
        for child in children:
            walk(child)

    walk(node)
    return out


def _flatten_dict_tree(node):
    """Flatten a normalized/pruned dict tree to (label, child_count) preorder."""
    out = []

    def walk(n):
        out.append((n["label"], len(n["children"])))
        for child in n["children"]:
            walk(child)

    walk(node)
    return out


@pytest.mark.parametrize("lang", NATIVE_LANGS)
def test_native_library_is_available(lang):
    """The compiled parsers should be present for the languages we built."""
    if not is_available(lang):
        pytest.skip(f"native library not built for {lang}")
    assert is_available(lang)


@pytest.mark.parametrize("lang", NATIVE_LANGS)
def test_raw_tree_matches_python(lang):
    """The native raw parse tree must be structurally identical to Python's."""
    from csim.utils import get_relabel_fn

    relabel_fn = get_relabel_fn(lang)
    for name, code in SAMPLES_BY_LANG[lang].items():
        native = _flatten(_parse_native_only("t", code, lang), relabel_fn)
        python = _flatten(_parse_python_only("t", code, lang), relabel_fn)
        assert native == python, f"{lang}/{name}: raw tree differs"


@pytest.mark.parametrize("lang", NATIVE_LANGS)
def test_normalized_tree_matches_python(lang):
    """Normalize() must produce the same tree from either parser."""
    for name, code in SAMPLES_BY_LANG[lang].items():
        native = Normalize(_parse_native_only("t", code, lang), lang)
        python = Normalize(_parse_python_only("t", code, lang), lang)
        assert _flatten_dict_tree(native) == _flatten_dict_tree(
            python
        ), f"{lang}/{name}: normalized tree differs"


@pytest.mark.parametrize("lang", NATIVE_LANGS)
def test_pruned_and_hashed_tree_matches_python(lang):
    """PruneAndHash() must produce the same tree and node count either way."""
    for name, code in SAMPLES_BY_LANG[lang].items():
        native_tree, native_count = PruneAndHash(
            Normalize(_parse_native_only("t", code, lang), lang), lang
        )
        python_tree, python_count = PruneAndHash(
            Normalize(_parse_python_only("t", code, lang), lang), lang
        )
        assert native_count == python_count, f"{lang}/{name}: node count differs"
        assert _flatten_dict_tree(native_tree) == _flatten_dict_tree(
            python_tree
        ), f"{lang}/{name}: pruned/hashed tree differs"


@pytest.mark.parametrize("lang", NATIVE_LANGS)
@pytest.mark.parametrize("algorithm", ["zss", "apted"])
def test_similarity_scores_match_python(lang, algorithm):
    """End-to-end similarity must be identical with either parser."""
    if not is_available(lang):
        pytest.skip(f"native library not built for {lang}")

    samples = list(SAMPLES_BY_LANG[lang].values())

    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            os.environ["CSIM_DISABLE_NATIVE"] = "1"
            from csim.native import loader

            loader._handles.clear()
            python_score = Compare(
                content_a=samples[i],
                content_b=samples[j],
                lang=lang,
                ted_algorithm=algorithm,
            )

            os.environ.pop("CSIM_DISABLE_NATIVE", None)
            loader._handles.clear()
            native_score = Compare(
                content_a=samples[i],
                content_b=samples[j],
                lang=lang,
                ted_algorithm=algorithm,
            )

            assert native_score == python_score, (
                f"{lang}/{algorithm}: similarity differs for pair ({i},{j}): "
                f"native={native_score} python={python_score}"
            )


@pytest.mark.parametrize("lang", NATIVE_LANGS)
def test_group_output_matches_python(lang, tmp_path):
    """`csim group` output must be identical with either parser."""
    if not is_available(lang):
        pytest.skip(f"native library not built for {lang}")

    samples = SAMPLES_BY_LANG[lang]
    file_names = list(samples.keys())
    file_contents = list(samples.values())

    from csim.native import loader

    os.environ["CSIM_DISABLE_NATIVE"] = "1"
    loader._handles.clear()
    python_result = group_by_exhaustive_search(
        file_names, file_contents, lang=lang, threshold=0.5, ted_algorithm="zss"
    )

    os.environ.pop("CSIM_DISABLE_NATIVE", None)
    loader._handles.clear()
    native_result = group_by_exhaustive_search(
        file_names, file_contents, lang=lang, threshold=0.5, ted_algorithm="zss"
    )

    assert native_result == python_result, f"{lang}: group output differs"


@pytest.mark.parametrize("lang", NATIVE_LANGS)
def test_report_output_matches_python(lang):
    """`csim report` output must be identical with either parser."""
    if not is_available(lang):
        pytest.skip(f"native library not built for {lang}")

    samples = SAMPLES_BY_LANG[lang]
    file_names = list(samples.keys())
    file_contents = list(samples.values())

    from csim.native import loader

    os.environ["CSIM_DISABLE_NATIVE"] = "1"
    loader._handles.clear()
    python_result = report_pairwise_similarity(
        file_names, file_contents, lang=lang, ted_algorithm="zss"
    )

    os.environ.pop("CSIM_DISABLE_NATIVE", None)
    loader._handles.clear()
    native_result = report_pairwise_similarity(
        file_names, file_contents, lang=lang, ted_algorithm="zss"
    )

    assert native_result == python_result, f"{lang}: report output differs"


def test_python_lang_falls_back_to_pure_python():
    """python_3_13 has no native parser and must keep using the Python path."""
    assert not is_available("python_3_13")

    similarity = Compare(
        content_a="x = 1\nprint(x)",
        content_b="y = 2\nprint(y)",
        lang="python_3_13",
    )
    assert similarity is not None


def test_missing_library_falls_back_gracefully(monkeypatch):
    """A missing/unloadable library must degrade to Python, not raise."""
    from csim.native import loader

    monkeypatch.setattr(loader, "_LIB_DIR", loader.Path("/nonexistent/csim/lib"))
    loader._handles.clear()

    assert loader.native_parse("public class A {}", "java_20") is None

    loader._handles.clear()
    similarity = Compare(
        content_a="public class A { void m(){} }",
        content_b="public class A { void m(){} }",
        lang="java_20",
    )
    assert similarity == 1.0
