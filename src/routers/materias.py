from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from src.database import get_session
from src.models.materia import Materia, MateriaCreate, MateriaPublic, MateriaPublicNested


router = APIRouter(prefix="/materias", tags=["Materias"])
SessionDep = Annotated[Session, Depends(get_session)]

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Materia con id {id} no encontrada",
                }
            }
        },
    },
}

# CREATE
@router.post("/", response_model=MateriaPublic, status_code=status.HTTP_201_CREATED)
def crear_materia(data: MateriaCreate, session: SessionDep):
    db_materia = Materia.model_validate(data)
    session.add(db_materia)
    session.commit()
    session.refresh(db_materia)
    return db_materia

# GET
@router.get("/", response_model=Page[MateriaPublic])
def listar_materias(session: SessionDep):
    return paginate(session, select(Materia))

@router.get("/{id}", response_model=MateriaPublic, responses=NOT_FOUND_RESPONSE)
def listar_materia_id(id: int, session: SessionDep):
    materia = session.get(Materia, id)
    if not materia:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    return materia

# UPDATE
@router.put("/{id}", response_model=MateriaPublic, responses=NOT_FOUND_RESPONSE)
def actualizar_materia(id: int, data: MateriaCreate, session: SessionDep):
    materia_db = session.get(Materia, id)
    if not materia_db:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    materia_data = data.model_dump(exclude_unset=True)
    materia_db.sqlmodel_update(materia_data)
    session.add(materia_db)
    session.commit()
    session.refresh(materia_db)
    return materia_db

# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND_RESPONSE)
def borrar_materia(id: int, session: SessionDep):
    materia = session.get(Materia, id)
    if not materia:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    session.delete(materia)
    session.commit()
    return None