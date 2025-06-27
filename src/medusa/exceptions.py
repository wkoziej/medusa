# ABOUTME: Custom exception classes for Medusa library operations
# ABOUTME: Defines hierarchical exception structure for upload, publish, and config errors

class MedusaError(Exception):
    """Base exception for all Medusa-related errors."""
    pass


class ConfigError(MedusaError):
    """Raised when configuration is invalid or missing."""
    pass


# Alias for backward compatibility and clearer naming
ConfigurationError = ConfigError


class UploadError(MedusaError):
    """Raised when media upload fails."""
    
    def __init__(self, message: str, platform: str, original_error: Exception | None = None):
        super().__init__(message)
        self.platform = platform
        self.original_error = original_error


class PublishError(MedusaError):
    """Raised when social media publishing fails."""
    
    def __init__(self, message: str, platform: str, original_error: Exception | None = None):
        super().__init__(message)
        self.platform = platform
        self.original_error = original_error


class TaskError(MedusaError):
    """Raised when task processing fails."""
    pass