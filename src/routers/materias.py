from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from src.database import get_session
from src.models.correlativa import Correlativa
from src.models.materia import (
    Materia,
    MateriaCreate,
    MateriaPublic,
    MateriaPublicNested,
    MateriaUpdate,
)

router = APIRouter(prefix="/materias", tags=["Materias"])
SessionDep = Annotated[Session, Depends(get_session)]

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Recurso no encontrado",
        "content": {
            "application/json": {
                "example": {"detail": "Materia con id {id} no encontrada"}
            }
        },
    },
}


@router.post("/", response_model=MateriaPublic, status_code=status.HTTP_201_CREATED)
def crear_materia(data: MateriaCreate, session: SessionDep):
    if session.exec(select(Materia).where(Materia.codigo == data.codigo)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El codigo de materia ya existe"
        )
    db_materia = Materia.model_validate(data)
    session.add(db_materia)
    session.commit()
    session.refresh(db_materia)
    return db_materia


@router.get("/", response_model=Page[MateriaPublic])
def listar_materias(session: SessionDep):
    relaciones = session.exec(select(Correlativa)).all()
    mapa_correlativas: dict[int, list[int]] = {}
    for r in relaciones:
        mapa_correlativas.setdefault(r.materia_id, []).append(r.correlativa_id)

    query = select(Materia).order_by(Materia.anio, Materia.id)
    paginada = paginate(session, query)

    items_public = []
    for m in paginada.items:
        m_dict = m.model_dump()
        m_dict["correlativas_ids"] = mapa_correlativas.get(m.id, [])
        items_public.append(MateriaPublic.model_validate(m_dict))

    paginada.items = items_public
    return paginada


@router.get("/{id}", response_model=MateriaPublicNested, responses=NOT_FOUND_RESPONSE)
def obtener_materia(id: int, session: SessionDep):
    materia = session.get(Materia, id)
    if not materia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Materia con id {id} no encontrada",
        )

    ids_requisitos = session.exec(
        select(Correlativa.correlativa_id).where(Correlativa.materia_id == id)
    ).all()
    materias_requisito = (
        session.exec(select(Materia).where(Materia.id.in_(ids_requisitos))).all()
        if ids_requisitos
        else []
    )

    respuesta = MateriaPublicNested.model_validate(materia)
    respuesta.correlativas = [MateriaPublic.model_validate(m) for m in materias_requisito]
    return respuesta


@router.patch("/{id}", response_model=MateriaPublic, responses=NOT_FOUND_RESPONSE)
def actualizar_materia(id: int, data: MateriaUpdate, session: SessionDep):
    materia_db = session.get(Materia, id)
    if not materia_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Materia con id {id} no encontrada",
        )
    datos = data.model_dump(exclude_unset=True)
    materia_db.sqlmodel_update(datos)
    session.add(materia_db)
    session.commit()
    session.refresh(materia_db)
    return materia_db


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND_RESPONSE)
def borrar_materia(id: int, session: SessionDep):
    materia = session.get(Materia, id)
    if not materia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Materia con id {id} no encontrada",
        )
    session.delete(materia)
    session.commit()
    return None