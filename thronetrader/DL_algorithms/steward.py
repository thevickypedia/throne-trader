from enum import Enum


class Optimizers(str, Enum):
    """Optimizers that can be used."""

    adam: str = "adam"
    sgd: str = "SGD"
