# auth.py
from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear un enrutador para los endpoints de autenticación
router = APIRouter()

# Configuración de OAuth
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),  # Obtiene el client_id del archivo .env
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),  # Obtiene el client_secret del archivo .env
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    redirect_uri="http://localhost:8000/auth/google/callback",
    client_kwargs={"scope": "openid profile email"}
)

@router.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = "http://localhost:8000/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    return {"email": user_info["email"], "name": user_info["name"]}
