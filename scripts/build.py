#!/usr/bin/env python3
"""Single source of truth: data/deals.json -> data/deals.csv + README.md."""
import csv, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
deals = json.load(open(R/'data/deals.json'))
FIELDS = ['category','service','status','deal','dates','ends','link','link_type','last_checked']
with open(R/'data/deals.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(deals)
CHECKED = max(o['last_checked'] for o in deals)
B = {'Live':'🟢 Live','Early':'🟡 Early','Not yet':'⚪ Not yet','Unverified':'🟠 Unverified','Never discounts':'⛔ Never discounts'}
CATS = [('🤖 AI tools',['AI']),('🔒 VPN',['VPN']),('🖥️ Hosting & VPS',['VPS']),('🍎 Mac & dev tools',['Mac/Dev']),('🔍 SEO',['SEO']),('🧰 SaaS & productivity',['SaaS'])]
def link(o): return f"[{'official' if o['link_type']=='official' else 'report'}]({o['link']})" if o['link'] else '—'
def table(rows):
    s = '| Service | Deal | Dates | Ends | Status | Link | Checked |\n|---|---|---|---|---|---|---|\n'
    for o in rows:
        s += f"| **{o['service']}** | {o['deal'].replace('|','/')} | {o['dates']} | {o['ends'] or 'not stated'} | {B[o['status']]} | {link(o)} | {o['last_checked']} |\n"
    return s
live = sorted([o for o in deals if o['status'] in ('Live','Early')], key=lambda o: (o['ends'] == '', o['ends']))
README = (R/'scripts/README.template.md').read_text()
sections = ''
for title, cats in CATS:
    sections += f"\n### {title}\n\n{table([o for o in deals if o['category'] in cats])}"
out = (README.replace('{{N}}', str(len(deals))).replace('{{LIVE}}', str(len(live)))
       .replace('{{CHECKED}}', CHECKED).replace('{{CHECKED_BADGE}}', CHECKED.replace('-','--'))
       .replace('{{LIVE_TABLE}}', table(live)).replace('{{CATEGORIES}}', sections))
(R/'README.md').write_text(out)
print(f'README.md + data/deals.csv rebuilt: {len(deals)} deals, {len(live)} live/early')
