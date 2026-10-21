"""Análisis espacial liviano (solo numpy / pandas / scikit-learn; no requiere geopandas).

- grilla: agrega unidades en celdas de N metros (mapa de calor / "hexbin" cuadrado).
- clusters_dbscan: aglomeraciones comerciales (ejes y corredores) con DBSCAN haversine.
- distancia_mas_cercana: distancia de cada origen al destino más cercano (desiertos de servicios).
- morans_i / getis_ord_gi_star: autocorrelación espacial global y puntos calientes locales.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

R_TIERRA_KM = 6371.0088


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * R_TIERRA_KM * np.arcsin(np.sqrt(a))


def _validas(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["latitud"].between(-5, 14) & df["longitud"].between(-82, -66)]


def grilla(df: pd.DataFrame, tam_m: float = 500, valor: str | None = None, agg: str = "count") -> pd.DataFrame:
    """Agrega puntos en celdas cuadradas de ~tam_m metros. Devuelve centroide y conteo/valor por celda."""
    d = _validas(df)
    lat0 = d["latitud"].mean()
    dlat = tam_m / 111_320
    dlon = tam_m / (111_320 * np.cos(np.radians(lat0)))
    gy = np.floor(d["latitud"] / dlat).astype(int)
    gx = np.floor(d["longitud"] / dlon).astype(int)
    g = d.assign(_gy=gy, _gx=gx)
    if valor:
        t = g.groupby(["_gy", "_gx"])[valor].agg(agg).rename("valor")
    else:
        t = g.groupby(["_gy", "_gx"]).size().rename("valor")
    t = t.reset_index()
    t["latitud"] = (t["_gy"] + 0.5) * dlat
    t["longitud"] = (t["_gx"] + 0.5) * dlon
    t["celda"] = t["_gy"].astype(str) + "_" + t["_gx"].astype(str)
    return t.drop(columns=["_gy", "_gx"])


def clusters_dbscan(df: pd.DataFrame, eps_m: float = 150, min_muestras: int = 15) -> pd.Series:
    """Etiqueta de clúster por unidad (-1 = ruido). eps en metros."""
    from sklearn.cluster import DBSCAN

    d = _validas(df)
    coords = np.radians(d[["latitud", "longitud"]].to_numpy(dtype=float))
    etiquetas = DBSCAN(eps=eps_m / 1000 / R_TIERRA_KM, min_samples=min_muestras,
                       metric="haversine", algorithm="ball_tree").fit_predict(coords)
    return pd.Series(etiquetas, index=d.index, name="cluster").reindex(df.index, fill_value=-1)


def resumen_clusters(df: pd.DataFrame, etiquetas: pd.Series, sector: str = "ciiu_seccion") -> pd.DataFrame:
    """Tamaño, centroide y sector dominante de cada clúster."""
    d = df.assign(cluster=etiquetas)
    d = d[d["cluster"] >= 0]
    g = d.groupby("cluster")
    out = g.agg(unidades=("latitud", "size"), latitud=("latitud", "mean"), longitud=("longitud", "mean"))
    if sector in d.columns:
        out["sector_dominante"] = g[sector].agg(lambda s: s.mode().iat[0] if not s.mode().empty else None)
        out["pct_sector_dominante"] = g[sector].agg(lambda s: 100 * s.value_counts(normalize=True).iat[0])
    return out.sort_values("unidades", ascending=False)


def distancia_mas_cercana(origenes: pd.DataFrame, destinos: pd.DataFrame) -> np.ndarray:
    """Distancia (km) de cada origen al destino más cercano. Ambos con columnas latitud/longitud."""
    from sklearn.neighbors import BallTree

    arbol = BallTree(np.radians(destinos[["latitud", "longitud"]].to_numpy(dtype=float)), metric="haversine")
    dist, _ = arbol.query(np.radians(origenes[["latitud", "longitud"]].to_numpy(dtype=float)), k=1)
    return dist[:, 0] * R_TIERRA_KM


def _knn_pesos(coords: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    from sklearn.neighbors import BallTree

    arbol = BallTree(np.radians(coords), metric="haversine")
    _, idx = arbol.query(np.radians(coords), k=k + 1)
    return idx[:, 1:], np.full((len(coords), k), 1.0 / k)  # pesos estandarizados por fila


def morans_i(valores: np.ndarray, coords: np.ndarray, k: int = 8, permutaciones: int = 499, semilla: int = 0) -> dict:
    """I de Moran global con pesos KNN estandarizados por fila y p-valor por permutación.

    I = (n / S0) * Σ_i Σ_j w_ij z_i z_j / Σ_i z_i²   (con pesos estandarizados S0 = n)
    I > 0 => valores similares se agrupan en el espacio (clústeres).
    """
    x = np.asarray(valores, dtype=float)
    idx, w = _knn_pesos(np.asarray(coords, dtype=float), k)
    z = x - x.mean()

    def estad(zz):
        return float((zz * (w * zz[idx]).sum(axis=1)).sum() / (zz ** 2).sum())

    obs = estad(z)
    rng = np.random.default_rng(semilla)
    sims = np.array([estad(rng.permutation(z)) for _ in range(permutaciones)])
    p = (np.sum(sims >= obs) + 1) / (permutaciones + 1) if obs >= 0 else (np.sum(sims <= obs) + 1) / (permutaciones + 1)
    return {"I": obs, "esperado": -1 / (len(x) - 1), "p_valor": float(p)}


def getis_ord_gi_star(valores: np.ndarray, coords: np.ndarray, radio_km: float = 1.0) -> np.ndarray:
    """Gi* de Getis-Ord (puntaje z) con pesos binarios por distancia (incluye la propia celda).

    z > 1.96 => punto caliente (95 %), z < -1.96 => punto frío.
    """
    from sklearn.neighbors import BallTree

    x = np.asarray(valores, dtype=float)
    c = np.radians(np.asarray(coords, dtype=float))
    n = len(x)
    vecinos = BallTree(c, metric="haversine").query_radius(c, r=radio_km / R_TIERRA_KM)
    xbar = x.mean()
    s = np.sqrt((x ** 2).mean() - xbar ** 2)
    z = np.empty(n)
    for i, v in enumerate(vecinos):
        wi = len(v)
        num = x[v].sum() - xbar * wi
        den = s * np.sqrt((n * wi - wi ** 2) / (n - 1)) if n > 1 else np.nan
        z[i] = num / den if den else 0.0
    return z
