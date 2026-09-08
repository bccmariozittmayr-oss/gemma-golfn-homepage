# -*- coding: utf-8 -*-
"""Laedt index.html nach gemma-golfn.at (FTPS, Hetzner, Web-Root public_html_backup_wordpress).
Rollback: vorherige index.html aus Git auschecken und erneut ausfuehren.
Nutzung: python deploy_index.py --echt"""
import sys
from ftplib import FTP_TLS
from pathlib import Path
PROTO = Path(__file__).parent.parent
ENV_FILE = PROTO.parent / ".env"
if "--echt" not in sys.argv:
    print("[trocken] wuerde index.html hochladen. Mit --echt ausfuehren."); sys.exit(0)
env = {}
for line in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1); env[k.strip()] = v.strip()
ftp = FTP_TLS("www193.your-server.de", timeout=60)
ftp.login(env["HETZNER_USER"], env["HETZNER_PASSWORD"]); ftp.prot_p(); ftp.cwd("public_html_backup_wordpress")
with open(PROTO / "index.html", "rb") as f:
    ftp.storbinary("STOR index.html", f)
ftp.quit(); print("hochgeladen: index.html")
