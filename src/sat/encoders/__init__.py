from . import pairwise
from . import seq_counter
from . import ladder
from . import commander
from . import binary
from . import product

ENCODERS = {
    "pairwise": pairwise,
    "seqcounter": seq_counter,
    "ladder": ladder,
    "commander": commander,
    "binary": binary,
    "product": product
}
