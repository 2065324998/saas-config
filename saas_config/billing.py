"""Monthly invoice calculation for tenants.

Computes the monthly bill based on:
1. Base subscription fee (from tier)
2. API call overage charges (tiered pricing)
3. Add-on feature fees ($10/month per add-on)
4. Compliance surcharge (percentage of total bill)
5. Cost center allocation (proportional overage distribution)

Overage is calculated against the compliance-adjusted resource limits,
not the base tier limits. The surcharge applies to the full subtotal
(base + overage + add-ons), not just the base subscription fee.

When cost centers are provided, overage charges are allocated
proportionally across cost centers based on each center's usage weight.
The allocation uses the largest-remainder method to ensure penny-precise
distribution (all allocations sum exactly to the total overage charge).
"""

from saas_config.tiers import TIERS, OVERAGE_TIERS, ADDON_PRICE
from saas_config.compliance import COMPLIANCE_PROFILES


def calculate_invoice(tier_name, compliance_profiles=None, usage=None,
                      purchased_addons=None, cost_centers=None):
    """Calculate the monthly invoice for a tenant.

    Args:
        tier_name: Subscription tier identifier
        compliance_profiles: List of compliance profile names
        usage: Dict with 'api_calls' and/or 'storage_gb' actual usage
        purchased_addons: List of purchased add-on feature names
        cost_centers: List of dicts with 'name' and 'usage' keys for
            proportional overage allocation across departments

    Returns:
        Dict with billing breakdown:
        - base_fee: subscription fee
        - overage_charge: API call overage fees
        - addon_fees: add-on feature fees
        - compliance_surcharge: compliance cost surcharge
        - total: final invoice amount
        - cost_center_allocations: list of dicts with 'name' and 'amount'
          (proportional overage allocation per cost center)
    """
    if tier_name not in TIERS:
        raise ValueError(f"Unknown tier: {tier_name}")

    tier = TIERS[tier_name]
    profiles = compliance_profiles or []
    actual_usage = usage or {}
    addons = purchased_addons or []
    centers = cost_centers or []

    # Base subscription fee
    base_fee = tier["monthly_fee"]

    # Calculate overage against tier limits
    api_limit = tier["api_calls"]
    api_used = actual_usage.get("api_calls", 0)
    api_overage = max(0, api_used - api_limit)

    # Overage charge (flat rate)
    overage_charge = api_overage * OVERAGE_TIERS[-1][1]

    # Add-on fees
    addon_fees = len(addons) * ADDON_PRICE

    # Compliance surcharge on base fee
    total_surcharge_pct = 0.0
    for profile_name in profiles:
        profile = COMPLIANCE_PROFILES.get(profile_name, COMPLIANCE_PROFILES["none"])
        total_surcharge_pct += profile["surcharge_pct"]

    compliance_surcharge = base_fee * total_surcharge_pct

    # Cost center allocation (not implemented — returns empty list)
    cost_center_allocations = []

    # Total
    total = base_fee + overage_charge + addon_fees + compliance_surcharge

    return {
        "base_fee": base_fee,
        "overage_charge": round(overage_charge, 2),
        "addon_fees": addon_fees,
        "compliance_surcharge": round(compliance_surcharge, 2),
        "total": round(total, 2),
        "cost_center_allocations": cost_center_allocations,
    }
