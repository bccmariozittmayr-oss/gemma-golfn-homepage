# STATUS — Gemma Golfn Homepage

**Letzte Aktualisierung:** 28.09.2026

## Aktueller Stand

Website **LIVE** unter gemma-golfn.at. Statischer Eigenbau in `prototype/`.
Zuletzt inhaltlich gearbeitet wurde am **24.08.2026**: Workshop-Sujets
September ausgerollt, Flyer-Werkzeug v2 (Originalfoto + Originallogo),
Cache-Buster für Aktionsbilder.

Am **30.08.2026** wurde die Projektstruktur auf den Hausstandard gebracht:
Das Git-Repo liegt jetzt auf Projektordner-Ebene statt in `prototype/`.
Es wurde ausschliesslich der `.git`-Ordner verschoben — keine Website-Datei
wurde angefasst, der Ausrollweg ist unverändert.

## Offene Punkte

- [ ] **Winter-Aktionen 2026/27 eingeplant, NICHT ausgerollt** (Zweig `winter-aktionen-2026`, 28.09.2026):
      7 neue Kacheln in `aktionen.json` mit `start`/`expires` (Super Sale B 01.–13.10., A 14.10.–10.11.,
      Stundenflat 02.10.–31.01., FLO(H)MARKT 12.–26.10., Winterleague bis 13.11., Touchkey 01.11.–28.02.,
      Griffwechsel 15.10.–28.02.; Gültigkeiten von Mario bestätigt). Bilder aus
      `marketing/winter-aktionen-2026/bau/build_homepage_kacheln.py`. Ausrollen mit
      `deploy_aktionen.py --echt` **erst nach Freigabe Mario**, spätestens 30.09. (Super Sale ab 01.10.).

- [x] **Team-Fotos LIVE seit 28.09.2026** (Go Mario): `index.html` + `team/` (10 Dateien),
      Hermann „Allround-Pro", Spike „Maskottchen & Caddie auf vier Pfoten". Melanie Leitner
      entfernt, ihre 20 Bildgrößen in `wp-content/uploads/2021/03/` gelöscht (Original lokal
      unter `marketing/fotos/Mitarbeiter Fotos/ehemalig/`). Live-Seite davor als Sicherung
      heruntergeladen (identisch mit Git `hotshots-winter-2026:prototype/index.html` = Rückweg).
- [ ] **Zweige zusammenführen:** `hotshots-winter-2026` und darauf `team-fotos-2026-09` sind
      live, aber noch nicht in `master`. Wartet auf Freigabe Mario.

- [ ] **Abgleich Repo gegen Live-Server.** Weil einzelne Dateien manuell per
      FTPS hochgeladen werden, kann der Server vom Repo abweichen. Vor der
      nächsten grösseren Änderung einmal gegenprüfen. Bisher nie gemacht.
- [ ] **Zugangsdaten in RoboForm sichern.** Die Hetzner-FTPS-Daten stehen
      aktuell nur in der lokalen `.env` auf einer einzigen Festplatte
      (Stand Mario 30.08.2026: Sammlung noch nicht vollständig).
- [ ] **Entscheidung offen:** `prototype/` in `site/` umbenennen? Passt besser
      zum Hausstandard, ist technisch unkritisch (Verzeichnistiefe bleibt
      gleich), aber ein eigener Eingriff. Bewusst getrennt vom Struktur-Umbau.
- [ ] Zwei alte Feature-Zweige (`feature/wa-link-newsletter-text`,
      `feature/workshops-september-2026`) sind inhaltlich in `master`
      enthalten und können gelöscht werden. Kein Datenverlust-Risiko.

## Was NICHT ansteht

Kein Framework, kein CMS, kein Build-Schritt. Die Seite bleibt statisch.
