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

    def __init__(self, config: Optional[CalculatorConfig] = None): 
        """ 
        Initialize the Calculator with optional configuration.

        Args:
            config (CalculatorConfig, optional): Configuration for the calculator. Defaults to None.
        """
        if config is None:
            current_file_path = Path(__file__)
            project_root = current_file_path.parent.parent
            config = CalculatorConfig(base_dir=project_root)
        
        # Assign configuration and initialize components
        self.config = config
        self.config.validate()

        # Check that log directory exists
        os.makedirs(self.config.log_dir, exist_ok=True)

        # Initialize calculation history and operation strategy
        self.history: List[Calculation] = []
        self.operation_strategy: Optional[Operation] = None

        # Initialize observers list for the Observer pattern
        self.observers: List[HistoryObserver] = []

        # Initialize Memento for state management
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        #Create directories for history management
        self._setup_directories()

        try: 
            # Attempt to load existing history
            self._load_history()  
        except Exception as e:
            # Log any errors during history loading
            logging.warning(f"Could not load existing history: {e}")

        # Log initialization of the calculator
        logging.info("Calculator initialized with configuration")

    def _setup_directories(self) -> None:
        """
        Set up necessary directories for history.
        """
        self.config.history_dir.mkdir(parents=True, exist_ok=True)

    def _setup_logging(self) -> None: 
        """
        Set up logging for the calculator.
        
        """
        try: 
            # Check that log directory exists
            os.makedirs(self.config.log_dir, exist_ok=True)
            log_file = self.config.log_file.resolve()

            # Configure logging
            logging.basicConfig(
                filename=str(log_file),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s'
                force=True ## To ensure reconfiguration in interactive environments ##
            )
            logging.info("Logging initialized at: {log_file}")
        except Exception as e:
            print(f"Failed to set up logging: {e}")
            raise
    
