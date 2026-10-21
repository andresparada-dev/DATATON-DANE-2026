#!/usr/bin/env python3
"""MVP "Donde Falta, Emprende": mapa de desiertos de servicios esenciales para una ciudad.

    python scripts/donde_falta.py --input data/raw/cenu.csv --municipio "Bogotá" --radio 500
    python scripts/donde_falta.py --sintetico            # ensayo con datos SINTÉTICOS

Salida en reports/donde_falta_<ciudad>/:
  resumen_desiertos.csv     % de demanda en desierto por categoría
  oportunidades_<cat>.csv   top 10 celdas para abrir cada tipo de negocio
  mapa_<cat>.png            mapa estático (respaldo para el pitch)
  mapa_interactivo.html     mapa folium con capas por categoría (si folium está instalado)
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "scripts"))

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from cenu import ciiu, oportunidad, report, schema, synthetic  # noqa: E402,F401


def slug(t: str) -> str:
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return "".join(c if c.isalnum() else "_" for c in t).strip("_")


def mapa_png(celdas: pd.DataFrame, cat: str, radio: int, ruta: Path, ciudad: str) -> None:
    col = f"dist_{cat}"
    des = celdas[celdas[col] > radio]
    ok = celdas[celdas[col] <= radio]
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.scatter(ok["longitud"], ok["latitud"], s=7, marker="s", c="#cde2fb", linewidths=0, label=f"A ≤ {radio} m")
    ax.scatter(des["longitud"], des["latitud"], s=7 + 30 * des["demanda"] / max(des["demanda"].max(), 1), marker="s",
               c="#e34948", alpha=0.8, linewidths=0, label=f"Desierto (> {radio} m), tamaño = demanda")
    pct = 100 * des["demanda"].sum() / celdas["demanda"].sum()
    ax.set_title(f"{ciudad}: {pct:.0f}% de la demanda está a más de {radio} m de: {cat}")
    ax.legend(frameon=False, loc="upper left", fontsize=8, markerscale=2)
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def mapa_html(celdas: pd.DataFrame, categorias: list[str], radio: int, ruta: Path) -> bool:
    try:
        import folium
    except ImportError:
        return False
    m = folium.Map(location=[celdas["latitud"].mean(), celdas["longitud"].mean()], zoom_start=12)
    for i, cat in enumerate(categorias):
        capa = folium.FeatureGroup(name=f"Desierto: {cat}", show=(i == 0))
        des = celdas[celdas[f"dist_{cat}"] > radio]
        for _, r in des.iterrows():
            folium.CircleMarker([r["latitud"], r["longitud"]], radius=2 + min(r["demanda"], 40) / 6,
                                color="#e34948", fill=True, fill_opacity=0.6, weight=0,
                                tooltip=f"{cat}: {r[f'dist_{cat}']:.0f} m al más cercano · demanda {r['demanda']:.0f}").add_to(capa)
        capa.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    m.save(str(ruta))
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input")
    ap.add_argument("--municipio", default=None, help="Nombre (o parte) del municipio; por defecto el de más unidades")
    ap.add_argument("--radio", type=int, default=500, help="Metros para considerar 'cerca'")
    ap.add_argument("--celda", type=int, default=250, help="Tamaño de celda en metros")
    ap.add_argument("--poblacion", default=None, help="CSV opcional con columnas celda,poblacion (misma grilla)")
    ap.add_argument("--mapeo", action="append", default=[])
    ap.add_argument("--sintetico", action="store_true")
    a = ap.parse_args()

    if a.sintetico:
        crudo = synthetic.generar(30_000)
    elif a.input:
        from analisis_rapido import leer
        crudo = leer(a.input, None, None)
    else:
        ap.error("Indique --input o --sintetico")
    df = ciiu.enriquecer_ciiu(schema.normalizar(crudo, dict(m.split("=", 1) for m in a.mapeo) or None, verbose=False))
    if "municipio" in df.columns:
        if a.municipio:
            df = df[df["municipio"].astype(str).str.contains(a.municipio, case=False, na=False)]
        else:
            df = df[df["municipio"] == df["municipio"].value_counts().idxmax()]
        ciudad = str(df["municipio"].iloc[0])
    else:
        ciudad = a.municipio or "Ciudad"
    if a.sintetico:
        ciudad += " [SINTÉTICO]"
    pob = pd.read_csv(a.poblacion) if a.poblacion else None

    celdas, resumen = oportunidad.desiertos(df, tam_celda_m=a.celda, radio_m=a.radio, poblacion_celdas=pob)
    out = RAIZ / "reports" / f"donde_falta_{slug(ciudad)}"
    out.mkdir(parents=True, exist_ok=True)
    resumen.round(2).to_csv(out / "resumen_desiertos.csv", index=False)
    print(f"{ciudad}: {len(df):,} unidades, {len(celdas):,} celdas con demanda")
    print(resumen.round(1).to_string(index=False))
    categorias = [c for c in resumen["categoria"] if resumen.set_index("categoria").loc[c, "unidades"] > 0]
    for cat in categorias[:6]:
        oportunidad.top_oportunidades(celdas, cat, 10, a.radio).round(5).to_csv(out / f"oportunidades_{slug(cat)}.csv", index=False)
        mapa_png(celdas, cat, a.radio, out / f"mapa_{slug(cat)}.png", ciudad)
    if mapa_html(celdas, categorias, a.radio, out / "mapa_interactivo.html"):
        print("Mapa interactivo:", out / "mapa_interactivo.html")
    print("Salida:", out)


if __name__ == "__main__":
    main()
