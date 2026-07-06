# KI-Depot – Paper Trading Dashboard

Fiktives 10.000-€-Depot, täglich von KI bewertet, Ziel: den S&P 500 schlagen. Kein echtes Geld, keine Anlageberatung.

## Wie es funktioniert

- **`index.html`** – Dashboard (GitHub Pages), von jedem Gerät im Browser abrufbar
- **`data.json`** – kompletter Depotzustand (Positionen, Orders, Trades, Historie)
- **`scripts/update.py`** – holt börsentäglich Kurse, führt offene Orders aus, schreibt die Historie
- **`.github/workflows/update.yml`** – lässt das Skript automatisch in der GitHub-Cloud laufen (Mac kann aus sein)
- **KI-Entscheidungen** – laufen als täglicher Cowork-Task auf dem Mac (verpasste Tage werden beim nächsten App-Start nachgeholt) und werden als Orders in `data.json` + Eintrag in `ENTSCHEIDUNGEN.md` gepusht

## Einmalige Einrichtung (ca. 10 Minuten)

1. **GitHub-Konto** anlegen auf [github.com](https://github.com) (kostenlos), falls noch keines vorhanden.
2. **Neues Repository** erstellen: Name z. B. `ki-depot`, Sichtbarkeit **Public** (nötig für kostenloses Pages).
3. **Dateien hochladen:** Im Repo „uploading an existing file" wählen und den kompletten Inhalt dieses Ordners hochladen (inkl. der Ordner `scripts` und `.github` – am einfachsten per Drag & Drop des Ordnerinhalts). Alternativ übernimmt Claude das per Git, sobald das Repo existiert.
4. **Actions-Schreibrechte:** Repo → Settings → Actions → General → „Workflow permissions" → **Read and write permissions** → Save.
5. **Ersten Lauf starten:** Repo → Actions → „Tägliches Depot-Update" → „Run workflow". Damit werden die Startkäufe zu echten Kursen ausgeführt.
6. **GitHub Pages aktivieren:** Repo → Settings → Pages → Source: „Deploy from a branch" → Branch `main`, Ordner `/ (root)` → Save.
7. Nach 1–2 Minuten ist das Dashboard erreichbar unter:
   `https://DEIN-BENUTZERNAME.github.io/ki-depot/`
   → Diese URL auf dem Handy als Lesezeichen/Homescreen-Icon speichern.

## Danach läuft automatisch

- **Börsentäglich 22:45 (MESZ):** GitHub Actions aktualisiert Kurse, Depotwert und Benchmark – auch wenn der Mac aus ist.
- **Täglich 22:15 (wenn Mac an, sonst nachgeholt):** Claude bewertet das Depot, entscheidet über Käufe/Verkäufe und pusht Orders + Begründung.
