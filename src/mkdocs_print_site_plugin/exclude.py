"""
Module to assist exclude certain files being processed by plugin.

Inspired by https://github.com/apenwarr/mkdocs-exclude
"""

import os
import fnmatch
from typing import List


import fnmatch
import os
from typing import List


def exclude(path: str, exclude_patterns: List[str]) -> bool:
    """
    Check if a path should be excluded based on a list of patterns.

    Args:
        path: The path to check
        exclude_patterns: List of glob patterns to exclude

    Returns:
        True if the path should be excluded, False otherwise
    """
    assert isinstance(path, str)
    assert isinstance(exclude_patterns, list)

    if not exclude_patterns:
        return False

    # Normalize path separators to handle both Windows and Unix paths
    path = path.replace("\\", "/")

    for pattern in exclude_patterns:
        # Normalize pattern separators
        pattern = pattern.replace("\\", "/")

        # Check for directory patterns (ending with /)
        if pattern.endswith("/"):
            if path.startswith(pattern) or path.startswith(pattern[:-1] + "/"):
                return True
        # Regular glob pattern matching
        elif fnmatch.fnmatch(path, pattern):
            return True
        # Check if path is in a directory that matches the pattern
        elif "/" in path:
            path_parts = path.split("/")
            for i in range(1, len(path_parts)):
                partial_path = "/".join(path_parts[:i])
                if fnmatch.fnmatch(partial_path, pattern) or partial_path == pattern:
                    return True

    return False
