#!/usr/bin/env python3
"""Análisis de las cifras PUBLICADAS del CENU 2024 y operaciones relacionadas (sin microdatos).

Lee data/cifras_oficiales/tabla_territorial_consolidada.csv y genera:
  docs/img/*.png          gráficas para el documento de análisis y el pitch
  docs/tablas/indicadores_territoriales.csv

Todas las cifras de entrada tienen fuente (columna `fuentes` o CSVs hermanos). Son preliminares
y varias provienen de prensa que cita al DANE: verificar contra el boletín oficial antes de publicar.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from cenu import report  # noqa: E402,F401  (aplica el estilo de gráficas del toolkit)

AZUL, NARANJA, GRIS, TINTA_2, SUP = "#2a78d6", "#eb6834", "#b4b2a9", "#52514e", "#fcfcfb"
IMG = RAIZ / "docs" / "img"
OUT = RAIZ / "docs" / "tablas"


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(IMG / nombre, dpi=150)
    plt.close(fig)
    print("  ", IMG / nombre)


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    t = pd.read_csv(RAIZ / "data" / "cifras_oficiales" / "tabla_territorial_consolidada.csv")
    nac = t[t["nivel"] == "pais"].iloc[0]

    t["pct_unidades_cenu"] = 100 * t["cenu_2024_unidades"] / nac["cenu_2024_unidades"]
    t["pct_pib_2024"] = 100 * t["pib_2024_miles_millones"] / nac["pib_2024_miles_millones"]
    # >1: el territorio genera más PIB del que su peso en número de unidades sugeriría
    t["indice_pib_por_unidad"] = t["pct_pib_2024"] / t["pct_unidades_cenu"]
    t["pib_por_unidad_millones"] = t["pib_2024_miles_millones"] * 1000 / t["cenu_2024_unidades"]
    t["pct_vendedores_calle"] = 100 * t["cenu_2024_vendedores_calle"] / t["cenu_2024_unidades"]
    t["var_pct_conteo2021_cenu2024"] = 100 * (t["cenu_2024_unidades"] / t["conteo_2021_unidades"] - 1)
    # Visibilidad: peso en unidades visibles urbanas (CENU) vs peso en micronegocios (EMICRON, incluye rural y no visibles)
    t["ratio_visible_vs_emicron"] = t["pct_unidades_cenu"] / t["emicron_2024_pct_micronegocios"]
    cols = ["territorio", "nivel", "cenu_2024_unidades", "pct_unidades_cenu", "pct_pib_2024", "indice_pib_por_unidad",
            "pib_por_unidad_millones", "pct_vendedores_calle", "var_pct_conteo2021_cenu2024", "ratio_visible_vs_emicron"]
    t[cols].round(2).to_csv(OUT / "indicadores_territoriales.csv", index=False)
    print(t[cols].round(2).to_string(index=False))

    # 1. Unidades por departamento
    d = t[t["nivel"] == "departamento"].sort_values("cenu_2024_unidades")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(d["territorio"], d["cenu_2024_unidades"], color=AZUL, height=0.6, edgecolor=SUP, linewidth=2)
    for y, (v, p) in enumerate(zip(d["cenu_2024_unidades"], d["pct_unidades_cenu"])):
        ax.text(v + 4000, y, f"{v:,.0f}  ({p:.1f}%)".replace(",", "."), va="center", fontsize=8.5, color=TINTA_2)
    ax.set_xlim(0, d["cenu_2024_unidades"].max() * 1.3)
    ax.grid(axis="y", visible=False)
    ax.set_title("CENU 2024: unidades económicas visibles, 7 mayores departamentos")
    ax.set_xlabel("Unidades (preliminar). Total nacional: 2.005.613")
    guardar(fig, "cenu_unidades_departamento.png")

    # 2. Conteo 2021 vs CENU 2024 (no comparables 1:1 — ilustra el cambio de definición)
    c = t.dropna(subset=["conteo_2021_unidades"]).sort_values("cenu_2024_unidades")
    fig, ax = plt.subplots(figsize=(8, 3.8))
    y = range(len(c))
    ax.hlines(y, c["cenu_2024_unidades"], c["conteo_2021_unidades"], color=GRIS, linewidth=2)
    ax.scatter(c["conteo_2021_unidades"], y, color=GRIS, s=60, label="Conteo 2021", zorder=3, edgecolor=SUP, linewidth=2)
    ax.scatter(c["cenu_2024_unidades"], y, color=AZUL, s=60, label="CENU 2024", zorder=3, edgecolor=SUP, linewidth=2)
    for i, (_, r) in enumerate(c.iterrows()):
        ax.text(r["conteo_2021_unidades"] * 1.03 if r["nivel"] != "pais" else r["conteo_2021_unidades"] * 1.02, i,
                f"{r['var_pct_conteo2021_cenu2024']:.0f}%", va="center", fontsize=8.5, color=TINTA_2)
    ax.set_yticks(list(y), c["territorio"])
    ax.set_xscale("log")
    ax.grid(axis="y", visible=False)
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("Conteo 2021 vs. CENU 2024 (definiciones distintas: no es crecimiento)")
    ax.set_xlabel("Unidades económicas (escala log)")
    guardar(fig, "conteo2021_vs_cenu2024.png")

    # 3. Peso en unidades vs peso en PIB
    p = t.dropna(subset=["pct_pib_2024"])
    p = p[p["nivel"] != "pais"]
    fig, ax = plt.subplots(figsize=(7, 3.4))
    x = range(len(p))
    ax.bar([i - 0.18 for i in x], p["pct_unidades_cenu"], width=0.34, color=AZUL, label="% de unidades (CENU 2024)",
           edgecolor=SUP, linewidth=2)
    ax.bar([i + 0.18 for i in x], p["pct_pib_2024"], width=0.34, color=NARANJA, label="% del PIB (2024p)",
           edgecolor=SUP, linewidth=2)
    for i, (_, r) in enumerate(p.iterrows()):
        ax.text(i, max(r["pct_unidades_cenu"], r["pct_pib_2024"]) + 1, f"índice {r['indice_pib_por_unidad']:.2f}",
                ha="center", fontsize=8.5, color=TINTA_2)
    ax.set_xticks(list(x), p["territorio"])
    ax.set_ylabel("% del total nacional")
    ax.set_ylim(0, 31)
    ax.grid(axis="x", visible=False)
    ax.legend(frameon=False, loc="upper right", fontsize=8.5)
    ax.set_title("Peso en número de negocios vs. peso en el PIB")
    guardar(fig, "unidades_vs_pib.png")

    # 4. Vendedores de calle como % de las unidades
    v = t.dropna(subset=["pct_vendedores_calle"]).sort_values("pct_vendedores_calle")
    fig, ax = plt.subplots(figsize=(7, 3.2))
    colores = [GRIS if n == "pais" else AZUL for n in v["nivel"]]
    ax.barh(v["territorio"], v["pct_vendedores_calle"], color=colores, height=0.6, edgecolor=SUP, linewidth=2)
    for yy, val in enumerate(v["pct_vendedores_calle"]):
        ax.text(val + 0.2, yy, f"{val:.1f}%", va="center", fontsize=8.5, color=TINTA_2)
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, 15)
    ax.set_title("Unidades de venta en calle como % de las unidades (CENU 2024)")
    ax.set_xlabel("% (gris = total nacional)")
    guardar(fig, "vendedores_calle_pct.png")

    # 5. Dos lentes sobre la misma economía: CENU (visibles urbanas) vs EMICRON (micronegocios)
    lentes = pd.DataFrame({
        "indicador": ["% con RUT", "% propietarias mujeres"],
        "CENU 2024 (unidades visibles urbanas)": [49.2, 51.6],
        "EMICRON (micronegocios)": [100 - 77.6, 37.5],
    }).set_index("indicador")
    fig, ax = plt.subplots(figsize=(7, 3.2))
    x = range(len(lentes))
    ax.bar([i - 0.18 for i in x], lentes.iloc[:, 0], width=0.34, color=AZUL, label=lentes.columns[0], edgecolor=SUP, linewidth=2)
    ax.bar([i + 0.18 for i in x], lentes.iloc[:, 1], width=0.34, color=NARANJA, label=lentes.columns[1], edgecolor=SUP, linewidth=2)
    for i in x:
        for dx, val in ((-0.18, lentes.iloc[i, 0]), (0.18, lentes.iloc[i, 1])):
            ax.text(i + dx, val + 1.2, f"{val:.1f}%", ha="center", fontsize=8.5, color=TINTA_2)
    ax.set_xticks(list(x), lentes.index)
    ax.set_ylim(0, 72)
    ax.grid(axis="x", visible=False)
    ax.legend(frameon=False, fontsize=8, loc="upper center", ncol=2)
    ax.set_title("Dos lentes, dos realidades: formalidad y género")
    ax.text(0, -0.2, "RUT CENU: sobre 1.547.275 unidades con información (may-2026). EMICRON RUT: 2024 nacional. "
            "Mujeres EMICRON: 24 ciudades 2025.", transform=ax.transAxes, fontsize=7, color=TINTA_2)
    guardar(fig, "cenu_vs_emicron.png")

    # 6. 1990 vs 2024
    fig, axs = plt.subplots(1, 2, figsize=(8, 3.2))
    axs[0].bar(["1990", "2024"], [1.001398, 2.005613], color=[GRIS, AZUL], width=0.5, edgecolor=SUP, linewidth=2)
    axs[0].set_title("Unidades urbanas (millones)")
    for i, val in enumerate([1.001398, 2.005613]):
        axs[0].text(i, val + 0.04, f"{val:.2f} M", ha="center", fontsize=9, color=TINTA_2)
    axs[0].set_ylim(0, 2.4)
    axs[1].bar(["1990", "2024"], [9.5, 5.2], color=[GRIS, AZUL], width=0.5, edgecolor=SUP, linewidth=2)
    axs[1].set_title("% de unidades en industria")
    for i, val in enumerate([9.5, 5.2]):
        axs[1].text(i, val + 0.2, f"{val:.1f}%", ha="center", fontsize=9, color=TINTA_2)
    axs[1].set_ylim(0, 11)
    for a in axs:
        a.grid(axis="x", visible=False)
    fig.suptitle("34 años después: el doble de negocios y menos industria", fontweight="bold", x=0.02, ha="left")
    guardar(fig, "censo1990_vs_cenu2024.png")


if __name__ == "__main__":
    main()
