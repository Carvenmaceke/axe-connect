"""Builds the J Masocha Photography pages. Edit the content here, then run: python3 build.py (needs Pillow)."""
from PIL import Image
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.jmasochaphoto.co.za"
PHONE_DISPLAY = "066 132 2462"
PHONE_INTL = "+27661322462"
EMAIL = "wanhloni@gmail.com"
ADDRESS_1 = "Shop 5A, Centre Walk"
ADDRESS_2 = "266 Pretorius Street, Pretoria Central"

LOGO = """<svg viewBox="0 0 800 520" role="img" aria-label="J Masocha Photography" xmlns="http://www.w3.org/2000/svg">
<g fill="none" stroke="currentColor" stroke-width="24" stroke-linejoin="round"><path d="M300 128V100a22 22 0 0 1 22-22h156a22 22 0 0 1 22 22v28"/><path d="M252 150H186v58M548 150h66v58M186 350v58h66M614 350v58h-66"/><path d="M292 222a125 125 0 0 1 216 0M292 336a125 125 0 0 0 216 0"/></g>
<path d="M48 222h704v114H48z" fill="currentColor"/>
<text x="400" y="312" text-anchor="middle" class="knock" font-family="'League Spartan',Arial,sans-serif" font-weight="800" font-size="96" letter-spacing="6">J MASOCHA</text>
<text x="400" y="478" text-anchor="middle" fill="currentColor" font-family="'League Spartan',Arial,sans-serif" font-weight="700" font-size="38" letter-spacing="9">PHOTOGRAPHY</text></svg>"""

ICON = {
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-.9 1.2-.3.2-.6.1a8.2 8.2 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.1 1.1 0 0 0-.8.4 3.4 3.4 0 0 0-1 2.5 5.9 5.9 0 0 0 1.2 3.1 13.4 13.4 0 0 0 5.2 4.6c1.9.8 2.7.9 3.6.8a3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.1-.3-.2-.6-.3zM12 21.8a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm8.4-18.2A11.8 11.8 0 0 0 1.8 17.9L.1 24l6.3-1.6a11.8 11.8 0 0 0 5.6 1.4A11.8 11.8 0 0 0 20.4 3.6z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="1"/><path d="m2 6 10 7 10-7"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "video": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="6" width="14" height="12" rx="1"/><path d="m16 10 6-3v10l-6-3z"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg>',
    "prev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m15 18-6-6 6-6"/></svg>',
    "next": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}

CUR = ' aria-current="page"'
SMALL_ARROW = ICON["arrow"].replace("<svg", '<svg style="width:20px;height:20px;vertical-align:-3px"')
NAV = [("index.html", "Home"), ("services.html", "Services"), ("gallery.html", "Gallery"),
       ("printing.html", "Printing"), ("about.html", "About"), ("contact.html", "Contact")]


def size(path):
    with Image.open(os.path.join(ROOT, path)) as im:
        return im.size


def img(slug, alt, w=700, cls="", lazy=True, sizes="(max-width: 600px) 100vw, 33vw"):
    p700 = f"assets/img/gallery/{slug}-700.webp"
    p1600 = f"assets/img/gallery/{slug}-1600.webp"
    W, H = size(p700)
    W2, _ = size(p1600)
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img src="{p700}" srcset="{p700} {W}w, {p1600} {W2}w" sizes="{sizes}" '
            f'width="{W}" height="{H}" alt="{alt}"{load}{c}>')


def page(fname, title, desc, body, extra_head=""):
    canon = SITE + "/" + ("" if fname == "index.html" else fname.replace(".html", "/"))
    links = "".join(
        f'<li><a href="{h}"{CUR if h == fname else ""}>{t}</a></li>' for h, t in NAV)
    html = f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/img/gallery/women-black-gown-1600.webp">
