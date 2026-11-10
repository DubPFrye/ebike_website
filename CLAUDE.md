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

| Folder here | Source repo | How it gets here |
|---|---|---|
| `configurator/` | `DubPFrye/ebike-battery-configurator` (day-to-day work on its `working` branch) | `sync_configurator.py` builds it locally; that repo's `publish-configurator.yml` can push it on every push to its `main` |
| `spoke-calculator/` | `DubPFrye/spoke-calculator` (calculator is on its `add-calculator` branch, not merged yet) | that repo's `publish.yml` copies the page files on every push to its `main` |
| `bms-translator/` | `DubPFrye/LLT-VESC-Bridge` | build guide written from that repo (currently from commit `b85dad9`) and committed here by hand |

- The publish workflows need a `WEBSITE_REPO` variable and a `WEBSITE_TOKEN` secret
  (a fine-grained token with Contents read/write on this repo only) set in each source repo.
  **They aren't set up yet**, so publishing is manual for now: sync or copy, commit, push.
- The owner may rename these repos (this one to `FryePower.com`). GitHub redirects old
  names, but update `WEBSITE_REPO`, the README links and `git remote` URLs to match.
- A cloud session only sees the repos attached to it. Check which repo the task is about
  before editing anything, and ask if it's unclear.

## Local development

- On the owner's PC the repo lives in a folder named `FryePower.com`, next to the
  `ebike-battery-configurator` folder (which `sync_configurator.py` expects by
  default; use `--src` if the folder is renamed).
- Run `python server.py --host 127.0.0.1 --port 8020`, then open http://localhost:8020.
  `.claude/launch.json` runs the same command.
- Test locally before pushing to `main`, because `main` is live.

## Site conventions

- The landing page (`index.html`, `styles.css`) keeps the `#parts`, `#about`, `#contact`
  and `#projects` sections. The configurator's header links back to them (`../#parts`, ...).
- Each project gets a card in the Projects section that links to its folder.
- Work in progress is clearly labelled on the page: the configurator has an alpha badge and
  a disclaimer the visitor must accept before downloading, and the BMS translator guide has
  a Draft badge and warning. Keep these until the owner says a project is ready.
- Keep everything plain static HTML/CSS/JS so it works on GitHub Pages without a build.

## Git habits

- Work on a feature branch and open a PR to `main`. Don't push straight to `main` unless asked.
- Make a PR only when the owner asks for one.

## Open to-do

- Real contact details in the Contact section (currently placeholders).
- Set up `WEBSITE_TOKEN` / `WEBSITE_REPO` so project repos publish automatically.
- BMS translator guide: add the prebuilt firmware once it's confirmed working on a VESC,
  then remove the Draft warning.
- Spoke calculator: merge `add-calculator` into `main` in its repo, and merge PR #1 here.
