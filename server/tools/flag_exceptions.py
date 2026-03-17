import json
import os

DEALS_PATH = os.path.join(os.path.dirname(__file__), "..", "mock_data", "deals.json")


def flag_exceptions(deal_id: str) -> dict:
    with open(DEALS_PATH) as f:
        deals = json.load(f)

    if deal_id not in deals:
        return {
            "error": f"Deal {deal_id} not found. Available deals: AUTO-001, CARD-001, ABCP-001"
        }

    deal = deals[deal_id]
    exc = deal["exceptions"]
    wf = deal["waterfall"]
    flags = []

    # Delinquency threshold check
    if exc["delinquency_rate"] > exc["delinquency_threshold"]:
        flags.append(
            f"DELINQUENCY BREACH: Current rate {exc['delinquency_rate'] * 100:.2f}% "
            f"exceeds threshold of {exc['delinquency_threshold'] * 100:.2f}%"
        )

    # Servicer report receipt check
    if not exc["servicer_report_received"]:
        flags.append(
            "MISSING SERVICER REPORT: Servicer report not received by the required deadline"
        )

    # Coverage test failures
    if not exc["coverage_test_pass"]:
        oc_pass = wf["oc_test_actual"] >= wf["oc_test_required"]
        ic_pass = wf["ic_test_actual"] >= wf["ic_test_required"]
        if not oc_pass:
            flags.append(
                f"OC TEST FAILURE: Actual {wf['oc_test_actual']:.2f}x is below "
                f"required {wf['oc_test_required']:.2f}x — credit enhancement insufficient"
            )
        if not ic_pass:
            flags.append(
                f"IC TEST FAILURE: Actual {wf['ic_test_actual']:.2f}x is below "
                f"required {wf['ic_test_required']:.2f}x — interest coverage deficient"
            )

    return {
        "deal_id": deal_id,
        "deal_name": deal["deal_name"],
        "status": "EXCEPTIONS FLAGGED" if flags else "CLEAN",
        "exception_count": len(flags),
        "exceptions": flags if flags else ["No exceptions found"],
    }