<meta name="theme-color" content="#0e0e0e">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&family=League+Spartan:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="brand" href="index.html" aria-label="J Masocha Photography home">{LOGO}</a>
    <ul class="nav-links" id="nav-links">{links}</ul>
    <a class="btn nav-cta" href="contact.html">Book a shoot</a>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav-links"><span></span><span></span><span></span></button>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html" aria-label="J Masocha Photography home">{LOGO}</a>
        <p style="margin-top:20px;max-width:320px">Photography, videography and printing studio in Pretoria Central, capturing life&rsquo;s milestones since 2010.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>{links}</ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="services.html#photoshoots">Photoshoots</a></li>
          <li><a href="services.html#videography">Videography</a></li>
          <li><a href="printing.html">Printing &amp; gifts</a></li>
          <li><a href="gallery.html">Our work</a></li>
          <li><a href="contact.html#faq">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit the studio</h4>
        <ul>
          <li>{ADDRESS_1}<br>{ADDRESS_2}</li>
          <li><a href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="https://wa.me/{PHONE_INTL[1:]}" target="_blank" rel="noopener">WhatsApp us</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> J Masocha Photography. All rights reserved.</span>
      <span>Pretoria, South Africa</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="https://wa.me/{PHONE_INTL[1:]}?text=Hi%20J%20Masocha%20Photography%2C%20I%27d%20like%20to%20book%20a%20shoot." target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{ICON["wa"]}</a>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    with open(os.path.join(ROOT, fname), "w") as f:
        f.write(html)


def head(eyebrow, title, lead, crumb):
    return f"""<section class="page-head">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / {crumb}</p>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    <p>{lead}</p>
  </div>
</section>"""


REVIEWS = [
    ("Everything about this shoot was flawless.", "Itumeleng Moneatse"),
    ("The service was excellent and the photographer really got my vision.", "Mokoena Ngoepe"),
    ("The photoshoot was very fun, the photographers are so professional.", "Sefularong Rikhotso"),
    ("Beautiful, quick, professional.", "Bonolo Samantha"),
    ("Had a good time and the photographer was patient and friendly.", "SollyM"),
]


def reviews_section():
    cards = "".join(
        f'<figure class="review reveal"><span class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
        f'<blockquote>{q}</blockquote><cite>{n}</cite></figure>' for q, n in REVIEWS[:3])
    return f"""<section class="section section--ink">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Client love</p><h2>Rated excellent<br>on Google</h2></div>
      <p class="muted">Based on 29 Google reviews from graduates, parents, brides-to-be and birthday stars across Pretoria.</p>
    </div>
    <div class="reviews">{cards}</div>
  </div>
</section>"""


def cta(title="Your moment deserves<br>to be remembered.", text="Tell us what you&rsquo;re celebrating and we&rsquo;ll send you our packages and available dates."):
    return f"""<section class="section cta-band">
  <div class="wrap">
    <p class="eyebrow">Book a session</p>
    <h2>{title}</h2>
    <p class="muted">{text}</p>
    <div class="hero-actions">
      <a class="btn" href="contact.html">Book a shoot {ICON["arrow"]}</a>
      <a class="btn btn--ghost" href="https://wa.me/{PHONE_INTL[1:]}" target="_blank" rel="noopener">{ICON["wa"]} WhatsApp us</a>
    </div>
  </div>
</section>"""


