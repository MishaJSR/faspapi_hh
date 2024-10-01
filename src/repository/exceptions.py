class CustomException(AttributeError):
    def __init__(self, message="Custom exception occurred"):
        self.message = message
        super().__init__(self.message)