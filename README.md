# Website Technology Checker

[![ci](https://github.com/quantumproxies/website-technology-checker/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/website-technology-checker/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Check what any website is built with, from Python or the command line: CMS, e-commerce platform, JavaScript frameworks, analytics, marketing pixels, payment providers, chat widgets, email marketing scripts, fonts, CDN and web server, plus the WordPress theme and plugins and the GA4, GTM, Google Ads and Meta Pixel ids printed in the page, for up to 50 domains per run, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there is no browser extension to install, no proxy to rotate and no headless browser to keep alive: sign in once and check a list of sites.

```bash
pip install git+https://github.com/quantumproxies/website-technology-checker
tech-checker login
tech-checker lookup allbirds.com -o stacks.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=website-technology-checker).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `tech-checker lookup` | domains or site URLs | CMS, e-commerce platform, frameworks, analytics, pixels, CDN, tracking ids, 24 fields per row ([fields and price](https://quanticdata.io/collectors/technology-lookup-api/?utm_source=github&utm_medium=readme&utm_campaign=website-technology-checker)) | up to 50 |

Up to 50 domains per run, one fetch per domain. Besides the grouped lists, each row carries every detection as `{ name, category }` in `technologies`, the WordPress theme and plugin slugs, the `X-Powered-By` header and the measurement and ad account ids printed in the page source (`tracking_ids`): sites that share an id belong to the same owner.

## Sample output

A real row from `tech-checker lookup nytimes.com allbirds.com --max-results 2` (2026-10-23):

```json
{
  "cdn": "Cloudflare",
  "cms": null,
  "url": "https://www.allbirds.com/",
  "chat": [],
  "fonts": [],
  "other": [],
  "domain": "allbirds.com",
  "server": null,
  "status": "ok",
  "payments": [],
  "security": [
    "hCaptcha"
  ],
  "analytics": [
    "Google Tag Manager",
    "Microsoft Clarity"
  ],
  "generator": null,
  "html_lang": "en-US",
  "marketing": [],
  "frameworks": [],
  "powered_by": null,
  "tech_count": 5,
  "technologies": [
    {
      "name": "Shopify",
      "category": "ecommerce"
    },
    {
      "name": "Google Tag Manager",
      "category": "analytics"
    },
    {
      "name": "Microsoft Clarity",
      "category": "analytics"
    },
    {
      "name": "hCaptcha",
      "category": "security"
    },
    {
      "name": "Cloudflare",
      "category": "cdn"
    }
  ],
  "tracking_ids": {
    "ga4": [],
    "gtm": [
      "GTM-TH8KRSBJ"
    ],
    "google_ads": [],
    "meta_pixel": []
  },
  "email_marketing": [],
  "wordpress_theme": null,
  "wordpress_plugins": [],
  "ecommerce_platform": "Shopify"
}
```

## Python

```python
from quanticdata_website_technology_checker import TechChecker

checker = TechChecker()  # saved login, or QUANTICDATA_API_KEY

sites = checker.lookup(["allbirds.com", "shopify.com"])
for s in sites:
    print(s["domain"], s["cms"], s["ecommerce_platform"], s["cdn"], s["analytics"])
sites.to_csv("stacks.csv")

for s in sites:
    print(s["domain"], s["tracking_ids"]["gtm"], [t["name"] for t in s["technologies"]])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Find the sites on a platform**: Check a list of domains and keep the ones running a given CMS or e-commerce platform (Shopify, WordPress, Magento...), with the rest of their stack: a qualified lead list for agencies and app vendors. See [`examples/find_platform.py`](examples/find_platform.py).
- **Sites with the same owner**: Group a list of domains by the GA4, GTM, Google Ads and Meta Pixel ids printed in their pages and see which ones belong to the same company. See [`examples/same_owner.py`](examples/same_owner.py).
- **Technology share in your market**: Count how many sites of a list use each technology, by category, and get the adoption table as a CSV. See [`examples/stack_report.py`](examples/stack_report.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `tech-checker run <id> -o out.csv` collects it later.

### `tech-checker lookup`

CMS, frameworks, analytics, pixels, payments, chat and hosting of any website, one fetch per domain.

```
tech-checker lookup DOMAINS [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `DOMAINS` | string[] |  | Domains or site URLs, one per line (max 50). |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `20` | How many sites to deliver at most (1–50). You pay only for delivered sites. |

## Output fields

<details><summary><code>tech-checker lookup</code>: 24 fields</summary>

| Field | Type | Description |
|---|---|---|
| `domain` | string | Registrable host (no www). |
| `url` | string | Final homepage URL fetched. |
| `status` | string | "ok" on every delivered row; sites that could not be read are listed under failed with their status (unreachable, blocked, invalid_domain). |
| `cms` | string or null | Content management system / site builder. |
| `ecommerce_platform` | string or null | E-commerce platform. |
| `frameworks` | string[] | JS frameworks and libraries. |
| `analytics` | string[] | Analytics and product-analytics tools. |
| `marketing` | string[] | Ad and marketing pixels. |
| `payments` | string[] | Payment providers loaded on the page. |
| `chat` | string[] | Chat / support widgets. |
| `email_marketing` | string[] | Email marketing / CRM scripts. |
| `security` | string[] | Security and bot-protection services loaded on the page. |
| `fonts` | string[] | Font services. |
| `other` | string[] | Other detected SaaS (CDN media, search, error tracking, consent). |
| `cdn` | string or null | CDN / edge platform from response headers. |
| `server` | string or null | Web server from the Server header. |
| `generator` | string or null | Raw content of the generator meta tag. |
| `technologies` | object[] | Every detection as { name, category }. |
| `tech_count` | integer | Total technologies detected. |
| `wordpress_plugins` | string[] | WordPress plugin slugs seen in the page's asset paths (elementor, woocommerce, contact-form-7…). |
| `wordpress_theme` | string or null | Active WordPress theme slug. |
| `tracking_ids` | object | { ga4, gtm, google_ads, meta_pixel }: the measurement and ad account ids printed in the page source — sites sharing an id belong to the same owner. |
| `powered_by` | string or null | X-Powered-By response header ("PHP/8.2.12", "Express", "ASP.NET"). |
| `html_lang` | string or null | Language declared on the page (&lt;html lang&gt;). |

</details>

## Sign-in and API keys

- `tech-checker login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `tech-checker login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `tech-checker login --api-key`.
- `tech-checker logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=website-technology-checker).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/tech_stack/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"domains": ["nytimes.com", "allbirds.com"], "max_results": 2}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=website-technology-checker) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=website-technology-checker) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this website technology checker free?**

The code is free and MIT-licensed. Lookups run on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies, a headless browser or a browser extension?**

No. You send a list of domains and get one row per site back; the pages are fetched on QuanticData's side.

**What does it detect?**

CMS and site builders, e-commerce platforms, JavaScript frameworks, analytics, ad and marketing pixels, payment providers, chat widgets, email marketing scripts, fonts, CDN, web server, security services, WordPress theme and plugins, and the GA4, GTM, Google Ads and Meta Pixel ids in the page.

**How many sites can one run check?**

Up to 50 domains per run, one fetch each; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Lists such as frameworks and analytics are joined with '; ' and tracking ids become tracking_ids.ga4, tracking_ids.gtm and so on, so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/stack_report.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Email Extractor](https://github.com/quantumproxies/email-extractor): Email extractor for Python and the command line.
- [Company Data API](https://github.com/quantumproxies/company-data-api): Company data API for Python and the command line.
- [Web Scraper API](https://github.com/quantumproxies/web-scraper-api): Web scraper API for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=website-technology-checker).
