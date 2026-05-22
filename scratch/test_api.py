import http.client
import json
import time

def run_api_tests():
    print("=== Iniciando Pruebas de Integración de API ===")
    
    # 1. Probar salud
    conn = http.client.HTTPConnection("127.0.0.1", 8080)
    try:
        conn.request("GET", "/health")
        res = conn.getresponse()
        print(f"1. /health: Status={res.status}")
        data = json.loads(res.read().decode())
        print(f"   Respuesta: {data}")
    except Exception as e:
        print(f"Error al conectar con el servidor local: {e}")
        print("Asegúrate de que el servidor está corriendo en el puerto 8080.")
        return

    # 2. Probar Login con credenciales incorrectas
    print("\n2. Intentando Login con credenciales incorrectas...")
    payload = json.dumps({"username": "admin", "password": "wrongpassword"})
    headers = {"Content-Type": "application/json"}
    conn.request("POST", "/api/auth/login", payload, headers)
    res = conn.getresponse()
    print(f"   Status={res.status}")
    body = res.read().decode()
    print(f"   Respuesta: {body}")
    assert res.status == 401, f"Se esperaba 401 pero se obtuvo {res.status}"

    # 3. Probar Login con credenciales válidas por defecto (admin / nova1234)
    print("\n3. Intentando Login con credenciales correctas...")
    payload = json.dumps({"username": "admin", "password": "nova1234"})
    conn.request("POST", "/api/auth/login", payload, headers)
    res = conn.getresponse()
    print(f"   Status={res.status}")
    body = res.read().decode()
    print(f"   Respuesta: {body}")
    assert res.status == 200, f"Se esperaba 200 pero se obtuvo {res.status}"
    
    # Extraer la cookie de sesión de las cabeceras
    cookie_header = res.getheader("Set-Cookie")
    print(f"   Cookie Set-Cookie recibida: {cookie_header}")
    assert cookie_header is not None, "No se recibió la cookie session_token"
    
    # Extraer el valor exacto del session_token
    session_token = ""
    for cookie in cookie_header.split(";"):
        if "session_token=" in cookie:
            session_token = cookie.split("=")[1].strip()
            break
    print(f"   Token de sesión extraído: {session_token}")

    # 4. Intentar acceder a ruta protegida sin autenticar
    print("\n4. Accediendo a /api/admin/prompts sin autenticar...")
    conn.request("GET", "/api/admin/prompts")
    res = conn.getresponse()
    print(f"   Status={res.status}")
    body = res.read().decode()
    print(f"   Respuesta: {body}")
    assert res.status == 401, f"Se esperaba 401 pero se obtuvo {res.status}"

    # 5. Acceder a ruta protegida usando la cookie session_token
    print("\n5. Accediendo a /api/admin/prompts autenticado...")
    auth_headers = {"Cookie": f"session_token={session_token}"}
    conn.request("GET", "/api/admin/prompts", headers=auth_headers)
    res = conn.getresponse()
    print(f"   Status={res.status}")
    body = res.read().decode()
    print(f"   Respuesta: {body}")
    assert res.status == 200, f"Se esperaba 200 pero se obtuvo {res.status}"

    # 6. Cerrar sesión
    print("\n6. Cerrando sesión en /api/auth/logout...")
    conn.request("POST", "/api/auth/logout", headers=auth_headers)
    res = conn.getresponse()
    print(f"   Status={res.status}")
    body = res.read().decode()
    print(f"   Respuesta: {body}")
    assert res.status == 200, f"Se esperaba 200 pero se obtuvo {res.status}"

    # 7. Verificar que el token quedó invalidado
    print("\n7. Accediendo a /api/admin/prompts post-logout...")
    conn.request("GET", "/api/admin/prompts", headers=auth_headers)
    res = conn.getresponse()
    print(f"   Status={res.status}")
    body = res.read().decode()
    print(f"   Respuesta: {body}")
    assert res.status == 401, f"Se esperaba 401 pero se obtuvo {res.status}"

    print("\n=== ¡SUCCESS! Todas las pruebas de integración pasaron con éxito ===")

if __name__ == "__main__":
    run_api_tests()
