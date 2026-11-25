# Design assets

Visual assets from the Mixed-Use page, grouped for designers and developers.
Regenerate everything with `python3 design-assets/export.py` (needs Google Chrome and
Pillow) after `python3 site/build.py`.

| Folder | Contents |
| --- | --- |
| `home-banners/` | Page hero rendered at 1440 px and 768 px, plus its source photo (`NB_No_8.jpg`) |
| `banners/` | Full-width section banners at 1440 px (Business Impact, Nomad spotlight, 24/7 band, final CTA) and the Nomad Building source photos |
| `flat-icons/png/` | The 15 line-art service icons used on the page (from the live site's uploads) |
| `flat-icons/svg/` | The 7 inline line icons, as standalone 24 × 24 SVGs (stroke `#1f1f1f`, 1.5 px) |
| `web-elements/` | UI components cropped from the page at 1440 px: header, footer, buttons, lead form, cards, icon grid, project facts, section heading |

All photos are the client's own Nomad Building construction photos. Rendered PNGs are
screenshots, so they show the Barlow fonts as loaded from Google Fonts.
