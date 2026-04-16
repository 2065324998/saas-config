"""Tests for resource limit calculation."""

import pytest
from saas_config.limits import get_effective_limits


class TestEffectiveLimits:
    def test_no_compliance(self):
        """Base tier limits with no compliance profiles."""
        limits = get_effective_limits("starter")
        assert limits["api_calls"] == 10_000
        assert limits["storage_gb"] == 10

    def test_no_compliance_professional(self):
        limits = get_effective_limits("professional")
        assert limits["api_calls"] == 50_000
        assert limits["storage_gb"] == 100

    def test_single_compliance_soc2(self):
        """Single compliance profile reduces limits by overhead factor."""
        limits = get_effective_limits("starter", ["soc2"])
        # SOC2 overhead = 10%, so 90% of base
        assert limits["api_calls"] == 9_000
        assert limits["storage_gb"] == 9

    def test_single_compliance_hipaa(self):
        limits = get_effective_limits("professional", ["hipaa"])
        # HIPAA overhead = 15%, so 85% of base
        assert limits["api_calls"] == 42_500
        assert limits["storage_gb"] == 85

    def test_unknown_tier_raises(self):
        with pytest.raises(ValueError, match="Unknown tier"):
            get_effective_limits("platinum")

    def test_empty_compliance_list(self):
        limits = get_effective_limits("enterprise", [])
        assert limits["api_calls"] == 200_000
        assert limits["storage_gb"] == 1_000

    def test_unknown_compliance_ignored(self):
        """Unknown compliance profiles are treated as 'none'."""
        limits = get_effective_limits("starter", ["unknown_profile"])
        assert limits["api_calls"] == 10_000
        assert limits["storage_gb"] == 10
