import os
import json


from dotenv import load_dotenv
from groq import Groq

from prompt import SYSTEM_PROMPT
from tools import (
    get_order,
    search_policy,
    check_eligibility,
    create_return,
    escalate
)

from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Get all details of a Trendly order. Use this whenever the user provides an order ID. This tool can be used to find an item's SKU when the user gives only the item name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Trendly order ID, for example TR-4530"
                    }
                },
                "required": ["order_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_policy",
            "description": "Find information in the official Trendly support policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The policy topic to search for"
                    }
                },
                "required": ["topic"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_eligibility",
            "description": "Check whether an item is eligible for a return or exchange.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string"
                    },
                    "item_sku": {
                        "type": "string"
                    },
                    "action": {
                        "type": "string",
                        "enum": [
                            "return",
                            "size_exchange",
                            "colour_exchange",
                            "style_exchange"
                        ]
                    }
                },
                "required": [
                    "order_id",
                    "item_sku",
                    "action"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "create_return",
            "description": "Create a return or exchange after eligibility has been checked.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string"
                    },
                    "item_sku": {
                        "type": "string"
                    },
                    "action": {
                        "type": "string",
                        "enum": [
                            "return",
                            "size_exchange"
                        ]
                    }
                },
                "required": [
                    "order_id",
                    "item_sku",
                    "action"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "escalate",
            "description": "Escalate an issue to a human support agent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string"
                    },
                    "reason": {
                        "type": "string"
                    }
                },
                "required": [
                    "order_id",
                    "reason"
                ]
            }
        }
    }
]
def run_tool(name, arguments):
    if name == "get_order":
        return get_order(**arguments)

    if name == "search_policy":
        return search_policy(**arguments)

    if name == "check_eligibility":
        return check_eligibility(**arguments)

    if name == "create_return":
        return create_return(**arguments)

    if name == "escalate":
        return escalate(**arguments)

    return {
        "error": "Unknown tool"
    }

sessions = {}


def chat(message, session_id="default"):
    if session_id not in sessions:
        sessions[session_id] = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    messages = sessions[session_id]

    messages.append({
        "role": "user",
        "content": message
    })

    while True:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2
        )

        assistant_message = response.choices[0].message

        messages.append(assistant_message)

        if not assistant_message.tool_calls:
            return assistant_message.content

        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            result = run_tool(
                tool_name,
                arguments
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": json.dumps(result)
            })

if __name__ == "__main__":
    while True:
        user_message = input("\nYou: ")

        if user_message.lower() == "exit":
            break

        answer = chat(user_message)

        print("\nAssistant:", answer)