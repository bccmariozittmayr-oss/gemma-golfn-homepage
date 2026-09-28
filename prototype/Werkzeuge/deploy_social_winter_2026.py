"""Laedt die Winter-Aktionen 2026/27 (Videos + Sujets) als oeffentliche Medienquelle fuer Metricool/Meta/WhatsApp hoch.

Ziel (Web-Root public_html_backup_wordpress): social/2026-10-winter/  -> https://gemma-golfn.at/social/2026-10-winter/<name>
Quelle: Ablage BCC-Zentrale/01_Kunden/gemma-golfn/marketing/Aktuelle Aktionen/Oktober 2026/ (fertige Werbemittel)
        + Kachel-Sujets 1080x1080 aus prototype/Aktuelle Aktionen/ (Winter-Aktionen).
Dateinamen werden URL-sicher umbenannt (keine Leerzeichen/Umlaute). Der Ordner ist nirgends verlinkt;
die Homepage selbst wird NICHT veraendert.

Zugangsdaten: .env eine Ebene ueber prototype/ (HETZNER_USER, HETZNER_PASSWORD) - werden nie ausgegeben.
Rollback: Ordner social/2026-10-winter/ per FTP loeschen.
Nutzung:  python deploy_social_winter_2026.py [--echt] [--neu]   (ohne --echt nur Liste; --neu ueberschreibt)
"""
import re
import sys
from ftplib import FTP_TLS
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROTO = SCRIPT_DIR.parent
ENV_FILE = PROTO.parent / ".env"
HOST = "www193.your-server.de"
WEBROOT = "public_html_backup_wordpress"
ABLAGE = PROTO.parent.parent.parent / "marketing" / "Aktuelle Aktionen" / "Oktober 2026"
KACHELN = PROTO / "Aktuelle Aktionen"
ZIEL = "2026-10-winter"
echt = "--echt" in sys.argv

VIDEOS = [
    ("01 Super Sale", "supersale-b-ohne-prozent-1080x1920-stimme.mp4"),
    ("01 Super Sale", "supersale-a-mit-prozent-1080x1920-stimme.mp4"),
    ("01 Super Sale", "supersale-b-ohne-prozent-1920x1080-stimme.mp4"),
    ("02 FLOH-MARKT Schlaeger", "spike-flohmarkt-vorstellung-1080x1920-erzaehler.mp4"),
    ("02 FLOH-MARKT Schlaeger", "spike-flohmarkt-vorstellung-1920x1080-erzaehler.mp4"),
    ("03 Stundenflat Winter", "stundenflat-rechnung-1080x1920-stimme.mp4"),
    ("04 Touchkey Aufladebonus", "touchkey-staffel-1080x1920-stimme.mp4"),
    ("05 Griffwechsel", "griffwechsel-stunde-1080x1920-stimme.mp4"),
    ("05 Griffwechsel", "griffwechsel-sujet-1080x1350.jpg"),
    ("05 Griffwechsel", "griffwechsel-sujet-1080x1920.jpg"),
    ("07 Winterleague", "winterleague-video-9x16-stimme.mp4"),
    ("08 BAR71 Air Fryzza", "air-fryzza-anleitung-1080x1920.mp4"),
]
KACHEL_MUSTER = ["Super Sale 2026*", "Schlaeger-Flohmarkt Oktober 2026 v2*", "Stundenflat Winter 2026-27*",
                 "Winterleague 2026-27 v2*", "Touchkey Aufladebonus 2026-27*", "Griffwechsel 2026-27*"]


def slug(name):
    s = name.lower().replace("ü", "ue").replace("ä", "ae").replace("ö", "oe").replace("ß", "ss")
    s = re.sub(r"[^a-z0-9.\-]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


namen = []
for ordner, datei in VIDEOS:
    p = ABLAGE / ordner / datei
    if not p.exists():
        raise SystemExit(f"Fehlt: {p}")
    namen.append((p, datei))
for m in KACHEL_MUSTER:
    for p in sorted(KACHELN.glob(m + ".jpg")):
        namen.append((p, "kachel-" + slug(p.name)))

for p, name in namen:
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
        ftp.storbinary(f"STOR {name}", f)
    print("  hochgeladen:", name)
ftp.quit()
print(f"\nFertig: https://gemma-golfn.at/social/{ZIEL}/")
