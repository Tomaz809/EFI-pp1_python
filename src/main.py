from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from src.routers import alumnos, carreras, correlativas, materias

app = FastAPI(
    title="Gestion Academica",
    description="API para gestion de carreras, materias, correlatividades y alumnos.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5500",
        # agregar url de vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(carreras.router)
app.include_router(materias.router)
app.include_router(alumnos.router)
app.include_router(correlativas.router)

add_pagination(app)