# ---------- Gallery data ----------
GALLERY = [
    ("women-black-gown", "Woman in a black beaded gown against a shadow-patterned backdrop", "Studio portrait", "women"),
    ("kids-rainbow-castle", "Baby girl with a rainbow unicorn cake in front of a pastel castle set", "Cake smash", "kids birthdays"),
    ("graduation-man-portrait", "Male graduate in his gown seated in the studio", "Graduation", "men graduation"),
    ("maternity-red-gown", "Mother-to-be in a flowing red gown on a sculpted set", "Maternity", "maternity women"),
    ("birthday-25th", "Woman in red with a silver 25 balloon on a director's chair", "25th birthday", "women birthdays"),
    ("outdoor-couple-union-buildings", "Couple posing in the gardens of the Union Buildings, Pretoria", "Outdoor couple", "couples outdoor"),
    ("kids-cake-smash-bluey", "Baby boy with a Bluey themed first birthday cake", "Cake smash", "kids birthdays"),
    ("maternity-silhouette", "Silhouette of a father kissing his partner's baby bump", "Maternity", "maternity couples"),
    ("birthday-roses-black-gown", "Woman in a black gown holding red roses", "Birthday shoot", "women birthdays"),
    ("graduation-family", "Graduate standing with his grandmother", "Graduation", "men graduation family"),
    ("kids-princess-throne", "Baby girl in a pink dress on a golden throne", "Kids portrait", "kids birthdays"),
    ("birthday-30th", "Woman celebrating her 30th with a glass of wine", "30th birthday", "women birthdays"),
    ("maternity-couple-red", "Expecting couple, partner kneeling to the bump", "Maternity couple", "maternity couples"),
    ("graduation-portrait", "Close-up graduation portrait on a green backdrop", "Graduation", "women graduation"),
    ("kids-tulle-dress", "Young girl in a navy tulle dress", "Kids portrait", "kids"),
    ("women-burgundy-suit", "Woman in a burgundy suit in front of SLAYING lettering", "Editorial", "women"),
    ("maternity-golden-crown", "Mother-to-be wearing a golden crown and blush robe", "Maternity", "maternity women"),
    ("birthday-21st", "Woman in red with a crown celebrating her 21st", "21st birthday", "women birthdays"),
    ("couple-mom-dad-caps", "Couple wearing Mom and Dad caps, seen from behind", "Couple", "couples family"),
    ("kids-first-birthday-beach", "Baby boy at a beach-themed first birthday cake smash", "First birthday", "kids birthdays"),
    ("birthday-clock", "Woman in black in front of a giant clock face", "Birthday shoot", "women birthdays"),
    ("maternity-green-drape", "Mother-to-be in mint green under a draped canopy", "Maternity", "maternity women"),
    ("graduation-woman-balloons", "Female graduate with black balloons and a cake", "Graduation", "women graduation"),
    ("birthday-pink-cake", "Woman with pink hair holding a Happy Birthday cake", "Birthday shoot", "women birthdays"),
    ("kids-second-birthday", "Toddler at a butterfly-themed second birthday set", "2nd birthday", "kids birthdays"),
    ("maternity-couple-pink", "Expecting couple in pink and white", "Maternity couple", "maternity couples"),
    ("women-flower-wreath", "Woman in red photographed from above inside a flower wreath", "Creative portrait", "women"),
    ("maternity-white-tulle", "Mother-to-be lying in white tulle", "Maternity", "maternity women"),
    ("birthday-crown-roses", "Woman in red with a tiara and rose ring", "Birthday shoot", "women birthdays"),
    ("outdoor-couple-kiss", "Couple sharing a kiss outdoors at the Union Buildings", "Outdoor couple", "couples outdoor"),
]

FILTERS = [("all", "All"), ("kids", "Kids"), ("women", "Women"), ("men", "Men"), ("couples", "Couples"),
           ("family", "Family"), ("maternity", "Maternity"), ("graduation", "Graduation"),
           ("birthdays", "Birthdays"), ("outdoor", "Outdoor")]


# ---------- HOME ----------
home_jsonld = json.dumps({
    "@context": "https://schema.org", "@type": "ProfessionalService",
    "name": "J Masocha Photography", "url": SITE, "telephone": PHONE_INTL, "email": EMAIL,
    "foundingDate": "2010", "image": SITE + "/assets/img/gallery/women-black-gown-1600.webp",
    "address": {"@type": "PostalAddress", "streetAddress": "Shop 5A, Centre Walk, 266 Pretorius Street",
                "addressLocality": "Pretoria Central", "addressRegion": "Gauteng", "addressCountry": "ZA"},
    "areaServed": "Pretoria", "priceRange": "R350+",
    "description": "Photography, videography and printing studio in Pretoria Central since 2010."
})

marquee_words = ["Birthdays", "Maternity", "Graduations", "Cake smash", "Couples", "Corporate", "Events", "Videography", "Printing"]
mq = "".join(f"<span>{w}</span>" for w in marquee_words)

preview = [g for g in GALLERY if g[0] in ("kids-rainbow-castle", "maternity-red-gown", "women-burgundy-suit",
                                          "graduation-woman-balloons", "couple-mom-dad-caps", "birthday-clock")]
preview_html = "".join(
    f'<figure tabindex="0"><a href="gallery.html#{t.split()[0]}">{img(s, a)}</a><figcaption>{c}</figcaption></figure>'
    for s, a, c, t in preview)

