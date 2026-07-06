# Strategie des KI-Depots

**Ziel:** Den S&P 500 schlagen – mit einem fiktiven Depot von 10.000 €, das täglich von einer KI neu bewertet wird. Kein echtes Geld.

## Regeln

1. **Universum:** Liquide Aktien aus USA und Europa (US-Listings/ADRs, alle Kurse in USD, Depotführung in EUR).
2. **Positionsgrößen:** Maximal 10 Positionen, maximal 20 % des Depotwerts je Position, mindestens 5 % Cash-Reserve.
3. **Bruchstücke:** Erlaubt (Paper Trading), keine Transaktionskosten (Vereinfachung – bei täglichem Handel real relevant, daher: wenige, begründete Trades).
4. **Orderausführung:** Die KI legt Orders an; ausgeführt werden sie beim nächsten automatischen Kurslauf (börsentäglich ~22:45 MESZ) zum dann aktuellen Kurs.
5. **Dokumentationspflicht:** Jede Kauf-/Verkaufsentscheidung wird mit Begründung in `data.json` (Trades) und `ENTSCHEIDUNGEN.md` festgehalten.
6. **Benchmark:** S&P 500, verankert am Indexstand des ersten Laufs. Benchmarkwert = 10.000 € × (Index heute / Index bei Start).
7. **Disziplin:** Kein Überhandeln. Trades nur bei klarer Begründung (neue Nachrichten, Bewertungsänderung, Risikomanagement) – nicht aus Langeweile. An den meisten Tagen ist „nichts tun" die richtige Entscheidung.

## Tagesablauf

- **~22:15 Uhr (Cowork-Task, holt verpasste Läufe nach):** KI prüft Marktnachrichten und Depot, entscheidet über Orders, dokumentiert die Analyse, pusht zu GitHub.
- **22:45 MESZ (GitHub Actions, läuft immer):** Skript holt Kurse, führt offene Orders aus, schreibt Depotwert und Benchmark in die Historie.

## Ausgangslage (06.07.2026)

S&P 500 bei ~7.483, +9 % YTD, bestes Quartal seit 2020. Treiber: AI-Investitionsboom. Risiko: BofA warnt vor extremer Spekulation bei hoch bewerteten Titeln (Kursziel 7.100), Goldman und Yardeni bullish (8.000–8.250). Konsequenz für das Startdepot: Fokus auf AI-*Engpässe* mit echten Gewinnen (Chips, Strom, Kühlung) statt Spekulationstitel, dazu Qualität außerhalb des AI-Themas (Visa) und 13 % Cash als Puffer.
