import os


def get_files_info(working_directory, directory="."):
    base_abs = os.path.abspath(working_directory)
    target_joined = os.path.join(working_directory, directory)
    target_abs = os.path.abspath(target_joined)
    if not (target_abs == base_abs or target_abs.startswith(base_abs + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_abs):
        return f'Error: "{directory}" is not a directory'
    
    try:
        lines = []
        for name in os.listdir(target_abs):
            full_path = os.path.join(target_abs, name)
            size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            line = f'- {name}: file_size={size} bytes, is_dir={is_dir}'
            lines.append(line)

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"