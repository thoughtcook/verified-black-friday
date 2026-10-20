# Contributing

Thanks for helping keep this list honest. Rules:

1. **Official link required.** Link the vendor's own pricing/BF page or official coupon URL. News or deal-site links alone go in as 🟠 Unverified.
2. **Copy, don't estimate.** Use the exact price, term (e.g. "2-yr, billed upfront") and dates shown. If no end date is published, write "end not stated".
3. **No affiliate, referral or tracking links.** PRs containing them are closed.
4. **No grey-market resellers** (shared/resold accounts, "lifetime" keys from unofficial sellers).
5. Edit `data/deals.json` (set `last_checked` to today and `ends` to YYYY-MM-DD if published), then run `python3 scripts/build.py && python3 scripts/validate.py`. Never edit README tables or deals.csv by hand.
6. Last year's prices must be prefixed "Last year's (2025)".
7. Vendors may submit their own deals; disclose it in the PR.

Status values: `Live`, `Early`, `Not yet`, `Unverified`, `Never discounts`.
8. Price changes go in CHANGELOG.md with the date and source.
