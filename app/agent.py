import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import (
    calculator,
    get_current_datetime,
    add_task,
    get_tasks,
    complete_task,
    get_location_coordinates,
    get_weather,
    convert_temperature
)


# --------------------------------------------------
# 1. Environment
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in .env"
    )


# --------------------------------------------------
# 2. Gemini client
# --------------------------------------------------

client = genai.Client(
    api_key=api_key
)


MODEL_NAME = "gemini-3.5-flash-lite"


# --------------------------------------------------
# 3. Tool registry
# --------------------------------------------------

tool_registry = {

    "calculator": calculator,

    "get_current_datetime":
        get_current_datetime,

    "add_task":
        add_task,

    "get_tasks":
        get_tasks,

    "complete_task":
        complete_task,

    "get_location_coordinates":
        get_location_coordinates,

    "get_weather":
        get_weather,

    "convert_temperature":
        convert_temperature
}


# --------------------------------------------------
# 4. Tools exposed to Gemini
# --------------------------------------------------

gemini_tools = [

    calculator,

    get_current_datetime,

    add_task,

    get_tasks,

    complete_task,

    get_location_coordinates,

    get_weather,

    convert_temperature
]


# --------------------------------------------------
# 5. Model configuration
# --------------------------------------------------

config = types.GenerateContentConfig(

    tools=gemini_tools,

    automatic_function_calling=(
        types.AutomaticFunctionCallingConfig(
            disable=True
        )
    ),

    system_instruction="""
You are a helpful AI assistant.

You have access to several tools.

Use tools whenever appropriate.

Never invent tool results.

Weather workflow:

1. Use get_location_coordinates to find
   the requested city.
2. Use the returned latitude and longitude
   with get_weather.
3. If the user requests Fahrenheit or Celsius
   conversion, use convert_temperature.
4. Use actual tool results in your final answer.

If a tool fails, explain the failure clearly.
"""
)


# --------------------------------------------------
# 6. Agent
# --------------------------------------------------

def run_agent(user_message: str):

    # Initial request
    contents = user_message

    # Maximum number of tool iterations
    max_iterations = 10

    for iteration in range(max_iterations):

        print(
            f"\n[AGENT ITERATION {iteration + 1}]"
        )

        # ------------------------------------------
        # Ask Gemini
        # ------------------------------------------

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=contents,

            config=config
        )

        # ------------------------------------------
        # Find function calls
        # ------------------------------------------

        function_calls = []

        for part in response.candidates[0].content.parts:

            if part.function_call:

                function_calls.append(
                    part.function_call
                )

        # ------------------------------------------
        # No tool call = final answer
        # ------------------------------------------

        if not function_calls:

            return response.text

        # ------------------------------------------
        # Execute tools
        # ------------------------------------------

        tool_response_parts = []

        for function_call in function_calls:

            tool_name = function_call.name

            tool_arguments = dict(
                function_call.args
            )

            print("\n" + "=" * 60)
            print("TOOL REQUEST")
            print("=" * 60)

            print("Name:", tool_name)

            print(
                "Arguments:",
                tool_arguments
            )

            # --------------------------------------
            # Find tool
            # --------------------------------------

            tool_function = tool_registry.get(
                tool_name
            )

            if tool_function is None:

                tool_result = {
                    "success": False,
                    "error": {
                        "type": "unknown_tool",
                        "message": (
                            f"Tool '{tool_name}' "
                            "does not exist."
                        )
                    }
                }

            else:

                try:

                    tool_result = tool_function(
                        **tool_arguments
                    )

                except Exception as error:

                    tool_result = {
                        "success": False,
                        "error": {
                            "type":
                                "tool_execution_error",

                            "message":
                                str(error)
                        }
                    }

            # --------------------------------------
            # Print result
            # --------------------------------------

            print("\nTOOL RESULT")
            print("=" * 60)

            print(tool_result)

            # --------------------------------------
            # Create function response
            # --------------------------------------

            tool_response_parts.append(

                types.Part.from_function_response(

                    name=tool_name,

                    response=tool_result
                )
            )

        # ------------------------------------------
        # Send tool results back to Gemini
        # ------------------------------------------

        contents = [

            response.candidates[0].content,

            types.Content(
                role="user",
                parts=tool_response_parts
            )
        ]

    # --------------------------------------------------
    # Safety limit
    # --------------------------------------------------

    return (
        "I couldn't complete the request because "
        "the maximum number of tool steps was reached."
    )


# --------------------------------------------------
# 7. Chat loop
# --------------------------------------------------

print("\nManual AI Agent")
print("Type 'exit' to quit.\n")


while True:

    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        break

    if not user_input:
        continue

    try:

        answer = run_agent(user_input)

        print("\nAI:", answer)

    except Exception as error:

        print(
            "\nAgent error:",
            error
        )