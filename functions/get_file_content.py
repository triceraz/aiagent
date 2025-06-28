import os
from functions.config import *


def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = abs_working_dir
        target_file = os.path.abspath(
            os.path.join(working_directory, file_path))
        if not target_file.startswith(abs_working_dir):
            return f"Error: Cannot read {file_path} as it is outside the permitted working directory"

        if not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: {file_path}"

        with open(target_file, "r") as f:
            contents = f.read(MAX_CHARS)
            if len(contents) >= MAX_CHARS:
                return f"{contents}, {file_path} truncated at {MAX_CHARS} characters"
            return contents
    except Exception as e:
        return f"Error reading file {file_path}: {e}"
