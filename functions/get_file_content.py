import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    base_abs = os.path.abspath(working_directory)
    target_joined = os.path.join(working_directory, file_path)
    target_abs = os.path.abspath(target_joined)
    if not (target_abs == base_abs or target_abs.startswith(base_abs + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(target_abs) > MAX_CHARS:
                return f'{file_content_string} [...File "{file_path}" truncated at {MAX_CHARS} characters]'
            else:
                return file_content_string
    except Exception as e:
        return f"Error: {e}"