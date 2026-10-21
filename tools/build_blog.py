#!/usr/bin/env python3
"""Builds the Tips & Guides blog (blog/index.html and blog/<slug>.html) and wires in Google AdSense.

Write posts in tools/posts/<slug>.html (see the comment block at the top of an existing post),
then run:   python3 tools/build_blog.py
It also re-runs tools/build_pages.py so the sitemap includes the blog.

AdSense is OFF until you paste your publisher ID below. While it is off, no ad code is added anywhere.
Once it is on, the AdSense script is added to blog pages ONLY. Service pages, the homepage, the quote
form and contact page never load it, so Auto ads cannot appear there.

Preview where ads would go (grey boxes, nothing loads from Google):
    python3 tools/build_blog.py --preview-ads
Run it again without the flag before you push.
"""
import html
import json
import re
import runpy
import sys
from datetime import date
from pathlib import Path

# ---- AdSense settings ---------------------------------------------------------------------------
# Your publisher ID from AdSense, e.g. 'ca-pub-1234567890123456'. Leave '' until you are approved.
ADSENSE_CLIENT = ''
# Optional: the data-ad-slot number of a display ad unit you created in AdSense (Ads -> By ad unit).
# Leave '' to rely on Auto ads only. When set, an ad unit is placed at every <!--ad--> marker in a post.
AD_SLOT = ''
# -------------------------------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://axeconnect.co.za'
POSTS_DIR = ROOT / 'tools' / 'posts'
OUT = ROOT / 'blog'
PREVIEW = '--preview-ads' in sys.argv

# Reuse the look of privacy.html (icon, theme switch, fonts, colour tokens, header bar, Google tag).
PRIV = (ROOT / 'privacy.html').read_text(encoding='utf-8')


def grab(pattern):
    m = re.search(pattern, PRIV, re.S)
    if not m:
        raise SystemExit(f'Could not find {pattern!r} in privacy.html')
    return m.group(0)


