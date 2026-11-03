from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from src.database import get_session
from src.models.correlativa import Correlativa, CorrelativaCreate, CorrelativaPublic
from src.models.materia import Materia

router = APIRouter(prefix="/correlativas", tags=["Correlativas"])
SessionDep = Annotated[Session, Depends(get_session)]

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Recurso no encontrado",
        "content": {
            "application/json": {
                "example": {"detail": "Relacion de correlatividad no encontrada"}
            }
        },
    },
}


@router.post("/", response_model=CorrelativaPublic, status_code=status.HTTP_201_CREATED)
def vincular_correlativa(data: CorrelativaCreate, session: SessionDep):
    if data.materia_id == data.correlativa_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Una materia no puede ser correlativa de si misma",
        )

    if not session.get(Materia, data.materia_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="La materia base no existe"
        )
    if not session.get(Materia, data.correlativa_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="La materia correlativa no existe"
        )

    relacion_existente = session.get(Correlativa, (data.materia_id, data.correlativa_id))
    if relacion_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La relacion de correlatividad ya se encuentra registrada",
        )

    db_correlativa = Correlativa.model_validate(data)
    session.add(db_correlativa)
    session.commit()
    session.refresh(db_correlativa)
    return db_correlativa


@router.get("/", response_model=Page[CorrelativaPublic])
def listar_correlativas(session: SessionDep):
    return paginate(session, select(Correlativa))


@router.delete(
    "/{materia_id}/{correlativa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=NOT_FOUND_RESPONSE,
)
def borrar_correlativa(materia_id: int, correlativa_id: int, session: SessionDep):
    relacion = session.get(Correlativa, (materia_id, correlativa_id))
    if not relacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relacion de correlatividad no encontrada",
        )
    session.delete(relacion)
    session.commit()
    return None