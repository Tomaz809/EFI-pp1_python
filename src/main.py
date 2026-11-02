from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from src.routers import alumnos, carreras, correlativas, materias

app = FastAPI(
    title= "Gestion academica",
    description= "Visualizacion de materias por carrera y regimen de correlativas.",
    version= "1.0.0",
)

app.include_router(alumnos.router)
app.include_router(carreras.router)
app.include_router(materias.router)
app.include_router(correlativas.router)

add_pagination(app)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5500"], #agregar la url de versel cuando se tenga
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)