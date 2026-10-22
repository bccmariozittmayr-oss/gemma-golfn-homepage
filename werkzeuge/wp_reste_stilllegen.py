"""Legt die alten WordPress-Reste im Gemma-Webspace still, ohne die Homepage zu beschaedigen.

Anlass (Pruefung PHP-Luecken 22.10.2026): Im aktiven Web-Root liegen noch wp-admin, wp-includes und
Plugins/Themes der alten WordPress-Seite; PHP fuehrt sie aus (wp-content/index.php -> 200).
Freigabe Mario 22.10.2026: „bitte alles erledigen aber es darf die websiten nicht zerstört werden“.

WICHTIG: Die statische Homepage laedt Bilder aus wp-content/uploads (Favicon, Galerie, Callaway).
uploads bleibt deshalb UNANGETASTET.

Was --echt tut (nichts wird geloescht):
  1. verschiebt wp-admin, wp-includes, alle wp-content-Unterordner AUSSER uploads und die WordPress-
     PHP-Dateien im Web-Root (wp-*.php, xmlrpc.php) in den Nachbarordner _wp_reste_ausser_betrieb_2026-10-22
     (liegt neben dem Web-Root, ist von aussen nicht erreichbar)
  2. legt in wp-content/uploads eine .htaccess an, die dort das Ausfuehren von Skripten sperrt
     (nur wenn dort noch keine .htaccess liegt; Bilder bleiben normal abrufbar)
  3. schreibt ein Protokoll (wp_reste_stilllegen_protokoll.json) fuer den Rueckweg

Aufrufe:
  python wp_reste_stilllegen.py            Probelauf: Bestand + Plan, aendert nichts
  python wp_reste_stilllegen.py --echt     ausfuehren
  python wp_reste_stilllegen.py --zurueck  alles laut Protokoll zurueckverschieben, eigene .htaccess entfernen

Zugangsdaten: .env dieses Projekts (HETZNER_USER, HETZNER_PASSWORD) - werden nie ausgegeben.
"""
import io
import json
import sys
from datetime import datetime
from ftplib import FTP_TLS, error_perm
from pathlib import Path

HIER = Path(__file__).resolve().parent
ENV_FILE = HIER.parent / ".env"
PROTOKOLL = HIER / "wp_reste_stilllegen_protokoll.json"
HOST = "www193.your-server.de"
WEBROOT = "public_html_backup_wordpress"
QUARANTAENE = "_wp_reste_ausser_betrieb_2026-10-22"
SKRIPT_ENDUNGEN = (".php", ".phtml", ".php3", ".php4", ".php5", ".php7", ".phar", ".pl", ".py", ".cgi", ".sh")
HTACCESS = (
    "# Gemma 22.10.2026: im Bilderordner werden keine Skripte ausgefuehrt (Bilder bleiben abrufbar)\n"
    '<FilesMatch "\\.(php[0-9]?|phtml|phar|pl|py|cgi|sh)$">\n'
    "  Require all denied\n"
    "</FilesMatch>\n"
).encode("utf-8")

modus = "zurueck" if "--zurueck" in sys.argv else ("echt" if "--echt" in sys.argv else "probe")

env = {}
for line in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

ftp = FTP_TLS(HOST, timeout=120)
ftp.login(env["HETZNER_USER"], env["HETZNER_PASSWORD"])
ftp.prot_p()
START = ftp.pwd()


def liste(pfad):
    try:
        return [(n, f) for n, f in ftp.mlsd(pfad, facts=["type", "size", "modify"]) if n not in (".", "..")]
    except error_perm:
        return None


def skripte_unter(pfad, tiefe=0):
    """Alle Skriptdateien unterhalb von pfad (fuer den Bericht)."""
    funde = []
    if tiefe > 12:
        return funde
    for n, f in liste(pfad) or []:
        p = f"{pfad}/{n}"
        if f.get("type") == "dir":
            funde += skripte_unter(p, tiefe + 1)
        elif n.lower().endswith(SKRIPT_ENDUNGEN):
            funde.append((p, f.get("modify", "")[:8]))
    return funde


def mkdir_p(pfad):
    ftp.cwd(START)
    for teil in pfad.split("/"):
        try:
            ftp.mkd(teil)
        except error_perm:
            pass
        ftp.cwd(teil)
    ftp.cwd(START)


