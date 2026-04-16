"""Tests for feature entitlement resolution."""

from saas_config.entitlements import resolve_entitlements


class TestEntitlements:
    def test_basic_tier_features(self):
        """Tier features returned without modifications."""
        result = resolve_entitlements("starter")
        assert result["basic_dashboard"] == "included"
        assert result["custom_reports"] == "included"
        assert result["sso"] == "available"
        assert result["dedicated_support"] == "blocked"

    def test_override_available_to_included(self):
        """Override can upgrade an available feature to included."""
        result = resolve_entitlements(
            "starter",
            feature_overrides={"sso": "included"},
        )
        assert result["sso"] == "included"

    def test_addon_upgrades_available(self):
        """Purchased add-on upgrades 'available' to 'included'."""
        result = resolve_entitlements(
            "starter",
            purchased_addons=["sso"],
        )
        assert result["sso"] == "included"

    def test_addon_does_not_upgrade_blocked(self):
        """Add-on cannot upgrade a blocked feature."""
        result = resolve_entitlements(
            "starter",
            purchased_addons=["dedicated_support"],
        )
        assert result["dedicated_support"] == "blocked"

    def test_compliance_required_features(self):
        """SOC2 requires audit_log, which should be force-included."""
        result = resolve_entitlements("starter", ["soc2"])
        assert result["audit_log"] == "included"

    def test_no_compliance_no_blocks(self):
        """Without compliance, professional tier has all features."""
        result = resolve_entitlements("professional")
        assert result["data_export_public"] == "included"
        assert result["sso"] == "included"