cats = [("kids", "Kids", "kids-cake-smash-bluey"), ("women", "Women", "birthday-crown-roses"),
        ("men", "Men", "graduation-man-portrait"), ("maternity", "Maternity", "maternity-golden-crown")]
cats_html = "".join(
    f'<a class="service-card reveal" href="gallery.html#{k}"><div class="media">{img(s, label + " photography by J Masocha", sizes="(max-width:600px) 100vw, 25vw")}</div>'
    f'<h3 style="font-size:1.3rem">{label} {SMALL_ARROW}</h3></a>'
    for k, label, s in cats)

home = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div class="reveal">
      <p class="eyebrow">Pretoria photography studio &middot; since 2010</p>
      <h1><span>Capturing</span><span class="outline">life&rsquo;s best</span><span>moments.</span></h1>
      <p class="hero-lead">Birthdays, maternity, graduations, cake smashes and couples &mdash; styled sets, professional lighting and a team that makes you feel confident in front of the camera.</p>
      <div class="hero-actions">
        <a class="btn" href="contact.html">Book a shoot {ICON["arrow"]}</a>
        <a class="btn btn--ghost" href="gallery.html">View gallery</a>
      </div>
      <div class="hero-stats">
        <div><strong>2010</strong><span>Shooting since</span></div>
        <div><strong>29</strong><span>Google reviews</span></div>
        <div><strong>3-in-1</strong><span>Photo &middot; video &middot; print</span></div>
      </div>
    </div>
    <div class="hero-photos">
      <figure class="tall vf">{img("women-black-gown", "Woman in a black beaded gown photographed at J Masocha studio", lazy=False, sizes="(max-width:860px) 50vw, 25vw")}</figure>
      <figure>{img("kids-princess-throne", "Baby girl on a golden throne at a pastel themed shoot", lazy=False, sizes="(max-width:860px) 50vw, 25vw")}</figure>
      <figure>{img("graduation-portrait", "Graduation portrait on a green backdrop", sizes="(max-width:860px) 50vw, 25vw")}</figure>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}{mq}</div></div>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">What we do</p><h2>Photo. Video. Print.</h2></div>
      <p class="muted">Everything under one roof in Pretoria Central &mdash; from the shoot itself to the canvas on your wall.</p>
    </div>
    <div class="grid-3">
      <a class="service-card reveal" href="services.html#photoshoots">
        <div class="media">{img("birthday-25th", "Birthday photoshoot in studio")}</div>
        <span class="num">01</span><h3>Photography</h3>
        <p class="muted">Birthdays, maternity, graduation, cake smash, family, corporate and product shoots in our styled studio or outdoors.</p>
      </a>
      <a class="service-card reveal" href="services.html#videography">
        <div class="media">{img("outdoor-couple-kiss", "Couple filmed outdoors at the Union Buildings")}</div>
        <span class="num">02</span><h3>Videography</h3>
        <p class="muted">Cinematic videos for events, graduations, outdoor stories and business profiles.</p>
      </a>
      <a class="service-card reveal" href="printing.html">
        <div class="media" style="background:var(--paper-2)"><img src="assets/img/shop/photo-canvas.webp" width="900" height="900" alt="Framed photo canvas on a bedroom wall" loading="lazy" style="aspect-ratio:4/5"></div>
        <span class="num">03</span><h3>Printing</h3>
        <p class="muted">Canvases, frames, albums, mugs, tumblers, photo globes, plates and T-shirts printed with your photos.</p>
      </a>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Browse by category</p><h2>Find your kind of shoot</h2></div>
      <a class="link-arrow" href="gallery.html">Full gallery</a>
    </div>
    <div class="grid-4">{cats_html}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="vf reveal">{img("maternity-silhouette", "Maternity silhouette of a couple", sizes="(max-width:860px) 100vw, 50vw")}</div>
    <div class="reveal">
      <p class="eyebrow">Why J Masocha</p>
      <h2>More than photos &mdash; memories you&rsquo;ll keep.</h2>
      <p class="muted">We&rsquo;ve been photographing Pretoria&rsquo;s milestones since 2010. Every shoot gets creative direction, a styled set and careful editing, so you leave with images you&rsquo;re proud to share and print.</p>
      <ul class="checks">
        <li>Themed studio sets for birthdays, cake smashes and maternity</li>
        <li>Patient, friendly photographers who guide your poses</li>
        <li>Photo, video and printing in one place</li>
        <li>Custom concepts &mdash; bring your own idea and we&rsquo;ll build it</li>
      </ul>
      <a class="btn" href="about.html">About the studio</a>
    </div>
  </div>
