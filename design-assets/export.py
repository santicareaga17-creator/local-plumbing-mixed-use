"""Export the design-asset folders from the built page.

Run from the repo root after `python3 site/build.py`:
    python3 design-assets/export.py

Needs Google Chrome (headless) and Pillow. Writes:
  home-banners/  hero banner, rendered at 1440 and 768 px, plus its source photo
  banners/       full-width section banners, rendered, plus their source photos
  flat-icons/    service icons (PNG) and the inline line icons (SVG)
  web-elements/  buttons, cards, form, header, footer, rendered at 1440 px
  icons/         favicons, UI and social icons (SVG), logos and badges
"""
import json, re, shutil, subprocess, tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
SITE = ROOT.parent / "site"
UPLOADS = SITE / "assets" / "wp-content" / "uploads"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HEIGHT = 12000  # tall enough that nothing scrolls, so element boxes = screenshot pixels

# name -> (CSS selector, index of the match)
HOME_BANNERS = {"hero": (".page_header", 0)}
BANNERS = {
    "business-impact": (".md_section.p-0", 0),
    "project-spotlight-nomad": (".project_spotlight", 0),
    "support-24-7": (".support_section", 0),
    "final-cta": (".redCTA", 0),
}
WEB_ELEMENTS = {
    "header-nav": ("#wrapper-navbar", 0),
    "footer": ("#wrapper-footer", 0),
    "button-primary-red": (".btn_commercial", 0),
    "button-outline": (".commercial_btn", 0),
    "button-call-red": (".btn-site.kitchen_btn", 0),
    "button-phone-dark": (".black_btn", 0),
    "lead-form-card": (".card.card-body", 0),
    "service-icon-grid": (".grid_icons_block", 0),
    "carousel-card": (".carousel_block .swiper-slide", 0),
    "service-list-card": (".service_grid > div", 0),
    "solution-card-red-title": (".twiceGrid > div", 0),
    "step-card": (".alt_block.imgBlock", 0),
    "project-facts-list": (".project_facts", 0),
    "section-heading-eyebrow": (".top_block_services", 0),
}
SOURCE_PHOTOS = {
    "home-banners": ["2020/03/NB_No_8.jpg"],
    "banners": ["2020/03/NB_No_%d.jpg" % i for i in (1, 2, 3, 4, 5, 6, 7, 9)],
}


# names for the inline icons, in order of first appearance on the page
SVG_NAMES = {1: "arrow-up-pressure", 2: "storefront-tenant", 3: "water-drop-hot-water", 4: "shield-backflow",
             5: "water-drop", 6: "pipe-flow", 7: "clipboard-checklist"}


FOLDERS = ("home-banners", "banners", "flat-icons", "web-elements", "icons")
FONTS = SITE / "assets/wp-content/themes/jm-understrap-child/assets/dist/fonts"
# Font Awesome 5 glyphs the page uses (Free license: CC BY 4.0)
FA_GLYPHS = {"ui": ("fa-solid-900.svg", ["phone", "phone-alt", "angle-left", "angle-right", "map-marker-alt"]),
             "social": ("fa-brands-400.svg", ["facebook-f", "instagram"])}
ICON_FILES = {
    "favicon": ["2020/01/local-plumbing-favicon-32x32-1.png", "2020/01/local-plumbing-favicon-32x32-1-150x150.png"],
    "ui": ["2020/03/icon_check.png"],
    "logos-badges": ["2020/01/local-plumbing-logo.png", "2023/02/local_footer_logo.png", "2025/04/SBA-Logo.png",
                     "2020/10/PHCC_blk.png", "2025/01/ABC_member.png", "2025/02/Google-Review-Logo-ftr.png"],
}


def export_icons():
    out = ROOT / "icons"
    for sub, files in ICON_FILES.items():
        (out / sub).mkdir(parents=True, exist_ok=True)
        for f in files:
            shutil.copy2(UPLOADS / f, out / sub / Path(f).name)
    for sub, (font, names) in FA_GLYPHS.items():
        (out / sub).mkdir(parents=True, exist_ok=True)
        svg = (FONTS / font).read_text(encoding="utf-8")
        default_w = re.search(r'<font [^>]*horiz-adv-x="(\d+)"', svg).group(1)
        for name in names:
            g = re.search(r'<glyph glyph-name="%s"([^>]*?)/>' % re.escape(name), svg, re.S).group(1)
            d = re.search(r'\bd="([^"]+)"', g).group(1)
            w = (re.search(r'horiz-adv-x="(\d+)"', g) or [None, default_w])[1]
            # SVG-font glyphs are y-up with ascent 448 / descent -64: flip into a normal viewBox
            (out / sub / f"{name}.svg").write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 512" fill="currentColor">'
                f'<path transform="translate(0 448) scale(1 -1)" d="{d}"/></svg>\n')


