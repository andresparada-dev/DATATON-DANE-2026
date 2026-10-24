#!/usr/bin/env python3
"""Construye ruta2/entrega/agente_voz/asistente_voz_cenu.html: página del agente de voz con el SDK de ElevenLabs incrustado.

SDK: @elevenlabs/client 1.26.0 (dist/lib.iife.js, global `ElevenLabsClient`), copiado en ruta2/vendor/.
Datos de la tabla: ruta2/insumos/dashboard_data_api.js (salida de la API).
"""

import json
import re
from pathlib import Path

R = Path(__file__).resolve().parent
AGENT_ID = "agent_5901m5q8fk19fzbsy4zh3d8ngcx4"


def main():
    js = (R / "insumos" / "dashboard_data_api.js").read_text(encoding="utf-8")
    divs = []
    for obj in re.findall(r"\{(.*?)\}", js, flags=re.S):
        def g(k):
            m = re.search(rf'\b{k}: "([^"]*)"', obj) or re.search(rf'\b{k}: ([^,\s}}]+)', obj)
            return m.group(1)
        divs.append({"div": g("division"), "name": g("name"), "units": int(g("units")), "low": float(g("low")),
                     "high": float(g("high")), "lowP": float(g("lowPers")), "tipo": g("tipologia")})
    corto = {"47": "Comercio al por menor", "56": "Comidas y bebidas", "45": "Vehículos y motos", "96": "Servicios personales",
             "46": "Comercio al por mayor", "95": "Reparación efectos pers.", "86": "Salud humana", "85": "Educación",
             "14": "Confección", "25": "Productos de metal", "10": "Alimentos", "52": "Almacenamiento"}
    tipo = {"Señal de subsistencia": "Subsistencia", "Base para escalar": "Escalar"}
    for d in divs:
        d["name"] = corto.get(d["div"], d["name"])
        d["tipo_corto"] = tipo.get(d["tipo"], d["tipo"])
    html = (R / "plantilla_asistente.html").read_text(encoding="utf-8")
    html = html.replace("__DIVS__", json.dumps(divs, ensure_ascii=False)).replace("__AGENT_ID__", AGENT_ID)
    sdk = (R / "vendor" / "elevenlabs-client-1.26.0.iife.js").read_text(encoding="utf-8")
    html = html.replace("<script>__SDK__</script>", "<script>" + sdk.replace("</script", "<\\/script") + "</script>")
    assert "__" not in re.sub(r"<script>.*?</script>", "", html, flags=re.S).replace("__proto__", ""), "placeholder sin reemplazar"
    dest = R / "entrega" / "agente_voz" / "asistente_voz_cenu.html"
    dest.write_text(html, encoding="utf-8")
    print("->", dest, f"({dest.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
