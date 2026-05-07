from .CodeSimilarity import Compare
from .language.parser import ANTLR_parse
from .processing.tree_processing import Normalize, PruneAndHash
from .processing.distance_metrics import SimilarityIndex
from .utils import group_by_similarity, compare_all