ICON = grab(r'<link rel="icon"[^\n]*')
THEME = grab(r'<script>\(function\(\)\{var t=null;.*?</script>')
FONTS = grab(r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?rel="stylesheet">')
TOKENS = '\n'.join(grab(p) for p in (r':root\{--bg[^\n]*', r'@media \(prefers-color-scheme:dark\)\{:root[^\n]*', r'html\.dark,:root\[data-theme="dark"\][^\n]*'))
BAR_CSS = '\n'.join(grab(p) for p in (r'\.bar\{[^\n]*', r'\.bar-in\{[^\n]*', r'\.logo\{[^\n]*', r'\.logo svg[^\n]*', r'\.back\{[^\n]*', r'\.back:hover[^\n]*'))
GTAG = grab(r'<!-- Google tag \(gtag\.js\) -->.*?</script>\s*<script>.*?</script>')
CALL_TRACK = grab(r'<script>\s*// Google Ads "Click to call".*?</script>')
LOGO = grab(r'<a class="logo" href="/".*?</a>')

CSS = TOKENS + '\n' + BAR_CSS + '''
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--f-body);font-size:17px;line-height:1.75;background:var(--bg);color:var(--text)}
a{color:var(--red);text-underline-offset:3px}
:focus-visible{outline:2px solid var(--red);outline-offset:3px;border-radius:4px}
.eyebrow{font-family:var(--f-mono);font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--red)}
.page{max-width:760px;margin-inline:auto;padding:56px 24px 96px}
.crumbs{font-size:.85rem;color:var(--muted);margin-bottom:18px}.crumbs a{color:var(--muted)}
h1{font-family:var(--f-display);font-weight:800;font-size:clamp(2rem,5vw,3rem);letter-spacing:-.035em;line-height:1.08;color:var(--ink);text-wrap:balance;margin:10px 0 14px}
.meta{font-family:var(--f-mono);font-size:.78rem;color:var(--muted)}
.post .lead{font-size:1.15rem;color:var(--ink);margin:26px 0 8px}
.post h2{font-family:var(--f-display);font-weight:700;font-size:1.5rem;letter-spacing:-.02em;color:var(--ink);margin:40px 0 10px;scroll-margin-top:90px}
.post h3{font-size:1.05rem;color:var(--ink);margin:24px 0 6px}
.post p+p{margin-top:12px}
.post ul,.post ol{padding-left:1.3rem;display:flex;flex-direction:column;gap:6px;margin:10px 0}
.post li::marker{color:var(--red);font-weight:700}
.post strong{color:var(--ink)}
.tip{background:var(--red-soft);border-radius:14px;padding:14px 18px;color:var(--ink);margin:18px 0;font-size:.97rem}
.cta{margin-top:48px;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:26px}
.cta h2{margin:6px 0 8px !important;font-size:1.35rem}
.cta p{color:var(--muted)}
.cta-btns{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:.92rem;text-decoration:none;padding:11px 18px;border-radius:999px;border:1px solid var(--line);color:var(--ink);background:var(--surface)}
.btn-primary{background:var(--red);border-color:var(--red);color:#fff}
.btn:hover{border-color:var(--ink)}.btn-primary:hover{filter:brightness(1.08);border-color:var(--red)}
.ad{margin:32px 0;min-height:100px}
.ad-label{display:block;font-family:var(--f-mono);font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.ad-preview{display:grid;place-items:center;min-height:120px;border:2px dashed var(--line);border-radius:14px;background:var(--surface-2);color:var(--muted);font-family:var(--f-mono);font-size:.8rem;text-align:center;padding:12px}
.list{display:flex;flex-direction:column;gap:14px;margin-top:34px}
.card{display:block;text-decoration:none;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:22px 24px;transition:border-color .2s,transform .2s}
.card:hover{border-color:var(--ink);transform:translateY(-2px)}
.card h2{font-family:var(--f-display);font-weight:700;font-size:1.3rem;letter-spacing:-.02em;color:var(--ink);margin:6px 0}
.card p{color:var(--muted);font-size:.97rem}
.card .meta{margin-top:10px}
.intro{font-size:1.1rem;color:var(--muted);max-width:60ch}
footer{border-top:1px solid var(--line);padding:28px 24px;text-align:center;font-size:.85rem;color:var(--muted)}
footer a{margin:0 8px}
@media(prefers-reduced-motion:reduce){*{transition:none !important;scroll-behavior:auto !important}}
@media(max-width:820px){.page{padding:36px 16px 72px}.bar-in{padding:12px 16px}.card{padding:18px}}
'''

CTAS = {
    'it': ('Still need help?', 'Let us fix it for you.',
           'On-site IT support in Pretoria and remote help anywhere in South Africa, available 24/7.',
           '/it-support.html', 'See IT support'),
    'web': ('Ready to get online?', 'Let us build your website.',
            'Business websites, online stores and booking systems built around your brand.',
            '/web-development.html', 'See web development'),
}


def ad_block():
    """What replaces each <!--ad--> marker in a post."""
    if PREVIEW:
        return ('<div class="ad"><span class="ad-label">Advertisement</span>'
                '<div class="ad-preview">AdSense ad appears here<br>(preview only)</div></div>')
    if ADSENSE_CLIENT and AD_SLOT:
        return (f'<div class="ad"><span class="ad-label">Advertisement</span>'
                f'<ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}" data-ad-slot="{AD_SLOT}" '
                f'data-ad-format="auto" data-full-width-responsive="true"></ins>'
                f'<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></div>')
    return ''  # Auto ads only (or AdSense off): Google decides placement, nothing to insert


def adsense_head():
    if ADSENSE_CLIENT and not PREVIEW:
        return (f'<meta name="google-adsense-account" content="{ADSENSE_CLIENT}">\n'
                f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>\n')
    return ''


def page(title, desc, url, body, jsonld, og_type='website'):
    return f'''<!DOCTYPE html>
<!-- Generated by tools/build_blog.py. Edit the post in tools/posts/ and re-run it. -->
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="{url}"/>
<meta property="og:type" content="{og_type}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:image" content="{SITE}/og-image.jpg"/>
{ICON}
{THEME}
{FONTS}
<style>
{CSS}</style>
<script type="application/ld+json">
{json.dumps(jsonld, indent=2, ensure_ascii=False)}
</script>
{adsense_head()}{GTAG}
</head>
<body>
<header class="bar"><div class="bar-in">
  {LOGO}
  <a class="back" href="/">← Back to site</a>
</div></header>
{body}
<footer>&#169; <span id="yr">2026</span> Axe Connect · <a href="/blog/">Tips &amp; guides</a><a href="/privacy.html">Privacy Policy</a><a href="/terms.html">Terms</a><a href="/">Home</a></footer>
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>
{CALL_TRACK}
</body>
</html>
'''


def read_post(path):
    raw = path.read_text(encoding='utf-8')
    m = re.match(r'\s*<!--(.*?)-->\s*(.*)', raw, re.S)
    if not m:
        raise SystemExit(f'{path.name}: missing the <!-- title: ... --> block at the top')
    meta = dict(re.findall(r'^\s*(\w+)\s*:\s*(.+?)\s*$', m.group(1), re.M))
    for key in ('title', 'description', 'date', 'category', 'cta'):
        if key not in meta:
            raise SystemExit(f'{path.name}: missing "{key}:" in the top comment block')
    if meta['cta'] not in CTAS:
        raise SystemExit(f'{path.name}: cta must be one of {", ".join(CTAS)}')
    body = m.group(2).strip()
    words = len(re.sub(r'<[^>]+>', ' ', body).split())
    meta.update(slug=path.stem, body=body, minutes=max(1, round(words / 200)),
                nice_date=date.fromisoformat(meta['date']).strftime('%-d %B %Y'))
    return meta


def build_post(p):
    url = f'{SITE}/blog/{p["slug"]}.html'
    eyebrow, h, text, link, label = CTAS[p['cta']]
    plain = lambda t: html.unescape(re.sub(r'<[^>]+>', '', t))
    body = f'''<main class="page">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/blog/">Tips &amp; guides</a></nav>
  <span class="eyebrow">{p["category"]}</span>
  <h1>{p["title"]}</h1>
  <p class="meta">{p["nice_date"]} · {p["minutes"]} min read · By Carven Maceke, Axe Connect</p>
  <article class="post">
{p["body"].replace("<!--ad-->", ad_block())}
  </article>
  <aside class="cta">
    <span class="eyebrow">{eyebrow}</span>
    <h2>{h}</h2>
    <p>{text}</p>
    <div class="cta-btns">
      <a class="btn btn-primary" href="{link}">{label} →</a>
      <a class="btn" href="https://wa.me/27607950837" target="_blank" rel="noopener">WhatsApp 060 795 0837</a>
    </div>
  </aside>
</main>'''
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BlogPosting', 'headline': plain(p['title']), 'description': plain(p['description']),
         'datePublished': p['date'], 'url': url, 'image': f'{SITE}/og-image.jpg',
         'author': {'@type': 'Person', 'name': 'Carven Maceke'},
         'publisher': {'@type': 'Organization', 'name': 'Axe Connect', 'url': SITE + '/'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Tips & guides', 'item': SITE + '/blog/'},
            {'@type': 'ListItem', 'position': 3, 'name': plain(p['title']), 'item': url}]}]}
    (OUT / f'{p["slug"]}.html').write_text(
        page(f'{p["title"]} | Axe Connect', p['description'], url, body, ld, 'article'), encoding='utf-8')


