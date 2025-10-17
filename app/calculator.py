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
from app.exceptions import OperationError, ValidationError
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
    
    def add_observer(self, observer: HistoryObserver) -> None:
        """
        Add an observer to the calculator.

        Args:
            observer (HistoryObserver): Observer to add
        """
        self.observers.append(observer)
        logging.info(f"Added observer: {observer.__class__.__name__}")

    def remove_observer(self, observer: HistoryObserver) -> None:
        """
        Remove an observer from the calculator.

        Args:
            observer (HistoryObserver): Observer to remove
        """
        self.observers.remove(observer)
        logging.info(f"Removed observer: {observer.__class__.__name__}")
    
    def _notify_observers(self, calculation: Calculation) -> None:
        """
        Notify all observers of a new calculation.

        Args:
            calculation (Calculation): The new calculation to notify about
        """
        for observer in self.observers:
            observer.update(calculation)
        
    def set_operation(self, operation: Operation) -> None:
        """
        Set the current operation strategy.

        Args:
            operation (Operation): Operation strategy to set
        """
        self.operation_strategy = operation
        logging.info(f"Set operation: {operation}")
    
    def perform_operation(
        self, 
        a: Union[str, Number],
        b: Union[str, Number]   
    ) -> CalculationResult:
        """
        Perform the current operation with validated inputs.

        Args:
            a (Union[str, Number]): First operand
            b (Union[str, Number]): Second operand

        Returns:
            CalculationResult: Result of the operation

        Raises:
            OperationError: If the operation fails
            ValueError: If no operation is set
        """
        if not self.operation_strategy:
            raise ValueError("No operation set")

        try: 
            # Validate inputs

            validated_a = InputValidator.validate_number(a, self.config)
            validated_b = InputValidator.validate_number(b, self.config)

            # Perform calculation
            result = self.operation_strategy.execute(validated_a, validated_b)

            # Create Calculation object and update history
            calculation = Calculation(
                operand1=validated_a,
                operand2=validated_b,
                operation=self.operation_strategy,  
            )
            self.history.append(calculation)

            # Save state for undo functionality
            self.undo_stack.append(CalculatorMemento(self.history.copy()))
            self.redo_stack.clear()

            if len(self.history) > self.config.max_history_size:
                self.history.pop(0)
            
            self._notify_observers(calculation)

            return result

        except ValidationError as e: 
            logging.error(f"Validation error: {str(e)}")
            raise

        except Exception as e:
            logging.error(f"Operation failed: {str(e)}")
            raise OperationError(f"Operation failed: {str(e)}")
        
    def get_history_dataframe(self) -> pd.DataFrame:
        """
        Get the calculation history as a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the calculation history
        """

        history_data = [
            {
                "operation": str(calc.operation),
                "operand1": str(calc.operand1),
                "operand2": str(calc.operand2),
                "result": str(calc.result),
                "timestamp": calc.timestamp
            }
            for calc in self.history
        ]
        return pd.DataFrame(history_data)
    
    def show_history(self) -> List[str]:
        """
        Get formatted history of calculations.

        Returns:
            List[str]: List of formatted calculation history entries.
        """
        return [
            f"{calc.operation}({calc.operand1}, {calc.operand2}) = {calc.result}"
            for calc in self.history
        ]

    def clear_history(self) -> None:
        """
        Clear calculation history.

        """
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        logging.info("History cleared")

    def undo(self) -> bool:
        """
        Undo the last operation.

        Restores the calculator's history to the state before the last calculation
        was performed.

        Returns:
            bool: True if an operation was undone, False if there was nothing to undo.
        """
        if not self.undo_stack:
            return False
        # Pop the last state from the undo stack
        memento = self.undo_stack.pop()
        # Push the current state onto the redo stack
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        # Restore the history from the memento
        self.history = memento.history.copy()
        return True

    def redo(self) -> bool:
        """
        Redo the previously undone operation.

        Restores the calculator's history to the state before the last undo.

        Returns:
            bool: True if an operation was redone, False if there was nothing to redo.
        """
        if not self.redo_stack:
            return False
        # Pop the last state from the redo stack
        memento = self.redo_stack.pop()
        # Push the current state onto the undo stack
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        # Restore the history from the memento
        self.history = memento.history.copy()
        return True
