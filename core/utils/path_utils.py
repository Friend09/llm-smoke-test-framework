import os
import pathlib

def ensure_directory_exists(file_path):
    """
    Ensures that the directory for the given file path exists.
    Creates the directory and any missing parent directories if necessary.

    Args:
        file_path (str): Path to a file
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def normalize_path(path):
    """
    Normalize file paths to be OS-agnostic by converting
    path separators appropriately.

    Args:
        path (str): File path to normalize

    Returns:
        str: Normalized path with correct separators for current OS
    """
    return os.path.normpath(path)
