import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=[]):
    base_abs = os.path.abspath(working_directory)
    target_joined = os.path.join(working_directory, file_path)
    target_abs = os.path.abspath(target_joined)
    if not (target_abs == base_abs or target_abs.startswith(base_abs + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_abs):
        return f'Error: File "{file_path}" not found.'
    
    if not target_abs.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    cmd = [sys.executable, file_path, *args]

    completed = subprocess.run(
        cmd,
        cwd=working_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=30,
    )

    out = completed.stdout.strip()
    err = completed.stderr.strip()

    try:
        if not out and not err:
            return "No output produced."
        
        lines = []
        lines.append(f"STDOUT: {out}")
        lines.append(f"STDERR: {err}")

        if completed.returncode != 0:
            lines.append("Processed exited with code {completed.returncode}")
        
        return "/n".join(lines)

    except Exception as e:
        return f"Error: executing Python file: {e}"