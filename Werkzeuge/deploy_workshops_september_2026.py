# -*- coding: utf-8 -*-
"""Deploy Workshops September 2026 auf gemma-golfn.at (FTPS, Hetzner).

Laedt hoch (Web-Root: public_html_backup_wordpress):
  1. Aktuelle Aktionen/aktionen.json            (neue Aktion September, expires 29.09.)
  2. Aktuelle Aktionen/Workshops September 2026 1080_1080 Gültig bis 29092026.jpg
  3. social/2026-09/*.jpg                       (Sujets als oeffentliche URLs fuer Metricool)

Zugangsdaten: .env eine Ebene ueber prototype/ (HETZNER_USER, HETZNER_PASSWORD).
Rollback: vorherige aktionen.json liegt in Git (Commit 45d1b27) — Datei auschecken
und dieses Skript erneut laufen lassen (laedt dann den alten Stand hoch).

Nutzung:  python deploy_workshops_september_2026.py
"""
from ftplib import FTP_TLS
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROTO = SCRIPT_DIR.parent
ENV_FILE = PROTO.parent / ".env"
HOST = "www193.your-server.de"
WEBROOT = "public_html_backup_wordpress"

env = {}
for line in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

ftp = FTP_TLS(HOST, timeout=60)
ftp.login(env["HETZNER_USER"], env["HETZNER_PASSWORD"])
ftp.prot_p()
ftp.cwd(WEBROOT)

def ensure_dir(name):
    try:
        ftp.mkd(name)
    except Exception:
        pass

def upload(local: Path, remote_name: str):
    with open(local, "rb") as f:
        ftp.storbinary("STOR " + remote_name, f)
    print("  hochgeladen:", remote_name)

# 1+2) Aktion
ftp.cwd("Aktuelle Aktionen")
upload(PROTO / "Aktuelle Aktionen" / "aktionen.json", "aktionen.json")
JPG = "Workshops September 2026 1080_1080 Gültig bis 29092026.jpg"
upload(PROTO / "Aktuelle Aktionen" / JPG, JPG)
ftp.cwd("..")

# 3) Social-Bilder
ensure_dir("social")
ftp.cwd("social")
ensure_dir("2026-09")
ftp.cwd("2026-09")
for p in sorted((PROTO / "social" / "2026-09").glob("*.jpg")):
    upload(p, p.name)

ftp.quit()
print("\nFERTIG. Kontrolle: https://gemma-golfn.at (Aktion 'Workshops September 2026')")
print("Social-URLs: https://gemma-golfn.at/social/2026-09/<dateiname>.jpg")
