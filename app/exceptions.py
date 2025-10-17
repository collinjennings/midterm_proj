##########################
# Exception Organization #
##########################

class CalculatorError(Exception):
    """
    Base class for calculator errors. 
    All custom exceptions should inherit from this class, which allows for unified error handling.
    """  
    pass

class ValidationError(CalculatorError):
    """
    Exception raised for validation errors in input data.
    This exception is used when the input data does not meet the required criteria.
    """  
    pass

class OperationError(CalculatorError):
    """
    Raised when a calculation operation fails.

    This exception is used to indicate failures during the execution of arithmetic
    operations, such as division by zero or invalid operations.
    """
    pass


class ConfigurationError(CalculatorError):
    """
    Raised when calculator configuration is invalid.

    Triggered when there are issues with the calculator's configuration settings,
    such as invalid directory paths or improper configuration values.
    """
    pass
