# FryePower.com

The FryePower website, published with GitHub Pages at https://fryepower.com.

All static files: `index.html` is the landing page, and `configurator/` is the battery configurator,
built from the separate `ebike-battery-configurator` project. The configurator runs entirely in the
visitor's browser (Pyodide), so no server is needed.

## Run locally

Needs Python 3.8+.

```
python server.py --host 127.0.0.1 --port 8020
```

Then open http://localhost:8020 (landing page) and http://localhost:8020/configurator/.
The server sends `Cache-Control: no-cache`, so a browser refresh picks up edits. Without
`--host`, it also serves on your LAN (useful for checking the site on a phone).

To pull in the latest configurator after changing it in the other project:

```
python sync_configurator.py
```

This runs `../ebike-battery-configurator/web/build_static.py` with that project's venv and writes
`configurator/` here.

## Publishing

- Push to `main` and GitHub Pages serves the repo root. `CNAME` holds the custom domain;
  `.nojekyll` makes Pages serve the files as they are.
- The configurator repo's `publish-configurator.yml` workflow rebuilds `configurator/` and pushes
  it here on every push to its `main` (it needs the `WEBSITE_REPO` variable and the `WEBSITE_TOKEN`
  secret set in that repo). You can also run `sync_configurator.py` and commit the result by hand.
- Don't edit files in `configurator/` here, because the next publish overwrites them. Change them
  in the configurator project instead.
- `spoke-length-calculator/` works the same way: it comes from the
  [spoke-calculator](https://github.com/DubPFrye/spoke-calculator) repo, whose `publish.yml`
  copies its page files here on every push to its `main` (same `WEBSITE_REPO` / `WEBSITE_TOKEN`
  setup). Change it there, not here.

## Files

- `index.html`, `styles.css`: the landing page. It keeps the `#parts`, `#about` and `#contact`
  sections, because the configurator's header links to them (`../#parts`, ...).
- `configurator/`: the built configurator (generated).
- `spoke-length-calculator/`: the spoke length calculator (copied in from its own repo).
- `server.py`: local static server (standard library only).
- `sync_configurator.py`: rebuilds `configurator/` from the configurator project.
- `CNAME`, `.nojekyll`: GitHub Pages settings.

## To do

- Real contact details in the Contact section (currently placeholders).
