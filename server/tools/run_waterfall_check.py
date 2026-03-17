import json
import os

DEALS_PATH = os.path.join(os.path.dirname(__file__), "..", "mock_data", "deals.json")


def run_waterfall_check(deal_id: str) -> dict:
    with open(DEALS_PATH) as f:
        deals = json.load(f)

    if deal_id not in deals:
        return {
            "error": f"Deal {deal_id} not found. Available deals: AUTO-001, CARD-001, ABCP-001"
        }

    deal = deals[deal_id]
    wf = deal["waterfall"]

    oc_pass = wf["oc_test_actual"] >= wf["oc_test_required"]
    ic_pass = wf["ic_test_actual"] >= wf["ic_test_required"]
    both_pass = oc_pass and ic_pass

    after_fees = wf["available_funds"] - wf["senior_fees"]
    after_interest = after_fees - wf["senior_interest"]

    return {
        "deal_id": deal_id,
        "deal_name": deal["deal_name"],
        "waterfall": {
            "step_1_available_funds": f"${wf['available_funds']:,.0f}",
            "step_2_senior_fees_paid": f"${wf['senior_fees']:,.0f}",
            "step_3_senior_interest_paid": f"${wf['senior_interest']:,.0f}",
            "step_3_balance_after_senior": f"${after_interest:,.0f}",
            "step_4_oc_test": {
                "result": "PASS" if oc_pass else "FAIL",
                "required": f"{wf['oc_test_required']:.2f}x",
                "actual": f"{wf['oc_test_actual']:.2f}x",
            },
            "step_4_ic_test": {
                "result": "PASS" if ic_pass else "FAIL",
                "required": f"{wf['ic_test_required']:.2f}x",
                "actual": f"{wf['ic_test_actual']:.2f}x",
            },
            "step_5_residual_to_equity": f"${wf['residual_to_equity']:,.0f}",
        },
        "overall_coverage_result": "PASS" if both_pass else "FAIL",
    }
