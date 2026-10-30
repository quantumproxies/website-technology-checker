"""How many sites of a list use each technology, by category.

    python stack_report.py @competitors.txt --out adoption.csv

Checks the domains in batches of 50 and writes one row per technology with
its category, the number of sites that use it, the share of the list and up
to ten of those sites. The ten most used technologies are printed.
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
    parser.add_argument("--out", default="adoption.csv")
    args = parser.parse_args()

    domains = read_domains(args.domains)
    checker = TechChecker()
    users = defaultdict(set)
    checked = 0
    for i in range(0, len(domains), BATCH):
        batch = domains[i:i + BATCH]
        for site in checker.lookup(batch, max_results=len(batch)):
            checked += 1
            for tech in site.get("technologies") or []:
                users[(tech.get("category") or "other", tech["name"])].add(site["domain"])

    rows = [{"technology": name, "category": category, "sites": len(sites),
             "share": round(len(sites) / checked, 3) if checked else 0, "examples": sorted(sites)[:10]}
            for (category, name), sites in users.items()]
    rows.sort(key=lambda r: (-r["sites"], r["technology"]))
    write(rows, args.out)
    print(f"{checked} sites checked, {len(rows)} technologies found, written to {args.out}")
    for r in rows[:10]:
        print(f"  {r['sites']:4d}  {r['share']:6.1%}  {r['technology']} ({r['category']})")


if __name__ == "__main__":
    main()
