# ASG Securitization Operations Assistant

A Model Context Protocol (MCP) server and web client that gives large language models structured, tool-based access to securitization deal data — built for TD Securities Asset Securitization Group back-office workflows.

## Use Case

The Asset Securitization Group at TD Securities manages a portfolio of structured finance vehicles — auto loan trusts, credit card receivables trusts, and asset-backed commercial paper conduits. Each month, operations analysts must verify payment waterfalls, check OC/IC coverage tests, flag exceptions, and submit payment direction letters to trustees before the 11AM cut-off. This assistant exposes those workflows as MCP tools, allowing an LLM to query deal data, run waterfall checks, surface exceptions, and generate payment summaries through natural language — dramatically reducing the manual effort of the daily morning ops review cycle. Deal data is sourced from `mock_data/deals.json`, which simulates the structured outputs of **TAO SecureHub**, TD's internal securitization administration and operations platform.

---

## Prerequisites

- **Python 3.13+**
- **OpenAI API key** (`sk-...`) with access to `gpt-4o`
- `pip` and `venv` (included with Python 3.13)

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/asg-mcp-server.git
cd asg-mcp-server
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-your-key-here
```

> The key can also be pasted directly into the web UI at runtime. The `.env` file is gitignored and never committed.

### 5. Start the Flask client

```bash
python client/app.py
```

### 6. Open the app

Navigate to [http://localhost:5000](http://localhost:5000) in your browser. Paste your OpenAI API key if not loaded from `.env`, then start querying.

---

## MCP Tools

| Tool | Arguments | Description |
|------|-----------|-------------|
| `get_deal_summary` | `deal_id` | Returns deal name, asset class, issuer, servicer, trustee, pool balance, pool factor, MTD collections, and next payment date |
| `run_waterfall_check` | `deal_id` | Runs a 5-step payment waterfall: available funds → senior fees → senior interest → OC/IC coverage tests (pass/fail with ratios) → residual to equity |
| `flag_exceptions` | `deal_id` | Checks for delinquency threshold breaches, missing servicer reports, OC test failures, and IC test failures |
| `compare_all_deals` | *(none)* | Portfolio-level comparison table: deal ID, asset class, pool balance, OC test status, open exception count, and inline exception descriptions for every deal |
| `generate_payment_summary` | `deal_id` | Generates a payment direction summary with per-tranche dollar amounts, trustee name, payment date, and `READY TO SUBMIT` or `BLOCKED` status based on coverage test results |

**Available deal IDs:** `AUTO-001` · `CARD-001` · `ABCP-001`

---

## Sample Prompts

1. `Run the waterfall check for CARD-001 and explain the results.`
2. `Flag any exceptions across all three deals: AUTO-001, CARD-001, and ABCP-001.`
3. `Generate the payment summary for AUTO-001 — is it ready to submit?`
4. `Show me a portfolio comparison of all deals.`
5. `Run a full review of CARD-001: deal summary, waterfall check, and exception report.`

---

## Project Structure

```
asg-mcp-server/
├── server/
│   ├── main.py                        # FastMCP server — registers all 5 tools
│   ├── mock_data/
│   │   └── deals.json                 # Simulated TAO SecureHub deal data
│   └── tools/
│       ├── get_deal_summary.py
│       ├── run_waterfall_check.py
│       ├── flag_exceptions.py
│       ├── compare_all_deals.py
│       └── generate_payment_summary.py
├── client/
│   ├── app.py                         # Flask web client + OpenAI tool-call routing
│   └── templates/
│       └── index.html                 # Chat UI with deal badges and health indicators
├── Procfile                           # Railway deployment entry point
├── runtime.txt                        # Python 3.13.3
├── requirements.txt
└── .env                               # Not committed — add your OPENAI_API_KEY here
```

---

## Health Check

Once running, `GET /health` returns server status:

```json
{
  "mcp_server": "online",
  "tools_available": 5,
  "deals_loaded": 3
}
```

---

## Deployment (Railway)

Push to GitHub and connect the repo in Railway. Set `OPENAI_API_KEY` as an environment variable in the Railway dashboard. The `Procfile` and `runtime.txt` are detected automatically.
