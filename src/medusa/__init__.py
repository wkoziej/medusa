# ABOUTME: Main module entry point exposing core Medusa functionality
# ABOUTME: Provides MedusaCore class and common exceptions for media upload automation

from .core import MedusaCore
from .exceptions import MedusaError, UploadError, PublishError

__version__ = "0.1.0"
__all__ = ["MedusaCore", "MedusaError", "UploadError", "PublishError"]