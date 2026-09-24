#!/usr/bin/env bash
#
# Reproduce the Linux wheel build locally, in the same manylinux container CI
# uses. Mirrors .github/workflows/build-wheels.yml so the workflow can be
# validated without pushing a tag and waiting on a CI round trip.
#
# Requires a running Docker daemon. The repo is mounted read-only and all output
# goes to ./dist-linux, so the working tree is left untouched.
#
# Usage:
#   scripts/verify_linux_wheel.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ANTLR_VERSION="${ANTLR_VERSION:-4.13.2}"
IMAGE="quay.io/pypa/manylinux_2_28_x86_64"
OUT_DIR="$REPO_ROOT/dist-linux"

if ! docker info >/dev/null 2>&1; then
    echo "error: the Docker daemon is not reachable. Start Docker and retry." >&2
    exit 1
fi

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

echo "Building the Linux wheel in $IMAGE"
echo "(this compiles the ANTLR C++ runtime from source; expect several minutes)"
echo

# --platform: on Apple Silicon this runs under emulation, which is slow but
# produces the x86_64 artifact Render actually needs.
docker run --rm \
    --platform linux/amd64 \
    -v "$REPO_ROOT:/src:ro" \
    -v "$OUT_DIR:/out" \
    -e "ANTLR_VERSION=$ANTLR_VERSION" \
    "$IMAGE" \
    bash -euo pipefail -c '
        echo "=== [1/7] build tools ==="
        yum install -y -q java-17-openjdk-headless cmake unzip >/dev/null
        java -version 2>&1 | head -1
        cmake --version | head -1

        # Work on a copy: /src is read-only and the build writes generated
        # sources and libraries into the tree.
        cp -r /src /work
        cd /work

        echo
        echo "=== [2/7] ANTLR C++ runtime ${ANTLR_VERSION} from source ==="
        curl -fsSL -o /tmp/runtime.zip \
            "https://www.antlr.org/download/antlr4-cpp-runtime-${ANTLR_VERSION}-source.zip"
        mkdir -p /tmp/antlr-src && unzip -q /tmp/runtime.zip -d /tmp/antlr-src
        cmake -S /tmp/antlr-src -B /tmp/antlr-build \
            -DCMAKE_BUILD_TYPE=Release \
            -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
            -DANTLR4_INSTALL=ON \
            -DCMAKE_INSTALL_PREFIX=/opt/antlr-runtime \
            -DWITH_DEMO=OFF \
            -DANTLR_BUILD_CPP_TESTS=OFF \
            -DANTLR_BUILD_SHARED=OFF >/dev/null
        cmake --build /tmp/antlr-build -j"$(nproc)" >/dev/null
        cmake --install /tmp/antlr-build >/dev/null
        ls -la /opt/antlr-runtime/lib/ | grep -E "\.a|\.so" || true

        echo
        echo "=== [3/7] ANTLR generator ==="
        curl -fsSL -o /tmp/antlr.jar \
            "https://www.antlr.org/download/antlr-${ANTLR_VERSION}-complete.jar"

        echo
        echo "=== [4/7] native parsers ==="
        export PATH="/opt/python/cp311-cp311/bin:$PATH"
        python -m pip install --quiet setuptools wheel
        export ANTLR_JAR=/tmp/antlr.jar
        export ANTLR_CPP_INCLUDE=/opt/antlr-runtime/include/antlr4-runtime
        export ANTLR_CPP_LIB=/opt/antlr-runtime/lib
        bash scripts/build_native_parsers.sh

        echo
        echo "=== [5/7] dependency check ==="
        for lib in csim/native/lib/*.so; do
            echo "== $lib"
            ldd "$lib"
            if ldd "$lib" | grep -Eq "libstdc\+\+|libantlr4"; then
                echo "FAIL: $lib links a C++/ANTLR runtime dynamically" >&2
                exit 1
            fi
        done
        echo "OK: only base system libraries"

        echo
        echo "=== [6/7] wheel ==="
        python setup.py bdist_wheel --plat-name manylinux_2_28_x86_64 >/dev/null
        ls -lh dist/

        echo
        echo "=== [7/7] smoke test in a clean venv ==="
        python -m venv /tmp/venv
        /tmp/venv/bin/pip install --quiet dist/*.whl
        /tmp/venv/bin/csim info
        /tmp/venv/bin/python -c "
from csim.native import is_available
missing = [l for l in (\"java_20\", \"cpp_14\") if not is_available(l)]
if missing:
    raise SystemExit(f\"FAIL: native parsers inactive: {missing}\")
print(\"native parsers active: java_20, cpp_14\")
"

        cp dist/*.whl /out/
    '

echo
echo "Wheel written to: $OUT_DIR"
ls -lh "$OUT_DIR"
