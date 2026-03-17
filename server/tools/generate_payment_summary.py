import json
import os

DEALS_PATH = os.path.join(os.path.dirname(__file__), "..", "mock_data", "deals.json")

_AVAILABLE = "AUTO-001, CARD-001, ABCP-001"


def generate_payment_summary(deal_id: str) -> dict:
    with open(DEALS_PATH) as f:
        deals = json.load(f)

    if deal_id not in deals:
        return {
            "error": f"Deal {deal_id} not found. Available deals: {_AVAILABLE}"
        }

    deal = deals[deal_id]
    wf = deal["waterfall"]

    oc_pass = wf["oc_test_actual"] >= wf["oc_test_required"]
    ic_pass = wf["ic_test_actual"] >= wf["ic_test_required"]
    both_pass = oc_pass and ic_pass

    blocking_reasons = []
    if not oc_pass:
        blocking_reasons.append(
            f"OC test failure: actual {wf['oc_test_actual']:.2f}x < required {wf['oc_test_required']:.2f}x"
        )
    if not ic_pass:
        blocking_reasons.append(
            f"IC test failure: actual {wf['ic_test_actual']:.2f}x < required {wf['ic_test_required']:.2f}x"
        )

    return {
        "deal_id": deal_id,
        "deal_name": deal["deal_name"],
        "trustee": deal["trustee"],
        "payment_date": deal["next_payment_date"],
        "submission_status": "READY TO SUBMIT" if both_pass else "BLOCKED",
        "tranches": {
            "senior_fees": f"${wf['senior_fees']:,.0f}",
            "senior_interest": f"${wf['senior_interest']:,.0f}",
            "residual_to_equity": f"${wf['residual_to_equity']:,.0f}",
        },
        "coverage_tests": {
            "oc_test": "PASS" if oc_pass else "FAIL",
            "ic_test": "PASS" if ic_pass else "FAIL",
        },
        "blocking_reasons": blocking_reasons if blocking_reasons else None,
    }
