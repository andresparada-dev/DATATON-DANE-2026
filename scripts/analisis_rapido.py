#!/usr/bin/env python3
"""Análisis rápido de cualquier archivo de unidades económicas (CSV, XLSX, Parquet, SAV, DTA).

Uso el día del evento:
    python scripts/analisis_rapido.py --input data/raw/cenu.csv --region municipio
    python scripts/analisis_rapido.py --input data/raw/cenu.xlsx --mapeo "COD_ACT=ciiu" --mapeo "OCUP=personal_ocupado"
Ensayo con datos sintéticos (NO oficiales):
    python scripts/analisis_rapido.py --sintetico 20000

Salida: reports/<nombre>/ con reporte.html (autocontenido), reporte.md, PNGs, kpis.json y CSVs.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import pandas as pd  # noqa: E402

from cenu import ciiu, report, schema, synthetic  # noqa: E402


def leer(ruta: str, sep: str | None, hoja: str | None) -> pd.DataFrame:
    p = Path(ruta)
    ext = p.suffix.lower()
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(p, sheet_name=hoja or 0, dtype=str)
    if ext == ".parquet":
        return pd.read_parquet(p)
    if ext in (".sav", ".dta"):
        import pyreadstat
        lector = pyreadstat.read_sav if ext == ".sav" else pyreadstat.read_dta
        df, _ = lector(str(p), apply_value_formats=True)
        return df
    # CSV/TXT: detecta separador y codificación típicos de archivos DANE (; y latin-1)
    for enc in ("utf-8", "latin-1"):
        try:
            return pd.read_csv(p, sep=sep, engine="python" if sep is None else "c", encoding=enc, dtype=str)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"No se pudo leer {ruta}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", help="Archivo de entrada")
    ap.add_argument("--sep", default=None, help="Separador CSV (por defecto se detecta)")
    ap.add_argument("--hoja", default=None, help="Hoja de Excel")
    ap.add_argument("--mapeo", action="append", default=[], help="columna_original=columna_estandar (repetible)")
    ap.add_argument("--region", default="municipio", help="Columna para LQ/HHI (municipio, sector_urbano, departamento...)")
    ap.add_argument("--peso", default=None, help="Columna de factor de expansión (muestras)")
    ap.add_argument("--salida", default=None)
    ap.add_argument("--titulo", default=None)
    ap.add_argument("--sintetico", type=int, default=0, help="Genera N registros sintéticos para ensayar")
    a = ap.parse_args()

    advertencia = None
    if a.sintetico:
        crudo = synthetic.generar(a.sintetico)
        nombre = "sintetico"
        advertencia = "DATOS SINTÉTICOS DE ENSAYO — NO SON CIFRAS OFICIALES DEL DANE"
    elif a.input:
        crudo = leer(a.input, a.sep, a.hoja)
        nombre = Path(a.input).stem
    else:
        ap.error("Indique --input o --sintetico")

    print(f"Registros: {len(crudo):,}  Columnas: {len(crudo.columns)}")
    mapeo = dict(m.split("=", 1) for m in a.mapeo)
    df = schema.normalizar(crudo, mapeo_manual=mapeo or None)
    df = ciiu.enriquecer_ciiu(df)
    salida = Path(a.salida or RAIZ / "reports" / nombre)
    salida.mkdir(parents=True, exist_ok=True)
    schema.perfil_calidad(df).to_csv(salida / "perfil_calidad.csv", index=False)
    df.to_parquet(salida / "datos_normalizados.parquet") if _hay_parquet() else df.to_csv(salida / "datos_normalizados.csv", index=False)
    region = a.region if a.region in df.columns else ("municipio" if "municipio" in df.columns else "cod_mpio")
    report.generar_reporte(df, salida, a.titulo or f"Análisis rápido — {nombre}", region=region, peso=a.peso,
                           advertencia=advertencia)
    print(f"Listo -> {salida / 'reporte.html'}")


def _hay_parquet() -> bool:
    try:
        import pyarrow  # noqa: F401
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    main()
