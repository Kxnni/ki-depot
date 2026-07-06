# KI-Depot – Paper Trading Dashboard

Fiktives 10.000-€-Depot, täglich von KI bewertet, Ziel: den S&P 500 schlagen. Kein echtes Geld, keine Anlageberatung.

## Wie es funktioniert

- **`index.html`** – Dashboard (GitHub Pages), von jedem Gerät im Browser abrufbar
- **`data.json`** – kompletter Depotzustand (Positionen, Orders, Trades, Historie)
- **`scripts/update.py`** – holt börsentäglich Kurse, führt offene Orders aus, schreibt die Historie
- **`.github/workflows/update.yml`** – lässt das Skript automatisch in der GitHub-Cloud laufen (Mac kann aus sein)
- **KI-Entscheidungen** – laufen als täglicher Cowork-Task auf dem Mac (verpasste Tage werden beim nächsten App-Start nachgeholt) und werden als Orders in `data.json` + Eintrag in `ENTSCHEIDUNGEN.md` gepusht



<<<<<<< Updated upstream
=======
## Danach läuft automatisch

- **Börsentäglich 17:00 (MESZ):** GitHub Actions aktualisiert Kurse, Depotwert und Benchmark und führt offene Orders aus – auch wenn der Mac aus ist.
- **Werktäglich 22:15 (wenn Mac an, sonst nachgeholt):** Claude bewertet das Depot, entscheidet über Käufe/Verkäufe und pusht Orders + Begründung. Ausführung am Folgetag um 17:00.
- **Beim Öffnen des Dashboards:** Live-Kurse der Positionen via Finnhub (kostenloser API-Key in `index.html`).
>>>>>>> Stashed changes
