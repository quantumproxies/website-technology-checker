"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class TechStackRow(TypedDict, total=False):
    """One row of `tech-checker lookup` (tech_stack v1.1.1)."""

    domain: str
    """Registrable host (no www)."""
    url: str
    """Final homepage URL fetched."""
    status: str
    """"ok" on every delivered row; sites that could not be read are listed under failed with their status (unreachable, blocked, invalid_domain)."""
    cms: Optional[str]
    """Content management system / site builder."""
    ecommerce_platform: Optional[str]
    """E-commerce platform."""
    frameworks: List[str]
    """JS frameworks and libraries."""
    analytics: List[str]
    """Analytics and product-analytics tools."""
    marketing: List[str]
    """Ad and marketing pixels."""
    payments: List[str]
    """Payment providers loaded on the page."""
    chat: List[str]
    """Chat / support widgets."""
    email_marketing: List[str]
    """Email marketing / CRM scripts."""
    security: List[str]
    """Security and bot-protection services loaded on the page."""
    fonts: List[str]
    """Font services."""
    other: List[str]
    """Other detected SaaS (CDN media, search, error tracking, consent)."""
    cdn: Optional[str]
    """CDN / edge platform from response headers."""
    server: Optional[str]
    """Web server from the Server header."""
    generator: Optional[str]
    """Raw content of the generator meta tag."""
    technologies: List[Dict[str, Any]]
    """Every detection as { name, category }."""
    tech_count: int
    """Total technologies detected."""
    wordpress_plugins: List[str]
    """WordPress plugin slugs seen in the page's asset paths (elementor, woocommerce, contact-form-7…)."""
    wordpress_theme: Optional[str]
    """Active WordPress theme slug."""
    tracking_ids: Dict[str, Any]
    """{ ga4, gtm, google_ads, meta_pixel }: the measurement and ad account ids printed in the page source — sites sharing an id belong to the same owner."""
    powered_by: Optional[str]
    """X-Powered-By response header ("PHP/8.2.12", "Express", "ASP.NET")."""
    html_lang: Optional[str]
    """Language declared on the page (<html lang>)."""
