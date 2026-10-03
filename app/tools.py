import json
import os
from datetime import datetime
import requests
from tool_logger import (log_tool_call, log_tool_result)


TASK_FILE = "app/tasks.json"


# --------------------------------------------------
# Calculator
# --------------------------------------------------

def calculator(operation: str, a: float, b: float) -> dict:
    """
    Perform a mathematical calculation.
    """

    valid_operations = {
        "add",
        "subtract",
        "multiply",
        "divide"
    }

    if operation not in valid_operations:

        return {
            "success": False,
            "error": {
                "type": "invalid_operation",
                "message": (
                    f"Unsupported operation '{operation}'. "
                    f"Supported operations are: "
                    f"{', '.join(valid_operations)}."
                )
            }
        }

    try:

        a = float(a)
        b = float(b)

    except (ValueError, TypeError):

        return {
            "success": False,
            "error": {
                "type": "invalid_input",
                "message": "Both numbers must be valid numeric values."
            }
        }

    if operation == "divide" and b == 0:

        return {
            "success": False,
            "error": {
                "type": "division_by_zero",
                "message": "Division by zero is not allowed."
            }
        }

    if operation == "add":
        result = a + b

    elif operation == "subtract":
        result = a - b

    elif operation == "multiply":
        result = a * b

    else:
        result = a / b

    return {
        "success": True,
        "data": {
            "result": result
        }
    }

# --------------------------------------------------
# Current date and time
# --------------------------------------------------

def get_current_datetime() -> dict:

    current_time = datetime.now()

    return {
        "date": current_time.strftime("%Y-%m-%d"),
        "time": current_time.strftime("%H:%M:%S")
    }


# --------------------------------------------------
# Load tasks
# --------------------------------------------------

def load_tasks():

    if not os.path.exists(TASK_FILE):
        return []

    with open(TASK_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# Save tasks
# --------------------------------------------------

def save_tasks(tasks):

    with open(TASK_FILE, "w", encoding="utf-8") as file:
        json.dump(
            tasks,
            file,
            indent=4,
            ensure_ascii=False
        )


# --------------------------------------------------
# Add task
# --------------------------------------------------

def add_task(title: str, due_date: str = "") -> dict:

    tasks = load_tasks()

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }

    tasks.append(task)

    save_tasks(tasks)

    return {
        "success": True,
        "message": f"Task '{title}' was added.",
        "task": task
    }


# --------------------------------------------------
# Get tasks
# --------------------------------------------------

def get_tasks() -> dict:

    tasks = load_tasks()

    return {
        "tasks": tasks
    }


# --------------------------------------------------
# Complete task
# --------------------------------------------------

def complete_task(task_id: int) -> dict:

    tasks = load_tasks()

    for task in tasks:

        if task["id"] == task_id:

            task["completed"] = True

            save_tasks(tasks)

            return {
                "success": True,
                "message": f"Task '{task['title']}' completed.",
                "task": task
            }

    return {
        "success": False,
        "message": f"Task with ID {task_id} was not found."
    }


    import requests


# --------------------------------------------------
# Weather tool
# --------------------------------------------------

def get_weather(latitude: float, longitude: float) -> dict:
    """
    Get the current weather for a location.
    """

    # -----------------------------
    # Validate input
    # -----------------------------

    if latitude is None or longitude is None:

        return {
            "success": False,
            "error": {
                "type": "invalid_input",
                "message": "Latitude and longitude are required."
            }
        }

    try:

        latitude = float(latitude)
        longitude = float(longitude)

    except (ValueError, TypeError):

        return {
            "success": False,
            "error": {
                "type": "invalid_input",
                "message": "Latitude and longitude must be numbers."
            }
        }

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        ),
        "timezone": "auto"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        current = data.get("current")

        if not current:

            return {
                "success": False,
                "error": {
                    "type": "invalid_response",
                    "message": "Weather data was not available."
                }
            }

        return {
            "success": True,
            "data": {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "wind_speed": current.get("wind_speed_10m"),
                "timezone": data.get("timezone")
            }
        }

    except requests.RequestException:

        return {
            "success": False,
            "error": {
                "type": "api_error",
                "message": "The weather service could not be reached."
            }
        }

    except (ValueError, KeyError, TypeError):

        return {
            "success": False,
            "error": {
                "type": "invalid_response",
                "message": "The weather service returned an unexpected response."
            }
        }


# --------------------------------------------------
# Geocoding tool
# --------------------------------------------------

