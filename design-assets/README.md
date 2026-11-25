# Design assets

The image files the Mixed-Use page uses, grouped by role. Every file keeps its original
WordPress upload name, so it maps 1:1 to `/wp-content/uploads/<year>/<month>/<name>` on
localplumbingco.com. Regenerate with `python3 design-assets/export.py` after
`python3 site/build.py`.

| Folder | Contents |
| --- | --- |
| `home-banners/` | Hero banner images: `NB_No_8.jpg` (this page), plus the Medical / Dental, Restaurants & Kitchens and HVAC heroes from the same theme |
| `banners/` | Section photos: Nomad Building construction photos `NB_No_1–7, 9` (spotlight, carousel, cards, steps) |
| `web-elements/` | Section background images from the theme: flag background (`.hvac_services_section`), clear flag (`.bg-flag`), dark texture (`.bg-texture`) |
| `flat-icons/png/` | The 15 service icons (PNG uploads) |
| `flat-icons/svg/` | The page's 7 inline line icons as standalone 24 × 24 SVGs (stroke `#1f1f1f`, 1.5 px) |
| `icons/favicon/` | Site favicons (32 px and 150 px PNG) |
| `icons/ui/` | Phone, arrows and map-pin icons as SVG (Font Awesome 5, `fill=currentColor`) + the red check bullet PNG |
| `icons/social/` | Facebook and Instagram icons as SVG (Font Awesome 5 Brands) |
| `icons/logos-badges/` | LOCAL logos and the SBA, PHCC, ABC and Google Reviews badges from the footer |

Font Awesome Free icons are licensed CC BY 4.0. Logos and badges belong to their owners.
All photos are the client's own Nomad Building construction photos.
