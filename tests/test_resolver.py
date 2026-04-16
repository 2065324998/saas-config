"""Tests for the main tenant resolver."""

from saas_config.resolver import resolve_tenant


class TestResolver:
    def test_basic_resolution(self):
        """Simple tenant resolution without compliance or overrides."""
        result = resolve_tenant({
            "tenant_id": "t-001",
            "tier": "starter",
        })
        assert result["tenant_id"] == "t-001"
        assert result["tier"] == "starter"
        assert result["effective_limits"]["api_calls"] == 10_000
        assert result["entitlements"]["basic_dashboard"] == "included"
        assert result["invoice"]["total"] == 29

    def test_resolution_with_addons(self):
        result = resolve_tenant({
            "tenant_id": "t-002",
            "tier": "starter",
            "purchased_addons": ["sso"],
        })
        assert result["entitlements"]["sso"] == "included"
        assert result["invoice"]["addon_fees"] == 10
        assert result["invoice"]["total"] == 39
