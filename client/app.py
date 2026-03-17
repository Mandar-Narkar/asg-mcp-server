import asyncio
import json
import os
import sys

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"), override=False)

app = Flask(__name__)

SERVER_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "server", "main.py")

# ---------------------------------------------------------------------------
# Tool definitions exposed to OpenAI (mirror the MCP server tools)
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_deal_summary",
            "description": (
                "Get a summary of a securitization deal: deal name, asset class, "
                "issuer, servicer, trustee, pool balance, pool factor, "
                "month-to-date collections, and next payment date."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "deal_id": {
                        "type": "string",
                        "description": "Deal identifier — one of: AUTO-001, CARD-001, ABCP-001",
                    }
                },
                "required": ["deal_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_waterfall_check",
            "description": (
                "Run a 5-step payment waterfall check for a securitization deal. "
                "Returns available funds, senior fees paid, senior interest paid, "
                "OC and IC coverage test results (pass/fail), and residual to equity."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "deal_id": {
                        "type": "string",
                        "description": "Deal identifier — one of: AUTO-001, CARD-001, ABCP-001",
                    }
                },
                "required": ["deal_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "flag_exceptions",
            "description": (
                "Check a securitization deal for operational exceptions: "
                "delinquency rate above threshold, missing servicer report, "
                "OC test failure, IC test failure."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "deal_id": {
                        "type": "string",
                        "description": "Deal identifier — one of: AUTO-001, CARD-001, ABCP-001",
                    }
                },
                "required": ["deal_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_payment_summary",
            "description": (
                "Generate a payment direction summary for a securitization deal. "
                "Returns dollar amounts per tranche (senior fees, senior interest, residual to equity), "
                "trustee name, payment date, and submission status: READY TO SUBMIT or BLOCKED "
                "based on OC/IC coverage test results."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "deal_id": {
                        "type": "string",
                        "description": "Deal identifier — one of: AUTO-001, CARD-001, ABCP-001",
                    }
                },
                "required": ["deal_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_all_deals",
            "description": (
                "Compare all securitization deals in the portfolio. "
                "Returns a table with deal ID, asset class, pool balance, OC test status, "
                "open exception count, and inline exception descriptions for each deal. "
                "Also includes a portfolio summary with total deal count, aggregate pool balance, "
                "deals with exceptions, and total exception count. No arguments required."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]

SYSTEM_PROMPT = """You are the ASG Securitization Operations Assistant for TD Securities \
Asset Securitization Group. You help back-office operations teams monitor, analyze, and \
review securitization deals.

Available deals:
- AUTO-001: TD Auto Receivables Trust 2024-1 (auto loans)
- CARD-001: TD Credit Card Receivables Trust 2023-3 (credit card receivables)
- ABCP-001: Maple Leaf Conduit Series 2024-A (asset-backed commercial paper)

Use the available tools to answer questions accurately. Always cite deal names and IDs \
in your responses. Present financial figures clearly and flag any issues prominently.

After every response that involves a tool result, append exactly one line in this format:
[WORKFLOW NOTE]: <A concise, italicised note explaining what the analyst would do next \
in a real TD Securities workflow. Be specific to the situation — e.g. for a waterfall \
FAIL mention front-office escalation and PSA cash diversion; for a missing servicer \
report mention the 2-business-day OSFI resolution window; for READY TO SUBMIT mention \
the payment direction letter and 11AM trustee cut-off; for a delinquency breach mention \
surveillance event triggers; for a portfolio comparison mention the morning ops review \
checklist.>"""


# ---------------------------------------------------------------------------
# MCP client helper
# ---------------------------------------------------------------------------
async def _call_mcp_tool(tool_name: str, tool_args: dict) -> str:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_SCRIPT],
        env=None,
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, tool_args)
            if result.content:
                item = result.content[0]
                return item.text if hasattr(item, "text") else str(item)
            return json.dumps({"error": "No result returned from MCP server"})


def call_mcp_tool(tool_name: str, tool_args: dict) -> str:
    return asyncio.run(_call_mcp_tool(tool_name, tool_args))


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/health")
def health():
    deals_path = os.path.join(os.path.dirname(__file__), "..", "server", "mock_data", "deals.json")
    with open(deals_path) as f:
        deals = json.load(f)
    return jsonify({
        "mcp_server": "online",
        "tools_available": len(TOOLS),
        "deals_loaded": len(deals),
    })


@app.route("/")
def index():
    default_key = os.getenv("OPENAI_API_KEY", "")
    return render_template("index.html", default_api_key=default_key)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    api_key = (data.get("api_key") or "").strip()
    user_message = (data.get("message") or "").strip()

    if not api_key:
        return jsonify({"error": "OpenAI API key is required."}), 400
    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    client = OpenAI(api_key=api_key)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    # First OpenAI call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    response_message = response.choices[0].message

    # If OpenAI wants to call tools, route them through the MCP server
    if response_message.tool_calls:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            tool_result = call_mcp_tool(tool_name, tool_args)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )

        # Second call to get the final natural-language response
        final = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        answer = final.choices[0].message.content
    else:
        answer = response_message.content

    return jsonify({"response": answer})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
