# Chat con Gemini - Asistente de IA Personal

Una aplicación web moderna para chatear con Google Gemini AI que incluye funcionalidad completa de historial de conversaciones usando SQLite.

![Chat con Gemini](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Características

- ✅ **Chat en tiempo real** con Google Gemini AI
- ✅ **Historial persistente** usando SQLite
- ✅ **Múltiples sesiones** de chat
- ✅ **Interfaz moderna** y responsiva
- ✅ **Gestión de sesiones** (crear, cargar, eliminar)
- ✅ **Base de datos local** sin dependencias externas
- ✅ **API REST** completa
- ✅ **Diseño mobile-first**

## 📋 Requisitos del Sistema

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **Memoria RAM**: Mínimo 512MB
- **Espacio en disco**: 100MB libres
- **Conexión a Internet**: Requerida para API de Gemini

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/camotor/BOT.git
cd BOT
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
API_KEY_GEMINI=tu_clave_api_aqui
```

**¿Cómo obtener la clave API de Gemini?**

1. Visita [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Crea una nueva clave API
4. Copia la clave y pégala en el archivo `.env`

### 5. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:8004`

## 📁 Estructura del Proyecto

```
BOT/
├── app.py                 # Servidor principal FastAPI
├── database.py           # Gestión de base de datos SQLite
├── gemini_chat.py        # Cliente original de Gemini (legacy)
├── requirements.txt      # Dependencias de Python
├── .env                  # Variables de entorno (crear manualmente)
├── .gitignore           # Archivos ignorados por Git
├── README.md            # Este archivo
├── chat_history.db      # Base de datos SQLite (se crea automáticamente)
├── templates/
│   └── index.html       # Plantilla HTML principal
└── static/
    ├── style.css        # Estilos CSS
    └── script.js        # Lógica JavaScript del frontend
```

## 🔧 Configuración Avanzada

### Variables de Entorno

| Variable | Descripción | Valor por defecto | Requerido |
|----------|-------------|-------------------|-----------|
| `API_KEY_GEMINI` | Clave API de Google Gemini | - | ✅ Sí |

### Configuración del Servidor

Para cambiar el puerto del servidor, modifica la línea final en `app.py`:

```python
uvicorn.run(app, host="0.0.0.0", port=8004)  # Cambiar 8004 por el puerto deseado
```

### Base de Datos

La aplicación usa SQLite con las siguientes tablas:

- **chat_sessions**: Almacena información de las sesiones
- **messages**: Almacena todos los mensajes del chat

La base de datos se crea automáticamente en `chat_history.db`.

## 🌐 API Endpoints

### Chat
- `POST /api/chat` - Enviar mensaje al chat
- `GET /api/sessions` - Obtener todas las sesiones
- `POST /api/sessions` - Crear nueva sesión
- `GET /api/sessions/{id}/messages` - Obtener mensajes de una sesión
- `PUT /api/sessions/{id}` - Actualizar título de sesión
- `DELETE /api/sessions/{id}` - Eliminar sesión

### Ejemplo de uso de la API

```bash
# Enviar mensaje
curl -X POST "http://localhost:8004/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hola, ¿cómo estás?"}'

# Obtener sesiones
curl -X GET "http://localhost:8004/api/sessions"
```

## 🐛 Solución de Problemas

### Error: "API_KEY_GEMINI no está configurada"

**Solución**: Verifica que el archivo `.env` existe y contiene la clave API válida.

```bash
# Verificar que el archivo .env existe
ls -la .env

# Verificar el contenido (sin mostrar la clave)
cat .env | grep API_KEY_GEMINI
```

### Error: "Port already in use"

**Solución**: El puerto 8004 está ocupado. Cambia el puerto en `app.py` o mata el proceso:

```bash
# Windows
netstat -ano | findstr :8004
taskkill /PID <PID_NUMBER> /F

# macOS/Linux
lsof -ti:8004 | xargs kill -9
```

### Error: "Failed to load resource: 422"

**Solución**: Problema con la validación de datos. Verifica que tienes la versión correcta de Pydantic:

```bash
pip install --upgrade pydantic
```

### Base de datos corrupta

**Solución**: Elimina el archivo de base de datos para recrearlo:

```bash
rm chat_history.db
# Reinicia la aplicación
python app.py
```

## 📊 Información para Soporte Técnico

### Logs del Sistema

Los logs se muestran en la consola donde ejecutas `python app.py`. Para guardar logs:

```bash
python app.py > app.log 2>&1
```

### Información del Sistema

```bash
# Versión de Python
python --version

# Paquetes instalados
pip list

# Variables de entorno (sin mostrar valores sensibles)
env | grep -v API_KEY
```

### Archivos de Configuración

- **Dependencias**: `requirements.txt`
- **Variables de entorno**: `.env`
- **Base de datos**: `chat_history.db`
- **Logs**: Consola o `app.log`

### Puertos y Servicios

- **Puerto por defecto**: 8004
- **Protocolo**: HTTP
- **Base de datos**: SQLite (local)
- **API externa**: Google Gemini AI

### Comandos de Diagnóstico

```bash
# Verificar conectividad
curl -I http://localhost:8004

# Verificar base de datos
sqlite3 chat_history.db ".tables"

# Verificar dependencias
pip check

# Verificar archivos estáticos
ls -la static/
ls -la templates/
```

## 🔄 Actualizaciones

Para actualizar la aplicación:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📝 Changelog

### v2.0.0 - Con Historial (Actual)
- ✅ Implementado historial completo con SQLite
- ✅ Múltiples sesiones de chat
- ✅ Interfaz renovada con sidebar
- ✅ API REST completa
- ✅ Gestión de sesiones
- ✅ Diseño responsivo

### v1.0.0 - Versión Inicial
- ✅ Chat básico con Gemini
- ✅ Interfaz simple
- ✅ Sin persistencia de datos

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Carlos Cruz** - [GitHub](https://github.com/camotor)

## 🙏 Agradecimientos

- Google por la API de Gemini
- FastAPI por el excelente framework
- SQLite por la base de datos embebida
- La comunidad de Python por las librerías

---

**¿Necesitas ayuda?** Abre un [issue](https://github.com/camotor/BOT/issues) en GitHub.