</section>

{reviews_section()}

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Recent work</p><h2>From the studio</h2></div>
      <a class="link-arrow" href="gallery.html">See all {len(GALLERY)} photos</a>
    </div>
    <div class="gallery">{preview_html}</div>
  </div>
</section>

{cta()}
"""
page("index.html", "J Masocha Photography | Photo Studio in Pretoria Central",
     "Professional photography, videography and printing studio in Pretoria Central since 2010. Birthday, maternity, graduation, cake smash and couple shoots.",
     home, f'<script type="application/ld+json">{home_jsonld}</script>\n')


# ---------- SERVICES ----------
PHOTO = [
    ("Kiddies Birthday Shoot", "kids-rainbow-castle", "Playful themed sets and cake smashes that capture genuine smiles, personality and precious childhood moments."),
    ("Adult Birthday Shoot", "birthday-25th", "Celebrate your new age in style with a luxury birthday shoot that shows off your confidence and beauty."),
    ("Maternity Shoot", "maternity-red-gown", "Celebrate motherhood with timeless portraits &mdash; solo or with your partner &mdash; that capture love and new beginnings."),
    ("Graduation Shoot", "graduation-portrait", "Celebrate your achievement with portraits that capture the pride of your milestone, with family welcome."),
    ("Couples &amp; Family Shoot", "couple-mom-dad-caps", "Relaxed sessions for couples, pregnancy announcements and families who want to remember this season together."),
    ("Outdoor Shoot", "outdoor-couple-union-buildings", "Natural light at Pretoria locations such as the Union Buildings for authentic, timeless images."),
    ("Corporate Shoot", "women-burgundy-suit", "Polished headshots and team photos that present your brand and business with confidence."),
    ("Event Shoot", "kids-second-birthday", "Parties, launches and special occasions covered from start to finish, so you can enjoy the day."),
    ("Product Shoot", None, "Clean, detailed product images for your online store, menu or social media that make your brand stand out."),
]
VIDEO = [
    ("Event Videography", "Weddings, birthdays, graduations and special events told through cinematic storytelling."),
    ("Graduation Videography", "Cinematic graduation videos that preserve every proud moment of your big day."),
    ("Outdoor Videography", "Natural storytelling videos filmed on location for authentic, timeless memories."),
    ("Corporate Videography", "Business videos for branding, marketing, promotions and company profiles."),
]


def pkg_photo(name, slug, text):
    media = (img(slug, f"{name} example", sizes="120px") if slug else
             '<img src="assets/img/shop/tumbler.webp" width="900" height="900" alt="Product photography example" loading="lazy">')
    plain = name.replace("&amp;", "&")
    return f"""<article class="pkg reveal">{media}<div><h3>{name}</h3><p class="muted">{text}</p>
<a class="link-arrow" data-book="{plain}" href="contact.html?shoot={plain.replace(' ', '+').replace('&', '%26')}">Request packages</a></div></article>"""


def pkg_video(name, text):
    return f"""<article class="pkg pkg--icon reveal"><div class="pkg-icon">{ICON["video"]}</div><div><h3>{name}</h3><p class="muted">{text}</p>
<a class="link-arrow" data-book="{name}" href="contact.html?shoot={name.replace(' ', '+')}">Request packages</a></div></article>"""


services = f"""{head("Services", "Shoots for every milestone", "Photography, videography and printing from our studio in Pretoria Central. Choose a shoot below to get packages and prices on WhatsApp, or ask us for a custom concept.", "Services")}

<section class="section" id="photoshoots">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">01 &middot; Photography</p><h2>Photoshoots</h2></div>
      <a class="btn btn--ghost" data-book="a custom photoshoot" href="contact.html?shoot=Custom+request">Custom request</a>
    </div>
    <div class="pkg-list">{"".join(pkg_photo(*p) for p in PHOTO)}</div>
  </div>