def build_index(posts):
    url = f'{SITE}/blog/'
    cards = '\n'.join(
        f'''    <a class="card" href="/blog/{p["slug"]}.html">
      <span class="eyebrow">{p["category"]}</span>
      <h2>{p["title"]}</h2>
      <p>{p["description"]}</p>
      <p class="meta">{p["nice_date"]} · {p["minutes"]} min read</p>
    </a>''' for p in posts)
    body = f'''<main class="page">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / Tips &amp; guides</nav>
  <span class="eyebrow">Tips &amp; guides</span>
  <h1>Practical tech help for South African homes and businesses.</h1>
  <p class="intro">Plain-language guides on fixing common computer problems and getting your business online, from the team at Axe Connect.</p>
  <div class="list">
{cards}
  </div>
</main>'''
    ld = {'@context': 'https://schema.org', '@type': 'Blog', 'name': 'Axe Connect Tips & guides', 'url': url,
          'publisher': {'@type': 'Organization', 'name': 'Axe Connect', 'url': SITE + '/'}}
    (OUT / 'index.html').write_text(
        page('Tips &amp; Guides | IT Help and Website Advice | Axe Connect',
             'Practical guides on fixing slow computers, staying safe online and getting your South African business online, from Axe Connect.',
             url, body, ld), encoding='utf-8')


def ads_txt():
    f = ROOT / 'ads.txt'
    if ADSENSE_CLIENT:
        pub = ADSENSE_CLIENT.replace('ca-', '', 1)
        f.write_text(f'google.com, {pub}, DIRECT, f08c47fec0942fa0\n', encoding='utf-8')
    elif f.exists():
        f.unlink()


posts = sorted((read_post(f) for f in POSTS_DIR.glob('*.html')), key=lambda p: p['date'], reverse=True)
OUT.mkdir(exist_ok=True)
for old in OUT.glob('*.html'):
    old.unlink()
for p in posts:
    build_post(p)
build_index(posts)
ads_txt()
state = 'PREVIEW boxes' if PREVIEW else (f'AdSense ON ({ADSENSE_CLIENT})' if ADSENSE_CLIENT else 'AdSense off')
print(f'blog: {len(posts)} posts, {state}')
runpy.run_path(str(ROOT / 'tools' / 'build_pages.py'))  # rebuilds pages + sitemap (includes the blog)
