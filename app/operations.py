##########################
# Operation Classes     #
##########################

from abc import ABC, abstractmethod
from typing import Dict
from app.exceptions import ValidationError
from decimal import Decimal


class Operation(ABC):
    """
    Abstract base class for all operations.
    Each operation must implement the execute method.
    """

    @abstractmethod
    def execute(self, *args, **kwargs) -> Decimal:
        pass