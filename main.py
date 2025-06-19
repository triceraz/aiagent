import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas import *
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


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if sys.argv[1:] == []:
    print("Please provide prompt")
    sys.exit(1)

user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ))


print(response.text)
if response.function_calls != []:
    for function_call_part in response.function_calls:
        print(
            f"Calling function: {function_call_part.name}({function_call_part.args})")


prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if sys.argv[-1] == "--verbose":
    print(f"User prompt: {user_prompt}")
    print(f"Promp tokens: {prompt_tokens}")
    print(f"Response tokens {response_tokens}")
