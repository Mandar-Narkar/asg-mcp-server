import json
import os

DEALS_PATH = os.path.join(os.path.dirname(__file__), "..", "mock_data", "deals.json")

_AVAILABLE = "AUTO-001, CARD-001, ABCP-001"


def compare_all_deals() -> dict:
    with open(DEALS_PATH) as f:
        deals = json.load(f)

    rows = []
    total_exceptions = 0

    for deal_id, deal in deals.items():
        wf = deal["waterfall"]
        exc = deal["exceptions"]

        oc_pass = wf["oc_test_actual"] >= wf["oc_test_required"]
        ic_pass = wf["ic_test_actual"] >= wf["ic_test_required"]

        oc_status = (
            f"PASS ({wf['oc_test_actual']:.2f}x vs {wf['oc_test_required']:.2f}x required)"
            if oc_pass
            else f"FAIL ({wf['oc_test_actual']:.2f}x vs {wf['oc_test_required']:.2f}x required)"
        )

        inline_exceptions = []
        if exc["delinquency_rate"] > exc["delinquency_threshold"]:
            inline_exceptions.append(
                f"Delinquency breach: {exc['delinquency_rate']*100:.2f}% > {exc['delinquency_threshold']*100:.2f}% threshold"
            )
        if not exc["servicer_report_received"]:
            inline_exceptions.append("Missing servicer report")
        if not oc_pass:
            inline_exceptions.append(
                f"OC test failure: {wf['oc_test_actual']:.2f}x < {wf['oc_test_required']:.2f}x required"
            )
        if not ic_pass:
            inline_exceptions.append(
                f"IC test failure: {wf['ic_test_actual']:.2f}x < {wf['ic_test_required']:.2f}x required"
            )

        total_exceptions += len(inline_exceptions)

        rows.append({
            "deal_id": deal_id,
            "asset_class": deal["asset_class"],
            "pool_balance_usd": deal["pool_balance"],
            "oc_test_status": oc_status,
            "open_exceptions": len(inline_exceptions),
            "exceptions": inline_exceptions if inline_exceptions else ["None"],
        })

    return {
        "portfolio_summary": {
            "total_deals": len(rows),
            "total_pool_balance_usd": sum(r["pool_balance_usd"] for r in rows),
            "deals_with_exceptions": sum(1 for r in rows if r["open_exceptions"] > 0),
            "total_exceptions_count": total_exceptions,
        },
        "deals": rows,
    }
