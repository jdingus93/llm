import os


def write_file(working_directory, file_path, content):
    base_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([base_abs, target_abs]) != base_abs:
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    
    parent = os.path.dirname(target_abs) or "."
    try:
        os.makedirs(parent, exist_ok=True)
        with open(target_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"