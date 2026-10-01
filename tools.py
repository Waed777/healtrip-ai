import json

from database import (
    search_doctors,
    search_hospitals,
)


def search_doctors_tool(
    specialty=None,
    city=None,
):

    results = search_doctors(
        specialty=specialty,
        city=city,
    )

    return {
        "tool": "search_doctors",
        "count": len(results),
        "results": results,
        "source": "HealTrip prototype database",
    }


def search_hospitals_tool(
    city=None,
    specialty=None,
    emergency_only=False,
):

    results = search_hospitals(
        city=city,
        specialty=specialty,
        emergency_only=emergency_only,
    )

    return {
        "tool": "search_hospitals",
        "count": len(results),
        "results": results,
        "source": "HealTrip prototype database",
    }


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_doctors",
            "description": (
                "Search the HealTrip prototype doctor database. "
                "Use this when the user requests a doctor or specialist. "
                "Never invent provider records."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "specialty": {
                        "type": "string",
                        "description": (
                            "Medical specialty such as Cardiology "
                            "or Internal Medicine."
                        ),
                    },
                    "city": {
                        "type": "string",
                        "description": "City to search.",
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_hospitals",
            "description": (
                "Search the HealTrip prototype hospital database. "
                "Use this when hospital options are requested."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City to search.",
                    },
                    "specialty": {
                        "type": "string",
                        "description": "Optional specialty.",
                    },
                    "emergency_only": {
                        "type": "boolean",
                        "description": (
                            "Return only hospitals with emergency capability."
                        ),
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    },
]


def execute_tool(
    name,
    arguments,
):

    if name == "search_doctors":

        result = search_doctors_tool(
            specialty=arguments.get("specialty"),
            city=arguments.get("city"),
        )

        return json.dumps(
            result,
            ensure_ascii=False,
        )

    if name == "search_hospitals":

        result = search_hospitals_tool(
            city=arguments.get("city"),
            specialty=arguments.get("specialty"),
            emergency_only=arguments.get(
                "emergency_only",
                False,
            ),
        )

        return json.dumps(
            result,
            ensure_ascii=False,
        )

    return json.dumps(
        {
            "error": "Unknown tool",
            "tool": name,
        }
    )
