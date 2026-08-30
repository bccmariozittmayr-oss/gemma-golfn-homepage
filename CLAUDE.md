# Projekt: Gemma Golfn Homepage

Website **gemma-golfn.at** — Golfschule, Toptracer, Pro Shop, BAR71,
Golfpark Metzenhof. Statischer Eigenbau im Unterordner `prototype/`, **LIVE**.

## Session-Start

Sofort die letzten 5 Commits mit Zeitstempel zeigen. **Nicht** fragen „was
willst du machen" — Mario sagt von selbst, was ansteht.

## Wo was liegt

Siehe `KOMPASS.md` — eine Seite, wird zuerst gelesen.

## Diese Seite ist LIVE — Regeln fürs Ausrollen

- **Ausgerollt wird per FTPS-Skript**, nicht über Git. Ein Push auf GitHub
  ändert an der Live-Seite **nichts**. Es gibt kein automatisches Deployment.
- Das Skript: `prototype/Werkzeuge/deploy_workshops_september_2026.py`.
  Es zieht die Zugangsdaten aus der `.env` **im Projektordner** (eine Ebene
  über `prototype/`).
- **Vor jedem Ausrollen: Freigabe von Mario für genau diesen einen Vorgang.**
  Vorher sagen, welche Dateien hochgehen und wie man es rückgängig macht.
  Eine Freigabe gilt nie für den nächsten Vorgang mit.
- Nie blind überschreiben — erst den Stand am Server prüfen. Zwischen Repo und
  Server kann es auseinanderlaufen, weil einzelne Dateien manuell hochgehen.

## Struktur — nicht flach machen

Das Git-Repo liegt seit 30.08.2026 auf **Projektordner-Ebene** (Hausstandard,
wie handycheck.at und Physio). Die Website bleibt im Unterordner `prototype/`.

**Wichtig:** `prototype/` darf **nicht** aufgelöst und der Inhalt nach oben
gezogen werden. Die Deploy-Skripte finden ihre `.env` und ihre Pfade über die
Verzeichnistiefe (`parents[4]`); wird die Struktur flacher, brechen sie.
Eine reine Umbenennung `prototype/` → `site/` wäre dagegen unkritisch.

## Was nicht im Git liegt

CI-Material (Logos, Schriften, Druckvorlagen) und die alte WordPress-Sicherung
liegen **bewusst in keinem Repo** (Entscheidung Mario 30.08.2026 — grosse
Dateien gehören auf OneDrive). Sie sind gesichert unter
`13 Claude Sicherung/Claude Code/gemma-golfn/`. Ebenfalls ausgeschlossen:
Videos (`*.mp4`), generierte Hero-Bilder, `Werkzeuge/output/`.

## Zwei .env-Dateien

- `.env` im Projektordner — Hetzner-FTPS-Zugang fürs Ausrollen
- `prototype/Werkzeuge/.env` — Gemini-API für die Grafikerzeugung

Beide sind über `.gitignore` doppelt ausgeschlossen. **Inhalte nie anzeigen,
nie ins Git, nie nach OneDrive.** Vorlagen ohne Werte: `.env.example`.

## Keep it smart & simple

Statische Seite, keine Datenbank, kein Framework. So soll es bleiben — die
Seite muss auch in zwei Jahren ohne Einarbeitung änderbar sein.

## Übergeordnete Regeln

`~/.claude/CLAUDE.md` und die Kunden-`CLAUDE.md` eine Ebene höher gelten
zusätzlich und gehen im Zweifel vor.
