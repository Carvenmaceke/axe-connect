"""Rebuilds the Portfolio section of index.html from the PROJECTS list below."""
from pathlib import Path
p = Path(__file__).resolve().parent.parent / 'index.html'
s = open(p).read()

# Newest project first. Add a new dict at the top, put its screenshots in portfolio/,
# then run: python3 tools/build_portfolio.py && python3 tools/build_pages.py
PROJECTS = [
    dict(name='Zicco Plumbers', tag='Plumbing company · Johannesburg', url='https://www.ziccoplumbers.co.za/', host='ziccoplumbers.co.za',
         shots=[('zicco-1', 1280, 800, 'Homepage'), ('zicco-2', 1280, 800, 'Services'), ('zicco-3', 1280, 800, 'Request a quote'), ('zicco-4', 1280, 800, 'Projects gallery')],
         desc='Website and job management system for a PIRB-registered plumber: customers request quotes online and track their job, and the business runs requests, quotes and invoices from its own dashboard.',
         more=['Quote requests from every service page, with photo upload', 'Ticket number and tracking page for every request', 'Admin dashboard for jobs, visit bookings and messages', 'Quotes and invoices emailed as PDF, with paid receipts', 'Automatic visit reminders and daily summary emails'],
         chips=['Website', 'Job tracking', 'Quotes &amp; invoices']),
    dict(name='J Masocha Photography', tag='Photography studio · Pretoria Central', url='https://www.jmasochaphoto.co.za/', host='jmasochaphoto.co.za',
         shots=[('jmasocha-home', 1440, 900, 'Homepage'), ('jmasocha-gallery', 1440, 900, 'Gallery'), ('jmasocha-booking', 1440, 900, 'Online booking')],
         desc='Website and online booking system for a photography, videography and printing studio, with a website manager the owner runs.',
         more=['Gallery sorted by backdrop, with filters and a full-screen viewer', 'Online booking with open dates, times and deposits', 'Website manager for photos, bookings and specials', 'Newsletter sign-ups and promotion emails'],
         chips=['Website', 'Booking system', 'Admin dashboard']),
    dict(name='POG Advisory &amp; Chartered Accountants', tag='Accounting firm · Gauteng &amp; Limpopo', url='https://pogidja.co.za/', host='pogidja.co.za',
         shots=[('pogidja-1', 1280, 800, 'Homepage'), ('pogidja-2', 1280, 800, 'Services'), ('pogidja-3', 1280, 800, 'About')],
         desc='A modern, professional website for a SAICA-registered accounting, tax and business advisory firm.',
         more=['Service pages for accounting, tax and advisory', 'Link to the POG Advisory client portal', 'WhatsApp contact button', 'Financial insights and tax deadline posts'],
         chips=['Website', 'Blog', 'Client portal link']),
    dict(name='Doxa Beach Hotel', tag='Beach hotel · Zavora Bay, Mozambique', url='https://doxabeachhotel.com/', host='doxabeachhotel.com',
         shots=[('doxa-1', 1280, 800, 'Homepage and booking'), ('doxa-2', 1280, 800, 'Rooms'), ('doxa-3', 1280, 800, 'Gallery')],
         desc='Hotel website with an online room booking form, a rooms showcase and a gallery of the beach and activities.',
         more=['Book-a-room form: dates, room type, guests and requests', 'Rooms showcase with photos', 'Gallery of activities and the bay', 'Contact details and newsletter sign-up'],
         chips=['Website', 'Booking form', 'Gallery']),
    dict(name='SAGIS Logistics', tag='Car rental · Pretoria East', url='https://sagislogistics.co.za/', host='sagislogistics.co.za',
         shots=[('sagis-1', 1280, 800, 'Homepage'), ('sagis-2', 1280, 800, 'Company overview'), ('sagis-3', 1280, 800, 'Pick-up points and car search')],
         desc='Car rental website for a company running since 1997, with a car search and its national pick-up points.',
         more=['Find-your-car search by pick-up and return location', 'Services, fleet and company overview', 'National list of airport and city pick-up points', 'Downloadable company info and FAQ'],
         chips=['Website', 'Car search', 'Downloads']),
    dict(name='TP Tshakafa Attorneys', tag='Law firm · Roodepoort', url='https://tshakafaattorneys.co.za/', host='tshakafaattorneys.co.za',
         shots=[('tshakafa-1', 1280, 800, 'Homepage'), ('tshakafa-2', 1280, 800, 'Services'), ('tshakafa-3', 1280, 800, 'About')],
         desc='Professional website for a law firm, presenting its legal services and making it easy for clients to get in touch.',
         more=['Homepage slider with clear call to action', 'Services page listing the legal services', 'About page with the firm\'s mission', 'Contact page with address, phone and email'],
         chips=['Website', 'Multi-page', 'Contact']),
    dict(name='M4 Foundation', tag='Non-profit · Limpopo &amp; Gauteng', url='https://www.m4foundation.co.za/', host='m4foundation.co.za',
         shots=[('m4-1', 1280, 800, 'Homepage'), ('m4-2', 1280, 800, 'About'), ('m4-3', 1280, 800, 'Services')],
         desc='Website for a registered NPO that develops mining communities and offers work experience to trainees.',
         more=['About, services, team and contact pages', 'Homepage slider of the foundation\'s work', 'WhatsApp contact button', 'Blog section for news'],
         chips=['Website', 'NPO', 'Multi-page']),
    dict(name='Mining CSI', tag='Mining magazine · South Africa', url='https://www.miningcsi.co.za/', host='miningcsi.co.za',
         shots=[('miningcsi-1', 1280, 800, 'Homepage'), ('miningcsi-2', 1280, 800, 'About'), ('miningcsi-3', 1280, 800, 'Magazine advertising')],
         desc='Website for Mining CSI, a magazine on local economic development by South African mines.',
         more=['Partner logos from major mining companies', 'Magazine advertising rates and specifications', 'Archive of past issues', 'About and contact pages'],
         chips=['Website', 'Magazine', 'Archives']),
]

