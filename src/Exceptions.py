class ArgumentTypeError(Exception):
    """Exception raised for errant argument types."""
    def __init__(self, value):
        self.value = value
        self.message = "Provided argument(s) inavlid. Expected: main.py <int> <float>"
        super().__init__(self.message)

class IterationRangeError(Exception):
    """Exception raised for iteration count is out of range of 0 to inf."""
    def __init__(self, value):
        self.value = value
        self.message = "Provided argument inavlid. Number of iterations must be grater than 0."
        super().__init__(self.message)

class MaxErrorRangeError(Exception):
    """Exception raised for Maximum allowed error is out of range of 0 to inf."""
    def __init__(self, value):
        self.value = value
        self.message = "Provided argument inavlid. Max error must be float between 0 and 1."
        super().__init__(self.message)