</section>

<section class="section section--ink" id="videography">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">02 &middot; Videography</p><h2>Videography</h2></div>
      <a class="btn btn--ghost" data-book="custom videography" href="contact.html?shoot=Custom+request">Custom request</a>
    </div>
    <div class="pkg-list">{"".join(pkg_video(*v) for v in VIDEO)}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">How it works</p><h2>Booking is easy</h2></div></div>
    <div class="steps">
      <div class="step reveal"><h3>Choose a shoot</h3><p class="muted">Pick a shoot above or tell us your own idea.</p></div>
      <div class="step reveal"><h3>Get packages</h3><p class="muted">We send packages, prices and open dates on WhatsApp.</p></div>
      <div class="step reveal"><h3>Shoot day</h3><p class="muted">Come to the studio &mdash; we style the set and guide every pose.</p></div>
      <div class="step reveal"><h3>Photos &amp; prints</h3><p class="muted">Receive your edited images and order prints, canvases or gifts.</p></div>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">03 &middot; Printing</p>
      <h2>Turn your photos into keepsakes</h2>
      <p class="muted">Canvases, frames, albums, mugs, tumblers, photo globes, plates and T-shirts &mdash; printed in-house from your shoot or your own photos.</p>
      <a class="btn" href="printing.html">See printing &amp; gifts</a>
    </div>
    <div class="reveal"><img src="assets/img/shop/photo-canvas.webp" width="900" height="900" alt="Large photo canvas hanging above a bed" loading="lazy"></div>
  </div>
</section>

{cta()}
"""
page("services.html", "Photography & Videography Services in Pretoria | J Masocha Photography",
     "Birthday, kiddies, maternity, graduation, couples, outdoor, corporate, event and product photoshoots plus videography in Pretoria Central.",
     services)


# ---------- GALLERY ----------
def full_img(s, a):
    return img(s, a).replace("<img ", f'<img data-full="assets/img/gallery/{s}-1600.webp" ', 1)


fig_html = "".join(
    f'<figure data-tags="{t}" tabindex="0" role="button" aria-label="Open photo: {a}">'
    f'{full_img(s, a)}<figcaption>{c}</figcaption></figure>'
    for s, a, c, t in GALLERY)
filters_html = "".join(
    f'<button class="filter" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v} <small></small></button>'
    for k, v in FILTERS)

gallery = f"""{head("Gallery", "Our work", "Browse our recent sessions by category. Tap any photo to view it full screen.", "Gallery")}
<section class="section" style="padding-top:48px">
  <div class="wrap">
    <div class="filters" role="toolbar" aria-label="Filter photos by category">{filters_html}</div>
    <div class="gallery">{fig_html}</div>
    <p class="gallery-empty" hidden>No photos in this category yet &mdash; <a href="contact.html">ask us</a> for more examples.</p>
  </div>
</section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="lb-close" aria-label="Close">{ICON["close"]}</button>
  <button class="lb-prev" aria-label="Previous photo">{ICON["prev"]}</button>
  <img alt="">
  <button class="lb-next" aria-label="Next photo">{ICON["next"]}</button>
  <p class="lb-caption"></p>
</div>
{cta("Love what you see?", "Book a similar shoot or bring your own concept &mdash; we&rsquo;ll style the set for you.")}
"""
page("gallery.html", "Gallery | Kids, Maternity, Birthday & Graduation Photos | J Masocha Photography",
     "See our photography portfolio: kids and cake smash, women, men, couples, family, maternity, graduation, birthday and outdoor shoots in Pretoria.",
     gallery)


# ---------- PRINTING ----------
PRODUCTS = [
    ("photo-canvas", "Photo Canvas", "R350 &ndash; R1&nbsp;550", "Gallery-wrapped canvas in multiple sizes, from desk size up to 24&times;36&Prime; statement pieces.", "Sale"),
    ("photo-globe", "Personalised Photo Globe", "R499", "A snow globe with your favourite photo inside &mdash; a gift that gets noticed.", None),
    ("tumbler", "Personalised Tumbler (500ml)", "R499", "Reusable 500ml tumbler printed with your photo, name or design.", None),
]
prod_html = "".join(f"""<article class="product reveal">
  <div class="media"><img src="assets/img/shop/{s}.webp" width="900" height="900" alt="{n}" loading="lazy"></div>
  <div class="body">{f'<span class="tag">{tag}</span>' if tag else ''}<h3>{n}</h3><p class="muted">{d}</p><p class="price">{p}</p>
  <a class="btn" data-book="{n.replace('(', '').replace(')', '')} (printing order)" href="contact.html?shoot=Printing">Order on WhatsApp</a></div>
