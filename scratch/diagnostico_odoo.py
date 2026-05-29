import asyncio
import httpx
import sys

async def run_diagnostico():
    print("=" * 60)
    print("  DIAGNÓSTICO: BÚSQUEDA DE VARIANTES EN ODOO EN VIVO")
    print("=" * 60)

    base_url = "https://tilyngo.odoo.com"
    api_key = "3de59600d375286d00b1814383fb8566c3b123cf"
    headers = {
        "Authorization": f"bearer {api_key}",
        "Content-Type": "application/json",
    }

    url_prod = f"{base_url}/json/2/product.product/search_read"

    # Término ingresado por el usuario/agente: "access point" (con doble s)
    query = "access point"
    
    # 1. Generar variantes
    q_clean = query.lower()
    variants = [query]
    if "access" in q_clean:
        variants.append(q_clean.replace("access", "acces"))
    elif "acces" in q_clean:
        variants.append(q_clean.replace("acces", "access"))
        
    if "swich" in q_clean:
        variants.append(q_clean.replace("swich", "switch"))
    elif "switch" in q_clean:
        variants.append(q_clean.replace("switch", "swich"))
        
    seen = set()
    variants = [v for v in variants if not (v.lower() in seen or seen.add(v.lower()))]
    print(f"Variantes generadas para '{query}': {variants}")

    # 2. Construir dominio dinámico con OR
    sub_domains = []
    for v in variants:
        sub_domains.append(["|", "|", "|",
            ["name", "ilike", v],
            ["default_code", "ilike", v],
            ["barcode", "ilike", v],
            ["categ_id.name", "ilike", v],
        ])
        
    if len(sub_domains) == 1:
        domain = sub_domains[0]
    else:
        domain = []
        for _ in range(len(sub_domains) - 1):
            domain.append("|")
        for sd in sub_domains:
            domain.extend(sd)

    print(f"Dominio construido: {domain}")

    # 3. Realizar consulta a Odoo
    payload = {
        "domain": domain,
        "fields": ["name", "default_code", "list_price", "qty_available"],
        "limit": 5
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.post(url_prod, headers=headers, json=payload)
            print(f"\nStatus Code: {resp.status_code}")
            data = resp.json()
            if isinstance(data, dict) and "error" in data:
                print(f"[ERROR ODOO]: {data['error']}")
            else:
                print(f"[ÉXITO] Resultados devueltos: {len(data)}")
                for p in data:
                    print(f"  - {p.get('name')} | SKU: {p.get('default_code')} | Precio: ${p.get('list_price')} | Stock: {p.get('qty_available')}")
        except Exception as e:
            print(f"Fallo HTTP: {e}")

if __name__ == "__main__":
    asyncio.run(run_diagnostico())
