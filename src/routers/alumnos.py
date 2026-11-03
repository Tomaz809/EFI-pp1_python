from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, select

from src.database import get_session
from src.models.alumno import (
    Alumno,
    AlumnoCreate,
    AlumnoPublic,
    AlumnoPublicNested,
    AlumnoUpdate,
)

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])
SessionDep = Annotated[Session, Depends(get_session)]

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Recurso no encontrado",
        "content": {
            "application/json": {
                "example": {"detail": "Alumno con id {id} no encontrado"}
            }
        },
    },
}


@router.post("/", response_model=AlumnoPublic, status_code=status.HTTP_201_CREATED)
def crear_alumno(data: AlumnoCreate, session: SessionDep):
    if session.exec(select(Alumno).where(Alumno.dni == data.dni)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El DNI ya se encuentra registrado"
        )
    if session.exec(select(Alumno).where(Alumno.email == data.email)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El Email ya se encuentra registrado"
        )
    if session.exec(select(Alumno).where(Alumno.legajo == data.legajo)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El legajo ya se encuentra registrado"
        )

    db_alumno = Alumno.model_validate(data)
    session.add(db_alumno)
    session.commit()
    session.refresh(db_alumno)
    return db_alumno


@router.get("/", response_model=Page[AlumnoPublic])
def listar_alumnos(session: SessionDep):
    return paginate(session, select(Alumno).order_by(Alumno.id))


@router.get("/{id}", response_model=AlumnoPublicNested, responses=NOT_FOUND_RESPONSE)
def obtener_alumno(id: int, session: SessionDep):
    alumno = session.get(Alumno, id)
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con id {id} no encontrado",
        )
    return alumno


@router.patch("/{id}", response_model=AlumnoPublic, responses=NOT_FOUND_RESPONSE)
def actualizar_alumno(id: int, data: AlumnoUpdate, session: SessionDep):
    alumno_db = session.get(Alumno, id)
    if not alumno_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con id {id} no encontrado",
        )
    datos = data.model_dump(exclude_unset=True)
    alumno_db.sqlmodel_update(datos)
    session.add(alumno_db)
    session.commit()
    session.refresh(alumno_db)
    return alumno_db


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND_RESPONSE)
def borrar_alumno(id: int, session: SessionDep):
    alumno = session.get(Alumno, id)
    if not alumno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alumno con id {id} no encontrado",
        )
    session.delete(alumno)
    session.commit()
    return None