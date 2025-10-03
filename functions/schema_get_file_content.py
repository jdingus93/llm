from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions_read = types.Tool(
    function_declarations=[
        schema_get_file_content,
    ]
)