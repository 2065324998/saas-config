"""Tests for invoice calculation."""

from saas_config.billing import calculate_invoice


class TestInvoice:
    def test_base_fee_only(self):
        """Invoice with no usage, no add-ons, no compliance."""
        invoice = calculate_invoice("starter")
        assert invoice["base_fee"] == 29
        assert invoice["overage_charge"] == 0
        assert invoice["addon_fees"] == 0
        assert invoice["compliance_surcharge"] == 0
        assert invoice["total"] == 29

    def test_no_overage(self):
        """Usage within limits produces no overage charge."""
        invoice = calculate_invoice("starter", usage={"api_calls": 5000})
        assert invoice["overage_charge"] == 0
        assert invoice["total"] == 29

    def test_addon_fees(self):
        """Each purchased add-on costs $10."""
        invoice = calculate_invoice(
            "starter",
            purchased_addons=["sso", "audit_log"],
        )
        assert invoice["addon_fees"] == 20
        assert invoice["total"] == 49  # 29 + 20

    def test_free_tier_zero_base(self):
        invoice = calculate_invoice("free")
        assert invoice["base_fee"] == 0
        assert invoice["total"] == 0
