"""Resource limit calculation with compliance adjustments.

Computes effective resource limits for a tenant by applying compliance
overhead factors to the base tier limits. When multiple compliance
profiles are active, their overhead factors compound multiplicatively.
"""

import math

from saas_config.tiers import TIERS
from saas_config.compliance import COMPLIANCE_PROFILES


def get_effective_limits(tier_name, compliance_profiles=None):
    """Calculate effective resource limits after compliance adjustments.

    Each compliance profile has a resource_overhead factor representing
    the fraction of capacity consumed by compliance infrastructure.
    Multiple profiles compound multiplicatively:

        SOC2 (10%) + HIPAA (15%):
        effective = base * (1 - 0.10) * (1 - 0.15) = base * 0.765

    Resource limits are always rounded DOWN to whole units (you can't
    provision a fraction of an API call or a fraction of a GB).

    Args:
        tier_name: Subscription tier identifier
        compliance_profiles: List of compliance profile names

    Returns:
        Dict with 'api_calls' and 'storage_gb' effective limits
    """
    if tier_name not in TIERS:
        raise ValueError(f"Unknown tier: {tier_name}")

    tier = TIERS[tier_name]
    profiles = compliance_profiles or []

    base_api = tier["api_calls"]
    base_storage = tier["storage_gb"]

    # Calculate combined compliance overhead
    total_overhead = 0.0
    for profile_name in profiles:
        profile = COMPLIANCE_PROFILES.get(profile_name, COMPLIANCE_PROFILES["none"])
        total_overhead += profile["resource_overhead"]

    multiplier = max(1.0 - total_overhead, 0.1)  # Floor at 10%

    return {
        "api_calls": round(base_api * multiplier),
        "storage_gb": round(base_storage * multiplier),
    }
