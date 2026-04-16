"""Main tenant configuration resolver.

Orchestrates the full tenant resolution pipeline:
1. Calculate effective resource limits (compliance-adjusted)
2. Resolve feature entitlements (tier + compliance + overrides)
3. Calculate monthly invoice (usage-based billing)
"""

from saas_config.limits import get_effective_limits
from saas_config.entitlements import resolve_entitlements
from saas_config.billing import calculate_invoice


def resolve_tenant(tenant_config):
    """Fully resolve a tenant's configuration and billing.

    Takes a tenant configuration dict and produces the complete
    resolved state including effective limits, feature entitlements,
    and the monthly invoice.

    Args:
        tenant_config: Dict with:
            - tenant_id: str
            - tier: str (free/starter/professional/enterprise)
            - compliance: list of str (none/soc2/hipaa/pci)
            - feature_overrides: dict of feature_name -> state (optional)
            - purchased_addons: list of feature names (optional)
            - usage: dict with api_calls, storage_gb (optional)

    Returns:
        Dict with:
            - tenant_id: str
            - tier: str
            - effective_limits: dict with api_calls, storage_gb
            - entitlements: dict of feature_name -> state
            - invoice: dict with billing breakdown
    """
    tier = tenant_config["tier"]
    compliance = tenant_config.get("compliance", [])
    overrides = tenant_config.get("feature_overrides", {})
    addons = tenant_config.get("purchased_addons", [])
    usage = tenant_config.get("usage", {})

    effective_limits = get_effective_limits(tier, compliance)

    entitlements = resolve_entitlements(
        tier, compliance,
        feature_overrides=overrides,
        purchased_addons=addons,
    )

    invoice = calculate_invoice(
        tier, compliance,
        usage=usage,
        purchased_addons=addons,
    )

    return {
        "tenant_id": tenant_config.get("tenant_id", "unknown"),
        "tier": tier,
        "effective_limits": effective_limits,
        "entitlements": entitlements,
        "invoice": invoice,
    }
