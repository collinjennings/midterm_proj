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