from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from src.database import get_session
from src.models.correlativa import Correlativa, CorrelativaBase, CorrelativaCreate, CorrelativaPublic


router = APIRouter(prefix="/correlativas", tags=["Correlativas"])
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
@router.post("/", response_model=CorrelativaPublic, status_code=status.HTTP_201_CREATED)
def crear_correlativa(data: CorrelativaCreate, session: SessionDep):
    db_correlativa = Correlativa.model_validate(data)
    session.add(db_correlativa)
    session.commit()
    session.refresh(db_correlativa)
    return db_correlativa

# GET
@router.get("/", response_model=Page[CorrelativaPublic])
def listar_correlativas(session: SessionDep):
    return paginate(session, select(Correlativa))

@router.get("/{id}", response_model=CorrelativaPublic, response=NOT_FOUND_RESPONSE)
def listar_correlativa_id(id: int, session: SessionDep):
    correlativa = session.get(Correlativa, id)
    if not correlativa:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    return correlativa

# UPDATE
@router.put("/{id}", response_model=CorrelativaPublic, responses=NOT_FOUND_RESPONSE)
def actualizar_correlativa(id: int, data: CorrelativaCreate, session: SessionDep):
    correlativa_db = session.get(Correlativa, id)
    if not correlativa_db:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    correlativa_data = data.model_dump(exclude_unset=True)
    correlativa_db.sqlmodel_update(correlativa_data)
    session.add(correlativa_db)
    session.commit()
    return correlativa_db

# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NOT_CONTENT, responses=NOT_FOUND_RESPONSE)
def borrar_correlativa(id: int, session: SessionDep):
    correlativa = session.get(Correlativa, id)
    if not correlativa:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    session.delete(correlativa)
    session.commit()
    return None



