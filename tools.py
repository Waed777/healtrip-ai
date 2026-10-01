import json

from database import search_doctors, search_hospitals


def search_doctors_tool(specialty=None, city="Riyadh"):
    results = search_doctors(
        specialty=specialty,
        city=city,
    )

    return {
        "tool": "search_doctors",
        "count": len(results),
        "results": results,
    }


def search_hospitals_tool(
    city="Riyadh",
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
    }


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "search_doctors",
        "description": (
            "Search the HealTrip verified provider database. "
            "Use this when the patient asks for a doctor or specialist. "
            "Never invent doctors. Only return providers found by this tool."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "specialty": {
                    "type": ["string", "null"],
                    "description": "Medical specialty, such as Cardiology.",
                },
                "city": {
                    "type": "string",
                    "description": "City to search.",
                },
            },
            "required": ["specialty", "city"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "search_hospitals",
        "description": (
            "Search the HealTrip verified hospital database. "
            "Use this when the patient needs hospital options. "
            "Never invent hospitals or availability."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City to search.",
                },
                "specialty": {
                    "type": ["string", "null"],
                    "description": "Optional medical specialty.",
                },
                "emergency_only": {
                    "type": "boolean",
                    "description": "Whether to return only hospitals with emergency services.",
                },
            },
            "required": ["city", "specialty", "emergency_only"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def execute_tool(name, arguments):
    if name == "search_doctors":
        result = search_doctors_tool(
            specialty=arguments.get("specialty"),
            city=arguments.get("city", "Riyadh"),
        )
        return json.dumps(result, ensure_ascii=False)

    if name == "search_hospitals":
        result = search_hospitals_tool(
            city=arguments.get("city", "Riyadh"),
            specialty=arguments.get("specialty"),
            emergency_only=arguments.get("emergency_only", False),
        )
        return json.dumps(result, ensure_ascii=False)

    return json.dumps(
        {
            "error": "Unknown tool",
            "tool": name,
        }
    )
