# KOMPASS — Gemma Golfn Homepage

## Wo stehen wir

Website gemma-golfn.at (Golfschule, Toptracer, Pro Shop, BAR71, Golfpark
Metzenhof). Die neue Seite ist ein statischer Eigenbau im Unterordner
`prototype/` und **LIVE**; die alte WordPress-Seite liegt nur noch als Sicherung
bei. Zuletzt inhaltlich aktiv am 24.08.2026: September-Sujets ausgerollt,
Flyer-Werkzeug auf Originalfoto und Originallogo umgestellt.
**Struktur seit 30.08.2026 auf Hausstandard:** Das Git-Repo liegt auf
Projektordner-Ebene, die Website im Unterordner `prototype/`. `prototype/`
darf nicht aufgeloest werden — die Deploy-Skripte haengen an der
Verzeichnistiefe.

## Welche Datei kann was

| Datei / Ordner | Inhalt |
|---|---|
| `prototype/` | die aktuelle Website — hier wird gearbeitet (kein eigenes Repo mehr) |
| `prototype/index.html` | Startseite |
| `prototype/impressum.html`, `datenschutz.html`, `agb.html`, `barrierefreiheit.html` | Rechtstexte |
| `prototype/range-ordnung.html` | Platz-/Range-Ordnung |
| `prototype/Werkzeuge/` | Python-Skripte fuer Aktionsgrafiken und Workshop-Flyer, plus Deploy |
| `prototype/Werkzeuge/workshop_*.json` | Textdaten der jeweiligen Workshop-Aktion |
| `prototype/Aktuelle Aktionen/`, `social/` | ausgespielte Grafiken |
| `prototype/Shop Fotos/`, `Sponsoren/`, `*.jpg`, `*.mp4` | Bild- und Videomaterial |
| `referenz-alte-seite.md` | Inhalte der alten Seite (Navigation, Kontakt, Oeffnungszeiten) |
| `CLAUDE.md` | Regeln fuer dieses Projekt, vor allem zum Ausrollen |
| `AGENTS.md` | Dasselbe fuer Codex (liest, aendert nie) |
| `STATUS.md` | Aktueller Stand und offene Punkte |
| `CHANGELOG.md` | Was fachlich wann passiert ist |
| `backup-alte-homepage/` | Sicherung der alten WordPress-Seite — **nicht im Git** |
| `backup_*.txt` | Einzelseiten-Sicherungen — **nicht im Git** |
| `Gemma Golfn BAR71 … Logos und Schriftarten` | CI-Material — **nicht im Git** |

## Wo schlage ich was nach

- Aktueller Seitenstand und was zuletzt geaendert wurde → `git log` in `prototype/`
- Wie ein Workshop-Flyer erzeugt und ausgerollt wird → `prototype/Werkzeuge/`
- Texte und Termine einer Aktion → `prototype/Werkzeuge/workshop_*.json`
- Kontaktdaten, Oeffnungszeiten, alte Seitenstruktur → `referenz-alte-seite.md`
- Alter WordPress-Inhalt einer Seite → `backup-alte-homepage/`
- Logos und Schriften → CI-Ordner im Projekt bzw. `../../ci-branding/`

## Ausrollen (LIVE-Seite)

Per FTPS-Skript `prototype/Werkzeuge/deploy_workshops_september_2026.py` auf
den Hetzner-Server. **Kein automatisches Deployment** — ein Push auf GitHub
aendert an der Live-Seite nichts. Jeder Ausrollvorgang braucht eine eigene
Freigabe von Mario.

## Sicherung

Git-Repo auf **Projektordner-Ebene**, Remote `origin` →
`bccmariozittmayr-oss/gemma-golfn-homepage` (Branch `master`).
CI-Material, alte WordPress-Sicherung, Videos und generierte Bilder liegen in
**keinem** Repo, sondern auf der Platte und in
`13 Claude Sicherung/Claude Code/gemma-golfn/` (Stand 30.08.2026).

**Es gibt ZWEI `.env`-Dateien** (frueher stand hier faelschlich, es gebe keine):
`.env` im Projektordner (Hetzner-FTPS fuers Ausrollen) und
`prototype/Werkzeuge/.env` (Gemini-API). Beide doppelt ueber `.gitignore`
ausgeschlossen. Inhalte nie anzeigen, nie ins Git, nie nach OneDrive.
