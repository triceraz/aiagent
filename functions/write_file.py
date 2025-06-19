import os


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = abs_working_dir
    target_file = os.path.abspath(
        os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f"Error: Cannot write {file_path} as it is outside the permitted working directory"

    try:
        if not os.path.isfile(target_file):
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f"Successfully wrote to {file_path} {len(content)} characters written"

    except Exception as e:
        return f"Error writing file: {e}"
