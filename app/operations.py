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
    All specific operations should inherit from this class and implement the execute method.
    """

    @abstractmethod
    def execute(self, *args, **kwargs) -> Decimal:
        """
        Each operation must implement the execute method.

        Arg: 
            a (Decimal): The first operand.
            b (Decimal): The second operand.

        Returns:
            Decimal: The result of the operation.
        
        Raises:
            OperationError: If the operation cannot be performed.
        """
        pass # pragma: no cover 
    
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validates the operands for the operation.
    

        Args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.
        
        Raises:
            ValidationError: If the operands are not valid.
        """
        pass 

    def __str__(self) -> str:
        """
        Return operation name for display
        
        Returns:
            str: The name of the operation.
        """

        return self.__class__.__name__
    
class Addition(Operation):
    """
    Addition operation implementation. 

    Performs the addition of two numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validcate_operands(a, b)
        """
        Add two numbers. 

        Args: 
            a (Decimal): The first operand.
            b (Decimal): The second operand.
        
        Returns:
            Decimal: The sum of the two operands.
    
        """
        self.validate_operands(a, b)
        return a + b
    
class Subtraction(Operation):
    """
    Subtraction operation implementation. 

    Performs the subtraction of two numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        """
        Subtract two numbers. 

        Args: 
            a (Decimal): The first operand.
            b (Decimal): The second operand.
        
        Returns:
            Decimal: The difference of the two operands.
    
        """
        self.validate_operands(a, b)
        return a - b
    
class Multiplication(Operation):
    """
    Multiplication operation implementation. 

    Performs the multiplication of two numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        """
        Multiply two numbers. 

        Args: 
            a (Decimal): The first operand.
            b (Decimal): The second operand.
        
        Returns:
            Decimal: The product of the two operands.
    
        """
        self.validate_operands(a, b)
        return a * b
    
class Division(Operation):
    """
    Division operation implementation. 

    Performs the division of two numbers.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """ 
        Validates the operands by checking for division by zero.
        
        Overrides the base class method to add specific validation for division.
        
        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.
        
        Raises:
            ValidationError: If the divisor is zero.   
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed.")   

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        """
        Divide two numbers. 

        Args: 
            a (Decimal): The first operand.
            b (Decimal): The second operand.
        
        Returns:
            Decimal: The quotient of the two operands.
    
        Raises:
            ValidationError: If division by zero is attempted.
    
        """
        self.validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed.")
        return a / b
