# Nova Voice Agent - Asistente de Voz AI Conmutador

## Objetivo del Sistema

Este proyecto consiste en el desarrollo de un asistente inteligente de voz basado en IA, diseñado para optimizar la gestión de llamadas telefónicas empresariales, proporcionar atención al cliente automatizada y ofrecer una plataforma integral para el manejo de extensiones y transferencias. La aplicación incluye varios módulos interconectados que facilitan la comunicación entre clientes y administradores, mejorando la eficiencia operativa y la experiencia del usuario.

## Características Principales

### Sistema de Gestión de Llamadas
El sistema permite registrar extensiones telefónicas mediante un panel administrativo especial, configurando empleados y departamentos. Además, el módulo de inventario ofrece información detallada sobre productos y servicios disponibles, permitiendo a los usuarios consultar especificaciones, precios y stock en tiempo real. Asimismo, el historial de llamadas proporciona un seguimiento exhaustivo de todas las interacciones, indicando duración, fecha, estado de conexión y acciones realizadas por el asistente de IA.

### Panel de Administración Protegido
El módulo administrativo está diseñado para la gestión eficiente de la plataforma. Los administradores pueden descargar y gestionar prompts personalizados para la IA, configurar herramientas y funciones disponibles, monitorear sesiones activas en tiempo real, y acceder a registros completos de llamadas. El panel incluye formularios para agregar extensiones, productos al inventario y editar prompts del sistema.

### Asistente de Voz Alimentado por IA
El sistema utiliza tecnología de IA en tiempo real (Google Gemini Live) para entender el lenguaje natural, responder consultas, transferir llamadas, consultar inventario y acceder a información de extensiones. El asistente puede mantener conversaciones fluidas, realizar búsquedas en la base de datos y ejecutar acciones complejas mediante function calling.

## Módulos del Sistema

### 1. **Interfaz de Llamadas (Público)**
- Página web para iniciar llamadas con el asistente de voz
- Integración con protocolo AudioSocket
- Conexión WebSocket en tiempo real
- Interfaz de usuario intuitiva y responsiva

### 2. **Panel de Administración (Protegido)**
- **Gestión de Extensiones**: CRUD de extensiones telefónicas con información de empleados
- **Gestión de Inventario**: Control de productos con precios, stock y categorías
- **Prompts del Sistema**: Edición de los prompts que guían el comportamiento de la IA
- **Monitoreo de Sesiones**: Visualización de llamadas activas en tiempo real
- **Historial de Llamadas**: Registro detallado de todas las interacciones

### 3. **Autenticación y Seguridad**
- Sistema de login con usuario y contraseña
- Tokens JWT para protección de API
- Rutas públicas para llamadas y login
- Rutas protegidas para panel administrativo
- Expiración automática de sesiones

### 4. **Base de Datos**
- SQLite para almacenamiento de extensiones
- Registro de inventario de productos
- Historial de llamadas y sesiones
- Seeds de datos iniciales para demostración

### 5. **API REST**
- Endpoints para gestión de extensiones
- Endpoints para gestión de inventario
- Endpoints para consulta de prompts y herramientas
- Endpoints de autenticación (login/logout)
- WebSocket para comunicación de audio bidireccional

## Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web de alto rendimiento
- **Python 3.13+**: Lenguaje de programación
- **SQLite + aiosqlite**: Base de datos asíncrona
- **Google Genai**: API de IA (Gemini Live 2.0)
- **Panoramisk**: Cliente AMI para Asterisk
- **PyJWT**: Autenticación con tokens JWT

### Frontend
- **HTML5 y CSS3**: Interfaz moderna y responsiva
- **JavaScript Vanilla**: Lógica del lado del cliente
- **Web Audio API**: Captura y reproducción de audio
- **LocalStorage**: Almacenamiento de tokens de sesión

### Infraestructura
- **Asterisk**: Conmutador telefónico privado
- **AudioSocket**: Protocolo de audio en tiempo real
- **Uvicorn**: Servidor ASGI
- **Loguru**: Sistema de logging avanzado

## Seguridad

