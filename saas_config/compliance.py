"""Compliance profile definitions for regulatory requirements.

Each compliance profile specifies:
- resource_overhead: fraction of resources consumed by compliance
  infrastructure (audit logging, encryption, etc.). For example,
  0.15 means 15% of the resource capacity is used for compliance,
  leaving 85% for the tenant.

  When multiple profiles apply, overheads compound multiplicatively:
  SOC2 (10%) + HIPAA (15%) = (1 - 0.10) * (1 - 0.15) = 0.765
  meaning 76.5% of capacity remains, not 75%.

- blocked_features: features that cannot be used under this profile,
  regardless of tier or overrides. Compliance blocks are absolute.

- required_features: features that MUST be enabled for compliance.
  If the tenant's tier doesn't include them, they're force-enabled.

- surcharge_pct: percentage surcharge on the total monthly bill
  (base + overage + add-ons) to cover compliance costs.
"""

COMPLIANCE_PROFILES = {
    "none": {
        "resource_overhead": 0.0,
        "blocked_features": [],
        "required_features": [],
        "surcharge_pct": 0.0,
    },
    "soc2": {
        "resource_overhead": 0.10,
        "blocked_features": [],
        "required_features": ["audit_log"],
        "surcharge_pct": 0.10,
    },
    "hipaa": {
        "resource_overhead": 0.15,
        "blocked_features": ["data_export_public"],
        "required_features": ["audit_log", "sso"],
        "surcharge_pct": 0.15,
    },
    "pci": {
        "resource_overhead": 0.25,
        "blocked_features": ["data_export_public", "realtime_streaming"],
        "required_features": ["audit_log", "sso"],
        "surcharge_pct": 0.20,
    },
}


def get_compliance_profile(name):
    """Look up a compliance profile by name.

    Returns the profile dict. Defaults to 'none' for unknown profiles.
    """
    return COMPLIANCE_PROFILES.get(name, COMPLIANCE_PROFILES["none"])
