"""Indicadores económicos derivables de un censo de unidades económicas.

Todas las funciones aceptan un DataFrame normalizado con `cenu.schema.normalizar`
(y enriquecido con `cenu.ciiu.enriquecer_ciiu`). Si existe `factor_expansion`
se puede pasar como `peso` para trabajar con muestras (p. ej. EMICRON).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

RANGOS_TAMANO = [0, 1, 3, 9, 50, 200, np.inf]
ETIQUETAS_TAMANO = ["1 persona", "2-3", "4-9", "10-50", "51-200", "Más de 200"]
RANGOS_ANTIGUEDAD = [-np.inf, 1, 3, 5, 10, np.inf]
ETIQUETAS_ANTIGUEDAD = ["Menos de 1 año", "1 a 3 años", "3 a 5 años", "5 a 10 años", "Más de 10 años"]


def _peso(df: pd.DataFrame, peso: str | None) -> pd.Series:
    return df[peso].fillna(0) if peso and peso in df.columns else pd.Series(1.0, index=df.index)


def conteo_por(df: pd.DataFrame, by: str | list[str], peso: str | None = None) -> pd.DataFrame:
    """Número de unidades (y % del total) por una o más dimensiones."""
    w = _peso(df, peso)
    t = w.groupby([df[b] for b in ([by] if isinstance(by, str) else by)]).sum().rename("unidades").reset_index()
    t["pct"] = 100 * t["unidades"] / t["unidades"].sum()
    return t.sort_values("unidades", ascending=False, ignore_index=True)


def densidad_empresarial(conteos: pd.DataFrame, poblacion: pd.DataFrame, llave: str = "cod_mpio",
                         col_unidades: str = "unidades", col_poblacion: str = "poblacion", por: int = 1000) -> pd.DataFrame:
    """Unidades económicas por cada `por` habitantes (por defecto 1.000).

    densidad_i = unidades_i / poblacion_i * 1000
    La población puede venir de las proyecciones DANE post-CNPV 2018.
    """
    t = conteos.merge(poblacion[[llave, col_poblacion]], on=llave, how="left")
    t["densidad_x1000hab"] = t[col_unidades] / t[col_poblacion] * por
    return t.sort_values("densidad_x1000hab", ascending=False, ignore_index=True)


def cociente_localizacion(df: pd.DataFrame, region: str, sector: str, peso: str | None = None,
                          min_unidades: int = 0) -> pd.DataFrame:
    """Cociente de localización (LQ) de cada sector en cada región.

    LQ_ij = (e_ij / e_i) / (E_j / E)
      e_ij unidades del sector j en la región i, e_i total de la región i,
      E_j total nacional (o del universo) del sector j, E total.
    LQ > 1 indica especialización relativa de la región en el sector.
    Para usar empleo en vez de unidades: peso="personal_ocupado".
    """
    w = _peso(df, peso)
    m = w.groupby([df[region], df[sector]]).sum().unstack(fill_value=0)
    m = m[m.sum(axis=1) >= min_unidades]
    part_region = m.div(m.sum(axis=1), axis=0)
    part_total = m.sum(axis=0) / m.values.sum()
    return part_region.div(part_total, axis=1)


def hhi_diversificacion(df: pd.DataFrame, region: str, sector: str, peso: str | None = None) -> pd.DataFrame:
    """Concentración sectorial por región.

    HHI_i = Σ_j s_ij²   (s = participación del sector j en la región i, 0-1). Rango 1/N..1.
    HHI normalizado = (HHI - 1/N) / (1 - 1/N).
    Entropía de Shannon H_i = -Σ s_ij ln s_ij  (más alta = más diversificada).
    """
    w = _peso(df, peso)
    m = w.groupby([df[region], df[sector]]).sum().unstack(fill_value=0)
    s = m.div(m.sum(axis=1), axis=0)
    n = m.shape[1]
    hhi = (s ** 2).sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        shannon = -(s * np.log(s.where(s > 0))).sum(axis=1)
    out = pd.DataFrame({
        "unidades": m.sum(axis=1),
        "hhi": hhi,
        "hhi_normalizado": (hhi - 1 / n) / (1 - 1 / n) if n > 1 else np.nan,
        "shannon": shannon,
        "sectores_presentes": (m > 0).sum(axis=1),
    })
    return out.sort_values("hhi")


def indice_formalidad(df: pd.DataFrame, by: str | list[str] | None = None, peso: str | None = None) -> pd.DataFrame:
    """% de unidades con registro mercantil, RUT y contabilidad, e índice compuesto (promedio simple).

    Es un índice de formalidad *empresarial* (de la unidad), distinto de la informalidad
    *laboral* de la GEIH (que mide personas ocupadas sin seguridad social).
    """
    cols = [c for c in ("registro_mercantil", "rut", "contabilidad") if c in df.columns]
    if not cols:
        raise ValueError("No hay columnas de formalidad (registro_mercantil, rut, contabilidad)")
    w = _peso(df, peso)
    datos = df[cols].astype("float").mul(w, axis=0)
    validos = df[cols].notna().astype(float).mul(w, axis=0)
    claves = [df[b] for b in ([by] if isinstance(by, str) else by)] if by else [pd.Series("Total", index=df.index, name="grupo")]
    num = datos.groupby(claves).sum()
    den = validos.groupby(claves).sum()
    pct = 100 * num / den.replace(0, np.nan)
    pct.columns = [f"pct_{c}" for c in cols]
    pct["indice_formalidad"] = pct.mean(axis=1)
    pct["unidades"] = w.groupby(claves).sum()
    return pct.reset_index().sort_values("indice_formalidad", ascending=False, ignore_index=True)


def distribucion_tamano(df: pd.DataFrame, by: str | None = None, peso: str | None = None) -> pd.DataFrame:
    """Distribución por rango de personal ocupado (1, 2-3, 4-9, 10-50, 51-200, >200)."""
    d = df.assign(rango_tamano=pd.cut(df["personal_ocupado"], RANGOS_TAMANO, labels=ETIQUETAS_TAMANO, right=True))
    return conteo_por(d, [by, "rango_tamano"] if by else "rango_tamano", peso)


def distribucion_antiguedad(df: pd.DataFrame, by: str | None = None, peso: str | None = None) -> pd.DataFrame:
    d = df.assign(rango_antiguedad=pd.cut(df["anios_funcionamiento"], RANGOS_ANTIGUEDAD,
                                          labels=ETIQUETAS_ANTIGUEDAD, right=False))
    return conteo_por(d, [by, "rango_antiguedad"] if by else "rango_antiguedad", peso)


def brecha_genero(df: pd.DataFrame, by: str = "gran_sector", peso: str | None = None) -> pd.DataFrame:
    """Participación de mujeres propietarias y comparación de tamaño/formalidad por sexo."""
    w = _peso(df, peso)
    d = df.assign(_w=w, _mujer=(df["sexo_propietario"] == "Mujer").astype(float))
    g = d.groupby(by)
    out = pd.DataFrame({
        "unidades": g["_w"].sum(),
        "pct_mujeres_propietarias": 100 * g.apply(lambda x: np.average(x["_mujer"], weights=x["_w"]) if x["_w"].sum() else np.nan,
                                                   include_groups=False),
    })
    if "personal_ocupado" in df.columns:
        pm = d.groupby([by, "sexo_propietario"]).apply(
            lambda x: np.average(x["personal_ocupado"].fillna(0), weights=x["_w"]) if x["_w"].sum() else np.nan,
            include_groups=False).unstack()
        for sexo in ("Mujer", "Hombre"):
            if sexo in pm.columns:
                out[f"personal_prom_{sexo.lower()}"] = pm[sexo]
    if "registro_mercantil" in df.columns:
        rm = d.groupby([by, "sexo_propietario"])["registro_mercantil"].mean().unstack()
        for sexo in ("Mujer", "Hombre"):
            if sexo in rm.columns:
                out[f"pct_registro_{sexo.lower()}"] = 100 * rm[sexo]
        if {"pct_registro_mujer", "pct_registro_hombre"} <= set(out.columns):
            out["brecha_registro_pp"] = out["pct_registro_hombre"] - out["pct_registro_mujer"]
    return out.sort_values("unidades", ascending=False).reset_index()


def brecha_oferta(df: pd.DataFrame, region: str, sector: str, poblacion: pd.DataFrame,
                  llave: str | None = None, col_poblacion: str = "poblacion", min_esperado: float = 5) -> pd.DataFrame:
    """Oportunidades: sectores con menos unidades de las esperadas para la población de la zona.

    esperado_ij = (E_j / P) * p_i     (tasa de referencia del universo x población de la zona)
    brecha_ij   = (esperado_ij - observado_ij) / esperado_ij   (>0 = zona sub-atendida)
    Útil para localización de negocios ("¿dónde falta una droguería / ferretería / panadería?").
    """
    llave = llave or region
    obs = df.groupby([region, sector]).size().unstack(fill_value=0)
    pob = poblacion.set_index(llave)[col_poblacion].reindex(obs.index)
    tasa = obs.sum(axis=0) / pob.sum()
    esperado = pd.DataFrame(np.outer(pob.values, tasa.values), index=obs.index, columns=obs.columns)
    largo = pd.DataFrame({
        "observado": obs.stack(),
        "esperado": esperado.stack(),
    })
    largo = largo[largo["esperado"] >= min_esperado]
    largo["brecha"] = (largo["esperado"] - largo["observado"]) / largo["esperado"]
    largo["unidades_faltantes"] = (largo["esperado"] - largo["observado"]).clip(lower=0).round()
    return largo.reset_index().sort_values("brecha", ascending=False, ignore_index=True)


def resumen_kpis(df: pd.DataFrame, peso: str | None = None) -> dict:
    """KPIs de cabecera para la primera diapositiva."""
    w = _peso(df, peso)
    k: dict = {"unidades_economicas": float(w.sum())}
    if "personal_ocupado" in df.columns:
        k["personal_ocupado_total"] = float((df["personal_ocupado"].fillna(0) * w).sum())
        k["personal_promedio"] = k["personal_ocupado_total"] / k["unidades_economicas"] if k["unidades_economicas"] else np.nan
        k["pct_unipersonales"] = float(100 * w[df["personal_ocupado"] == 1].sum() / w.sum())
        k["pct_micro_1a9"] = float(100 * w[df["personal_ocupado"].between(1, 9)].sum() / w.sum())
    for c in ("registro_mercantil", "rut", "contabilidad"):
        if c in df.columns:
            v = df[c].notna()
            k[f"pct_{c}"] = float(100 * (df.loc[v, c].astype(float) * w[v]).sum() / w[v].sum()) if v.any() else np.nan
    if "sexo_propietario" in df.columns:
        k["pct_mujeres_propietarias"] = float(100 * w[df["sexo_propietario"] == "Mujer"].sum() / w.sum())
    if "gran_sector" in df.columns:
        k["sector_dominante"] = str(w.groupby(df["gran_sector"]).sum().idxmax())
    if "tipo_unidad" in df.columns:
        for t, v in (w.groupby(df["tipo_unidad"]).sum() / w.sum() * 100).items():
            k[f"pct_tipo_{t}"] = float(v)
    if "cod_mpio" in df.columns:
        k["municipios"] = int(df["cod_mpio"].nunique())
    return k
