# Nova Voice Agent - Asistente de Voz AI Conmutador

## Objetivo del Sistema

Este proyecto consiste en el desarrollo de un asistente inteligente de voz basado en IA, diseñado para optimizar la gestión de llamadas telefónicas empresariales, proporcionar atención al cliente automatizada y ofrecer una plataforma integral para el manejo de extensiones, transferencias e inventario en tiempo real. La aplicación incluye varios módulos interconectados que facilitan la comunicación entre clientes y administradores, mejorando la eficiencia operativa y la experiencia del usuario.

## Características Principales

### Sistema de Gestión de Llamadas e Inventario
El sistema permite registrar extensiones telefónicas mediante un panel administrativo especial, configurando empleados y departamentos. Además, el módulo de inventario ofrece información detallada sobre productos y servicios disponibles, permitiendo a los usuarios consultar especificaciones, precios y stock en tiempo real. Asimismo, el historial de llamadas proporciona un seguimiento exhaustivo de todas las interacciones, indicando duración, fecha, estado de conexión y acciones realizadas por el asistente de IA.

### Integración con Odoo ERP (Cotizaciones y Órdenes)
El conmutador inteligente se conecta de forma directa a **Odoo ERP** utilizando la API JSON-2 externa. Cuando el asistente de voz identifica que el cliente tiene intención real de compra, puede buscar productos y existencias de manera dinámica y registrar cotizaciones o borradores de pedidos de venta (`sale.order`) y crear o asociar clientes (`res.partner`) de forma automática en el sistema Odoo.

### Panel de Administración Protegido
El módulo administrativo está diseñado para la gestión eficiente de la plataforma. Los administradores pueden descargar y gestionar prompts personalizados para la IA, configurar herramientas y funciones disponibles, monitorear sesiones activas en tiempo real, y acceder a registros completos de llamadas. El panel incluye formularios para agregar extensiones, productos al inventario y editar prompts del sistema.

### Asistente de Voz Alimentado por IA
El sistema utiliza tecnología de IA en tiempo real (Google Gemini Live) para entender el lenguaje natural, responder consultas, transferir llamadas, consultar inventario y acceder a información de extensiones. El asistente puede mantener conversaciones fluidas, realizar búsquedas en la base de datos y ejecutar acciones complejas mediante function calling.

## Módulos del Sistema

### 1. **Interfaz de Llamadas (Público)**
- Página web para iniciar llamadas con el asistente de voz.
- Integración con protocolo AudioSocket.
- Conexión WebSocket en tiempo real.
- Interfaz de usuario intuitiva y responsiva.

### 2. **Panel de Administración (Protegido)**
- **Gestión de Extensiones**: CRUD de extensiones telefónicas con información de empleados.
- **Gestión de Inventario**: Control de productos con precios, stock y categorías.
- **Prompts del Sistema**: Edición y carga dinámica de prompts de comportamiento para la IA.
- **Monitoreo de Sesiones**: Visualización de llamadas activas en tiempo real.
- **Historial de Llamadas**: Registro detallado de todas las interacciones.

### 3. **Integración con Odoo ERP**
- Cliente asíncrono robusto para la External JSON-2 API de Odoo.
- Creación automática de clientes (`res.partner`) y presupuestos (`sale.order`).
- Validación de existencias y precios en pesos mexicanos (MXN) y conversión a dólares (USD) para clientes internacionales.

### 4. **Cargador Dinámico de Prompts (Prompt Loader)**
- Configuración modular de prompts mediante plantillas YAML/Markdown (`nova_sales.yaml`, `nova_support.yaml`, etc.).
- Comportamientos preestablecidos según el departamento: Ventas, Soporte, Finanzas y Atención Telefónica.
- Inyección de instrucciones estrictas para el inventario, prevención de alucinaciones y protocolos inmutables de confirmación de compra.

### 5. **Autenticación y Seguridad**
- Sistema de login con usuario y contraseña.
- Tokens JWT para protección de API.
- Rutas públicas para llamadas y login; protegidas para el panel administrativo.
- Expiración automática de sesiones.

### 6. **Base de Datos**
- SQLite para almacenamiento de extensiones.
- Registro de inventario de productos.
- Historial de llamadas y sesiones.
- Seeds de datos iniciales para demostración.

### 7. **API REST**
- Endpoints para gestión de extensiones, inventario, prompts y herramientas.
- Endpoints de autenticación (login/logout).
- WebSocket para comunicación de audio bidireccional.

## Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web de alto rendimiento.
- **Python 3.13+**: Lenguaje de programación.
- **SQLite + aiosqlite**: Base de datos asíncrona.
- **Google Genai**: API de IA (Gemini Live 2.0 / Gemini 2.0 Flash).
- **Panoramisk**: Cliente AMI para Asterisk.
- **PyJWT**: Autenticación con tokens JWT.
- **httpx**: Cliente HTTP asíncrono para las llamadas a la API JSON-2 de Odoo.

### Frontend
- **HTML5 y CSS3**: Interfaz moderna y responsiva.
- **JavaScript Vanilla**: Lógica del lado del cliente.
- **Web Audio API**: Captura y reproducción de audio.
- **LocalStorage**: Almacenamiento de tokens de sesión.

### Infraestructura
- **Asterisk**: Conmutador telefónico privado.
- **AudioSocket**: Protocolo de audio en tiempo real.
- **Uvicorn**: Servidor ASGI.
- **Loguru**: Sistema de logging avanzado.

## Seguridad

El sistema implementa múltiples capas de seguridad:
- **Autenticación JWT**: Tokens firmados con clave secreta.
- **Protección de rutas**: API administrativa requiere autenticación.
- **HTTPS recomendado**: En producción usar conexiones cifradas.
- **Variables de entorno**: Credenciales no expuestas en el código.
- **Validación de entrada**: Sanitización de datos.

