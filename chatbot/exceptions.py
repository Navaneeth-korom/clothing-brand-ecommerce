class ChatbotServiceError(Exception):
    def __init__(self, message, status_code= 502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
