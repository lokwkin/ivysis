import os


def safe_write_file(path: str, content: str):
    """Write content to a file, creating directory structure if needed."""
    # Create directory structure if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
