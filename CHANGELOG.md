# CHANGELOG — Gemma Golfn Homepage

Neueste Einträge oben. Details stehen in der Git-Historie (`git log`);
hier steht nur, was fachlich wichtig war.

## 2026-09-28 — Team-Bereich mit neuen Fotos (Zweig `team-fotos-2026-09`, noch nicht live)

- Alle Mitarbeiterfotos gegen die neuen Aufnahmen getauscht. Bilder liegen
  jetzt lokal in `prototype/team/` statt auf den alten WordPress-Uploads.
  Einheitlich 4:5, 360×450 px (doppelte Anzeigegröße für scharfe Displays),
  je ca. 20 KB, ohne Metadaten. Auch die zwei Bilder bei „Unsere
  Professionals" (Golfschule) nutzen jetzt die neuen Fotos.
- Gruppenfoto neu über den Einzelkarten (1600 px und 800 px fürs Handy).
- Melanie Leitner entfernt, Hermann Rohm aufgenommen (Titel vorläufig
  „Allround-Pro").
- Maskottchen Spike (Flos Hund) als eigene Karte, lokal freigestellt (rembg,
  kein Cloud-Dienst, nichts dazuerfunden).
- Handy-Ansicht der Teamkarten: Name und Funktion stehen jetzt untereinander
  statt in zwei schmalen Spalten nebeneinander.

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
