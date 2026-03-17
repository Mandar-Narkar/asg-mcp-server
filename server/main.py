import sys
import os

# Ensure the server directory is on the path so tool imports resolve
sys.path.insert(0, os.path.dirname(__file__))

from mcp.server.fastmcp import FastMCP
from tools.get_deal_summary import get_deal_summary as _get_deal_summary
from tools.run_waterfall_check import run_waterfall_check as _run_waterfall_check
from tools.flag_exceptions import flag_exceptions as _flag_exceptions
from tools.compare_all_deals import compare_all_deals as _compare_all_deals
from tools.generate_payment_summary import generate_payment_summary as _generate_payment_summary

mcp = FastMCP("ASG Securitization Operations Assistant")


@mcp.tool()
def get_deal_summary(deal_id: str) -> dict:
    """
    Get a summary of a securitization deal.

    Returns deal name, asset class, issuer, servicer, trustee, original and
    current pool balance, pool factor, month-to-date collections, and next
    payment date.

    Available deal IDs: AUTO-001, CARD-001, ABCP-001
    """
    return _get_deal_summary(deal_id)


@mcp.tool()
def run_waterfall_check(deal_id: str) -> dict:
    """
    Run a 5-step payment waterfall check for a securitization deal.

    Steps: available funds → senior fees paid → senior interest paid →
    OC/IC coverage test results (pass/fail with required vs actual) →
    residual amount distributed to equity.

    Available deal IDs: AUTO-001, CARD-001, ABCP-001
    """
    return _run_waterfall_check(deal_id)


@mcp.tool()
def flag_exceptions(deal_id: str) -> dict:
    """
    Check a securitization deal for operational exceptions.

    Checks for: delinquency rate above threshold, missing servicer report,
    OC test failure, IC test failure. Returns a list of flagged issues or
    confirms the deal is clean.

    Available deal IDs: AUTO-001, CARD-001, ABCP-001
    """
    return _flag_exceptions(deal_id)


@mcp.tool()
def compare_all_deals() -> dict:
    """
    Compare all securitization deals in the portfolio.

    Returns a portfolio-level table showing deal ID, asset class, pool balance,
    OC test status (pass/fail with actual vs required ratio), and open exception
    count for each deal. Also includes a portfolio summary with total deal count,
    aggregate pool balance, and number of deals with active exceptions.

    No arguments required — reads all deals from the data store.
    """
    return _compare_all_deals()


@mcp.tool()
def generate_payment_summary(deal_id: str) -> dict:
    """
    Generate a payment summary for a securitization deal.

    Returns dollar amounts per tranche (senior fees, senior interest, residual to
    equity), the trustee name, payment date, and a submission status of either
    READY TO SUBMIT (all coverage tests pass) or BLOCKED (OC or IC test failure),
    with specific blocking reasons when applicable.

    Available deal IDs: AUTO-001, CARD-001, ABCP-001
    """
    return _generate_payment_summary(deal_id)


if __name__ == "__main__":
    mcp.run()
