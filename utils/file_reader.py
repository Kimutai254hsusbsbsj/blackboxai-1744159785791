import os
import magic
from typing import Optional

def read_code_file(file_path: str) -> Optional[str]:
    """Read and return the content of a code file with language detection."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Detect file type
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)

        # Check if it's a text file
        if not file_type.startswith('text/'):
            raise ValueError(f"Unsupported file type: {file_type}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    except Exception as e:
        print(f"Error reading file: {e}")
        return None