</article>""" for s, n, p, d, tag in PRODUCTS)

printing = f"""{head("Printing &amp; gifts", "Print it. Frame it. Gift it.", "Premium custom printing from your shoot or your own photos &mdash; ordered on WhatsApp and collected at our Pretoria Central studio.", "Printing")}
<section class="section">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">Popular items</p><h2>Best sellers</h2></div></div>
    <div class="grid-3">{prod_html}</div>
  </div>
</section>
<section class="section section--ink">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Also available</p>
      <h2>We print on almost anything</h2>
      <p class="muted">Send us your photo and idea and we&rsquo;ll quote you on WhatsApp.</p>
      <a class="btn" data-book="a custom printing quote" href="contact.html?shoot=Printing">Get a quote</a>
    </div>
    <ul class="chip-list">
      <li>Photo frames</li><li>Albums</li><li>Canvases</li><li>Custom mugs</li><li>Tumblers</li>
      <li>Photo globes</li><li>Plates</li><li>T-shirts</li><li>Photo prints</li>
    </ul>
  </div>
</section>
{cta("Have photos waiting on your phone?", "Bring them to life in print. Send them to us on WhatsApp and we&rsquo;ll handle the rest.")}
"""
page("printing.html", "Photo Printing, Canvas & Personalised Gifts in Pretoria | J Masocha Photography",
     "Photo canvases from R350, personalised photo globes, tumblers, mugs, frames, albums, plates and T-shirts printed in Pretoria Central.",
     printing)


# ---------- ABOUT ----------
TEAM = [("Njabulo", "Photographer", "N"), ("Lwazi Mjuba", "Photographer", "LM"), ("Siseko Ngeno", "Receptionist", "SN")]
team_html = "".join(f'<div class="team-card reveal"><div class="monogram">{m}</div><h3>{n}</h3><p>{r}</p></div>' for n, r, m in TEAM)
about = f"""{head("About us", "Pretoria&rsquo;s milestone studio since 2010", "J Masocha Photography is a photography, videography and printing studio in the heart of Pretoria Central.", "About")}
<section class="section">
  <div class="wrap split">
    <div class="vf reveal">{img("graduation-family", "Graduate with his grandmother at J Masocha studio", sizes="(max-width:860px) 100vw, 50vw")}</div>
    <div class="reveal">
      <p class="eyebrow">Who we are</p>
      <h2>Your story, beautifully told.</h2>
      <p class="muted">Since 2010 we&rsquo;ve photographed graduations, first birthdays, pregnancies, love stories and businesses across Pretoria. We combine creative direction, attention to detail and a welcoming studio experience to deliver more than photos &mdash; memories you&rsquo;ll want to print and keep.</p>
      <a class="btn" href="gallery.html">See our work</a>
    </div>
  </div>
</section>
<section class="section section--paper">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">What drives us</p><h2>Mission, goals &amp; promise</h2></div></div>
    <div class="grid-3 values">
      <div class="value reveal"><h3>Our mission</h3><p class="muted">To capture life&rsquo;s most meaningful moments with creativity, passion and professionalism, turning every client&rsquo;s story into timeless visual memories.</p></div>
      <div class="value reveal"><h3>Our goal</h3><p class="muted">To deliver photography, videography and printing that exceeds expectations, while making every client feel confident, valued and celebrated.</p></div>
      <div class="value reveal"><h3>Why us</h3><p class="muted">Experience since 2010, styled sets, careful editing and everything from shoot to print under one roof.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">The team</p><h2>Meet the people behind the lens</h2></div></div>
    <div class="grid-3">{team_html}</div>
  </div>
