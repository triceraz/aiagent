import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas import *
from functions.call_function import call_function, available_functions
import sys

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    MAX_ITERATIONS = 20

    for i in range(MAX_ITERATIONS):
        if verbose:
            print(f"\n--- Iteration {i + 1} ---\n")

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        if not response.function_calls:
            print("\n Final response:\n")
            print(response.text)
            return

        for function_call_part in response.function_calls:
            if verbose:
                print(
                    f"\n Calling function: {function_call_part.name}\n")

            function_call_result = call_function(function_call_part, verbose)

            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("Empty function call result")

            messages.append(
                types.Content(
                    role="function",
                    parts=[function_call_result.parts[0]],
                )
            )

    print("\n Max iterations reached. Stopping.")


if __name__ == "__main__":
    main()
