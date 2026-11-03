from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from src.database import get_session
from src.models.carrera import (
    Carrera,
    CarreraCreate,
    CarreraPublic,
    CarreraPublicNested,
    CarreraUpdate,
)

router = APIRouter(prefix="/carreras", tags=["Carreras"])
SessionDep = Annotated[Session, Depends(get_session)]

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Recurso no encontrado",
        "content": {
            "application/json": {
                "example": {"detail": "Carrera con id {id} no encontrada"}
            }
        },
    },
}


@router.post("/", response_model=CarreraPublic, status_code=status.HTTP_201_CREATED)
def crear_carrera(data: CarreraCreate, session: SessionDep):
    if session.exec(select(Carrera).where(Carrera.codigo == data.codigo)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El codigo de carrera ya existe"
        )
    db_carrera = Carrera.model_validate(data)
    session.add(db_carrera)
    session.commit()
    session.refresh(db_carrera)
    return db_carrera


@router.get("/", response_model=Page[CarreraPublic])
def listar_carreras(session: SessionDep):
    return paginate(session, select(Carrera).order_by(Carrera.id))


@router.get("/{id}", response_model=CarreraPublicNested, responses=NOT_FOUND_RESPONSE)
def obtener_carrera(id: int, session: SessionDep):
    carrera = session.get(Carrera, id)
    if not carrera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carrera con id {id} no encontrada",
        )
    return carrera


@router.patch("/{id}", response_model=CarreraPublic, responses=NOT_FOUND_RESPONSE)
def actualizar_carrera(id: int, data: CarreraUpdate, session: SessionDep):
    carrera_db = session.get(Carrera, id)
    if not carrera_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carrera con id {id} no encontrada",
        )
    datos = data.model_dump(exclude_unset=True)
    carrera_db.sqlmodel_update(datos)
    session.add(carrera_db)
    session.commit()
    session.refresh(carrera_db)
    return carrera_db


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND_RESPONSE)
def borrar_carrera(id: int, session: SessionDep):
    carrera = session.get(Carrera, id)
    if not carrera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Carrera con id {id} no encontrada",
        )
    session.delete(carrera)
    session.commit()
    return None