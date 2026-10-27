"""Laedt EINE Datei aus prototype/ an dieselbe Stelle nach gemma-golfn.at (FTPS, Web-Root public_html_backup_wordpress).
Nutzung:  python deploy_datei.py "Sponsoren/handycheck-page.html"          (Probelauf, aendert nichts)
          python deploy_datei.py "Sponsoren/handycheck-page.html" --echt
Vor dem Upload: Live-Stand pruefen (z.B. mit Git vergleichen). Rollback: alte Fassung aus Git auschecken, erneut hochladen.
Zugangsdaten aus ../../.env (HETZNER_USER/HETZNER_PASSWORD), werden nie ausgegeben."""
import sys
from ftplib import FTP_TLS
from pathlib import PurePosixPath, Path

PROTO = Path(__file__).resolve().parent.parent
ENV_FILE = PROTO.parent / ".env"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) != 1:
    sys.exit(__doc__)
rel = PurePosixPath(args[0].replace("\\", "/"))
if rel.is_absolute() or ".." in rel.parts:
    sys.exit("Nur Pfade innerhalb von prototype/ erlaubt.")
quelle = PROTO / Path(*rel.parts)
if not quelle.is_file():
    sys.exit(f"Datei fehlt: {quelle}")
if "--echt" not in sys.argv:
    print(f"[Probelauf] wuerde {rel} ({quelle.stat().st_size} Bytes) hochladen. Mit --echt ausfuehren."); sys.exit(0)
env = {}
for line in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1); env[k.strip()] = v.strip()
ftp = FTP_TLS("www193.your-server.de", timeout=60)
ftp.login(env["HETZNER_USER"], env["HETZNER_PASSWORD"]); ftp.prot_p(); ftp.cwd("public_html_backup_wordpress")
for teil in rel.parts[:-1]:
    ftp.cwd(teil)
with open(quelle, "rb") as f:
    ftp.storbinary(f"STOR {rel.name}", f)
ftp.quit(); print(f"hochgeladen: {rel}")
