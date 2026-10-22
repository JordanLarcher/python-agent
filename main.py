import argparse
import os
import json
from system_prompt import system_prompt
from dotenv import load_dotenv
from openai import OpenAI
from functions.index import available_functions, call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
    )

user_prompt = args.user_prompt

messages = [
    { "role": "system", "content": system_prompt},
    { "role": "user", "content": user_prompt },
]
while True: 
    response = client.chat.completions.create(
        model="openrouter/free",
        messages= messages,
        tools=available_functions,
    )

    message = response.choices[0].message

    # if args.verbose:
    #     print("User prompt:", user_prompt)
    #     print("Prompt tokens:", response.usage.prompt_tokens)
    #     print("Response tokens:", response.usage.completion_tokens)


    # if message.tool_calls:
    #     for tool_call in message.tool_calls:
    #         result_message = call_function(tool_call, verbose = args.verbose)
    #         if not result_message.get("content"):
    #             raise Exception("Empty function response")

    #         if args.verbose:
    #             print(f"-> {result_message['content']}")

            
    #         messages.append(result_message)
    #     response2 = client.chat.completions.create(
    #         model="openrouter/free",
    #         messages= messages,
    #         tools=available_functions,
    #     )

    #     print(response2.choices[0].message.content)
    # else: 
    #     print(response.choices[0].message.content)

    if not message.tool_calls:
        print(message.content)
        break

    messages.append(message.model_dump())
    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, verbose=args.verbose)
        if not result_message.get("content"):
            raise Exception("Empty function response")
        if args.verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)
