#!/usr/bin/env python3
"""Builds the separate SEO pages (web-development.html, it-support.html, ...) from index.html.

index.html stays the single source of design, header, footer, modals and scripts.
Each page gets its own title, description, canonical URL, H1, breadcrumbs, structured
data and FAQs, plus the homepage sections that belong to it.

Run after changing index.html:  python3 tools/build_pages.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://axeconnect.co.za/'
SRC = (ROOT / 'index.html').read_text(encoding='utf-8')


def section(marker):
    """Return a homepage <section> by its opening tag text, e.g. 'id="system"'."""
    start = SRC.index('<section ' + marker)
    end = SRC.index('</section>', start) + len('</section>')
    return SRC[start:end]


def faq_block(items, eyebrow, title):
    rows = []
    for i, (q, a) in enumerate(items):
        rows.append(
            f'      <details class="faq-item"{" open" if i == 0 else ""}>\n'
            f'        <summary><h3>{q}</h3><span class="faq-plus" aria-hidden="true"></span></summary>\n'
            f'        <p>{a}</p>\n'
            f'      </details>')
    return (
        '<section class="sec page-faq">\n  <div class="wrap">\n    <div class="sec-head">\n      <div>\n'
        f'        <span class="eyebrow">{eyebrow}</span>\n        <h2>{title}</h2>\n      </div>\n    </div>\n'
        '    <div class="faq-list">\n' + '\n'.join(rows) + '\n    </div>\n  </div>\n</section>')


def see_also(current):
    links = [(p['file'], p['crumb']) for p in PAGES if p['file'] != current]
    items = ''.join(f'<a href="{f}">{c} <svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>' for f, c in links)
    return ('<section class="sec see-more">\n  <div class="wrap">\n    <span class="eyebrow">Explore more</span>\n'
            f'    <div class="see-also">{items}</div>\n  </div>\n</section>')


ARROW = '<svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg>'
PHONE = '<svg class="icon" aria-hidden="true"><use href="#i-phone"/></svg>'


def check(t):
    return f'<li><svg class="icon" aria-hidden="true"><use href="#i-check-circle"/></svg>{t}</li>'


def phero(p):
    return f'''<section class="phero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a><svg class="icon" aria-hidden="true"><use href="#i-chevron-right"/></svg><span aria-current="page">{p["crumb"]}</span></nav>
    <span class="eyebrow">{p["eyebrow"]}</span>
    <h1>{p["h1"]}</h1>
    <p class="phero-lead">{p["lead"]}</p>
    <div class="hero-btns">
      <button type="button" class="btn btn-primary" onclick="{p["cta"]}">{p["cta_label"]} {ARROW}</button>
      <button type="button" class="btn btn-ghost" onclick="openCallModal()">{PHONE} Call or WhatsApp</button>
    </div>
    <ul class="hero-checks">{"".join(check(c) for c in p["checks"])}</ul>
    <aside class="phero-card" aria-label="Contact Axe Connect">
      <span class="pc-k"><i></i>Available 24/7</span>
      <b class="pc-t">Talk to a real person</b>
      <a href="tel:0607950837"><svg class="icon" aria-hidden="true"><use href="#i-phone"/></svg><span><small>Call</small>060 795 0837</span></a>
      <a href="https://wa.me/27607950837" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-message-circle"/></svg><span><small>WhatsApp</small>Send us a message</span></a>
      <a href="mailto:info@axeconnect.co.za"><svg class="icon" aria-hidden="true"><use href="#i-mail"/></svg><span><small>Email</small>info@axeconnect.co.za</span></a>
    </aside>
  </div>
</section>'''


SMM = '''<section class="sec smm">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <span class="eyebrow">What's included</span>
        <h2>Your pages, <em>active and on-brand.</em></h2>
      </div>
      <p>We take social media off your plate, so you can focus on running the business while your pages keep working for you.</p>
    </div>
    <div class="smm-grid">
      <div class="smm-card"><svg class="icon" aria-hidden="true"><use href="#i-cal"/></svg><h3>Content planning</h3><p>A monthly plan of posts built around your products, services, specials and seasons.</p></div>
      <div class="smm-card"><svg class="icon" aria-hidden="true"><use href="#i-image"/></svg><h3>Post &amp; graphic design</h3><p>Eye-catching graphics, posters and flyers designed in your brand colours.</p></div>
      <div class="smm-card"><svg class="icon" aria-hidden="true"><use href="#i-edit"/></svg><h3>Captions that sell</h3><p>Clear, friendly captions that speak to your customers and tell them what to do next.</p></div>
      <div class="smm-card"><svg class="icon" aria-hidden="true"><use href="#i-user"/></svg><h3>Page setup &amp; branding</h3><p>Profile picture, cover, bio and contact details set up properly on Facebook and Instagram.</p></div>
      <div class="smm-card"><svg class="icon" aria-hidden="true"><use href="#i-sync"/></svg><h3>Consistent posting</h3><p>Regular posts so customers can see you're active, open and ready for business.</p></div>
      <div class="smm-card"><svg class="icon" aria-hidden="true"><use href="#i-chart"/></svg><h3>Growth</h3><p>The right hashtags, timing and content to grow your pages and get your business seen.</p></div>
    </div>
  </div>
</section>'''

GMARK = SRC[SRC.index('<svg class="gmark"'):SRC.index('</svg>', SRC.index('<svg class="gmark"')) + 6]

CONTACT = f'''<section class="sec contact-ways">
  <div class="wrap">
    <div class="cgrid">
      <a class="ccard" href="tel:0607950837"><svg class="icon" aria-hidden="true"><use href="#i-phone"/></svg><small>Call</small><b>060 795 0837</b><span>Talk to us directly, any time.</span></a>
      <a class="ccard" href="https://wa.me/27607950837" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="#i-message-circle"/></svg><small>WhatsApp</small><b>Chat on WhatsApp</b><span>Send a message, photos or a voice note.</span></a>
      <a class="ccard" href="mailto:info@axeconnect.co.za"><svg class="icon" aria-hidden="true"><use href="#i-mail"/></svg><small>Email</small><b>info@axeconnect.co.za</b><span>For quotes, documents and project details.</span></a>
      <button type="button" class="ccard" onclick="openQuoteModal()"><svg class="icon" aria-hidden="true"><use href="#i-clipboard"/></svg><small>Quote</small><b>Request a quote</b><span>Tell us what you need and get a clear price.</span></button>
      <a class="ccard" href="https://g.page/r/CRoZR2mD81AZEAI" target="_blank" rel="noopener">{GMARK}<small>Google</small><b>Business Profile</b><span>Find us on Google Search and Maps.</span></a>
      <div class="ccard"><svg class="icon" aria-hidden="true"><use href="#i-clock"/></svg><small>Hours &amp; area</small><b>Available 24/7</b><span data-for="web">Fully remote, working with clients anywhere.</span><span data-for="it">Pretoria, Gauteng, plus remote support anywhere.</span></div>
    </div>
  </div>
</section>'''

MORE_SHOTS = '''<div class="case-more">
      <figure><img src="portfolio/jmasocha-gallery.jpg" width="1440" height="900" loading="lazy" decoding="async" alt="J Masocha Photography gallery, grouped by backdrop colour with a timeline"><figcaption><b>Gallery.</b> Photos grouped by backdrop, with filters and a full-screen viewer.</figcaption></figure>
      <figure><img src="portfolio/jmasocha-booking.jpg" width="1440" height="900" loading="lazy" decoding="async" alt="J Masocha Photography online booking: choose a session, date and time"><figcaption><b>Online booking.</b> Four steps: session, date and time, details, deposit.</figcaption></figure>
    </div>'''
WORK = section('id="work"').replace('<!--more-shots-->', MORE_SHOTS)

PAGES = [
    dict(
        file='web-development.html', crumb='Web Development', nav='web-development.html', mode='web',
        title='Web Developer South Africa | Website Design &amp; Development | Axe Connect',
        desc='Hire a web developer in South Africa. Axe Connect designs and builds fast, mobile-friendly business websites, online stores and web apps that match your brand. Affordable and fully remote.',
        service='Website design and development',
        eyebrow='Web development &amp; design',
        h1='Website design &amp; development <em>that fits your brand.</em>',
        lead='We design and build business websites, online stores, landing pages and web applications for individuals, startups and companies across South Africa. Every site is built around your brand, your clients and your goals, never a generic template.',
        cta="openQuoteModal('Web Development')", cta_label='Get a website quote',
        checks=['Mobile-first', 'SEO-ready', 'Fully remote, anywhere in SA'],
        body=['id="web-dev"', 'class="sec process"', 'id="hire"', 'id="reviews"'],
    ),
    dict(
        file='it-support.html', crumb='IT Support', nav='it-support.html', mode='it',
        title='IT Support Pretoria | Laptop &amp; PC Repairs, Remote IT Help | Axe Connect',
        desc='IT support in Pretoria and remote IT help across South Africa. Laptop and PC repairs, virus removal, software installs, email, printers and office networks. Available 24/7.',
        service='IT support and computer repairs', area='Pretoria',
        eyebrow='IT support &amp; repairs',
        h1='IT support &amp; PC repairs <em>in Pretoria.</em>',
        lead='Laptop and desktop repairs, slow computers, viruses, software, email, printers and office networks. On-site help in Pretoria and remote support anywhere, available 24/7 for homes, startups and businesses.',
        cta="openQuoteModal('IT Support &amp; Repairs')", cta_label='Get an IT support quote',
        checks=['On-site in Pretoria', 'Remote support', 'Available 24/7'],
        body=['id="it-support"', 'class="sec process"', 'id="reviews"'],
        faq=('IT support questions', 'IT support in Pretoria: common questions', [
            ('Do you offer on-site IT support in Pretoria?', 'Yes. We come to homes and offices in Pretoria for repairs, setups and troubleshooting, and offer remote support anywhere else.'),
            ('Can you fix my computer remotely?', 'Many software, email, printer and performance problems can be fixed remotely, wherever you are in South Africa. Hardware repairs like screens and batteries are done in person.'),
            ('Is there a diagnosis fee?', 'Yes. A diagnosis fee applies to find out what is wrong. It is non-refundable, but it is credited toward your final bill if you go ahead with the repair.'),
            ('Do you offer monthly IT support for businesses?', 'Yes. Businesses can pay per job or keep their computers, email and network covered with a monthly IT support plan.'),
            ('Do you fix laptops and PCs?', 'Yes: screen and battery replacements, keyboard and trackpad fixes, slow PCs, virus removal, software installs and other hardware repairs.'),
            ('Are you available after hours?', 'Yes. We are available 24/7, so you can reach us whenever something stops working.'),
        ]),
    ),
    dict(
        file='business-systems.html', crumb='Business Systems', nav='business-systems.html', mode='web',
        title='Business Management Systems &amp; Admin Dashboards South Africa | Axe Connect',
        desc='Custom business systems for South African businesses: a customer website plus an admin dashboard for bookings, orders, clients, stock, invoices and reports. One connected, affordable system.',
        service='Custom business management systems',
        eyebrow='Business systems',
        h1='Your website and your dashboard, <em>one system.</em>',
        lead='We build both sides of your business online: the website your customers use to book, buy and enquire, and the admin dashboard your team uses to run orders, clients, stock and invoices. Connected, so everything updates in real time.',
        cta="openQuoteModal('Web Development')", cta_label='Get a system quote',
        checks=['Customer website', 'Admin dashboard', 'Affordable for small business'],
        body=['id="system"', 'class="sec ba"', 'class="aff"', 'class="sec process"', 'id="reviews"'],
        faq=('Business systems', 'Business system questions', [
            ('What is a business management system?', 'It is your customer website and your back-office in one. Customers book, buy or enquire online, and your team manages those bookings, orders, clients, stock and invoices from an admin dashboard.'),
            ('What can the admin dashboard do?', 'It depends on your business: bookings and calendars, orders and payments, client records, stock and inventory, invoices and quotes, and reports that show how the business is doing.'),
            ('Is a custom system affordable for a small business?', 'Yes. We start with the features you need most and add more as you grow, and we recommend an option that fits your budget in the quote.'),
            ('What technology do you build with?', 'We build web applications, back-end systems, APIs and databases using technologies like Java, Spring Boot, SQL and JavaScript.'),
        ]),
    ),
    dict(
        file='online-presence.html', crumb='Online Presence', nav='online-presence.html', mode='web',
        title='Domain Registration, Branding &amp; Google Business Profile Setup | Axe Connect',
        desc='Get your business found online: .co.za domain registration at the best price, logo and branding, Google Business Profile setup, business email and SEO. Done for you by Axe Connect.',
        service='Online presence: domains, branding, Google Business Profile, business email and SEO',
        eyebrow='Online presence',
        h1='Get your business <em>found online.</em>',
        lead='A website is only the start. We register your domain at the best price, build your brand, set up your Google Business Profile and business email, and handle the SEO basics so customers can find, trust and choose you.',
        cta="openQuoteModal('Web Development')", cta_label='Get started',
        checks=['Domain &amp; email', 'Branding', 'Google Business Profile'],
        body=['id="presence"', 'class="sec process"', 'id="reviews"'],
        faq=('Online presence', 'Domains, branding &amp; Google questions', [
            ('Can you register a .co.za domain for me?', 'Yes. We suggest good available names for your business and register the domain at the best price we can find.'),
            ('Can you set up my Google Business Profile?', 'Yes. We create your profile with your services, hours, contact details and photos, and guide you through Google\'s verification so you show up on Google Search and Maps.'),
            ('Can you set up a business email address?', 'Yes, a professional address on your own domain, such as info@yourbusiness.co.za, set up on your phone and computer.'),
            ('Do you design logos and brand kits?', 'Yes. Logos, brand colours and fonts, social media graphics, business cards, posters and flyers, so everything about your business looks consistent.'),
            ('Do you do SEO?', 'Every site we build gets the SEO basics: page titles, descriptions, headings, structured data, a sitemap and Google Search Console set up so people can find you.'),
        ]),
    ),
    dict(
        file='social-media-management.html', crumb='Social Media Management', nav='', mode='web',
        title='Social Media Manager South Africa | Social Media Management for Business | Axe Connect',
        desc='Hire a social media manager in South Africa. Axe Connect plans and creates posts, designs graphics and grows your Facebook and Instagram pages so your business stays active online.',
        service='Social media management',
        eyebrow='Social media management',
        h1='Social media management, <em>done for you.</em>',
        lead='Running a business leaves little time for posting. We plan your content, design on-brand graphics, write captions and keep your Facebook, Instagram and other pages active, so customers can see you are open for business.',
        cta='openSocialEnquiry(event)', cta_label='Ask about social media',
        checks=['Facebook &amp; Instagram', 'On-brand graphics', 'Regular posting'],
        body=[SMM, 'class="sec process"', 'id="reviews"'],
        faq=('Social media', 'Social media management questions', [
            ('Which platforms do you manage?', 'Mainly Facebook and Instagram, and other platforms on request.'),
            ('How much does social media management cost?', 'It depends on how many posts you need each month and how many platforms. Contact us and we will recommend a plan that fits your budget.'),
            ('Do I need to send you photos?', 'Photos of your products, team or work help a lot. Send what you have and we design the rest.'),
            ('Can you manage my social media and build my website?', 'Yes. Doing both means your website, pages and graphics all match your brand.'),
        ]),
    ),
    dict(
        file='portfolio.html', crumb='Portfolio', nav='portfolio.html', mode='web',
        title='Portfolio | Websites &amp; Booking Systems We Built | Axe Connect',
        desc='See websites and business systems built by Axe Connect, including J Masocha Photography in Pretoria: a photography website with online booking, deposits and an admin website manager.',
        service=None,
        eyebrow='Portfolio',
        h1='Websites that work <em>for real businesses.</em>',
        lead='Every project here is live and in use. We build the website customers see and the tools the owner runs it with, so the business can take bookings, sell and grow online.',
        cta="openQuoteModal('Web Development')", cta_label='Start your project',
        checks=['Live sites', 'Websites &amp; systems', 'Built for SA businesses'],
        body=[WORK, 'class="sec process"', 'id="reviews"'],
    ),
    dict(
        file='services.html', crumb='Services', nav='services.html', mode=None,
        title='Services | Websites, Business Systems, IT Support &amp; Branding | Axe Connect',
        desc='All Axe Connect services: website design and development, business systems and dashboards, domains and branding, Google Business Profile, social media management and IT support in Pretoria.',
        service=None,
        eyebrow='Our services',
        h1='Everything your business needs, <em>in one team.</em>',
        lead='Websites and complete business systems for clients anywhere, the online presence that gets you found, and hands-on IT support in Pretoria. Pick one service or let us take care of all of it.',
        cta='openQuoteModal()', cta_label='Request a quote',
        checks=['Websites &amp; systems', 'Branding &amp; online presence', 'IT support'],
        body=['id="outsourcing"', 'class="sec process"', 'id="reviews"'],
    ),
    dict(
        file='about.html', crumb='About', nav='about.html', mode=None,
        title='About Axe Connect | Software &amp; Web Developer and IT Support, South Africa',
        desc='Axe Connect is a South African software, web and IT team. We build brand-aligned websites and business systems for clients anywhere, and provide IT support in Pretoria.',
        service=None,
        eyebrow='About us',
        h1='Built by people, <em>not prompts.</em>',
        lead='Axe Connect is a South African software, web and IT team. We build websites and business systems that match your brand and speak to your clients, and we keep computers and offices running in Pretoria.',
        cta='openQuoteModal()', cta_label='Work with us',
        checks=['Available 24/7', 'Clear quotes', 'Kept in the loop'],
        body=['id="about"', 'class="sec process"', 'id="reviews"'],
    ),
    dict(
        file='contact.html', crumb='Contact', nav='contact.html', mode=None,
        title='Contact Axe Connect | Get a Quote · 060 795 0837 · Available 24/7',
        desc='Contact Axe Connect for websites, business systems, branding, social media or IT support. Call or WhatsApp 060 795 0837, email info@axeconnect.co.za. Available 24/7.',
        service=None,
        eyebrow='Contact',
        h1='Let\'s talk about <em>what you need.</em>',
        lead='Call, WhatsApp or email us, or send a quote request. We are available 24/7 and come back to you with clear recommendations and pricing.',
        cta='openQuoteModal()', cta_label='Request a quote',
        checks=['Available 24/7', 'Quick replies', 'Clear quotes'],
        body=[CONTACT, 'class="sec process"'],
    ),
]


def faqs_in(markup):
    out = []
    for q, a in re.findall(r'<details class="faq-item"[^>]*>\s*<summary><h3>(.*?)</h3>.*?</summary>\s*<p>(.*?)</p>', markup, re.S):
        clean = lambda t: html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
        out.append({'@type': 'Question', 'name': clean(q), 'acceptedAnswer': {'@type': 'Answer', 'text': clean(a)}})
    return out


def jsonld(p, url, main):
    plain = lambda t: html.unescape(re.sub(r'<[^>]+>', '', t))
    graph = [{
        '@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': plain(p['title']),
        'description': plain(p['desc']), 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': 'Axe Connect'},
        'about': {'@id': SITE + '#business'},
    }, {
        '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE},
            {'@type': 'ListItem', 'position': 2, 'name': plain(p['crumb']), 'item': url}],
    }]
    if p.get('service'):
        graph.append({
            '@type': 'Service', 'name': p['service'], 'serviceType': p['service'], 'url': url,
            'description': plain(p['desc']),
            'provider': {'@type': 'ProfessionalService', '@id': SITE + '#business', 'name': 'Axe Connect',
                         'url': SITE, 'telephone': '+27607950837', 'email': 'info@axeconnect.co.za'},
            'areaServed': ({'@type': 'City', 'name': 'Pretoria'} if p.get('area') else {'@type': 'Country', 'name': 'South Africa'}),
        })
    faqs = faqs_in(main)
    if faqs:
        graph.append({'@type': 'FAQPage', 'mainEntity': faqs})
    return ('<script type="application/ld+json">\n'
            + json.dumps({'@context': 'https://schema.org', '@graph': graph}, indent=2, ensure_ascii=False)
            + '\n</script>')


def build(p):
    url = SITE + p['file']
    head_end = SRC.index('<body>')
    head = SRC[:head_end]
    attrs = f'lang="en" data-mode="{p["mode"] or "web"}" data-page="{p["file"][:-5]}"'
    if p['mode']:
        attrs += f' data-page-mode="{p["mode"]}"'
    head = head.replace('<html lang="en" data-mode="web">', f'<html {attrs}>', 1)
    head = re.sub(r'<title>.*?</title>', f'<title>{p["title"]}</title>', head, 1, re.S)
    head = re.sub(r'<meta name="description" content=".*?"/>', f'<meta name="description" content="{p["desc"]}"/>', head, 1)
    head = re.sub(r'<meta name="keywords" content=".*?"/>\n', '', head, 1)
    head = re.sub(r'<!-- Replace with your real live URL once hosted -->\n', '', head)
    head = re.sub(r'<!-- Replace og-image.jpg.*?-->\n', '', head)
    head = head.replace('<link rel="canonical" href="https://axeconnect.co.za/"/>', f'<link rel="canonical" href="{url}"/>')
    head = head.replace('<meta property="og:url" content="https://axeconnect.co.za/"/>', f'<meta property="og:url" content="{url}"/>')
    for k in ('og:title', 'twitter:title'):
        head = re.sub(rf'(<meta (?:property|name)="{k}" content=").*?("/>)', rf'\g<1>{p["title"]}\g<2>', head, 1)
    for k in ('og:description', 'twitter:description'):
        head = re.sub(rf'(<meta (?:property|name)="{k}" content=").*?("/>)', rf'\g<1>{p["desc"]}\g<2>', head, 1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', head, flags=re.S)

    top = SRC[head_end:SRC.index('<main id="home">')]
    top = top.replace('<a href="./" class="active">Home</a>', '<a href="./">Home</a>', 1)
    if p['nav']:
        top = top.replace(f'<a href="{p["nav"]}"', f'<a href="{p["nav"]}" class="active" aria-current="page"', 1)

    parts = [phero(p)]
    for b in p['body']:
        parts.append(b if b.startswith('<section') else section(b))
    if p.get('faq'):
        parts.append(faq_block(p['faq'][2], p['faq'][0], p['faq'][1]))
    parts.append(see_also(p['file']))
    main = '\n\n'.join(parts)

    tail = SRC[SRC.index('<section id="contact" class="cta">'):]
    if p['file'] == 'social-media-management.html':
        tail = tail.replace('onclick="openQuoteModal()"><svg class="icon" aria-hidden="true"><use href="#i-clipboard"/></svg> Request a quote',
                            'onclick="openSocialEnquiry(event)"><svg class="icon" aria-hidden="true"><use href="#i-clipboard"/></svg> Ask about social media', 1)

    head = head.replace('</style>\n', '</style>\n' + jsonld(p, url, main) + '\n', 1)
    out = (f'<!-- Generated from index.html by tools/build_pages.py. Edit the generator or index.html, then re-run it. -->\n'
           + head + top + '<main id="main">\n' + main + '\n\n' + tail)
    out = out.replace('<!DOCTYPE html>', '', 1)
    (ROOT / p['file']).write_text('<!DOCTYPE html>\n' + out, encoding='utf-8')


def sitemap():
    rows = [(SITE, 'monthly', '1.0')] + [(SITE + p['file'], 'monthly', '0.9' if p['service'] else '0.7') for p in PAGES] \
        + [(SITE + 'terms.html', 'yearly', '0.3'), (SITE + 'privacy.html', 'yearly', '0.3')]
    body = ''.join(f'  <url>\n    <loc>{u}</loc>\n    <changefreq>{c}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n' for u, c, pr in rows)
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '</urlset>\n', encoding='utf-8')


for page in PAGES:
    build(page)
sitemap()
print('built', ', '.join(p['file'] for p in PAGES))
