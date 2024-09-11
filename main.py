from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from appv1.routers import users
from db.database import test_db_connection
from appv1.routers import login, users, roles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir en el objeto app los routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(login.router, prefix="/access", tags=["access"])
app.include_router(roles.router, prefix="/role", tags=["role"])

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)

@app.on_event("startup")
def on_startup():
    test_db_connection()

@app.get("/")
def read_root():
    return {
                "message": "ADSO 2670586",
                "autor": "Diego Legarda"
            }
