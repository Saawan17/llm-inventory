import json
from datetime import datetime


def log_tool_call(tool_name: str, arguments: dict):
    """
    Log a tool call before the tool is executed.
    """

    print("\n" + "=" * 60)
    print("TOOL CALL")
    print("=" * 60)

    print("Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Name:", tool_name)

    print("Arguments:")
    print(
        json.dumps(
            arguments,
            indent=4,
            ensure_ascii=False
        )
    )


def log_tool_result(tool_name: str, result: dict):
    """
    Log the result returned by a tool.
    """

    print("\n" + "=" * 60)
    print("TOOL RESULT")
    print("=" * 60)

    print("Tool:", tool_name)

    if result.get("success"):

        print("Status: SUCCESS")

        print("Data:")
        print(
            json.dumps(
                result.get("data"),
                indent=4,
                ensure_ascii=False
            )
        )

    else:

        print("Status: FAILED")

        print("Error:")

        print(
            json.dumps(
                result.get("error"),
                indent=4,
                ensure_ascii=False
            )
        )

    print("=" * 60)