import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.schema_get_files_info import schema_get_files_info
from functions.schema_get_files_info import available_functions as tool_list
from functions.schema_get_file_content import schema_get_file_content
from functions.schema_get_file_content  import available_functions_read as tool_read
from functions.schema_run_python_file import schema_run_python_file
from functions.schema_run_python_file import available_functions_run as tool_run
from functions.schema_write_file import schema_write_file
from functions.schema_write_file import available_functions_write as tool_write


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from llm!")

    if len(sys.argv) == 1:
        print("Unable to answer empty prompt")
        sys.exit(1)

    is_verbose = (sys.argv[-1] == "--verbose")
    if is_verbose:
        prompt_parts = sys.argv[1:-1]
    else:
        prompt_parts = sys.argv[1:]

    if not prompt_parts:
        print("Unable to answer empty prompt")
        sys.exit(1)

    system_prompt = """You are a helpful AI coding agent.  When a user askes a question or makes a request, make a function call plan.
    You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    All paths you provide should be relative to the working directory.  You do not need to specify the working directory in your function calls as it is automatically injected for security reasons."""
    user_prompt="".join(prompt_parts)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[tool_list, tool_read, tool_run, tool_write], system_instruction=system_prompt)
    )

    calls = getattr(response, "function_calls", None)

    if calls:
        for fc in calls:
            print(f"Calling function: {fc.name}({fc.args})")
    else:
        print(response.text)

    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
