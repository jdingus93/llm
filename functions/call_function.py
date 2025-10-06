from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file


function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content, 
        "run_python_file": run_python_file,
        "write_file": write_file,
}

def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    args = function_call_part.args
    if verbose:
        print(f"Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

    function_obj = function_map.get(name)
    if function_obj is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )
    
    kwargs = dict(args)
    kwargs["working_directory"] = "./calculator"

    if name == "wtire_file":
        target = kwargs.get("file_path", "")
        print(f"WRITE TARGET: {target}")
        if target != "pkg/calculator.py":
            return types.Content(
                role="tool",
                parts=[types.Part.from_function_response(
                    name=name,
                    response={"result": f"Refusing write to '{target}'.  Only 'pkg/calculator.py' alllowed."},
                )],
            )
        
    function_obj = function_map.get(name)

    result = function_obj(**kwargs)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
        ],
    )