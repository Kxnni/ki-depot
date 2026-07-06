#!/usr/bin/env python3
"""Tägliches Depot-Update: Kurse holen, offene Orders ausführen, Historie fortschreiben.

Läuft in GitHub Actions (börsentäglich nach US-Schluss). Nutzt nur die Python-Standardbibliothek.
"""
import datetime
import json
import os
import urllib.parse
import urllib.request

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data.json")
UA = {"User-Agent": "Mozilla/5.0 (compatible; DepotBot/1.0)"}


def fetch_price(symbol: str) -> float:
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        + urllib.parse.quote(symbol, safe="")
        + "?interval=1d&range=5d"
    )
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    return float(d["chart"]["result"][0]["meta"]["regularMarketPrice"])


def main() -> None:
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)

    today = datetime.date.today().isoformat()
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    eurusd = fetch_price("EURUSD=X")  # USD je 1 EUR
    bench = fetch_price(data["config"]["benchmark"])

    symbols = {p["symbol"] for p in data["positions"]} | {o["symbol"] for o in data["orders"]}
    quotes = {}
    for s in sorted(symbols):
        try:
            quotes[s] = fetch_price(s)
        except Exception as e:  # Kurs nicht verfügbar -> Order bleibt offen
            print(f"WARNUNG: Kurs für {s} nicht abrufbar: {e}")

    # --- Offene Orders ausführen ---
    remaining = []
    for o in data["orders"]:
        px = quotes.get(o["symbol"])
        if px is None:
            remaining.append(o)
            continue
        pos = next((p for p in data["positions"] if p["symbol"] == o["symbol"]), None)

        if o["type"] == "buy":
            amount = round(min(o["amountEur"], data["cash"]), 2)
            if amount <= 0:
                print(f"Order {o['symbol']} übersprungen: kein Cash.")
                continue
            shares = round(amount * eurusd / px, 4)
            data["cash"] = round(data["cash"] - amount, 2)
            if pos:
                pos["shares"] = round(pos["shares"] + shares, 4)
                pos["investedEur"] = round(pos["investedEur"] + amount, 2)
            else:
                data["positions"].append({
                    "symbol": o["symbol"],
                    "name": o.get("name", o["symbol"]),
                    "shares": shares,
                    "investedEur": amount,
                    "entryDate": today,
                    "reason": o.get("reason", ""),
                })
            data["trades"].append({
                "date": today, "type": "buy", "symbol": o["symbol"],
                "name": o.get("name", o["symbol"]), "shares": shares,
                "priceUsd": px, "amountEur": amount, "reason": o.get("reason", ""),
            })

        elif o["type"] == "sell":
            if not pos:
                print(f"Verkaufsorder {o['symbol']} übersprungen: keine Position.")
                continue
            shares = pos["shares"] if o.get("all") else min(float(o.get("shares", 0)), pos["shares"])
            if shares <= 0:
                continue
            proceeds = round(shares * px / eurusd, 2)
            frac = shares / pos["shares"]
            cost = round(pos["investedEur"] * frac, 2)
            data["cash"] = round(data["cash"] + proceeds, 2)
            pos["shares"] = round(pos["shares"] - shares, 4)
            pos["investedEur"] = round(pos["investedEur"] - cost, 2)
            if pos["shares"] <= 0.0001:
                data["positions"].remove(pos)
            data["trades"].append({
                "date": today, "type": "sell", "symbol": o["symbol"],
                "name": o.get("name", o["symbol"]), "shares": shares,
                "priceUsd": px, "amountEur": proceeds,
                "realizedPnlEur": round(proceeds - cost, 2),
                "reason": o.get("reason", ""),
            })
    data["orders"] = remaining

    # --- Benchmark beim ersten Lauf verankern ---
    if not data["config"].get("started"):
        data["config"]["started"] = today
        data["config"]["benchmarkStart"] = bench

    # --- Bewertung ---
    value = data["cash"]
    for p in data["positions"]:
        px = quotes.get(p["symbol"])
        if px is not None:
            p["lastPriceUsd"] = px
            p["valueEur"] = round(p["shares"] * px / eurusd, 2)
        value += p.get("valueEur", p["investedEur"])
    value = round(value, 2)

    bench_value = round(
        data["config"]["startCapital"] * bench / data["config"]["benchmarkStart"], 2
    )

    data["quotes"] = {s: {"usd": q, "eur": round(q / eurusd, 2)} for s, q in quotes.items()}
    data["fx"] = {"EURUSD": eurusd}
    data["lastUpdate"] = now

    entry = {"date": today, "depot": value, "benchmark": bench_value, "spx": bench}
    data["history"] = [h for h in data["history"] if h["date"] != today] + [entry]

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"OK {today}: Depot {value} € | {data['config']['benchmarkName']} {bench_value} € | Cash {data['cash']} €")


if __name__ == "__main__":
    main()
