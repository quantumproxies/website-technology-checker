"""Keep the websites of a list that run on a given platform, CMS or tool.

    python find_platform.py @domains.txt --uses Shopify --out shopify_sites.csv

Checks the domains in batches of 50 (the most one run takes) and keeps the
sites where any detection matches --uses (case-insensitive: Shopify,
WordPress, WooCommerce, Klaviyo...). Each kept row has the CMS, e-commerce
platform, analytics, marketing pixels, payments, chat and CDN of the site.
"""

import argparse

from quanticdata_website_technology_checker import TechChecker, write

BATCH = 50
FIELDS = ["domain", "cms", "ecommerce_platform", "analytics", "marketing", "payments", "chat",
          "email_marketing", "cdn", "tech_count", "url"]


def read_domains(values):
    domains = []
    for v in values:
        if v.startswith("@"):
            with open(v[1:], encoding="utf-8") as fh:
                domains += [line.strip() for line in fh if line.strip() and not line.startswith("#")]
        else:
            domains.append(v)
    return domains


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("domains", nargs="+", help="domains, URLs or @file.txt")
    parser.add_argument("--uses", required=True, help="technology name to look for, e.g. Shopify")
    parser.add_argument("--out", default="matches.csv")
    args = parser.parse_args()

    domains = read_domains(args.domains)
    wanted = args.uses.lower()
    checker = TechChecker()
    matches = []
    checked = 0
    for i in range(0, len(domains), BATCH):
        batch = domains[i:i + BATCH]
        for site in checker.lookup(batch, max_results=len(batch)):
            checked += 1
            names = [t["name"].lower() for t in site.get("technologies") or []]
            names += [(site.get("wordpress_theme") or "").lower()] + [p.lower() for p in site.get("wordpress_plugins") or []]
            if any(wanted in n for n in names if n):
                matches.append({k: site.get(k) for k in FIELDS})

    write(matches, args.out)
    print(f"{len(matches)} of {checked} sites use {args.uses}, written to {args.out}")


if __name__ == "__main__":
    main()
