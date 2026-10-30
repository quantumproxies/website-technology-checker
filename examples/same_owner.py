"""Group websites by the GA4, GTM, Google Ads and Meta Pixel ids in their pages.

    python same_owner.py @domains.txt --out shared_ids.csv

Sites that print the same measurement or ad account id are run by the same
owner (or the same agency). Writes one row per id shared by two or more of
the sites, with the id type and the domains that carry it.
"""

import argparse
from collections import defaultdict

from quanticdata_website_technology_checker import TechChecker, write

BATCH = 50


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
    parser.add_argument("--out", default="shared_ids.csv")
    args = parser.parse_args()

    domains = read_domains(args.domains)
    checker = TechChecker()
    owners = defaultdict(set)
    checked = 0
    for i in range(0, len(domains), BATCH):
        batch = domains[i:i + BATCH]
        for site in checker.lookup(batch, max_results=len(batch)):
            checked += 1
            for kind, ids in (site.get("tracking_ids") or {}).items():
                for tracking_id in ids or []:
                    owners[(kind, tracking_id)].add(site["domain"])

    rows = [{"id_type": kind, "id": tracking_id, "sites": len(sites), "domains": sorted(sites)}
            for (kind, tracking_id), sites in owners.items() if len(sites) > 1]
    rows.sort(key=lambda r: -r["sites"])
    write(rows, args.out)
    print(f"{checked} sites checked, {len(rows)} ids shared by two or more of them, written to {args.out}")
    for r in rows[:10]:
        print(f"  {r['id_type']:10} {r['id']:20} {', '.join(r['domains'])}")


if __name__ == "__main__":
    main()
