from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from contextlib import asynccontextmanager
from pathlib import Path
from alembic.config import Config
from alembic import command


from src.routers import alumnos, carreras, correlativas, materias

BASE_DIR = Path(__file__).resolve().parent.parent

def run_migrations():
    init_path = BASE_DIR / "alembic.ini"
    alembic_dir = BASE_DIR / "alembic"

    if not init_path.exists():
        raise FileNotFoundError(f"No se encontro alembic")

    alembic_cfg = Config(str(init_path))

    alembic_cfg.set_main_option("script_location", str(alembic_dir))

    command.upgrade(alembic_cfg, "head")

@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


app = FastAPI(
    lifespan=lifespan,
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