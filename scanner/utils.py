import os
import logging

logging.basicConfig(level=logging.INFO)


def ensure_dir_exists(path):
    """
    Ensure the directory exists; if not, create it.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")


def human_readable_size(size, decimal_places=2):
    """
    Convert a file size in bytes to a human-readable format.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024
    return f"{size:.{decimal_places}f} PB"


def log_deleted_file(filename, inode, size):
    """
    Log information about a deleted file.
    """
    logging.info(f"Deleted file found: {filename} | Inode: {inode} | Size: {human_readable_size(size)}")


def save_binary_file(data, output_path):
    """
    Save binary data to a file.
    """
    try:
        with open(output_path, "wb") as f:
            f.write(data)
        logging.info(f"File saved: {output_path}")
        return True
    except Exception as e:
        logging.error(f"Error saving file {output_path}: {e}")
        return False


def detect_file_type(file_path):
    """
    Try to detect file type from file extension or content signature.
    (Simple version based on extension for now.)
    """
    _, ext = os.path.splitext(file_path)
    return ext.lower()