## Estructura del Proyecto

```
TestV1_Speech/
├── auth/                          # Autenticación JWT
│   ├── jwt_handler.py            # Gestor de tokens
│   └── dependencies.py           # Protección de rutas
├── api/                          # Endpoints API
│   ├── admin.py                 # Panel administrativo (protegido)
│   ├── auth.py                  # Login/Logout (público)
│   └── health.py                # Health check
├── ai/                           # Motor de IA
│   ├── gemini_live.py           # Cliente Gemini Live
│   ├── odoo_worker.py           # Worker de inventario de Odoo
│   ├── function_registry.py     # Registro de funciones/herramientas
│   └── prompt_loader.py         # Cargador dinámico de prompts
├── actions/                      # Acciones de IA (Function Calling)
│   ├── lookup_extension.py      # Buscar extensión en base de datos
│   ├── lookup_inventory.py      # Buscar producto en inventario
│   ├── create_odoo_order.py     # Crear requisición/presupuesto en Odoo
│   ├── transfer_call.py         # Transferir llamada
│   └── end_call.py              # Terminar llamada
├── core/                         # Lógica central del sistema
│   ├── session.py               # Gestor de sesiones activas
│   ├── audio_processor.py       # Procesamiento de audio
│   ├── odoo_client.py           # Cliente asíncrono JSON-2 API de Odoo
│   ├── exchange_updater.py      # Actualizador de tipo de cambio USD/MXN
│   ├── vad.py                   # Detección de Actividad de Voz (VAD)
│   └── events.py                # Sistema de eventos
├── database/                     # Persistencia de Datos
│   ├── manager.py               # Gestor de BD
│   ├── models.py                # Modelos de datos
│   └── seed.py                  # Datos iniciales
├── telephony/                    # Integración Asterisk
│   ├── ami_client.py            # Cliente AMI
│   └── audiosocket_server.py    # Servidor AudioSocket
├── config/                       # Configuración general
│   ├── settings.py              # Variables de entorno y ajustes
│   ├── prompts/                 # Plantillas de Prompts de IA (YAML / MD)
│   └── tools/                   # Definición de herramientas (JSON)
├── web/                          # Frontend de la aplicación
│   ├── index.html               # Página de llamadas
│   ├── admin.html               # Panel de control administrativo
│   ├── login.html               # Página de inicio de sesión
│   ├── js/
│   │   ├── app.js              # Lógica de llamadas y audio
│   │   └── admin.js            # Lógica del panel administrativo
│   └── css/
│       └── styles.css          # Estilos CSS generales
├── main.py                       # Aplicación FastAPI principal
├── requirements.txt              # Dependencias de Python
└── .env.example                  # Variables de entorno de ejemplo
```

## Instalación y Uso

### Requisitos Previos
- Python 3.10+
- Asterisk (para telefonía/AMI)
- Google API Key (para Gemini Live)
- Credenciales de Odoo (opcional, para integración ERP)

### Instalación

```bash
# 1. Clonar o descargar el proyecto
cd TestV1_Speech

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores reales (ver sección de Configuración de Odoo)

# 5. Ejecutar servidor
python main.py
```

### Configuración de Odoo
Para habilitar el registro automático de presupuestos en Odoo, añade las siguientes líneas a tu archivo `.env`:

```env
ODOO_BASE_URL=https://tu-instancia.odoo.com
ODOO_DB=tu_base_de_datos
ODOO_API_KEY=tu_api_key_de_odoo
```

### Acceso local

- **Llamadas (público)**: http://localhost:8000/
- **Login**: http://localhost:8000/login
- **Admin**: http://localhost:8000/admin (requiere autenticación)

### Credenciales Predeterminadas

- **Usuario**: admin
- **Contraseña**: admin123

⚠️ **Cambiar estas credenciales en producción.**

## Proceso de Desarrollo

Este informe documenta el proceso de desarrollo, desde la planificación de la base de datos hasta los requisitos técnicos necesarios y la integración de múltiples tecnologías utilizadas para estructurar cada fase del proyecto. El desarrollo incluyó:

1. **Diseño de arquitectura**: Separación de responsabilidades en módulos.
2. **Integración de IA en tiempo real**: Conexión con Google Gemini Live 2.0 y soporte para function calling.
3. **Módulo de Odoo**: Desarrollo de un cliente JSON-2 robusto para operaciones atómicas.
4. **Sistema de Prompts Dinámicos**: Implementación del `PromptLoader` para estructurar la personalidad y capacidades del agente según el departamento seleccionado.
5. **Autenticación y Seguridad**: Implementación de protección JWT en APIs.
6. **Integración telefónica**: Conexión con Asterisk y AudioSocket.

## Próximos Pasos Recomendados

1. Configurar Asterisk y AudioSocket en el entorno objetivo.
2. Obtener API Key de Google Gemini.
3. Configurar la URL de Odoo y su respectiva API Key.
4. Personalizar prompts del sistema para ajustar el tono a tu negocio.
5. Migrar a una base de datos más robusta (PostgreSQL) para producción.
6. Implementar análisis y reportes avanzados de llamadas.

## Contacto y Soporte

Para más información o soporte técnico, consulta la documentación incluida:
- [AUTENTICACION.md](file:///c:/Users/jjzg_/Desktop/WEB%20APPS/TestV1_Speech/AUTENTICACION.md) - Guía de autenticación
- [CAMBIOS_AUTENTICACION.md](file:///c:/Users/jjzg_/Desktop/WEB%20APPS/TestV1_Speech/CAMBIOS_AUTENTICACION.md) - Cambios de autenticación implementados

---

**Nova Voice Agent v1.0** - Asistente Inteligente de Voz para Empresas
