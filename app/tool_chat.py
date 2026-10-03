# import os

# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# from tools import calculator, get_current_datetime


# # --------------------------------------------------
# # 1. Load API key
# # --------------------------------------------------

# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("GEMINI_API_KEY was not found in .env")


# # --------------------------------------------------
# # 2. Initialize Gemini client
# # --------------------------------------------------

# client = genai.Client(api_key=api_key)

# MODEL_NAME = "gemini-3.5-flash-lite"


# # --------------------------------------------------
# # 3. Define tool declarations
# # --------------------------------------------------

# calculator_declaration = types.FunctionDeclaration(
#     name="calculator",
#     description="Perform a mathematical calculation.",
#     parameters=types.Schema(
#         type=types.Type.OBJECT,
#         properties={
#             "operation": types.Schema(
#                 type=types.Type.STRING,
#                 description="Operation: add, subtract, multiply, or divide."
#             ),
#             "a": types.Schema(
#                 type=types.Type.NUMBER,
#                 description="First number."
#             ),
#             "b": types.Schema(
#                 type=types.Type.NUMBER,
#                 description="Second number."
#             )
#         },
#         required=["operation", "a", "b"]
#     )
# )


# datetime_declaration = types.FunctionDeclaration(
#     name="get_current_datetime",
#     description="Get the current date and time.",
#     parameters=types.Schema(
#         type=types.Type.OBJECT,
#         properties={}
#     )
# )


# # --------------------------------------------------
# # 4. Register tools
# # --------------------------------------------------

# tools = [
#     types.Tool(
#         function_declarations=[
#             calculator_declaration,
#             datetime_declaration
#         ]
#     )
# ]


# # --------------------------------------------------
# # 5. Create chat
# # --------------------------------------------------

# chat = client.chats.create(
#     model=MODEL_NAME,
#     config=types.GenerateContentConfig(
#         tools=tools,
#         automatic_function_calling=types.AutomaticFunctionCallingConfig(
#             disable=False
#         )
#     )
# )


# # --------------------------------------------------
# # 6. Chat loop
# # --------------------------------------------------

# print("Tool-enabled assistant is ready!")
# print("Try: What is 125 multiplied by 48?")
# print("Type 'exit' to quit.\n")


# while True:

#     user_input = input("You: ").strip()

#     if user_input.lower() == "exit":
#         print("Goodbye!")
#         break

#     if not user_input:
#         continue

#     try:
#         response = chat.send_message(user_input)

#         print("\nAI:", response.text, "\n")

#     except Exception as error:
#         print("\nAn error occurred:", error, "\n")


import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import calculator, get_current_datetime


# --------------------------------------------------
# 1. Load API key
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


# --------------------------------------------------
# 2. Initialize Gemini client
# --------------------------------------------------

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash-lite"


# --------------------------------------------------
# 3. Register actual Python functions as tools
# --------------------------------------------------

chat = client.chats.create(
    model=MODEL_NAME,
    config=types.GenerateContentConfig(
        tools=[
            calculator,
            get_current_datetime
        ],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=False
        )
    )
)


# --------------------------------------------------
# 4. Chat loop
# --------------------------------------------------

print("Tool-enabled assistant is ready!")
print("Try: What is 125 multiplied by 48?")
print("Type 'exit' to quit.\n")


while True:

    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input:
        continue

    try:

        response = chat.send_message(user_input)

        if response.text:
            print("\nAI:", response.text, "\n")
        else:
            print("\nAI: No text response was returned.\n")

    except Exception as error:

        print("\nAn error occurred:", error, "\n")