from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from app.routes.credenciales import router as credenciales_router

# Importaciones limpias de tus routers
from app.routes import vendedores, productos
from app.core.exceptions import validation_exception_handler

app = FastAPI( 
    title="API de Ventas_mi_ruta_sjr",
    description="Gestión de vendedores y productos con conexión a Supabase",
    version="1.0.0",
    docs_url="/docs"
)

# 1. --- CONFIGURACIÓN DE CORS (Indispensable para consumo externo) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite conexiones desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# 2. --- REGISTRO DE EXCEPCIONES ---
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 3. --- REDIRECCIÓN INICIAL ---
@app.get("/", include_in_schema=False)
async def root():
    """Redirige a la documentación al entrar a la raíz"""
    return RedirectResponse(url="/docs")

# 4. --- REGISTRO DE RUTAS ---

# Vendedores
app.include_router(
    vendedores.router, 
    prefix="/api/v1", 
    tags=["Vendedores"]
)

# Productos
app.include_router(
    productos.router, 
    prefix="/api/v1", 
    tags=["Productos"]
)

app.include_router(
    credenciales_router,
    prefix="/api/v1",
    tags=["Credenciales"]
)
# Nota: Si vas a usar la ruta de Tareas (Utils), 
# asegúrate de crear el archivo app/routes/utils.py primero.