def get_location_coordinates(
    city: str,
    country: str = ""
) -> dict:
    """
    Find the latitude and longitude of a city.

    Provide the country when known to avoid ambiguous
    city names.
    """

    if not city or not city.strip():
        return {
            "success": False,
            "error": {
                "type": "invalid_input",
                "message": "City name cannot be empty."
            }
        }

    city = city.strip()

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 10,
        "language": "en",
        "format": "json"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            return {
                "success": False,
                "error": {
                    "type": "not_found",
                    "message": f"Could not find location '{city}'."
                }
            }

        # -----------------------------------------
        # Filter by country if provided
        # -----------------------------------------

        if country:

            matching_results = [
                result
                for result in results
                if result.get("country", "").lower()
                == country.lower()
            ]

            if matching_results:
                results = matching_results

            else:
                return {
                    "success": False,
                    "error": {
                        "type": "not_found",
                        "message": (
                            f"Could not find '{city}' "
                            f"in {country}."
                        )
                    }
                }

        # -----------------------------------------
        # Select first matching result
        # -----------------------------------------

        location = results[0]

        return {
            "success": True,
            "data": {
                "city": location.get("name"),
                "country": location.get("country"),
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
                "timezone": location.get("timezone")
            }
        }

    except requests.RequestException:

        return {
            "success": False,
            "error": {
                "type": "api_error",
                "message": (
                    "The location service could not be reached."
                )
            }
        }

    except (ValueError, KeyError, TypeError):

        return {
            "success": False,
            "error": {
                "type": "invalid_response",
                "message": (
                    "The location service returned "
                    "an unexpected response."
                )
            }
        }

    # -----------------------------
    # Network/API error
    # -----------------------------

    except requests.RequestException as error:

        return {
            "success": False,
            "error": {
                "type": "api_error",
                "message": "The location service could not be reached."
            }
        }

    # -----------------------------
    # Unexpected response
    # -----------------------------

    except (ValueError, KeyError, TypeError):

        return {
            "success": False,
            "error": {
                "type": "invalid_response",
                "message": "The location service returned an unexpected response."
            }
        }


def get_location_coordinates_with_logging(
    city: str,
    country: str = ""
) -> dict:

    arguments = {
        "city": city,
        "country": country
    }

    log_tool_call(
        "get_location_coordinates",
        arguments
    )

    result = get_location_coordinates(
        city,
        country
    )

    log_tool_result(
        "get_location_coordinates",
        result
    )

    return result


def get_weather_with_logging(
    latitude: float,
    longitude: float
) -> dict:

    arguments = {
        "latitude": latitude,
        "longitude": longitude
    }

    log_tool_call(
        "get_weather",
        arguments
    )

    result = get_weather(
        latitude,
        longitude
    )

    log_tool_result(
        "get_weather",
        result
    )

    return result


def logged_calculator(
    operation: str,
    a: float,
    b: float
) -> dict:

    arguments = {
        "operation": operation,
        "a": a,
        "b": b
    }

    log_tool_call(
        "calculator",
        arguments
    )

    result = calculator(
        operation,
        a,
        b
    )

    log_tool_result(
        "calculator",
        result
    )

    return result


# -----------------------------------------
# Convert between the temprature units Celsius, Fahrenheit, and Kelvin
# -----------------------------------------

def convert_temperature(
        temperature: float,
        from_unit: str,
        to_unit: str
) -> dict:

    """
    Convert temperature between Celsius and Fahrenheit.
    """

    try:
         
        temperature = float(temperature)

    except (ValueError, TypeError):
        return {
            "success": False,
            "error": {
                "type": "invalid_input",
                "message": "Temperature must be a valid numeric value."
            }
        }

    valid_units = {"C", "F", "K"}

    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    if from_unit not in valid_units or to_unit not in valid_units:
        return {
            "success": False,
            "error": {
                "type": "invalid_unit",
                "message": (
                    f"Unsupported unit. Supported units are: "
                    f"{', '.join(valid_units)}."
                )
            }
        }

    # -----------------------------------------
    # Celsius -> Fahrenheit
    # -----------------------------------------

    if from_unit == "C" and to_unit == "F":

        result = (temperature * 9 / 5) + 32

    # -----------------------------------------
    # Fahrenheit -> Celsius
    # -----------------------------------------

    elif from_unit == "F" and to_unit == "C":

        result = (temperature - 32) * 5 / 9

    # -----------------------------------------
    # Same unit, no conversion needed
    # -----------------------------------------

    elif from_unit == to_unit:
        
        result = temperature

     # -----------------------------------------
    # Unsupported conversion
    # -----------------------------------------

    else:

        return {
            "success": False,
            "error": {
                "type": "unsupported_conversion",
                "message": (
                    f"Cannot convert from {from_unit} "
                    f"to {to_unit}."
                )
            }
        }

    return {
        "success": True,
        "data": {
            "value": round(result, 2),
            "unit": to_unit
        }
    }



