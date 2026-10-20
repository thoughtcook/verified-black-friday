#!/usr/bin/env python3
"""Validate data/deals.json schema and that deals.csv matches it."""
import csv, json, re, sys, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(R/'data/deals.json')); errs = []
STATUS = {'Live','Early','Not yet','Unverified','Never discounts'}
REQ = ['category','service','status','deal','dates','ends','link','link_type','last_checked']
BANNED = re.compile(r'(ref=|aff|affiliate|utm_|irclickid|clickid|partner=)', re.I)
for i, o in enumerate(d):
    n = o.get('service', f'#{i}')
    for k in REQ:
        if k not in o: errs.append(f'{n}: missing {k}')
    if o.get('status') not in STATUS: errs.append(f'{n}: bad status {o.get("status")}')
    if o.get('link_type') not in ('official','report','none'): errs.append(f'{n}: bad link_type')
    if o.get('link') and not o['link'].startswith('https://'): errs.append(f'{n}: link must be https')
    if o.get('link') and BANNED.search(o['link']): errs.append(f'{n}: looks like an affiliate/tracking link')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', o.get('last_checked','')): errs.append(f'{n}: last_checked must be YYYY-MM-DD')
    if o.get('ends') and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', o['ends']): errs.append(f'{n}: ends must be YYYY-MM-DD or empty')
    if re.search(r'2025', o.get('deal','')) and "Last year's (2025)" not in o['deal']: errs.append(f"{n}: 2025 figures need the \"Last year's (2025)\" prefix")
    if o.get('status') in ('Live','Early') and not o.get('link'): errs.append(f'{n}: live deals need a link')
rows = list(csv.DictReader(open(R/'data/deals.csv')))
if [dict(r) for r in rows] != [{k: str(o[k]) for k in REQ} for o in d]: errs.append('data/deals.csv is out of sync, run scripts/build.py')
print('\n'.join(errs) or f'OK: {len(d)} deals valid'); sys.exit(1 if errs else 0)
