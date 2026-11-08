# ebike_website

Landing page for an e-bike parts company, served from a small Python server on the LAN.

"Voltline" is a placeholder brand name. Search and replace it in `index.html` once there's a real name, and put real contact details in the Contact section.

## Run

Needs Python 3.8+ and nothing else.

```
python server.py
```

Open the printed LAN address (`http://<LAN-IP>:8000`) from another device on your network. Options: `--port 8080`, `--host 127.0.0.1` (this machine only).

On Windows, the first run may show a firewall prompt; allow it on **Private** networks. If other devices can't connect, check that inbound TCP 8000 is allowed.

## Files

- `index.html` — single self-contained page (no external fonts, scripts or images), so it works without internet.
- `server.py` — standard-library static file server.

## Later

The "Battery configurator" section is a placeholder for the configurator app in `../ebike-battery-configurator`. It can link to that app once it has a web front end, or `server.py` can proxy to it.
