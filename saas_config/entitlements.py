"""Feature entitlement resolution for tenants.

Determines which features a tenant can access based on their subscription
tier, compliance requirements, feature overrides, and purchased add-ons.

Resolution precedence (highest to lowest):
1. Compliance blocks — absolute, cannot be overridden by any mechanism
2. Compliance required features — force-enabled for regulatory compliance
3. Feature overrides — tenant-specific customizations (e.g., beta access)
4. Purchased add-ons — upgrade "available" features to "included"
5. Tier defaults — base feature set for the subscription tier
"""

from saas_config.tiers import TIERS
from saas_config.compliance import COMPLIANCE_PROFILES


def resolve_entitlements(tier_name, compliance_profiles=None,
                         feature_overrides=None, purchased_addons=None):
    """Resolve the effective feature entitlements for a tenant.

    Args:
        tier_name: Subscription tier identifier
        compliance_profiles: List of compliance profile names
        feature_overrides: Dict mapping feature names to desired states
        purchased_addons: List of feature names purchased as add-ons

    Returns:
        Dict mapping feature names to their effective states:
        "included", "available", or "blocked"
    """
    if tier_name not in TIERS:
        raise ValueError(f"Unknown tier: {tier_name}")

    tier = TIERS[tier_name]
    features = dict(tier["features"])
    profiles = compliance_profiles or []
    overrides = feature_overrides or {}
    addons = set(purchased_addons or [])

    # Collect compliance constraints
    blocked = set()
    required = set()
    for profile_name in profiles:
        profile = COMPLIANCE_PROFILES.get(profile_name, COMPLIANCE_PROFILES["none"])
        blocked.update(profile["blocked_features"])
        required.update(profile["required_features"])

    # Apply compliance blocks first
    for feature in blocked:
        if feature in features:
            features[feature] = "blocked"

    # Apply feature overrides
    for feature, state in overrides.items():
        if feature in features:
            features[feature] = state

    # Apply purchased add-ons (upgrade "available" to "included")
    for feature in addons:
        if feature in features and features[feature] == "available":
            features[feature] = "included"

    # Apply compliance required features (force-enable for compliance)
    for feature in required:
        if feature in features and features[feature] != "blocked":
            features[feature] = "included"

    return features