if modus == "zurueck":
    eintraege = json.loads(PROTOKOLL.read_text(encoding="utf-8"))
    for e in reversed(eintraege["verschoben"]):
        ftp.rename(e["nach"], e["von"])
        print("  zurueck:", e["von"])
    if eintraege.get("htaccess_angelegt"):
        ftp.delete(f"{WEBROOT}/wp-content/uploads/.htaccess")
        print("  entfernt: wp-content/uploads/.htaccess")
    ftp.quit()
    print("FERTIG (Rueckweg)")
    sys.exit(0)

root = liste(WEBROOT)
if root is None:
    raise SystemExit(f"Web-Root {WEBROOT} nicht lesbar - Abbruch")
if liste(QUARANTAENE) is not None and modus == "echt":
    raise SystemExit(f"{QUARANTAENE} existiert schon - wurde schon ausgefuehrt? Abbruch, nichts geaendert.")

plan = []  # (von, nach)
for n, f in root:
    if f.get("type") == "dir" and n in ("wp-admin", "wp-includes"):
        plan.append((f"{WEBROOT}/{n}", f"{QUARANTAENE}/{n}"))
    elif f.get("type") == "file" and n.lower().endswith(".php") and (n.startswith("wp-") or n == "xmlrpc.php"):
        plan.append((f"{WEBROOT}/{n}", f"{QUARANTAENE}/root/{n}"))
wpc = liste(f"{WEBROOT}/wp-content") or []
for n, f in wpc:
    if n == "uploads":
        continue
    if n == ".htaccess":
        continue
    plan.append((f"{WEBROOT}/wp-content/{n}", f"{QUARANTAENE}/wp-content/{n}"))

print(f"Web-Root: {WEBROOT}  |  Modus: {modus}\n")
print("1) Andere Skriptdateien direkt im Web-Root (werden NICHT verschoben, nur gemeldet):")
andere = [n for n, f in root if f.get("type") == "file" and n.lower().endswith(SKRIPT_ENDUNGEN)
          and not (n.startswith("wp-") or n == "xmlrpc.php")]
print("   " + (", ".join(andere) if andere else "keine"))

print("\n2) Wird aus dem Web-Root genommen (verschieben, nicht loeschen):")
for von, nach in plan:
    print(f"   {von}  ->  {nach}")
if not plan:
    print("   nichts")

print("\n3) Inhalt wp-content (bleibt): uploads" if any(n == "uploads" for n, _ in wpc) else "\n3) KEIN uploads-Ordner gefunden!")
up_skripte = skripte_unter(f"{WEBROOT}/wp-content/uploads")
print(f"   Skriptdateien in uploads: {len(up_skripte)}" + (" (VERDAECHTIG, bitte ansehen):" if up_skripte else ""))
for p, d in up_skripte[:50]:
    print(f"     {p}  ({d})")
up_htaccess = any(n == ".htaccess" for n, _ in (liste(f"{WEBROOT}/wp-content/uploads") or []))
print(f"   .htaccess in uploads vorhanden: {'ja (wird nicht angefasst)' if up_htaccess else 'nein (wird angelegt)'}")

print("\n4) Plugins/Themes, die stillgelegt werden:")
for teil in ("plugins", "themes"):
    namen = [n for n, f in (liste(f"{WEBROOT}/wp-content/{teil}") or []) if f.get("type") == "dir"]
    print(f"   {teil}: {', '.join(namen) if namen else '-'}")

if modus == "probe":
    ftp.quit()
    print("\nPROBELAUF - nichts geaendert. Ausfuehren mit --echt")
    sys.exit(0)

protokoll = {"zeit": datetime.now().isoformat(timespec="seconds"), "verschoben": [], "htaccess_angelegt": False}
mkdir_p(f"{QUARANTAENE}/root")
mkdir_p(f"{QUARANTAENE}/wp-content")
for von, nach in plan:
    ftp.rename(von, nach)
    protokoll["verschoben"].append({"von": von, "nach": nach})
    PROTOKOLL.write_text(json.dumps(protokoll, indent=2, ensure_ascii=False), encoding="utf-8")
    print("  verschoben:", von)
if not up_htaccess and any(n == "uploads" for n, _ in wpc):
    ftp.storbinary(f"STOR {WEBROOT}/wp-content/uploads/.htaccess", io.BytesIO(HTACCESS))
    protokoll["htaccess_angelegt"] = True
    print("  angelegt: wp-content/uploads/.htaccess")
PROTOKOLL.write_text(json.dumps(protokoll, indent=2, ensure_ascii=False), encoding="utf-8")
ftp.quit()
print(f"\nFERTIG. Protokoll: {PROTOKOLL}\nRueckweg: python wp_reste_stilllegen.py --zurueck")
