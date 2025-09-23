import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    user_prompt="".join(prompt_parts)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    if is_verbose:
        print(f"User prompt: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
