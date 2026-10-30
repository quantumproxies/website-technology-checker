"""Website Technology Checker: Website technology checker for Python and the command line: CMS, e-commerce platform, frameworks, analytics, ad pixels, payments, chat and CDN of any website, plus WordPress theme and plugins and GA4, GTM and Meta Pixel ids, as JSON or CSV. Free and open source; sign in with your QuanticData account, no browser extension or proxies needed.

    from quanticdata_website_technology_checker import TechChecker

    scraper = TechChecker()   # saved login (`tech-checker login`) or QUANTICDATA_API_KEY
    run = scraper.lookup(...)   # the technologies a list of websites run on
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["TechChecker", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class TechChecker:
    """Website Technology Checker on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="tech-checker/0.1.0 (+https://github.com/quantumproxies/website-technology-checker)", timeout=timeout)

    def lookup(
        self, domains: Union[str, Sequence[str]],
        *,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """CMS, frameworks, analytics, pixels, payments, chat and hosting of any website, one fetch per domain.

        Args:
            domains: Domains or site URLs, one per line (max 50).
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many sites to deliver at most (1–50). You pay only for delivered sites.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per site: see ``types.TechStackRow``.
        """
        payload = {
            "domains": _as_list(domains),
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("tech_stack", payload, wait=wait, timeout=timeout)
