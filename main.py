import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.schema_get_files_info import schema_get_files_info
from functions.schema_get_files_info import available_functions
from functions.schema_get_file_content import schema_get_file_content
from functions.schema_get_file_content  import available_functions_read
from functions.schema_run_python_file import schema_run_python_file
from functions.schema_run_python_file import available_functions_run
from functions.schema_write_file import schema_write_file
from functions.schema_write_file import available_functions_write
from functions.call_function import call_function


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

    for i in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions, available_functions_read, available_functions_run, available_functions_write], system_instruction=system_prompt)
            )

            candidate = response.candidates[0]
            parts = candidate.content.parts

            function_call_part = None
            for part in parts:
                if hasattr(part, "function_call") and part.function_call is not None:
                    function_call_part = part.function_call
                    break

            for cand in response.candidates:
                messages.append(cand.content)


            if function_call_part is None and response.text:
                print(response.text)
                break

            if function_call_part is not None:
                function_call_result = call_function(function_call_part, is_verbose)
                
                tool_content = types.Content(
                    role="user",
                    parts=function_call_result.parts,
                )
                messages.append(tool_content)

        except Exception as e:
            print(f"Error: {e}")
            break

        if is_verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