</section>
{reviews_section()}
{cta()}
"""
page("about.html", "About J Masocha Photography | Photographers in Pretoria Central",
     "Meet J Masocha Photography, a Pretoria Central photography, videography and printing studio capturing milestones since 2010.",
     about)


# ---------- CONTACT ----------
SHOOT_OPTIONS = [p[0].replace("&amp;", "&") for p in PHOTO] + [v[0] for v in VIDEO] + ["Printing", "Custom request"]
opts = "".join(f'<option value="{o.replace("&", "&amp;")}">{o.replace("&", "&amp;")}</option>' for o in SHOOT_OPTIONS)
FAQ = [
    ("How do I book a shoot?", "Fill in the form on this page or message us on WhatsApp at 066 132 2462. We&rsquo;ll reply with packages, prices and available dates."),
    ("Where is the studio?", f"We&rsquo;re at {ADDRESS_1}, {ADDRESS_2}. We also shoot outdoors at locations around Pretoria."),
    ("Can I bring my own theme or concept?", "Yes. Choose &ldquo;Custom request&rdquo; and describe your idea &mdash; colours, props, outfits or inspiration photos &mdash; and we&rsquo;ll plan the set with you."),
    ("Do you do video as well?", "Yes. We film events, graduations, outdoor stories and corporate videos. Ask for a combined photo and video package."),
    ("Can you print photos I took myself?", "Yes. Send us your photos on WhatsApp and we&rsquo;ll print them on canvas, frames, mugs, tumblers, globes, plates or T-shirts."),
]
faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
map_q = "Centre+Walk+266+Pretorius+Street+Pretoria+Central"
contact = f"""{head("Contact", "Let&rsquo;s plan your shoot", "Send us a few details and we&rsquo;ll get back to you with packages and available dates.", "Contact")}
<section class="section">
  <div class="wrap contact-grid">
    <div>
      <div class="contact-item"><span class="ico">{ICON["pin"]}</span><div><h3>Studio</h3><p>{ADDRESS_1}<br>{ADDRESS_2}</p></div></div>
      <div class="contact-item"><span class="ico">{ICON["phone"]}</span><div><h3>Call</h3><a href="tel:{PHONE_INTL}">{PHONE_DISPLAY}</a></div></div>
      <div class="contact-item"><span class="ico">{ICON["wa"]}</span><div><h3>WhatsApp</h3><a href="https://wa.me/{PHONE_INTL[1:]}" target="_blank" rel="noopener">Chat with us</a></div></div>
      <div class="contact-item"><span class="ico">{ICON["mail"]}</span><div><h3>Email</h3><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
    </div>
    <form id="booking-form" novalidate>
      <div class="form-row">
        <div class="field"><label for="name">Name *</label><input id="name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="phone">Phone *</label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email"></div>
        <div class="field"><label for="date">Preferred date</label><input id="date" name="date" type="date"></div>
      </div>
      <div class="field"><label for="shoot">What are you booking? *</label><select id="shoot" name="shoot" required>{opts}</select></div>
      <div class="field"><label for="message">Tell us about your shoot *</label><textarea id="message" name="message" rows="5" required placeholder="Theme, number of people, outfits, ideas..."></textarea></div>
      <div class="form-actions">
        <button class="btn" type="submit" value="whatsapp">{ICON["wa"]} Send on WhatsApp</button>
        <button class="btn btn--ghost" type="submit" value="email">{ICON["mail"]} Send by email</button>
      </div>
      <p class="form-note">Your message opens in WhatsApp or your email app, ready to send.</p>
    </form>
  </div>
</section>
<iframe class="map" title="Map to J Masocha Photography studio" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={map_q}&amp;output=embed"></iframe>
<section class="section" id="faq">
  <div class="wrap" style="max-width:900px">
    <p class="eyebrow">FAQ</p>
    <h2>Good to know</h2>
    <div class="faq">{faq_html}</div>
  </div>
</section>
"""
page("contact.html", "Contact & Bookings | J Masocha Photography Pretoria",
     "Book a photoshoot at J Masocha Photography, Shop 5A Centre Walk, 266 Pretorius Street, Pretoria Central. Call or WhatsApp 066 132 2462.",
     contact)

print("built")
