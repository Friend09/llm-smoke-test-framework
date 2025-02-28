"""Custom exceptions for the test generator framework"""

class TestGeneratorError(Exception):
    """Base exception for the framework"""
    pass

class AuthenticationError(TestGeneratorError):
    """Raised when authentication fails"""
    pass

class CrawlerError(TestGeneratorError):
    """Raised when crawler encounters an error"""
    pass

class LLMError(TestGeneratorError):
    """Raised when LLM processing fails"""
    pass
