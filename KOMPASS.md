# KOMPASS — Gemma Golfn Homepage

## Wo stehen wir

Website gemma-golfn.at (Golfschule, Toptracer, Pro Shop, BAR71, Golfpark
Metzenhof). Die neue Seite ist ein statischer Eigenbau im Unterordner
`prototype/` und **LIVE**; die alte WordPress-Seite liegt nur noch als Sicherung
bei. Zuletzt aktiv im August 2026: Aktionsgrafiken und Workshop-Flyer
(September-Sujets ausgerollt, Flyer-Werkzeug auf Originalfoto und Originallogo
umgestellt). Kein STATUS.md und kein CHANGELOG — der Stand steht nur in der
Git-Historie von `prototype/`.
**Wichtig:** Nur `prototype/` ist ein eigenes Repo, der uebergeordnete Ordner nicht.

## Welche Datei kann was

| Datei / Ordner | Inhalt |
|---|---|
| `prototype/` | die aktuelle Website — eigenes Git-Repo, hier wird gearbeitet |
| `prototype/index.html` | Startseite |
| `prototype/impressum.html`, `datenschutz.html`, `agb.html`, `barrierefreiheit.html` | Rechtstexte |
| `prototype/range-ordnung.html` | Platz-/Range-Ordnung |
| `prototype/Werkzeuge/` | Python-Skripte fuer Aktionsgrafiken und Workshop-Flyer, plus Deploy |
| `prototype/Werkzeuge/workshop_*.json` | Textdaten der jeweiligen Workshop-Aktion |
| `prototype/Aktuelle Aktionen/`, `social/` | ausgespielte Grafiken |
| `prototype/Shop Fotos/`, `Sponsoren/`, `*.jpg`, `*.mp4` | Bild- und Videomaterial |
| `referenz-alte-seite.md` | Inhalte der alten Seite (Navigation, Kontakt, Oeffnungszeiten) |
| `backup-alte-homepage/` | vollstaendige Sicherung der alten WordPress-Seite |
| `backup_*.txt` | Einzelseiten-Sicherungen (Impressum, Ueber uns) |
| `Gemma Golfn BAR71 … Logos und Schriftarten` | CI-Material |

## Wo schlage ich was nach

- Aktueller Seitenstand und was zuletzt geaendert wurde → `git log` in `prototype/`
- Wie ein Workshop-Flyer erzeugt und ausgerollt wird → `prototype/Werkzeuge/`
- Texte und Termine einer Aktion → `prototype/Werkzeuge/workshop_*.json`
- Kontaktdaten, Oeffnungszeiten, alte Seitenstruktur → `referenz-alte-seite.md`
- Alter WordPress-Inhalt einer Seite → `backup-alte-homepage/`
- Logos und Schriften → CI-Ordner im Projekt bzw. `../../ci-branding/`

## Sicherung

Das Git-Repo liegt **eine Ebene tiefer** in `prototype/`, Remote `origin` →
`bccmariozittmayr-oss/gemma-golfn-homepage`. Alles ausserhalb von `prototype/`
(Sicherungen der alten Seite, CI-Material) haengt am BCC-Zentrale-Repo bzw.
gehoert bei grossen Dateien auf OneDrive. Keine `.env` im Projekt.