ARROW = '<svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg>'
CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>'

cards = []
for n, pr in enumerate(PROJECTS):
    imgs = ''.join(
        f'<img src="portfolio/{f}.jpg" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{pr["name"]} website: {cap}">'
        for f, w, h, cap in pr['shots'])
    dots = ''.join('<i class="on"></i>' if i == 0 else '<i></i>' for i in range(len(pr['shots'])))
    more = ''.join(f'<li>{m}</li>' for m in pr['more'])
    chips = ''.join(f'<li>{c}</li>' for c in pr['chips'])
    cards.append(f'''      <article class="proj">
        <div class="proj-media">
          <div class="pm-bar" aria-hidden="true"><i></i><i></i><i></i><span>{pr["host"]}</span></div>
          <div class="pm-track" tabindex="0" aria-label="Screenshots of the {pr["name"]} website, swipe to see more">{imgs}</div>
          <button type="button" class="pm-nav pm-prev" aria-label="Previous screenshot">{CHEV.format(d="M15 6l-6 6 6 6")}</button>
          <button type="button" class="pm-nav pm-next" aria-label="Next screenshot">{CHEV.format(d="M9 6l6 6-6 6")}</button>
          <div class="pm-dots" aria-hidden="true">{dots}</div>
        </div>
        <div class="proj-body">
          <span class="proj-tag">{pr["tag"]}</span>
          <h3>{pr["name"]}</h3>
          <p class="proj-desc">{pr["desc"]}</p>
          <div class="proj-more" id="pm-more-{n}" hidden><ul>{more}</ul></div>
          <ul class="proj-chips">{chips}</ul>
          <div class="proj-actions">
            <button type="button" class="proj-rm" aria-expanded="false" aria-controls="pm-more-{n}">Read more</button>
            <a class="proj-visit" href="{pr["url"]}" target="_blank" rel="noopener">Visit website {ARROW}</a>
          </div>
        </div>
      </article>''')

section = f'''<!-- PORTFOLIO -->
<section id="work" class="sec work" data-for="web">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <span class="eyebrow">Portfolio</span>
        <h2>Real work, <em>live and working.</em></h2>
      </div>
      <p>Websites and systems we've built for South African businesses. Swipe through each project, read what we built, or visit the live site.</p>
    </div>
    <div class="proj-grid">
{chr(10).join(cards)}
    </div>
    <div class="work-all"><a class="btn btn-ghost" href="portfolio.html">View all {len(PROJECTS)} projects {ARROW}</a></div>
  </div>
</section>

'''
a = s.index('<!-- PORTFOLIO -->')
b = s.index('<!-- SERVICES OVERVIEW -->')
s = s[:a] + section + s[b:]

open(p, 'w').write(s)
print('portfolio:', len(PROJECTS), 'projects')
