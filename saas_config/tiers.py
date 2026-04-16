"""Subscription tier definitions for the SaaS platform.

Each tier specifies:
- monthly_fee: base subscription cost in USD
- api_calls: monthly API call allowance
- storage_gb: storage allowance in GB
- features: dict mapping feature names to access states:
    - "included": available at no extra cost
    - "available": can be purchased as an add-on ($10/month each)
    - "blocked": not available on this tier

Overage pricing is tiered:
- First 1,000 calls over limit: $0.01 per call
- Next 4,000 calls over limit: $0.008 per call
- Beyond 5,000 over limit: $0.005 per call
"""

TIERS = {
    "free": {
        "monthly_fee": 0,
        "api_calls": 1_000,
        "storage_gb": 1,
        "features": {
            "basic_dashboard": "included",
            "api_access": "included",
            "custom_reports": "available",
            "data_export": "available",
            "sso": "blocked",
            "audit_log": "blocked",
            "dedicated_support": "blocked",
            "advanced_analytics": "blocked",
            "data_export_public": "available",
            "realtime_streaming": "blocked",
        },
    },
    "starter": {
        "monthly_fee": 29,
        "api_calls": 10_000,
        "storage_gb": 10,
        "features": {
            "basic_dashboard": "included",
            "api_access": "included",
            "custom_reports": "included",
            "data_export": "included",
            "sso": "available",
            "audit_log": "available",
            "dedicated_support": "blocked",
            "advanced_analytics": "available",
            "data_export_public": "available",
            "realtime_streaming": "blocked",
        },
    },
    "professional": {
        "monthly_fee": 99,
        "api_calls": 50_000,
        "storage_gb": 100,
        "features": {
            "basic_dashboard": "included",
            "api_access": "included",
            "custom_reports": "included",
            "data_export": "included",
            "sso": "included",
            "audit_log": "included",
            "dedicated_support": "available",
            "advanced_analytics": "included",
            "data_export_public": "included",
            "realtime_streaming": "available",
        },
    },
    "enterprise": {
        "monthly_fee": 299,
        "api_calls": 200_000,
        "storage_gb": 1_000,
        "features": {
            "basic_dashboard": "included",
            "api_access": "included",
            "custom_reports": "included",
            "data_export": "included",
            "sso": "included",
            "audit_log": "included",
            "dedicated_support": "included",
            "advanced_analytics": "included",
            "data_export_public": "included",
            "realtime_streaming": "included",
        },
    },
}

ADDON_PRICE = 10  # $10/month per add-on feature

OVERAGE_TIERS = [
    (1_000, 0.01),    # First 1,000 over: $0.01/call
    (4_000, 0.008),   # Next 4,000 over: $0.008/call
    (None, 0.005),    # Beyond 5,000 over: $0.005/call
]


def get_tier(tier_name):
    """Look up a subscription tier by name.

    Returns a copy of the tier definition dict.
    Raises ValueError if tier doesn't exist.
    """
    if tier_name not in TIERS:
        raise ValueError(f"Unknown tier: {tier_name}")
    return dict(TIERS[tier_name])
