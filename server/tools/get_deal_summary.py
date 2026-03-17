import json
import os

DEALS_PATH = os.path.join(os.path.dirname(__file__), "..", "mock_data", "deals.json")


def get_deal_summary(deal_id: str) -> dict:
    with open(DEALS_PATH) as f:
        deals = json.load(f)

    if deal_id not in deals:
        return {
            "error": f"Deal {deal_id} not found. Available deals: AUTO-001, CARD-001, ABCP-001"
        }

    deal = deals[deal_id]
    pool_pct = deal["pool_balance"] / deal["original_pool_balance"] * 100

    return {
        "deal_id": deal_id,
        "deal_name": deal["deal_name"],
        "asset_class": deal["asset_class"],
        "issuer": deal["issuer"],
        "servicer": deal["servicer"],
        "trustee": deal["trustee"],
        "original_pool_balance": f"${deal['original_pool_balance']:,.0f}",
        "current_pool_balance": f"${deal['pool_balance']:,.0f}",
        "pool_factor": f"{pool_pct:.1f}%",
        "collections_month_to_date": f"${deal['collections_mtd']:,.0f}",
        "next_payment_date": deal["next_payment_date"],
    }
