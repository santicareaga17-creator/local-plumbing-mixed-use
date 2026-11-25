"""Build site/index.html: the live Medical/Dental page shell (header, footer, theme CSS/JS)
wrapped around the new Mixed-Use content in content.html.

Run: python3 site/build.py   (from the project root)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNAP = (ROOT.parent / "html-snapshots" / "medical-dental-desktop.html").read_text(encoding="utf-8")
CONTENT = (ROOT / "content.html").read_text(encoding="utf-8")
LIVE = "https://www.localplumbingco.com"


def between(start, end):
    i = SNAP.index(start)
    return SNAP[i:SNAP.index(end, i)]


# --- pieces reused verbatim from the live page ---
head = SNAP[:SNAP.index('<section class="page_header')]
tail = SNAP[SNAP.index("</div><!-- .entry-content -->"):]
form = between('<div class="wpcf7 no-js"', "\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t</div>")
contact_and_ig = between("<!-- CONTACT SECTION -->", '<section class="kitchen_section">\n  <div class="container">\n    <div class="top_block_services">')

form = form.replace(' selected="selected"', "").replace('<option value="Mixed Use">', '<option value="Mixed Use" selected="selected">')
form = form.replace("/commercial/medical-dental/#", "/commercial/mixed-use/#")

# --- icons (same stroke style as the live page) ---
def svg(path):
    return ('<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#1f1f1f" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0">{path}</svg>')

ICONS = {
    "ICON_UP": svg('<path d="M12 20V6"></path><path d="m7 11 5-5 5 5"></path><path d="M4 20h16"></path>'),
    "ICON_DROP": svg('<path d="M12 3s5.5 5.8 5.5 9.4a5.5 5.5 0 0 1-11 0C6.5 8.8 12 3 12 3Z"></path>'),
    "ICON_PIPE": svg('<path d="M4 8h11a3 3 0 1 0-3-3"></path><path d="M4 12h14a3 3 0 1 1-3 3"></path><path d="M4 16h8"></path>'),
    "ICON_CHECK": svg('<rect x="5" y="4" width="14" height="17" rx="2"></rect><path d="M9 4V3h6v1"></path><path d="m8.5 11 1.6 1.6L14 9"></path><path d="m8.5 16.5 1.6 1.6L14 14.5"></path>'),
    "ICON_STORE": svg('<path d="M3 21h18"></path><path d="M5 21V8l7-4 7 4v13"></path><path d="M9 21v-6h6v6"></path>'),
    "ICON_SHIELD": svg('<path d="M12 3 5 6v6c0 4.4 3 7.7 7 9 4-1.3 7-4.6 7-9V6l-7-3Z"></path><path d="m9 12 2 2 4-4"></path>'),
}

# --- grouped services: desktop grid + mobile carousel, like the live page ---
SERVICES = [
    ("/wp-content/uploads/2026/09/md_remodel_plumbing.png", "Construction &amp; Tenant Work",
     ["New Construction Commercial Plumbing", "Tenant Improvement / Remodel Plumbing", "Waste Piping", "Gas Piping", "Building Domestic Water Re-Piping"]),
    ("/wp-content/uploads/2026/09/md_domestic_water.png", "Water Systems",
     ["Domestic Water Booster Pumps", "Pump Systems", "Domestic Hot Water with Recirculation", "Domestic Water Filtration", "Premise Isolation RPBA", "Backflow Install, Test &amp; Repair"]),
    ("/wp-content/uploads/2026/09/local_plumbing_05_boiler_installation.png", "Building Support",
     ["24/7 Emergency Response", "Video Inspection", "Boiler Installation &amp; Repair", "Heating &amp; Cooling Installation &amp; Repair", "Commercial Plumbing Diagnosis"]),
]

def service_card(img, title, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return (f'<div><div><img decoding="async" src="{img}" alt=""><div class="dividerL"></div>'
            f'<div><h3>{title}</h3></div></div><ul>{lis}</ul></div>')

STEPS = [
    ("/wp-content/uploads/2020/03/NB_No_1.jpg", "01", "Send Us the Project",
     "Share plans, bid documents or the issue you&#8217;re dealing with. We review the scope with your team."),
    ("/wp-content/uploads/2020/03/NB_No_3.jpg", "02", "We Build It With Your Schedule",
     "Underground, rough-in, booster and water systems, gas and tenant spaces, coordinated with the GC and the other trades."),
    ("/wp-content/uploads/2020/03/NB_No_9.jpg", "03", "Turnover and Beyond",
     "Testing, trim-out and turnover. After occupancy, the same team is available 24/7 for service, backflow testing and repairs."),
]

def step_card(img, n, title, text):
    return (f'<div class="alt_block imgBlock"><img decoding="async" src="{img}" alt="">'
            f'<div><h2>{n}</h2><h3>{title}</h3><p>{text}</p></div></div>')

def grid_and_carousel(cards):
    slides = "".join(f'<div class="swiper-slide"><div class="serviceBlock">{c}</div></div>' for c in cards)
    return (f'<div class="service_grid">{"".join(cards)}</div>'
            '<div class="mobile_carousel"><div class="swiper swiper-container mySwiper"><div class="nav_rows">'
            '<div class="swiper-button-prev"><i class="fas fa-angle-left"></i></div>'
            '<div class="swiper-button-next"><i class="fas fa-angle-right"></i></div></div>'
            f'<div class="swiper-wrapper">{slides}</div></div></div>')

body = CONTENT
body = body.replace("{{FORM}}", form)
body = body.replace("{{SERVICE_GRID}}", grid_and_carousel([service_card(*s) for s in SERVICES]))
body = body.replace("{{STEPS}}", grid_and_carousel([step_card(*s) for s in STEPS]))
body = body.replace("{{CONTACT_AND_INSTAGRAM}}", contact_and_ig)
for k, v in ICONS.items():
    body = body.replace("{{%s}}" % k, v)
assert "{{" not in body, re.findall(r"\{\{\w+\}\}", body)

# --- page-specific CSS (only what the theme doesn't already cover) ---
EXTRA_CSS = """<style id="mixed-use-page">
.page_header.dental_bg.mixed_use_bg{background:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,.45)),url(/wp-content/uploads/2020/03/NB_No_8.jpg) center 40%/cover}
.project_facts{list-style:none;padding:0;margin:0 0 1.25rem}
.project_facts li{display:flex;gap:1rem;padding:.45rem 0;border-bottom:1px solid rgba(0,0,0,.12);font-size:16px}
.project_facts strong{flex:0 0 170px;text-transform:uppercase;font-size:13px;letter-spacing:.04em}
.project_strip img{width:100%;height:260px;object-fit:cover;display:block}
.carousel_block .swiper-slide img{width:100%;height:220px;object-fit:cover}
@media (max-width:575px){.page_header.mixed_use_bg h1{font-size:34px;white-space:normal}}
@media (max-width:767px){.project_strip img{height:120px}.project_facts li{display:block}.project_facts strong{display:block}}
</style>
"""

# --- metadata ---
TITLE = "Mixed-Use Commercial Plumbing in Portland &amp; Salem, OR | LOCAL Plumbing"
DESC = ("Commercial plumbing for mixed-use buildings in Portland and Salem: new construction, tenant improvements, "
        "booster pumps, backflow and 24/7 service. Veteran-owned.")
meta, nav = head.split("</head>", 1)  # only touch <head>; the nav must keep its real links
meta = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", meta, flags=re.S)
meta = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*"', rf'\g<1>{DESC}"', meta)
meta = meta.replace("Medical Dental | Local Plumbing Co. | Serving Salem, OR &amp; Sherwood, OR", TITLE)
meta = re.sub(r'<meta name="robots" content="[^"]*"', '<meta name="robots" content="noindex, nofollow"', meta)  # mock-up: keep it out of Google
meta = meta.replace('content="Medical Dental"', 'content="Mixed-Use Plumbing"')
meta = meta.replace("/commercial/medical-dental/", "/commercial/mixed-use/").replace("%2Fmedical-dental%2F", "%2Fmixed-use%2F")
# move the nav "active" state from Medical / Dental to Mixed Use
ACTIVE = " current-menu-item page_item page-item-3823 current_page_item active"
nav = nav.replace(ACTIVE, "").replace(' aria-current="page"', "")
nav = nav.replace("menu-item-object-page menu-item-1307", "menu-item-object-page current-menu-item active menu-item-1307")
head = meta + EXTRA_CSS + "</head>" + nav

# Live-site bugs fixed in this build: stray "e" in the Salem tel link.
html = (head + body + "\n\n\t\t" + tail).replace("tel:5038776971e", "tel:5038776971")

# Relative URLs → live site, so theme CSS, JS and images load from a local file.
html = re.sub(r'((?:src|href|action|srcset)=["\'])/(?!/)', rf"\g<1>{LIVE}/", html)
html = re.sub(r"url\(/(?!/)", f"url({LIVE}/", html)

# --- mock-up must not fire the client's tracking or submit to their real form ---
TRACKING = re.compile(r"googletagmanager|gtm\.js|gtag\(|cookieyes|clarity|yextapis|tctm\.co|NITROPACK|nitro-|sfs\.io|pAuth|__CF\$cv|recaptcha|speculationrules|wp-emoji|contact-form-7", re.I)
html = re.sub(r"<script\b[^>]*>.*?</script>", lambda m: "" if TRACKING.search(m.group(0)) else m.group(0), html, flags=re.S)
html = re.sub(r"<link rel='dns-prefetch'[^>]*>\n?", "", html)
html = re.sub(r"""\s*onclick="gtag\([^"]*\"""", "", html)
html = re.sub(r'<form action="[^"]*"', '<form action="#" onsubmit="return false"', html)
html = re.sub(r"""\s(?:srcset|sizes)=(["'])[^"']*\1""", "", html)  # src alone is enough; srcset would pull remote files

# --- download every localplumbingco.com asset so the page works offline in any browser ---
import os, urllib.request
from urllib.parse import urlsplit, urljoin

ASSETS = ROOT / "assets"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"}

def fetch(url):
    """Download url once into assets/<server path>; return the local Path."""
    local = ASSETS / urlsplit(url).path.lstrip("/")
    if not local.exists():
        local.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            local.write_bytes(r.read())
    return local

def localize_css(url):
    path = fetch(url)
    css = path.read_text(encoding="utf-8", errors="ignore")
    def fix(m):
        ref = m.group(2)
        if ref.startswith(("data:", "#")):
            return m.group(0)
        absolute = urljoin(url, ref)
        if urlsplit(absolute).netloc != urlsplit(LIVE).netloc:
            return m.group(0)
        try:
            target = fetch(absolute.split("#")[0])
        except Exception as e:  # missing font/image on the server: leave the reference as is
            print("skip", absolute, e)
            return m.group(0)
        return f"url({m.group(1)}{os.path.relpath(target, path.parent)}{m.group(1)})"
    path.write_text(re.sub(r"url\((['\"]?)([^)'\"]+)\1\)", fix, css), encoding="utf-8")

def localize(m):
    url = html_unescape(m.group(2))
    if url.endswith(".css") or ".css?" in url:
        localize_css(url)
    else:
        try:
            fetch(url)
        except Exception as e:
            print("skip", url, e)
            return m.group(0)
    return m.group(1) + "assets" + urlsplit(url).path + m.group(3)

from html import unescape as html_unescape
html = re.sub(r"""(["'(])https://www\.localplumbingco\.com(/(?:wp-content|wp-includes)/[^"'()\s]+?)(["')])""",
              lambda m: localize(re.match(r"(.)(.*)(.)", m.group(1) + LIVE + m.group(2) + m.group(3))), html)

(ROOT / "index.html").write_text(html, encoding="utf-8")
print("wrote", ROOT / "index.html", len(html), "bytes")
