import os

def to_raw_path(path):
    r"""
    Converts a normal Windows drive path to a raw device path.
    Example: C:\ → \\.\C:
    """
    drive_letter = os.path.splitdrive(path)[0]
    if drive_letter:
        return r"\\.\{}".format(drive_letter)
    return path

def ensure_dir(path):
    """
    Creates a directory if it does not exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
