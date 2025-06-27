# ABOUTME: Data models and enums for task status, metadata, and platform configurations
# ABOUTME: Defines structured data types used throughout the Medusa library

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass


class TaskStatus(Enum):
    """Enumeration of possible task states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskResult:
    """Represents the result of a completed task."""
    status: TaskStatus
    message: Optional[str] = None
    error: Optional[str] = None
    failed_platform: Optional[str] = None
    results: Optional[Dict[str, Any]] = None


@dataclass
class MediaMetadata:
    """Container for media-specific metadata."""
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list] = None
    privacy: Optional[str] = None


@dataclass
class PlatformConfig:
    """Configuration for a specific platform."""
    platform_name: str
    credentials: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None