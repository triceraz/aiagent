import os
import subprocess
import sys


def run_python_file(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = abs_working_dir
        target_file = os.path.abspath(
            os.path.join(working_directory, file_path))
        if not target_file.startswith(abs_working_dir):
            return f"Error: Cannot execute {file_path} as it is outside the permitted working directory"

        if not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: {file_path}"

        if not target_file[-3:] == ".py":
            return f"Error: {file_path} is not a python file"

        result = subprocess.run(
            [sys.executable, target_file],
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []
        if result.stdout.strip():
            output_parts.append("STOUD:\n" + result.stdout.strip())

        if result.stderr.strip():
            output_parts.append("STDERR:\n" + result.stderr.strip())

        if result.returncode != 0:
            output_parts.append(
                f"Process exited with code {result.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return f"Error: Execution of {file_path} timed out after 30 seconds"

    except Exception as e:
        return f"Error: {str(e)}"
