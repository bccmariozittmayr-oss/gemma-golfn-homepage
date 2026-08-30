# CHANGELOG — Gemma Golfn Homepage

Neueste Einträge oben. Details stehen in der Git-Historie (`git log`);
hier steht nur, was fachlich wichtig war.

## 2026-08-30 — Projektstruktur auf Hausstandard gebracht

- Git-Repo von `prototype/` auf Projektordner-Ebene gezogen. Nur der
  `.git`-Ordner wurde verschoben, keine Website-Datei angefasst. Historie
  vollständig erhalten (`git log --follow` für einzelne Dateien).
- Projektordner aus dem BCC-Zentrale-Repo ausgetragen — er lag vorher in
  zwei Repos gleichzeitig, `git status` zeigte deshalb den falschen Stand.
- CI-Material (49 MB) und alte WordPress-Sicherung (58 MB) aus dem Git
  genommen. Liegen weiter auf der Platte und in der OneDrive-Sicherung.
- `CLAUDE.md`, `AGENTS.md`, `STATUS.md`, `CHANGELOG.md` erstmals angelegt —
  fehlten bisher komplett. KOMPASS korrigiert (behauptete fälschlich, es gebe
  keine `.env`; es gibt zwei).
- Vollständige OneDrive-Sicherung vor dem Umbau: 384 Dateien, 172 MB.

## 2026-08-24 — Workshops September, Flyer-Werkzeug v2

- Workshop-Sujets September 2026 ausgerollt
- Flyer-Werkzeug auf Originalfoto und Originallogo umgestellt
- Cache-Buster für Aktionsbilder (Browser zeigte bei gleichem Dateinamen
  das alte Bild)
- Deploy-Skript und Social-Bilder ergänzt

## Davor

Siehe `git log`. Die neue statische Seite löste die alte WordPress-Seite ab;
deren Sicherung liegt in `backup-alte-homepage/` (nicht mehr im Git).
