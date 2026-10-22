import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args:
            command.extend(args)

        completed = subprocess.run(
            command,
            cwd = working_dir_abs,
            capture_output= True,
            text = True,
            timeout = 30,
        )

        output_lines = []
        if completed.returncode != 0:
            output_lines.append(f"Process exited with code {completed.returncode}")
        if not completed.stdout and not completed.stderr:
            output_lines.append("No output produced")
        else:
            if completed.stdout:
                output_lines.append(f"STDOUT:\n{completed.stdout}")
            if completed.stderr:
                output_lines.append(f"STDERR:\n{completed.stderr}")
        return "\n".join(output_lines)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file relative to the working directory and returns its stdout, stderr and exit code",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of command line arguments passed to the script",
                },
            },
            "required": ["file_path"],
        },
    },
}