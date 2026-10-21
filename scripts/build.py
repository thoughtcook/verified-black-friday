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

# Prerender deal cards into the site so content is in the served HTML (JS re-renders for filtering).
import html, re as _re
H = R/'docs/index.html'; page = H.read_text()
rank = {'Live':0,'Early':1,'Unverified':2,'Not yet':3,'Never discounts':4}
e = lambda s: html.escape(str(s), quote=True)
cards = ''.join(
    f'<div class="c"><span class="b {e(o["status"])}">{e(o["status"])}</span> <span class="cat">{e(o["category"])}</span><h3>{e(o["service"])}</h3><div class="d">{e(o["deal"])}</div>'
    f'<div class="cat">{e(o["dates"])}{" · ends "+e(o["ends"]) if o["ends"] else ""} · checked {e(o["last_checked"])}</div>'
    + (f'<a href="{e(o["link"])}" rel="noopener nofollow" target="_blank">{"Official page" if o["link_type"]=="official" else "Source report"} ↗</a>' if o['link'] else '') + '</div>\n'
    for o in sorted(deals, key=lambda o: (rank[o['status']], o['ends'] or '9')))
meta = f'{len(deals)} deals tracked · {len(live)} live · last checked {CHECKED}'
page = _re.sub(r'<p class="sub" id="meta">.*?</p>', f'<p class="sub" id="meta">{meta}</p>', page, flags=_re.S)
page = _re.sub(r'<main id="g">.*?</main>', lambda m: f'<main id="g">\n{cards}</main>', page, flags=_re.S)
page = _re.sub(r'"dateModified":"[\d-]+"', f'"dateModified":"{CHECKED}"', page)
H.write_text(page)
S = R/'docs/sitemap.xml'; S.write_text(_re.sub(r'<lastmod>[\d-]+</lastmod>', f'<lastmod>{CHECKED}</lastmod>', S.read_text()))
print('docs/index.html prerendered')
