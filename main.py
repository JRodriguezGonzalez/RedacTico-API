from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from auth import router as auth_router  # Importa el enrutador de autenticación desde auth.py
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

# Configura la sesión para la autenticación
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

# Incluye el enrutador de autenticación en la aplicación principal
app.include_router(auth_router)
