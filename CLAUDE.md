# CLAUDE.md

Notes for Claude sessions working on this repo. The README has the run and publish details;
this file covers the context and habits behind them.

## What this is

The FryePower website: static files served by GitHub Pages at https://fryepower.com
(e-bike parts and DIY e-bike projects). No build step and no backend. Everything runs in
the visitor's browser, so never add API keys or secrets to these files.

- The domain is registered at Cloudflare. DNS has 4 A records plus 1 CNAME, all set to
  **DNS only** (grey cloud). Leave them grey, because GitHub issues the HTTPS certificate.
- `CNAME` holds `fryepower.com` and `.nojekyll` makes Pages serve files as they are.
  Don't delete either one.
- Pages serves `main`. Anything pushed to `main` goes live within a minute or two.

## Repos that make up the site

The site pulls in pages from separate project repos. Make changes in the project repo,
not in its copy here, because the next publish overwrites the copy.

This repo is `DubPFrye/fryepower-com` (renamed from `ebike_website`; GitHub redirects the old name).

| Folder here | Source repo | How it gets here |
|---|---|---|
| `configurator/` | `DubPFrye/pev_battery_configurator` (**private**; local folder `ebike-battery-configurator`; day-to-day work on its `working` branch) | `sync_configurator.py` runs that repo's `web/build_static.py`; its `publish-configurator.yml` can push the build on every push to its `main` |
| `spoke-length-calculator/` | `DubPFrye/spoke-length-calculator` (has Node tests in `tests/`) | that repo's `publish.yml` copies the page files on every push to its `main` |
| `bms-translator/` | `DubPFrye/bms-vesc-bridge` (formerly `LLT-VESC-Bridge`; STM32CubeIDE project, GPL-3.0) | build guide written from that repo (currently from commit `b85dad9`) and committed here by hand |

- The configurator page's source is `web/index.html` in its repo (renamed from
  `configurator.html` in commit `73508cc`). Its alpha badge, warning box and download
  disclaimer live there; the static-site tests in that repo should pass after changes.
- The publish workflows need a `WEBSITE_REPO` variable (`DubPFrye/fryepower-com`) and a
  `WEBSITE_TOKEN` secret (one fine-grained token with Contents read/write on this repo only,
  reused in every source repo). **They aren't set up yet**, so publishing is manual for now:
  sync or copy, commit, push.
- A cloud session only sees the repos attached to it. Check which repo the task is about
  before editing anything, and ask if it's unclear.

## Local development

- On the owner's PC the repo lives in a folder named `FryePower.com`, next to the
  `ebike-battery-configurator` folder (which `sync_configurator.py` expects by
  default; use `--src` if the folder is renamed).
- Run `python server.py --host 127.0.0.1 --port 8020`, then open http://localhost:8020.
  `.claude/launch.json` runs the same command.
- Test locally before pushing to `main`, because `main` is live.
- The owner often works from a phone (Remote Control or a cloud session). `localhost` only
  works on the PC, so away from home point them at https://fryepower.com to see changes,
  which means the change has to be merged to `main` first. Phones may cache the old page
  for a few minutes; a pull-to-refresh fixes it.

## Site conventions

- The landing page (`index.html`, `styles.css`) keeps the `#parts`, `#about`, `#contact`
  and `#projects` sections. The configurator's header links back to them (`../#parts`, ...).
- Each project gets a card in the Projects section that links to its folder.
- Work in progress is clearly labelled on the page: the configurator has an alpha badge and
  a disclaimer the visitor must accept before downloading, and the BMS translator guide has
  a Draft badge and warning. Keep these until the owner says a project is ready.
- The owner hasn't built a pack from the configurator, and its cell data is placeholder.
  The disclaimer text is a plain-language starting point, not lawyer-reviewed; suggest a
  lawyer reviews it if FryePower starts selling parts or packs.
- Keep everything plain static HTML/CSS/JS so it works on GitHub Pages without a build.

## BMS translator plans (discussed, not built)

- Goal: an STM32 reads cell data from a cheap LLT/JBD-style BMS over UART and sends it to
  a VESC over CAN, so the VESC can cut off on individual cell voltage. The 20A BMS is used
  only for charging and balancing; its FET output isn't wired in.
- That makes the bridge and the VESC the only discharge protection, so the firmware must
  fail safe: a watchdog, and if cell data goes stale (STM32 hang, UART wire off, BMS not
  replying) the VESC cuts or limits current instead of trusting the last reading. The
  guide must say this plainly.
- Page layout, Instructables-style: intro, alpha/safety warning, parts and tools, notes,
  numbered steps with photos and diagrams (wiring, flashing, VESC setup, bench test),
  troubleshooting, downloads (firmware, source zip, diagrams), and the commit it was built from.
- Ideas for later: keep the guide as Markdown in the bridge repo and build the page in CI;
  compile the firmware in CI so the download matches `main`; draw wiring with WireViz;
  a shared guide page style for future projects.

## Git habits

- Work on a feature branch and open a PR to `main`. Don't push straight to `main` unless asked.
- Fetch before pushing. Changing the custom domain in the Pages settings makes GitHub commit
  to `CNAME` itself (it has done "Delete CNAME" / "Create CNAME"), so `main` can move without
  anyone pushing. After rebasing, check `CNAME` still says `fryepower.com`.
- Make a PR only when the owner asks for one.

## Open to-do

- Real contact details in the Contact section (currently placeholders).
- Set up `WEBSITE_TOKEN` / `WEBSITE_REPO` so project repos publish automatically.
- BMS translator guide: add the prebuilt firmware once it's confirmed working on a VESC,
  then remove the Draft warning.
- Spoke calculator: check its `add-calculator` branch is merged into `main` in its repo (the live page came from PR #1 here).
