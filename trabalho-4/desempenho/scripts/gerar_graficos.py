#!/usr/bin/env python3
"""Gera gráficos PNG a partir dos CSV Locust do Trabalho 4."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError as exc:
    raise SystemExit("Instale matplotlib: pip install matplotlib") from exc

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "resultados"
GRAFICOS = ROOT / "graficos"


def read_aggregated(stats_path: Path) -> dict | None:
    with stats_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("Name") == "Aggregated":
                return row
    return None


def collect(manifest: Path) -> list[dict]:
    data = json.loads(manifest.read_text(encoding="utf-8"))
    rows = []
    for e in data:
        stats = read_aggregated(Path(e["stats_csv"]))
        if not stats:
            continue
        rows.append({
            "cenario": e["cenario"],
            "usuarios": int(e["usuarios"]),
            "linguagem": e.get("linguagem", ""),
            "cache": e.get("cache", ""),
            "rps": float(stats.get("Requests/s", 0) or 0),
            "avg_ms": float(stats.get("Average Response Time", 0) or 0),
            "median_ms": float(stats.get("Median Response Time", 0) or 0),
            "p95_ms": float(stats.get("95%", 0) or 0),
        })
    return rows


def plot_by_users(rows: list[dict], metric: str, ylabel: str, out: Path) -> None:
    by_cen = defaultdict(list)
    for r in rows:
        by_cen[r["cenario"]].append(r)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    for cenario, items in sorted(by_cen.items()):
        items.sort(key=lambda x: x["usuarios"])
        ax.plot(
            [i["usuarios"] for i in items],
            [i[metric] for i in items],
            marker="o",
            label=cenario,
        )
    ax.set_xlabel("Usuários virtuais (Locust)")
    ax.set_ylabel(ylabel)
    ax.set_title(f"Link Extractor — {ylabel}")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Gráfico: {out}")


def plot_cache_compare(rows: list[dict], users: int, out: Path) -> None:
    """Barras: Python/Ruby × com/sem cache para um nível de usuários."""
    subset = [r for r in rows if r["usuarios"] == users]
    labels = [r["cenario"] for r in sorted(subset, key=lambda x: x["cenario"])]
    avg = [r["avg_ms"] for r in sorted(subset, key=lambda x: x["cenario"])]
    rps = [r["rps"] for r in sorted(subset, key=lambda x: x["cenario"])]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    x = range(len(labels))
    axes[0].bar(x, avg, color=["#2a9d8f", "#e76f51", "#264653", "#f4a261"])
    axes[0].set_xticks(list(x))
    axes[0].set_xticklabels(labels, rotation=20, ha="right", fontsize=8)
    axes[0].set_ylabel("Tempo médio (ms)")
    axes[0].set_title(f"Latência média — {users} usuários")
    axes[0].grid(True, axis="y", alpha=0.3)

    axes[1].bar(x, rps, color=["#2a9d8f", "#e76f51", "#264653", "#f4a261"])
    axes[1].set_xticks(list(x))
    axes[1].set_xticklabels(labels, rotation=20, ha="right", fontsize=8)
    axes[1].set_ylabel("Requisições/s")
    axes[1].set_title(f"Throughput — {users} usuários")
    axes[1].grid(True, axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Gráfico: {out}")


def main() -> None:
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    rows = collect(RESULTS / "manifest.json")
    if not rows:
        raise SystemExit("Nenhum resultado. Rode a matriz ou gerar_dados_simulados.py")

    plot_by_users(rows, "rps", "Requisições por segundo", GRAFICOS / "rps_por_usuarios.png")
    plot_by_users(rows, "avg_ms", "Tempo médio (ms)", GRAFICOS / "avg_por_usuarios.png")
    plot_by_users(rows, "p95_ms", "Percentil 95 (ms)", GRAFICOS / "p95_por_usuarios.png")
    plot_by_users(rows, "median_ms", "Mediana (ms)", GRAFICOS / "median_por_usuarios.png")
    plot_cache_compare(rows, 15, GRAFICOS / "comparativo_15_usuarios.png")
    plot_cache_compare(rows, 40, GRAFICOS / "comparativo_40_usuarios.png")


if __name__ == "__main__":
    main()