El sistema implementa múltiples capas de seguridad:

- **Autenticación JWT**: Tokens firmados con clave secreta
- **Protección de rutas**: API administrativa requiere autenticación
- **HTTPS recomendado**: En producción usar conexiones cifradas
- **Variables de entorno**: Credenciales no hardcodeadas
- **Validación de entrada**: Sanitización de datos
- **Rate limiting**: Puede implementarse para prevenir abuso

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
│   ├── gemini_live.py           # Cliente Gemini
│   ├── function_registry.py     # Registro de funciones
│   └── prompt_loader.py         # Cargador de prompts
├── actions/                      # Acciones de IA
│   ├── lookup_extension.py      # Buscar extensión
│   ├── lookup_inventory.py      # Buscar producto
│   ├── transfer_call.py         # Transferir llamada
│   └── end_call.py              # Terminar llamada
├── core/                         # Lógica central
│   ├── session.py               # Gestor de sesiones
│   ├── audio_processor.py       # Procesamiento de audio
│   └── events.py                # Sistema de eventos
├── database/                     # Persistencia
│   ├── manager.py               # Gestor de BD
│   ├── models.py                # Modelos de datos
│   └── seed.py                  # Datos iniciales
├── telephony/                    # Integración Asterisk
│   ├── ami_client.py            # Cliente AMI
│   └── audiosocket_server.py    # Servidor AudioSocket
├── config/                       # Configuración
│   ├── settings.py              # Variables de entorno
│   ├── prompts/                 # Prompts de IA
│   └── tools/                   # Definición de herramientas
├── web/                          # Frontend
│   ├── index.html               # Página de llamadas
│   ├── admin.html               # Panel admin
│   ├── login.html               # Página de login
│   ├── js/
│   │   ├── app.js              # Lógica de llamadas
│   │   └── admin.js            # Lógica de admin
│   └── css/
│       └── styles.css          # Estilos
├── main.py                       # Aplicación principal
├── requirements.txt              # Dependencias
└── .env.example                  # Variables de ejemplo
```

## Instalación y Uso

### Requisitos Previos
- Python 3.10+
- Asterisk (para telefonía)
- Google API Key (para Gemini)

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
# Editar .env con valores reales

# 5. Ejecutar servidor
python main.py
```

### Acceso

- **Llamadas (público)**: http://localhost:8000/
- **Login**: http://localhost:8000/login
- **Admin**: http://localhost:8000/admin (requiere autenticación)

### Credenciales Predeterminadas

- **Usuario**: admin
- **Contraseña**: admin123

⚠️ **Cambiar en producción**

## Proceso de Desarrollo

Este informe documenta el proceso de desarrollo, desde la planificación de la base de datos hasta los requisitos técnicos necesarios y la integración de múltiples tecnologías utilizadas para estructurar cada fase del proyecto. El desarrollo incluyó:

1. **Diseño de arquitectura**: Separación de responsabilidades en módulos
2. **Implementación de IA**: Integración con Google Gemini Live 2.0
3. **Sistema de autenticación**: Tokens JWT para seguridad
4. **API REST**: Endpoints para gestión administrativo
5. **Interfaz de usuario**: Diseño responsivo y accesible
6. **Integración telefónica**: Conexión con Asterisk y AudioSocket
7. **Testing**: Validación del sistema de autenticación

## Próximos Pasos Recomendados

1. Configurar Asterisk y AudioSocket
2. Obtener API Key de Google Gemini
3. Personalizar prompts del sistema
4. Agregar más funciones al IA
5. Implementar base de datos más robusta (PostgreSQL)
6. Agregar soporte para múltiples idiomas
7. Implementar análisis y reportes avanzados
8. Escalar a producción con HTTPS

## Contacto y Soporte

Para más información o soporte técnico, consulta la documentación incluida:
- [AUTENTICACION.md](AUTENTICACION.md) - Guía de autenticación
- [CAMBIOS_AUTENTICACION.md](CAMBIOS_AUTENTICACION.md) - Cambios implementados

---

**Nova Voice Agent v1.0** - Asistente Inteligente de Voz para Empresas
