"""Collect the page's uploaded image files into design-asset folders.

Run from the repo root after `python3 site/build.py` (which mirrors the live uploads
into site/assets/):
    python3 design-assets/export.py

Files keep their original WordPress upload names, so each one can be matched to
/wp-content/uploads/<year>/<month>/<name> on localplumbingco.com.

  home-banners/  hero banner images (this page + the sibling industry pages)
  banners/       photos used in the page's sections (Nomad Building)
  web-elements/  section background images used by the theme
  flat-icons/    service icons (PNG uploads) + the page's inline line icons (SVG)
  icons/         favicons, UI and social icons, logos and badges
"""
import re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT.parent / "site"
UPLOADS = SITE / "assets" / "wp-content" / "uploads"
FONTS = SITE / "assets/wp-content/themes/jm-understrap-child/assets/dist/fonts"

# folder -> upload paths (relative to /wp-content/uploads/)
UPLOAD_FILES = {
    "home-banners": [
        "2020/03/NB_No_8.jpg",                                # Mixed-Use hero
        "2026/09/banner-medical-dental_bg.webp",              # Medical / Dental hero
        "2026/09/local_plumbing_hero_banner_kitchen.webp",    # Restaurants & Kitchens hero
        "2026/08/local_plumbing_hero_hvac.webp",              # HVAC hero
    ],
    "banners": ["2020/03/NB_No_%d.jpg" % i for i in (1, 2, 3, 4, 5, 6, 7, 9)],
    "web-elements": [
        "2026/08/local_plumbing_flag-bg.webp",   # .hvac_services_section background
        "2020/03/us-flag-clear.jpg",             # .bg-flag background
        "2020/03/texture-dark-grunge.jpg",       # .bg-texture background
    ],
    "icons/favicon": ["2020/01/local-plumbing-favicon-32x32-1.png", "2020/01/local-plumbing-favicon-32x32-1-150x150.png"],
    "icons/ui": ["2020/03/icon_check.png"],
    "icons/logos-badges": ["2020/01/local-plumbing-logo.png", "2023/02/local_footer_logo.png", "2025/04/SBA-Logo.png",
                           "2020/10/PHCC_blk.png", "2025/01/ABC_member.png", "2025/02/Google-Review-Logo-ftr.png"],
}
FOLDERS = ("home-banners", "banners", "web-elements", "flat-icons", "icons")

# Font Awesome 5 glyphs the page uses (Free license: CC BY 4.0)
FA_GLYPHS = {"icons/ui": ("fa-solid-900.svg", ["phone", "phone-alt", "angle-left", "angle-right", "map-marker-alt"]),
             "icons/social": ("fa-brands-400.svg", ["facebook-f", "instagram"])}

# names for the page's inline line icons, in order of first appearance
SVG_NAMES = {1: "arrow-up-pressure", 2: "storefront-tenant", 3: "water-drop-hot-water", 4: "shield-backflow",
             5: "water-drop", 6: "pipe-flow", 7: "clipboard-checklist"}


def copy(rel, folder):
    dst = ROOT / folder / Path(rel).name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(UPLOADS / rel, dst)


def main():
    for d in FOLDERS:
        shutil.rmtree(ROOT / d, ignore_errors=True)

    for folder, files in UPLOAD_FILES.items():
        for rel in files:
            copy(rel, folder)

    html = (SITE / "index.html").read_text(encoding="utf-8")

    # flat icons: every service-icon PNG upload the page uses
    for rel in sorted(set(re.findall(r'src="assets/wp-content/uploads/(2026/09/[^"]+\.png)"', html))):
        copy(rel, "flat-icons/png")

    # the page's inline line icons, once each, as standalone SVGs
    svg_dir = ROOT / "flat-icons" / "svg"
    svg_dir.mkdir(parents=True)
    for i, body in enumerate(dict.fromkeys(re.findall(r'<svg width="(?:26|34)"[^>]*>(.*?)</svg>', html, re.S)), 1):
        (svg_dir / f"{SVG_NAMES.get(i, 'line-icon-%02d' % i)}.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" '
            'stroke="#1f1f1f" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">' + body + "</svg>\n")

    # Font Awesome glyphs → standalone SVGs
    for folder, (font, names) in FA_GLYPHS.items():
        out = ROOT / folder
        out.mkdir(parents=True, exist_ok=True)
        svg = (FONTS / font).read_text(encoding="utf-8")
        default_w = re.search(r'<font [^>]*horiz-adv-x="(\d+)"', svg).group(1)
        for name in names:
            g = re.search(r'<glyph glyph-name="%s"([^>]*?)/>' % re.escape(name), svg, re.S).group(1)
            d = re.search(r'\bd="([^"]+)"', g).group(1)
            m = re.search(r'horiz-adv-x="(\d+)"', g)
            w = m.group(1) if m else default_w
            # SVG-font glyphs are y-up with ascent 448 / descent -64: flip into a normal viewBox
            (out / f"{name}.svg").write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 512" fill="currentColor">'
                f'<path transform="translate(0 448) scale(1 -1)" d="{d}"/></svg>\n')

    for d in FOLDERS:
        print(f"{d}: {sum(1 for p in (ROOT / d).rglob('*') if p.is_file())} files")


if __name__ == "__main__":
    main()