def chrome(args):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--user-data-dir={tempfile.mkdtemp()}", "--virtual-time-budget=15000", *args],
                   check=True, capture_output=True, text=True)


def render(width):
    """Full-page screenshot plus the bounding boxes of every selector we need."""
    selectors = {k: v for d in (HOME_BANNERS, BANNERS, WEB_ELEMENTS) for k, v in d.items()}
    probe = ("<script>addEventListener('load',()=>setTimeout(()=>{const o={};"
             f"for(const [k,[s,i]] of Object.entries({json.dumps(selectors)}))"
             "{const vis=[...document.querySelectorAll(s)].map(e=>e.getBoundingClientRect())"
             ".filter(r=>r.width>0&&r.height>0&&r.left>=0&&r.right<=innerWidth+1);"  # skip hidden/off-screen carousel clones
             "const r=vis[i];if(r)o[k]=[r.left+scrollX,r.top+scrollY,r.width,r.height];}"
             "const p=document.createElement('pre');p.id='__rects';p.textContent=JSON.stringify(o);"
             "document.body.appendChild(p);},500));</script></body>")
    tmp = SITE / "__export.html"
    tmp.write_text((SITE / "index.html").read_text(encoding="utf-8").replace("</body>", probe, 1), encoding="utf-8")
    shot = Path(tempfile.mkdtemp()) / "page.png"
    try:
        chrome([f"--window-size={width},{HEIGHT}", f"--screenshot={shot}", tmp.as_uri()])
        dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={tempfile.mkdtemp()}",
                              "--virtual-time-budget=15000", f"--window-size={width},{HEIGHT}", "--dump-dom", tmp.as_uri()],
                             check=True, capture_output=True, text=True).stdout
    finally:
        tmp.unlink()
    m = re.search(r'<pre id="__rects">(.*?)</pre>', dom, re.S)
    assert m, "probe script did not run"
    return Image.open(shot), json.loads(m.group(1).replace("&quot;", '"'))


def crop(img, rect, out):
    x, y, w, h = (round(v) for v in rect)
    assert w > 0 and h > 0, f"empty box for {out.name}"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.crop((x, y, x + w, y + h)).save(out, optimize=True)


def main():
    for d in FOLDERS:
        shutil.rmtree(ROOT / d, ignore_errors=True)

    for width in (1440, 768):
        img, rects = render(width)
        for name in HOME_BANNERS:
            crop(img, rects[name], ROOT / "home-banners" / f"mixed-use-{name}-{width}.png")
        if width == 1440:
            for name in BANNERS:
                crop(img, rects[name], ROOT / "banners" / f"{name}-{width}.png")
            for name in WEB_ELEMENTS:
                crop(img, rects[name], ROOT / "web-elements" / f"{name}.png")

    for folder, files in SOURCE_PHOTOS.items():
        for f in files:
            dst = ROOT / folder / "source-photos" / Path(f).name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(UPLOADS / f, dst)

    # flat icons: every PNG icon the page uses, and every inline SVG once
    html = (SITE / "index.html").read_text(encoding="utf-8")
    icons = ROOT / "flat-icons"
    (icons / "png").mkdir(parents=True)
    for rel in sorted(set(re.findall(r'src="assets/wp-content/uploads/(2026/09/[^"]+\.png)"', html))):
        shutil.copy2(UPLOADS / rel, icons / "png" / Path(rel).name)
    (icons / "svg").mkdir()
    for i, body in enumerate(dict.fromkeys(re.findall(r"<svg width=\"(?:26|34)\"[^>]*>(.*?)</svg>", html, re.S)), 1):
        (icons / "svg" / f"{SVG_NAMES.get(i, 'line-icon-%02d' % i)}.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" '
            'stroke="#1f1f1f" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">' + body + "</svg>\n")

    export_icons()

    for d in FOLDERS:
        n = sum(1 for p in (ROOT / d).rglob("*") if p.is_file())
        print(f"{d}: {n} files")


if __name__ == "__main__":
    main()
