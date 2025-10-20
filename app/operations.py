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
            raise ValidationError("Division by zero is not allowed")   

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
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
        return a / b
    
class Power(Operation):
    """
    Power operation implementation. 

    Performs the exponentiation of a number.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validates the operands for the power operation.
        
        Overrides the base class method to make sure the exponent is not negative.

        Args:
            a (Decimal): The base.
            b (Decimal): The exponent.
            
        Raises:
            ValidationError: If the exponent is negative.
        """
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents not supported")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Raise a number to the power of another number. 

        Args: 
            a (Decimal): The base.
            b (Decimal): The exponent.
        
        Returns:
            Decimal: The result of raising the base to the exponent.
    
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b)))

class Root(Operation):
    """
    Root operation implementation.

    Calculates the nth root of a number.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for root operation.

        Overrides the base class method to ensure that the number is non-negative
        and the root degree is not zero.

        Args:
            a (Decimal): Number from which the root is taken.
            b (Decimal): Degree of the root.

        Raises:
            ValidationError: If the number is negative or the root degree is zero.
        """
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the nth root of a number.

        Args:
            a (Decimal): Number from which the root is taken.
            b (Decimal): Degree of the root.

        Returns:
            Decimal: Result of the root calculation.
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))
    

class Modulus(Operation):
    """
    Modulus operation implementation.

    Calculates the remainder of the division of one number by another.
    """
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands, checking for modulus by zero and negative dividend.

        Overrides the base class method to ensure that the divisor is not zero
        and the dividend is not negative.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.
        Raises:
            ValidationError: If the divisor is zero or dividend is negative.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Modulus by zero is not allowed")
        if a < 0:
            raise ValidationError("Negative dividend not allowed for modulus")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the modulus of one number by another.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Returns:
            Decimal: Remainder of the division.
        """
        self.validate_operands(a, b)
        return a % b
    
class IntegerDivision(Operation):
    """
    Integer Division operation implementation.

    Performs the floor division of one number by another.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands, checking for division by zero and negative dividend.

        Overrides the base class method to ensure that the divisor is not zero
        and the dividend is not negative.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.
        
        Raises:
            ValidationError: If the divisor is zero or dividend is negative.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Integer division by zero is not allowed")
        if a < 0:
            raise ValidationError("Negative dividend not allowed for integer division")
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Perform integer (floor) division of one number by another.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Returns:
            Decimal: Result of the integer division.
        """
        self.validate_operands(a, b)
        return a // b
    
class Percentage(Operation):
    """
    Percentage operation implementation.

    Calculates what percentage the first number is of the second number.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for percentage operation.

        Overrides the base class method to ensure that the second operand is not zero.

        Args:
            a (Decimal): Value to calculate percentage for.
            b (Decimal): Total value.

        Raises:
            ValidationError: If the total value is zero.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Percentage calculation with zero as whole value is not allowed")
    
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate what percentage the first number is of the second number.

        Args:
            a (Decimal): Value to calculate percentage for.
            b (Decimal): Total value.

        Returns:
            Decimal: Percentage value (e.g., 50 for 50%).
        """
        self.validate_operands(a, b)
        return (a / b) * 100
    
class AbsoluteDifference(Operation):
    """
    Absolute Difference operation implementation.

    Calculates the absolute difference between two numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the absolute difference between two numbers.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Absolute difference between the two operands.
        """
        self.validate_operands(a, b)
        return abs(a - b)
    


class OperationFactory:
    """
    Factory class for creating operation instances.

    Implements the Factory pattern by providing a method to instantiate
    different operation classes based on a given operation type. This promotes
    scalability and decouples the creation logic from the Calculator class.
    """

    # Dictionary mapping operation identifiers to their corresponding classes
    _operations: Dict[str, type] = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root,
        'modulus': Modulus, 
        'int_divide': IntegerDivision,
        'percent': Percentage,
        'abs_diff': AbsoluteDifference,
    }

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """
        Register a new operation type.

        Allows dynamic addition of new operations to the factory.

        Args:
            name (str): Operation identifier (e.g., 'modulus').
            operation_class (type): The class implementing the new operation.

        Raises:
            TypeError: If the operation_class does not inherit from Operation.
        """
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls._operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """
        Create an operation instance based on the operation type.

        This method retrieves the appropriate operation class from the
        _operations dictionary and instantiates it.

        Args:
            operation_type (str): The type of operation to create (e.g., 'add').

        Returns:
            Operation: An instance of the specified operation class.

        Raises:
            ValueError: If the operation type is unknown.
        """
        operation_class = cls._operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class()