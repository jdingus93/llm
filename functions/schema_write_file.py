from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to write",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Exact text to write (overwrites existing contents)"
            ),
        },
        required=["file_path", "content"],
    ),
)

available_functions_write = types.Tool(
    function_declarations=[
        schema_write_file,
    ]
)