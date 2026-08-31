# -*- coding: utf-8 -*-
"""Rollt die Aktionen von gemma-golfn.at aus (FTPS, Hetzner).

Loest die Einzelskripte je Aktion ab: Statt fuer jede neue Werbung ein eigenes
Deploy-Skript anzulegen (deploy_workshops_september_2026.py und Nachfolger),
liest dieses Skript die aktionen.json und laedt genau das hoch, was dort
tatsaechlich referenziert wird.

Was hochgeladen wird:
  1. Aktuelle Aktionen/aktionen.json
  2. jedes in der JSON unter "bild" genannte, noch nicht abgelaufene Bild

Abgelaufene Aktionen werden uebersprungen — die Homepage blendet sie ohnehin
aus (index.html filtert expires >= heute), ihre Bilder muessen nicht auf dem
Server liegen. Geloescht wird auf dem Server NICHTS: das Backup darf wachsen,
aber nie automatisch loeschen (Vorgabe Mario, Vorfall 06.07.2026).

Zugangsdaten: .env eine Ebene ueber prototype/ (HETZNER_USER, HETZNER_PASSWORD).
Werte werden nie ausgegeben.

Nutzung:
  python deploy_aktionen.py --probelauf    zeigt nur an, was hochgeladen wuerde
  python deploy_aktionen.py --echt         laedt wirklich hoch

Rollback: Die vorherige aktionen.json liegt in Git. Datei auschecken und dieses
Skript erneut laufen lassen. Einzelne Aktion sofort ausblenden: "expires" auf
ein vergangenes Datum setzen und neu ausrollen.
"""
import json
import sys
from datetime import date
from ftplib import FTP_TLS
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROTO = SCRIPT_DIR.parent
ENV_FILE = PROTO.parent / ".env"
AKTIONEN_DIR = PROTO / "Aktuelle Aktionen"
HOST = "www193.your-server.de"
WEBROOT = "public_html_backup_wordpress"

echt = "--echt" in sys.argv

# ── Was steht an? ────────────────────────────────────────────────────────────
liste = json.loads((AKTIONEN_DIR / "aktionen.json").read_text(encoding="utf-8"))
heute = date.today().isoformat()

aktiv, abgelaufen, fehlend = [], [], []
for eintrag in liste:
    bild = eintrag.get("bild", "")
    if eintrag.get("expires", "") < heute:
        abgelaufen.append(eintrag.get("titel", bild))
        continue
    pfad = AKTIONEN_DIR / bild
    if not pfad.exists():
        fehlend.append(bild)
        continue
    aktiv.append(pfad)

print("Aktionen-Deploy" + ("" if echt else "  [PROBELAUF — es wird nichts hochgeladen]"))
print("  aktiv:      %d" % len(aktiv))
print("  abgelaufen: %d (uebersprungen: %s)" % (len(abgelaufen), ", ".join(abgelaufen) or "-"))

if fehlend:
    # Fail safe, nicht fail silent: lieber abbrechen als eine Aktion ohne Bild
    # ausrollen — die Seite zeigt sonst ein kaputtes Vorschaubild.
    print("\nABBRUCH: In aktionen.json stehen Bilder, die es nicht gibt:")
    for b in fehlend:
        print("  fehlt:", b)
    sys.exit(1)

print("\nHochzuladen:")
print("  aktionen.json")
for p in aktiv:
    print("  " + p.name)

if not echt:
    print("\nZum echten Lauf: --echt anhaengen.")
    sys.exit(0)

# ── Hochladen ────────────────────────────────────────────────────────────────
env = {}
for line in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

for schluessel in ("HETZNER_USER", "HETZNER_PASSWORD"):
    if not env.get(schluessel):
        print("ABBRUCH: %s fehlt in der .env." % schluessel)
        sys.exit(1)

ftp = FTP_TLS(HOST, timeout=60)
ftp.login(env["HETZNER_USER"], env["HETZNER_PASSWORD"])
ftp.prot_p()
ftp.cwd(WEBROOT)
ftp.cwd("Aktuelle Aktionen")


def upload(local: Path, remote_name: str):
    with open(local, "rb") as f:
        ftp.storbinary("STOR " + remote_name, f)
    print("  hochgeladen:", remote_name)


print("")
for p in aktiv:
    upload(p, p.name)
upload(AKTIONEN_DIR / "aktionen.json", "aktionen.json")  # zuletzt: erst wenn die Bilder liegen

ftp.quit()
print("\nFERTIG. Kontrolle: https://gemma-golfn.at")
print("Oeffentliche Bild-URLs: https://gemma-golfn.at/Aktuelle%20Aktionen/<dateiname>")
