import os
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Configura la clave de API para la biblioteca de Gemini
api_key = os.environ.get("API_KEY_GEMINI")
if not api_key or api_key == "YOUR_API_KEY":
    raise ValueError("API_KEY_GEMINI no está configurada. Por favor, añade tu clave al archivo .env.")

genai.configure(api_key=api_key)

# Inicializa el modelo
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount templates
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_api(message: Message):
    if not message.message:
        return JSONResponse(content={'error': 'No message provided'}, status_code=400)

    try:
        response = chat.send_message(message.message)
        bot_response = response.text
        return JSONResponse(content={'reply': bot_response})
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
