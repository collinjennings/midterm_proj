########################
# Calculator Class     #
########################

from decimal import Decimal
import logging 
import os 
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd 

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.input_validators import InputValidator
from app.calculator_memento import CalculatorMemento
from app.history import HistoryObserver
from app.operations import Operation


# Type aliases for readability
Number = Union[int, float, Decimal]
CalculationResult = Union[Number, str]

class Calculator:
    """
    Main calculator class that implements different design patterns.

    The class serves as the core of the application. It manages operations, calculation history, observers, configurations, and data persistence.
    It uses different design patterns for flexibility, maintainability, and scalability.
    """
    