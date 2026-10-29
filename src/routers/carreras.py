from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from src.database import get_session
from src.models.carrera import Carrera, CarreraCreate, CarreraPublic, CarreraPublicNested


router = APIRouter(prefix="/carreras", tags=["Carreras"])
SessionDep = Annotated[Session, Depends(get_session)]

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Carrera con id {id} no encontrada",
                }
            }
        },
    },
}

# CREATE
@router.post("/", response_model=CarreraPublic, status_code=status.HTTP_201_CREATED)
def crear_carrera(data: CarreraCreate, session: SessionDep):
    db_carrera = Carrera.model_validate(data)
    session.add(db_carrera)
    session.commit()
    session.refresh(db_carrera)
    return db_carrera

# GET
@router.get("/", response_model=Page[CarreraPublic])
def listar_carreras(session: SessionDep):
    return paginate(session, select(Carrera))

@router.get("/{id}", response_model=CarreraPublic, responses=NOT_FOUND_RESPONSE)
def listar_carrera_id(id: int, session: SessionDep):
    carrera = session.get(Carrera, id)
    if not carrera:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    return carrera

# UPDATE
@router.put("/{id}", response_model=CarreraPublic)
def actualizar_carrera(id: int, data: CarreraCreate, session: SessionDep):
    carrera_db = session.get(Carrera, id)
    if not carrera_db:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    carrera_data = data.model_dump(exclude_unset=True)
    carrera_db.sqlmodel_update(carrera_data)
    session.commit()
    session.refresh(carrera_db)
    return carrera_db

# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND_RESPONSE)
def borrar_carrera(id: int, session: SessionDep):
    carrera = session.get(Carrera, id)
    if not carrera:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    session.delete(carrera)
    session.commit()
    return None