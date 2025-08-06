import os
import uuid
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel
from database import ChatDatabase

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Configura la clave de API para la biblioteca de Gemini
api_key = os.environ.get("API_KEY_GEMINI")
if not api_key or api_key == "YOUR_API_KEY":
    raise ValueError("API_KEY_GEMINI no está configurada. Por favor, añade tu clave al archivo .env.")

genai.configure(api_key=api_key)

# Inicializa el modelo
model = genai.GenerativeModel('gemini-1.5-flash')

# Inicializa la base de datos
db = ChatDatabase()

app = FastAPI()

# Diccionario para mantener las sesiones de chat activas
active_chats = {}

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount templates
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    message: str
    session_id: Optional[str] = None

class SessionCreate(BaseModel):
    title: Optional[str] = None

class SessionUpdate(BaseModel):
    title: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_api(message: Message):
    if not message.message:
        return JSONResponse(content={'error': 'No message provided'}, status_code=400)

    try:
        # Si no hay session_id, crear una nueva sesión
        if not message.session_id:
            session_id = str(uuid.uuid4())
            db.create_session(session_id)
            active_chats[session_id] = model.start_chat(history=[])
        else:
            session_id = message.session_id
            
            # Si la sesión no está activa, cargar historial
            if session_id not in active_chats:
                history = []
                messages = db.get_session_messages(session_id)
                
                # Convertir mensajes a formato de Gemini
                for msg in messages:
                    if msg['type'] == 'user':
                        history.append({'role': 'user', 'parts': [msg['content']]})
                    else:
                        history.append({'role': 'model', 'parts': [msg['content']]})
                
                active_chats[session_id] = model.start_chat(history=history)

        # Guardar mensaje del usuario
        db.add_message(session_id, 'user', message.message)
        
        # Enviar mensaje al modelo
        chat_session = active_chats[session_id]
        response = chat_session.send_message(message.message)
        bot_response = response.text
        
        # Guardar respuesta del bot
        db.add_message(session_id, 'bot', bot_response)
        
        return JSONResponse(content={
            'reply': bot_response,
            'session_id': session_id
        })
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

@app.post("/api/sessions")
async def create_session(session_data: SessionCreate):
    """Crear una nueva sesión de chat"""
    session_id = str(uuid.uuid4())
    success = db.create_session(session_id, session_data.title)
    
    if success:
        active_chats[session_id] = model.start_chat(history=[])
        return JSONResponse(content={'session_id': session_id})
    else:
        raise HTTPException(status_code=500, detail="Error creating session")

@app.get("/api/sessions")
async def get_sessions():
    """Obtener todas las sesiones de chat"""
    sessions = db.get_all_sessions()
    return JSONResponse(content={'sessions': sessions})

@app.get("/api/sessions/{session_id}/messages")
async def get_session_messages(session_id: str):
    """Obtener mensajes de una sesión específica"""
    messages = db.get_session_messages(session_id)
    return JSONResponse(content={'messages': messages})

@app.put("/api/sessions/{session_id}")
async def update_session(session_id: str, session_data: SessionUpdate):
    """Actualizar título de una sesión"""
    success = db.update_session_title(session_id, session_data.title)
    
    if success:
        return JSONResponse(content={'success': True})
    else:
        raise HTTPException(status_code=500, detail="Error updating session")

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Eliminar una sesión"""
    success = db.delete_session(session_id)
    
    # Remover de sesiones activas si existe
    if session_id in active_chats:
        del active_chats[session_id]
    
    if success:
        return JSONResponse(content={'success': True})
    else:
        raise HTTPException(status_code=500, detail="Error deleting session")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
