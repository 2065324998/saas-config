"""Tests for tier definitions and lookup."""

import pytest
from saas_config.tiers import TIERS, get_tier, OVERAGE_TIERS


class TestTierDefinitions:
    def test_all_tiers_exist(self):
        assert set(TIERS.keys()) == {"free", "starter", "professional", "enterprise"}

    def test_tier_has_required_keys(self):
        for name, tier in TIERS.items():
            assert "monthly_fee" in tier, f"{name} missing monthly_fee"
            assert "api_calls" in tier, f"{name} missing api_calls"
            assert "storage_gb" in tier, f"{name} missing storage_gb"
            assert "features" in tier, f"{name} missing features"

    def test_tiers_ordered_by_price(self):
        fees = [TIERS[t]["monthly_fee"] for t in ["free", "starter", "professional", "enterprise"]]
        assert fees == sorted(fees)

    def test_get_tier_returns_copy(self):
        tier = get_tier("starter")
        tier["monthly_fee"] = 9999
        assert TIERS["starter"]["monthly_fee"] == 29

    def test_get_tier_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown tier"):
            get_tier("mythical")

    def test_overage_tiers_defined(self):
        assert len(OVERAGE_TIERS) >= 2
        assert OVERAGE_TIERS[-1][0] is None  # Last tier is unlimited

    def test_free_tier_features(self):
        features = TIERS["free"]["features"]
        assert features["basic_dashboard"] == "included"
        assert features["sso"] == "blocked"
