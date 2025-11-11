import os
import uuid
from datetime import datetime

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Check if file has an allowed extension

    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions

    Returns:
        True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_unique_filename(filename: str) -> str:
    """
    Generate a unique filename to avoid conflicts

    Args:
        filename: Original filename

    Returns:
        Unique filename with timestamp and UUID
    """
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{name}_{timestamp}_{unique_id}{ext}"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove dangerous characters

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    import re
    # Remove any characters that aren't alphanumeric, dash, underscore, or dot
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename

def format_file_size(size_in_bytes: int) -> str:
    """
    Format file size in human-readable format

    Args:
        size_in_bytes: File size in bytes

    Returns:
        Formatted file size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"
