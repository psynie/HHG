"""SplitWise Lite: settle shared expenses with the fewest payments."""

from .ledger import Ledger
from .settle import settle

__all__ = ["Ledger", "settle"]
__version__ = "0.1.0"
