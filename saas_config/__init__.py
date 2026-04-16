"""Multi-tenant SaaS configuration resolver.

Resolves tenant configurations by combining subscription tiers,
compliance profiles, feature overrides, and usage data to produce
effective resource limits, feature entitlements, and monthly invoices.
"""

from saas_config.resolver import resolve_tenant
from saas_config.limits import get_effective_limits
from saas_config.entitlements import resolve_entitlements
from saas_config.billing import calculate_invoice

__version__ = "0.2.0"
