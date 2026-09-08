# -*- coding: utf-8 -*-
"""Laedt die Hot-Shots-Sujets 2026/27 als oeffentliche Medienquelle fuer Metricool/Meta hoch.

Ziel (Web-Root public_html_backup_wordpress): social/2026-09-hotshots/
  - 1080x1080/*.png, 1080x1920/*.png, reels/*.mp4 aus
    BCC-Zentrale/01_Kunden/gemma-golfn/marketing/Hot Shots Winter Abo 2026-27/output/
Der Ordner ist nirgends verlinkt; die Homepage-Aktion ("Das laeuft gerade") wird
davon NICHT beruehrt (dafuer: deploy_aktionen.py).

Zugangsdaten: .env eine Ebene ueber prototype/ (HETZNER_USER, HETZNER_PASSWORD).
Rollback: Dateien im Ordner social/2026-09-hotshots/ per FTP loeschen.
Nutzung:  python deploy_social_hotshots_2026.py [--echt]   (ohne --echt nur Liste)
"""
import sys
from ftplib import FTP_TLS
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROTO = SCRIPT_DIR.parent
ENV_FILE = PROTO.parent / ".env"
HOST = "www193.your-server.de"
WEBROOT = "public_html_backup_wordpress"
QUELLE = PROTO.parent.parent.parent / "marketing" / "Hot Shots Winter Abo 2026-27" / "output"
ZIEL = "2026-09-hotshots"
echt = "--echt" in sys.argv

dateien = sorted(list((QUELLE / "1080x1080").glob("*.png")) + list((QUELLE / "1080x1920").glob("*.png"))
                 + list((QUELLE / "reels").glob("*.mp4")))
namen = []
for p in dateien:
    ordner = p.parent.name
    name = p.name if ordner == "reels" else f"{p.stem}_{ordner}{p.suffix}"
    namen.append((p, name))
    print(("  " if echt else "  [trocken] ") + name, round(p.stat().st_size / 1e6, 1), "MB")

if not echt:
    print(f"\n{len(namen)} Dateien. Mit --echt hochladen nach https://gemma-golfn.at/social/{ZIEL}/")
    sys.exit(0)

env = {}
for line in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

ftp = FTP_TLS(HOST, timeout=120)
ftp.login(env["HETZNER_USER"], env["HETZNER_PASSWORD"])
ftp.prot_p()
ftp.cwd(WEBROOT)
for d in ("social", ZIEL):
    try:
        ftp.mkd(d)
    except Exception:
        pass
    ftp.cwd(d)
vorhanden = set(ftp.nlst())
for p, name in namen:
    if name in vorhanden and "--neu" not in sys.argv:
        print("  vorhanden, uebersprungen:", name)
        continue
    with open(p, "rb") as f:
        ftp.storbinary("STOR " + name, f)
    print("  hochgeladen:", name)
ftp.quit()
print(f"\nFERTIG. URLs: https://gemma-golfn.at/social/{ZIEL}/<dateiname>")
