from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from appv1.routers import category, transaction, users
from db.database import test_db_connection
from appv1.routers import login, users, roles, prueba

app = FastAPI()
# Montar la carpeta estática que permitira almacenar 
# y usar archivos desde rutas externas
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir en el objeto app los routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(login.router, prefix="/access", tags=["access"])
app.include_router(roles.router, prefix="/role", tags=["role"])
app.include_router(category.router, prefix="/category", tags=["category"])
app.include_router(transaction.router, prefix="/transaction", tags=["transaction"])
app.include_router(prueba.router, prefix="/prueba", tags=["prueba"])

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
