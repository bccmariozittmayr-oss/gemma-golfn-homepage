# STATUS — Gemma Golfn Homepage

**Letzte Aktualisierung:** 30.08.2026

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
