// Configurator engine in the browser: loads Pyodide (Python compiled to WebAssembly), unpacks
// engine.zip (the repo's Python engine, built by web/bundle.py) into /app and calls web/api.py.
// No server needed, so the page can be hosted on GitHub Pages.
//
//   await Engine.start(onStatus)   load once (about 10 MB the first time, cached afterwards)
//   Engine.options()               form choices, limits and defaults
//   Engine.pack(choices)           errors, warnings, specs, dims, part drawings, BOM
//   Engine.package(choices)        { name, bytes } of the build-package zip
// A malformed request throws an Error with the engine's message.
(function () {
  const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
  let py = null, starting = null;

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = Object.assign(document.createElement("script"), { src, async: true });
      s.onload = resolve;
      s.onerror = () => reject(new Error("could not load " + src));
      document.head.append(s);
    });
  }

  async function boot(onStatus) {
    const say = msg => onStatus && onStatus(msg);
    say("Loading the Python runtime…");
    if (!window.loadPyodide) await loadScript(PYODIDE_URL + "pyodide.js");
    const p = await window.loadPyodide({ indexURL: PYODIDE_URL });
    say("Loading the configurator engine…");
    const res = await fetch("engine.zip", { cache: "no-cache" });
    if (!res.ok) throw new Error("engine.zip: " + res.status + " " + res.statusText);
    p.unpackArchive(await res.arrayBuffer(), "zip", { extractDir: "/app" });
    p.runPython(`
import json, sys
sys.path.insert(0, "/app/web")
import api

def _call(name, choices_json):
    try:
        args = () if choices_json is None else (json.loads(choices_json),)
        return json.dumps({"ok": True, "result": getattr(api, name)(*args)})
    except (api.ChoiceError, api.ConfigError) as exc:
        return json.dumps({"ok": False, "error": str(exc)})

def _package(choices_json):
    try:
        name, data = api.package(json.loads(choices_json))
        return name, data, ""
    except (api.ChoiceError, api.ConfigError) as exc:
        return "", b"", str(exc)
`);
    py = p;
    say("");
  }

  function call(name, choices) {
    const out = JSON.parse(py.globals.get("_call")(name, choices === undefined ? null : JSON.stringify(choices)));
    if (!out.ok) throw new Error(out.error);
    return out.result;
  }

  window.Engine = {
    start(onStatus) { return starting || (starting = boot(onStatus)); },
    options() { return call("options"); },
    pack(choices) { return call("pack", choices); },
    package(choices) {
      const t = py.globals.get("_package")(JSON.stringify(choices));
      const [name, data, err] = t.toJs();
      t.destroy();
      if (err) throw new Error(err);
      return { name, bytes: data instanceof Uint8Array ? data : new Uint8Array(data) };
    },
  };
})();
