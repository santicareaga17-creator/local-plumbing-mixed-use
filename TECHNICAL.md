# Technical Specification — Mixed-Use Plumbing Page

Engineering reference for the LOCAL Plumbing Co. **Mixed-Use** page
(`/commercial/mixed-use/`). Written for the developer who moves it from this static
mock-up into the production WordPress site, or maintains the mock-up.

For the project overview see [README.md](README.md).

---

## 1. System overview

| | |
| --- | --- |
| Type | Single static HTML page (mock-up of a WordPress page) |
| Production target | `https://www.localplumbingco.com/commercial/mixed-use/` (WordPress, page ID unknown — the mock-up borrows Medical / Dental's post ID `3823`) |
| Mock-up URL | <https://local-plumbing-mixed-use.vercel.app> |
| Hosting (mock-up) | Vercel, static, no functions, no environment variables |
| Server-side code | **None.** No database, no API, no secrets in this repo |
| Build | `site/build.py` — Python 3 standard library only |
| Runtime JS | jQuery 3.7.1, jQuery Migrate 3.4.1, Swiper, AOS, theme `child-theme.js` (all mirrored from the live theme) |
| CSS | Live theme `jm-understrap-child/assets/dist/css/child-theme.css` (Bootstrap-based Understrap child theme) + one inline `<style id="mixed-use-page">` block |
| Fonts | Barlow, Barlow Condensed, Oswald (Google Fonts, remote) · Font Awesome 5 (local, via theme CSS) |
| Brand red | `#d0212b` (`.btn_commercial` background) |

### Live site stack (as observed, not verified on the server)

WordPress with the `jm-understrap-child` theme, Contact Form 7 6.2.6, CF7 Honeypot,
`wpcf7-recaptcha` (reCAPTCHA v2), Smash Balloon Instagram Feed 6.17.0, Rank Math SEO,
NitroPack page cache, Cloudflare in front.

---

## 2. Repository map

```
.
├── site/                     ← Vercel Root Directory
│   ├── content.html          Page body (sections between header and footer). Edit copy here.
│   ├── build.py              Build script → index.html
│   ├── index.html            Generated. Committed, served by Vercel.
│   ├── assets/               Mirror of the live site's /wp-content and /wp-includes files (79 files)
│   ├── vercel.json           Vercel config: clean URLs, noindex header, asset caching
│   └── .vercelignore         Keeps build.py and content.html off the CDN
├── design-assets/            Exported banners, icons and UI elements (see its README)
├── html-snapshots/           Live pages as served 2026-11-24 (build input + reference)
├── docs/                     Strategy, SEO and final copy (non-technical)
├── README.md                 Project overview
└── TECHNICAL.md              This file
```

---

## 3. Build pipeline

```bash
python3 site/build.py
```

Input: `html-snapshots/medical-dental-desktop.html` + `site/content.html`.
Output: `site/index.html` (~84 KB) and `site/assets/`.

| Step | What `build.py` does |
| --- | --- |
| 1. Shell | Splits the snapshot at `<section class="page_header` and `</div><!-- .entry-content -->`; keeps `<head>`, header and footer |
| 2. Templating | Replaces `{{FORM}}`, `{{SERVICE_GRID}}`, `{{STEPS}}`, `{{CONTACT_AND_INSTAGRAM}}`, `{{ICON_*}}` in `content.html`. Services and steps data live in the `SERVICES` / `STEPS` lists in `build.py` |
| 3. Metadata | Rewrites `<title>`, meta/OG/Twitter descriptions and titles, canonical, oEmbed links; sets `robots` to `noindex, nofollow`; moves the nav active state to Mixed Use |
| 4. Hardening | Removes tracking `<script>` blocks, `gtag()` `onclick`s, `srcset`/`sizes`; sets the form to `action="#" onsubmit="return false"`; fixes `tel:5038776971e` |
| 5. Asset mirror | Downloads every referenced `localplumbingco.com/wp-content|wp-includes` file (and files referenced inside CSS) to `site/assets/`, rewrites URLs to relative paths |

Guards: the build asserts no `{{…}}` placeholder survives. Downloads are cached (a file
already in `site/assets/` is not re-fetched); delete it to refresh.

Known limitation: the build depends on the snapshot's exact markers
(`<section class="page_header`, `<!-- CONTACT SECTION -->`, etc.). If the snapshot is
replaced with a newer copy of the live page, re-check those markers.

---

## 4. Deployment

| | |
| --- | --- |
| Trigger | Push to `main` → production. Other branches → preview URL |
| Vercel project | `local-plumbing-mixed-use` (team `santicareaga17-2681s-projects`) |
| Root Directory | `site` |
| Framework / build / install | None / empty / empty. Output directory `.` |
| Config | `site/vercel.json` — clean URLs, `X-Robots-Tag: noindex`, long cache on `/assets/` |
| Pre-push | Run `python3 site/build.py` and commit `site/index.html` (Vercel does not run Python) |

Do **not** run `vercel deploy` from `site/`: with Root Directory `site` the CLI resolves
`site/site` and fails.

---

## 5. Page structure

Section order, with the theme classes each block depends on. Any WordPress template must
output the same class names for `child-theme.css` to apply.

| # | Section | Root element / key classes |
| --- | --- | --- |
| 1 | Hero | `section.page_header.section_wide.dental_bg.mixed_use_bg` (background set in the inline style block) |
| 2 | Intro, icon grid, lead form | `section#commercial_service.hvac_services_section` · `.grid_icons_block.five_grid` · `.card.card-body` · CF7 markup |
| 3 | "One Building. Many Demands." | `div.md_section` (`.top_md`) + `section.md_section` · `.carousel_block .swiper-container.mySwiper` |
| 4 | Services (3 cards) | `section.kitchen_section.hvac_services_section` · `.service_grid` (desktop) + `.mobile_carousel .swiper` (mobile, same content) |
| 5 | Business Impact | `section.md_section.p-0` · `.commercial_text_block.reduced_block` · `.min_block .full_big_img` |
| 6 | Residential / Ground-floor cards | `.twiceGrid` · `.redTitle` · `.solutionsBlock` |
| 7 | Nomad Building spotlight | `section.md_section.p-0.project_spotlight` · `ul.project_facts` · `.row.project_strip` (**new classes**, styled inline) |
| 8 | How It Works | `section.kitchen_section` · `.alt_block.imgBlock` (grid + mobile carousel) |
| 9 | 24/7 band | `section.support_section` · `.buttons_block` · `.black_btn` |
| 10 | Map + Instagram | `section.hvac_red_section` (Google Maps iframe) · `#sb_instagram` (Smash Balloon) |
| 11 | One Local Team | `section.kitchen_section` · `.commercial_btn` |
| 12 | Veteran-owned partner | `section.section_content.bg-light` |
| 13 | Final CTA | `div.redCTA` · `.btn_commercial.alt_black` / `.alt_t` |

Page-specific CSS (everything not in the theme) is the `EXTRA_CSS` string in `build.py`:
`.mixed_use_bg`, `.project_facts`, `.project_strip`, fixed-height carousel images, and a
≤575 px hero title override.

Swiper instances are initialised by the theme's `swiper-init.js` on `.mySwiper`; no
page-specific JS exists.

---

## 6. Lead form contract

The mock-up form is inert. In production it is **Contact Form 7 form ID `5`** (same form
as every industry page).

| Field (`name`) | Type | Required | Notes |
| --- | --- | --- | --- |
| `your-first-name` | text, max 400 | yes | |
| `your-last-name` | text, max 400 | yes | |
| `your-email` | email, max 400 | yes | |
| `your-phone` | tel, max 400 | no | |
| `your-industry` | select | no | Options: Government, Commercial Property Management, Beverage Industry, Medical / Dental Facilities, Schools, Manufacturing, Restaurants, Offices, Hospitality, Shopping Centers, Mixed Use, Other. **Preselect `Mixed Use` on this page** |
| `your-comments` | textarea, max 2000 | no | |
| `your-cookie-consent` | acceptance checkbox | yes | Pre-checked |
| `your-additional-email` (+ `-time-start`, `-time-check`) | honeypot | — | Must stay empty |
| `g-recaptcha-response` | reCAPTCHA v2 | yes | Site key is domain-locked to localplumbingco.com |

Hidden CF7 fields: `_wpcf7=5`, `_wpcf7_version=6.2.6`, `_wpcf7_locale=en_US`,
`_wpcf7_unit_tag`, `_wpcf7_container_post` (the real page's post ID).

**Production change needed:** the live Mixed Use page's dropdown currently has no
"Mixed Use" option. Add it in the CF7 form (or a page-specific default), and consider the
optional "Project stage" field proposed in `docs/03_seo-sem.md`.

---

## 7. Moving it into WordPress

Recommended path (the theme already contains every component used):

1. Create or edit the Mixed Use page; use the same page template as Medical / Dental.
2. Paste the sections of `site/content.html` into the page body (or the template's
   section fields). Its `/wp-content/...` paths already match the live upload paths.
3. Replace `{{FORM}}` with the CF7 shortcode for form `5`, and `{{CONTACT_AND_INSTAGRAM}}`
   with the theme's existing contact + Instagram sections.
4. Add the `EXTRA_CSS` rules to the child theme (or Customizer → Additional CSS).
5. Set Rank Math title / description from `docs/03_seo-sem.md`. Keep the URL
   `/commercial/mixed-use/`. **Remove** `noindex` (the mock-up's, not the live page's).
6. Restore tracking: it lives in the theme header, so nothing to do unless the page uses a
   custom header.
7. Purge NitroPack and Cloudflare caches after publishing.

Images used: Nomad Building photos `uploads/2020/03/NB_No_1–9.jpg` (already on the live
server) and existing icons in `uploads/2026/09/`. No new uploads are required.

---

## 8. Third-party scripts removed from the mock-up

These are present on the live page and **intentionally stripped** here, so they need no
action in WordPress:

Google Ads `AW-608306962` (gtag + call-conversion `onclick`s) · Google Tag Manager
`GTM-P2WTC3L` · Microsoft Clarity · CookieYes · Yext Knowledge Tags · call tracking
(`tctm.co`) · lead-capture script (`libs.sfs.io`) · reCAPTCHA · NitroPack beacons ·
Cloudflare challenge script · WP emoji loader · Contact Form 7 JS.

---

## 9. Performance & limits

| | |
| --- | --- |
| HTML | ~84 KB |
| Files referenced directly from `index.html` | 47, ~3.5 MB (photos are the bulk; Nomad JPGs up to 1920 × 1080, unoptimised) |
| Mirrored assets total | 79 files, 8.3 MB (includes fonts/images referenced by CSS) |
| Images | No `srcset` (stripped), no `loading="lazy"` on content images |

Suggested before production: serve the Nomad photos through WordPress's resized variants
or WebP, and add `loading="lazy"` below the fold.

---

## 10. Known issues

| Issue | Where | Impact |
| --- | --- | --- |
| `tel:5038776971e` (stray `e`) | Live Restaurants and Medical / Dental pages | Salem call button may fail on some devices. Fixed in the mock-up only |
| "503-642-2067" text dials the Salem number | Live Medical / Dental partner paragraph | Wrong office receives calls |
| No "Mixed Use" in the industry dropdown | Live Mixed Use page form | Leads mis-categorised |
| Google Maps iframe and Instagram feed | Mock-up | Load from Google / show no posts offline; fine on the live site |
| Mobile check | Mock-up | Verified only by headless Chrome against the live page; test on a real phone |
