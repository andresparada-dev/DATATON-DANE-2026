"""Reporte automático: de un DataFrame normalizado a gráficas PNG + reporte Markdown + HTML autocontenido.

Pensado para los primeros 20 minutos del reto: correr, mirar, decidir la historia.
Paleta: azul de una sola tonalidad para magnitudes; azul<->rojo con gris al centro para LQ.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm  # noqa: E402

from . import indicators as ind  # noqa: E402
from . import spatial  # noqa: E402

AZUL = "#2a78d6"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]  # máximo 3 categorías en dispersión; el resto -> "Otros" gris
GRIS_OTROS = "#b4b2a9"
SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
SEQ = LinearSegmentedColormap.from_list("azul", ["#cde2fb", "#86b6ef", "#3987e5", "#256abf", "#184f95", "#0d366b"])
DIV = LinearSegmentedColormap.from_list("div", ["#2a78d6", "#f0efec", "#e34948"])

plt.rcParams.update({
    "figure.facecolor": SUPERFICIE, "axes.facecolor": SUPERFICIE, "savefig.facecolor": SUPERFICIE,
    "axes.edgecolor": "#d9d8d2", "axes.labelcolor": TINTA_2, "xtick.color": TINTA_2, "ytick.color": TINTA_2,
    "text.color": TINTA, "axes.spines.top": False, "axes.spines.right": False, "font.size": 10,
    "axes.titleweight": "bold", "axes.titlesize": 12, "axes.titlelocation": "left",
    "axes.grid": True, "grid.color": "#ecebe6", "grid.linewidth": 0.8, "axes.axisbelow": True,
})


def _barras_h(serie: pd.Series, titulo: str, xlabel: str, ruta: Path, fmt: str = "{:,.0f}", max_n: int = 15) -> Path:
    s = serie.sort_values(ascending=False).head(max_n)[::-1]
    fig, ax = plt.subplots(figsize=(9, 0.38 * len(s) + 1.4))
    ax.barh([str(i)[:60] for i in s.index], s.values, color=AZUL, height=0.62, edgecolor=SUPERFICIE, linewidth=2)
    ax.grid(axis="y", visible=False)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    tope = s.max() if len(s) else 0
    for y, v in enumerate(s.values):
        ax.text(v + tope * 0.01, y, fmt.format(v), va="center", fontsize=8.5, color=TINTA_2)
    ax.set_xlim(0, tope * 1.15 if tope else 1)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def _mapa_puntos(df: pd.DataFrame, cat: str, titulo: str, ruta: Path, max_puntos: int = 60_000) -> Path:
    d = df.dropna(subset=["latitud", "longitud"])
    d = d[d["latitud"].between(-5, 14) & d["longitud"].between(-82, -66)]
    if len(d) > max_puntos:
        d = d.sample(max_puntos, random_state=0)
    top = d[cat].value_counts().index[:3].tolist() if cat in d.columns else []
    fig, ax = plt.subplots(figsize=(8, 8))
    if top:
        otros = d[~d[cat].isin(top)]
        ax.scatter(otros["longitud"], otros["latitud"], s=2, c=GRIS_OTROS, alpha=0.5, linewidths=0, label="Otros")
        for color, valor in zip(SERIES, top):
            sub = d[d[cat] == valor]
            ax.scatter(sub["longitud"], sub["latitud"], s=3, c=color, alpha=0.7, linewidths=0, label=str(valor)[:45])
        ax.legend(markerscale=5, frameon=False, loc="upper left", fontsize=8)
    else:
        ax.scatter(d["longitud"], d["latitud"], s=2, c=AZUL, alpha=0.5, linewidths=0)
    ax.set_title(titulo)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def _mapa_calor(df: pd.DataFrame, titulo: str, ruta: Path, tam_m: int = 500) -> Path:
    g = spatial.grilla(df, tam_m=tam_m)
    fig, ax = plt.subplots(figsize=(8, 8))
    sc = ax.scatter(g["longitud"], g["latitud"], c=g["valor"], cmap=SEQ, s=6, marker="s", linewidths=0,
                    norm=matplotlib.colors.LogNorm(vmin=1, vmax=max(g["valor"].max(), 2)))
    fig.colorbar(sc, ax=ax, shrink=0.7, label=f"Unidades por celda de {tam_m} m (escala log)")
    ax.set_title(titulo)
    ax.set_aspect("equal", adjustable="datalim")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def _heatmap_lq(lq: pd.DataFrame, titulo: str, ruta: Path) -> Path:
    fig, ax = plt.subplots(figsize=(min(1 + 0.45 * lq.shape[1], 14), 0.35 * lq.shape[0] + 1.6))
    vmax = max(float(np.nanmax(lq.values)), 1.01)
    im = ax.imshow(lq.values, cmap=DIV, norm=TwoSlopeNorm(vcenter=1, vmin=0, vmax=min(vmax, 4)), aspect="auto")
    ax.set_xticks(range(lq.shape[1]), lq.columns, fontsize=8)
    ax.set_yticks(range(lq.shape[0]), [str(i)[:30] for i in lq.index], fontsize=8)
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.8, label="LQ (1 = igual al promedio; >1 especializado)")
    ax.set_title(titulo)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def _tabla_md(df: pd.DataFrame, n: int = 15, dec: int = 1) -> str:
    d = df.head(n).copy()
    for c in d.select_dtypes("number").columns:
        d[c] = d[c].round(dec)
    return d.to_markdown(index=False) if _tiene_tabulate() else "```\n" + d.to_string(index=False) + "\n```"


def _tiene_tabulate() -> bool:
    try:
        import tabulate  # noqa: F401
        return True
    except ImportError:
        return False


def generar_reporte(df: pd.DataFrame, salida: str | Path = "reports/auto", titulo: str = "Reporte CENU",
                    region: str = "municipio", peso: str | None = None, advertencia: str | None = None) -> Path:
    """Genera PNGs + reporte.md + reporte.html + kpis.json + tablas CSV en `salida`."""
    out = Path(salida)
    out.mkdir(parents=True, exist_ok=True)
    figs: list[tuple[str, Path]] = []
    secciones: list[str] = [f"# {titulo}\n"]
    if advertencia:
        secciones.append(f"> **{advertencia}**\n")

    k = ind.resumen_kpis(df, peso)
    (out / "kpis.json").write_text(json.dumps(k, ensure_ascii=False, indent=2))
    secciones.append("## KPIs\n\n" + "\n".join(f"- **{c}**: {v:,.1f}" if isinstance(v, float) else f"- **{c}**: {v}"
                                               for c, v in k.items()) + "\n")

    if "gran_sector" in df.columns:
        t = ind.conteo_por(df, "gran_sector", peso)
        t.to_csv(out / "unidades_gran_sector.csv", index=False)
        figs.append(("Unidades por gran sector", _barras_h(t.set_index("gran_sector")["unidades"],
                     "Unidades económicas por gran sector", "Unidades", out / "01_gran_sector.png")))
    if "ciiu_division" in df.columns:
        from .ciiu import DIVISIONES_FRECUENTES
        t = ind.conteo_por(df, "ciiu_division", peso)
        t["nombre"] = t["ciiu_division"].map(lambda d: f"{int(d):02d} {DIVISIONES_FRECUENTES.get(int(d), '')}" if pd.notna(d) else "Sin dato")
        t.to_csv(out / "unidades_division.csv", index=False)
        figs.append(("Top divisiones CIIU", _barras_h(t.set_index("nombre")["unidades"],
                     "Top 15 divisiones CIIU por número de unidades", "Unidades", out / "02_divisiones.png")))
    if "personal_ocupado" in df.columns:
        t = ind.distribucion_tamano(df, peso=peso)
        t.to_csv(out / "distribucion_tamano.csv", index=False)
        s = t.set_index("rango_tamano")["pct"].reindex(ind.ETIQUETAS_TAMANO)
        fig, ax = plt.subplots(figsize=(8, 3.6))
        ax.bar(s.index.astype(str), s.values, color=AZUL, width=0.62, edgecolor=SUPERFICIE, linewidth=2)
        for x, v in enumerate(s.values):
            if pd.notna(v):
                ax.text(x, v + 0.8, f"{v:.1f}%", ha="center", fontsize=8.5, color=TINTA_2)
        ax.set_title("Distribución por tamaño (personal ocupado)")
        ax.set_ylabel("% de unidades")
        ax.grid(axis="x", visible=False)
        fig.tight_layout()
        fig.savefig(out / "03_tamano.png", dpi=150)
        plt.close(fig)
        figs.append(("Tamaño", out / "03_tamano.png"))
    if any(c in df.columns for c in ("registro_mercantil", "rut", "contabilidad")):
        by = "gran_sector" if "gran_sector" in df.columns else None
        t = ind.indice_formalidad(df, by, peso)
        t.to_csv(out / "formalidad.csv", index=False)
        secciones.append("## Formalidad empresarial\n\n" + _tabla_md(t) + "\n")
        if by:
            figs.append(("Formalidad", _barras_h(t.set_index(by)["indice_formalidad"],
                         "Índice de formalidad empresarial por gran sector", "% (promedio registro/RUT/contabilidad)",
                         out / "04_formalidad.png", fmt="{:.1f}%")))
        if region in df.columns:
            t2 = ind.indice_formalidad(df, region, peso)
            t2.to_csv(out / f"formalidad_{region}.csv", index=False)
    if "sexo_propietario" in df.columns and "gran_sector" in df.columns:
        t = ind.brecha_genero(df, "gran_sector", peso)
        t.to_csv(out / "brecha_genero.csv", index=False)
        secciones.append("## Brecha de género (propiedad)\n\n" + _tabla_md(t) + "\n")
        if "ciiu_division" in df.columns:
            from .ciiu import DIVISIONES_FRECUENTES
            d = df.assign(div=df["ciiu_division"].map(lambda x: f"{int(x):02d} {DIVISIONES_FRECUENTES.get(int(x), '')}" if pd.notna(x) else None))
            g = ind.brecha_genero(d[d["div"].notna()], "div", peso)
            g = g[g["unidades"] >= max(30, g["unidades"].quantile(0.5))]
            figs.append(("Mujeres propietarias", _barras_h(g.set_index("div")["pct_mujeres_propietarias"],
                         "% de unidades con propietaria mujer (divisiones con más unidades)", "%",
                         out / "05_genero.png", fmt="{:.1f}%")))
    if "anios_funcionamiento" in df.columns:
        t = ind.distribucion_antiguedad(df, peso=peso)
        t.to_csv(out / "antiguedad.csv", index=False)
        secciones.append("## Antigüedad\n\n" + _tabla_md(t) + "\n")
    if region in df.columns and "ciiu_seccion" in df.columns and df[region].nunique() > 1:
        lq = ind.cociente_localizacion(df, region, "ciiu_seccion", peso, min_unidades=30)
        lq = lq.loc[lq.index[:40]]
        lq.round(3).to_csv(out / f"lq_{region}_seccion.csv")
        figs.append(("Especialización (LQ)", _heatmap_lq(lq, f"Cociente de localización: {region} x sección CIIU",
                                                         out / "06_lq.png")))
        h = ind.hhi_diversificacion(df, region, "ciiu_division" if "ciiu_division" in df.columns else "ciiu_seccion", peso)
        h.to_csv(out / f"hhi_{region}.csv")
        secciones.append(f"## Diversificación sectorial por {region} (HHI / Shannon)\n\n" + _tabla_md(h.reset_index(), 20, 3) + "\n")
    if {"latitud", "longitud"} <= set(df.columns) and df["latitud"].notna().sum() > 50:
        cat = "gran_sector" if "gran_sector" in df.columns else "tipo_unidad"
        # Un mapa nacional de puntos no se lee: si hay varios municipios se mapea el de más unidades.
        dm, lugar = df, "todas las unidades"
        if "municipio" in df.columns and df["municipio"].nunique() > 1:
            lugar = str(df["municipio"].value_counts().idxmax())
            dm = df[df["municipio"] == lugar]
        figs.append(("Mapa de puntos", _mapa_puntos(dm, cat, f"Unidades por {cat.replace('_', ' ')} — {lugar}",
                                                    out / "07_mapa_puntos.png")))
        figs.append(("Mapa de calor", _mapa_calor(dm, f"Densidad de unidades (grilla 500 m) — {lugar}",
                                                  out / "08_mapa_calor.png")))
        etiquetas = spatial.clusters_dbscan(dm, eps_m=150, min_muestras=max(10, len(dm) // 2000))
        rc = spatial.resumen_clusters(dm, etiquetas, "gran_sector" if "gran_sector" in dm.columns else "ciiu_seccion")
        rc.to_csv(out / "clusters_dbscan.csv")
        secciones.append(f"## Aglomeraciones (DBSCAN 150 m) — {lugar}\n\n" + _tabla_md(rc.reset_index(), 10, 4) + "\n")

    secciones.append("## Gráficas\n\n" + "\n".join(f"### {t}\n\n![{t}]({p.name})\n" for t, p in figs))
    md = "\n".join(secciones)
    (out / "reporte.md").write_text(md, encoding="utf-8")

    html_figs = "".join(
        f"<figure><img alt='{t}' src='data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}'/><figcaption>{t}</figcaption></figure>"
        for t, p in figs)
    kpi_html = "".join(f"<div class='kpi'><span>{c.replace('_', ' ')}</span><b>{v:,.1f}</b></div>" if isinstance(v, float)
                       else f"<div class='kpi'><span>{c.replace('_', ' ')}</span><b>{v}</b></div>" for c, v in k.items())
    aviso = f"<p class='aviso'>{advertencia}</p>" if advertencia else ""
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title><style>
body{{font-family:system-ui,sans-serif;background:#fcfcfb;color:#0b0b0b;max-width:1100px;margin:auto;padding:16px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
.kpi{{border:1px solid #e4e3dd;border-radius:8px;padding:10px}} .kpi span{{display:block;color:#52514e;font-size:12px}}
.kpi b{{font-size:20px}} figure{{margin:24px 0}} img{{max-width:100%}} figcaption{{color:#52514e;font-size:13px}}
.aviso{{background:#fff4d6;border-left:4px solid #eda100;padding:8px 12px}}
</style></head><body><h1>{titulo}</h1>{aviso}<div class="kpis">{kpi_html}</div>{html_figs}</body></html>"""
    (out / "reporte.html").write_text(html, encoding="utf-8")
    return out
