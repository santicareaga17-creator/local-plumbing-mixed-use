# Mixed-Use Plumbing Landing Page

Mock-up of a new **Mixed-Use** industry page for LOCAL Plumbing Co., built on the live
site's own page template and deployed on Vercel.

**Live:** <https://local-plumbing-mixed-use.vercel.app>

A commercial plumbing page for LOCAL Plumbing Co. that targets general contractors,
developers and property managers working on mixed-use buildings in Portland & Salem, OR.
It replaces today's [Mixed Use page](https://www.localplumbingco.com/commercial/mixed-use/),
which is only a service list and a form.

> This project is **completely separate** from the Tree Care / LA Grinding project and
> from the [Medical / Dental landing page](https://github.com/santicareaga17-creator/medical-dental-landing-page).
> It shares no repository, no build, and no Vercel deployment with them.

---

## What this is

A single page at `/`: the live Medical / Dental page's shell (header, footer, theme CSS
and JS) wrapped around new Mixed-Use content. It reuses the site's own markup classes,
so it looks like the client's other industry pages and can be moved into their WordPress
theme section by section.

| | |
| --- | --- |
| Production | <https://local-plumbing-mixed-use.vercel.app> |
| Vercel project | `local-plumbing-mixed-use` (deployed from `site/`) |
| Content source | `site/content.html` |
| Build | `site/build.py` (Python 3, standard library only) |
| Output | `site/index.html` + 79 files in `site/assets/` |
| Market | Portland & Salem, Oregon |

### Page sections

Hero · intro with service icon grid and lead form · "One Building. Many Demands." card
carousel · services split into Construction & Tenant Work / Water Systems / Building
Support · Business Impact · Residential Floors and Ground-Floor Commercial & Garage cards ·
**Nomad Building project spotlight** · "One Call" steps · 24/7 support band · map ·
One Local Team (with internal links) · veteran-owned partner · final CTA · footer.

All project photos are the client's own Nomad Building construction photos from their
[Projects page](https://www.localplumbingco.com/projects/).

---

## Quick start

```bash
git clone https://github.com/santicareaga17-creator/local-plumbing-mixed-use.git
```

```bash
cd local-plumbing-mixed-use && python3 site/build.py && open site/index.html
```

The page opens straight from disk: every stylesheet, script and image is local. Only the
Barlow fonts come from Google Fonts.

### Deploy

```bash
cd site && vercel deploy --prod
```

`site/.vercelignore` keeps `build.py` and `content.html` off the server.

---

## Repository layout

```
.
├── site/
│   ├── content.html    The new page content. Edit text here.
│   ├── build.py        Wraps content.html in the live page shell → index.html
│   ├── index.html      Build output (committed; this is what Vercel serves)
│   └── assets/         Theme CSS/JS, icons and photos, mirrored from the live site
├── docs/               Strategy and copy (see below)
└── html-snapshots/     The live pages as served on 2026-11-24, desktop and mobile
```

### docs/

| File | Contents |
| --- | --- |
| `01-03_audits.md` | Competitor benchmark, brand & social audit, internal page benchmark |
| `03_seo-sem.md` | Keyword map, metadata, internal links, conversion and Google Ads notes |
| `04_mixed-use-page-copy.md` | Final page copy, text only |
| `05_client-validation.md` | What the client still has to confirm |

---

## How the build works

[`site/build.py`](site/build.py) starts from `html-snapshots/medical-dental-desktop.html`
and:

1. Keeps the page's `<head>`, header and footer, and swaps everything between them for
   `site/content.html`.
2. Fills the `{{FORM}}`, `{{SERVICE_GRID}}`, `{{STEPS}}`, `{{CONTACT_AND_INSTAGRAM}}` and
   icon placeholders. The services and steps lists live in `build.py`, and each one is
   rendered twice, as the desktop grid and the mobile carousel, the way the live page does.
3. Rewrites the title, meta description, Open Graph tags and canonical URL for
   `/commercial/mixed-use/`, and moves the nav's active state to Mixed Use.
4. Downloads every `localplumbingco.com` stylesheet, script and image into `site/assets/`,
   including files referenced from inside the CSS, and points the page at the local copies.

It fails the build if any `{{ … }}` placeholder is left in the output.

### What the mock-up deliberately does not do

- **No tracking.** Google Ads / GTM, Microsoft Clarity, CookieYes, call tracking and the
  lead script are stripped, so viewing the mock-up never shows up in the client's
  analytics.
- **No form submissions.** The form is wired to `#` and does nothing. The real form posts
  to the client's WordPress site.
- **Not indexed.** `robots` is `noindex, nofollow`, so Google never treats it as a copy of
  the client's site.
- **No reCAPTCHA.** It only works on the client's domain.

---

## Verification

- Rendered at 1440px with headless Chrome, section by section, with **localplumbingco.com
  blocked**: all styles, icons and photos load from `site/assets/`.
- The live URL, the theme CSS and a project photo return `200`. `build.py` returns `404`.
- At 390px the layout matches the live Medical / Dental page rendered the same way.
  Headless Chrome crops both on the right, so check it on a real phone before going live.

---

## Before this goes live on localplumbingco.com

See [`docs/05_client-validation.md`](docs/05_client-validation.md). The main items:

- Nomad Building: location, completion year and LOCAL's exact plumbing scope.
- License numbers, current association memberships and bid turnaround.
- More project photos (some Nomad photos are reused across sections).
- Add "Mixed Use" to the industry dropdown on the live form, and fix the
  `tel:5038776971e` link on the Restaurants and Medical / Dental pages.
