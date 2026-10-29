from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from src.database import get_session
from src.models.alumno import Alumno, AlumnoCreate, AlumnoPublic, AlumnoPublicNested

router = APIRouter(prefix="/alumnos", tags=["Alumno"])

SessionDep = Annotated[Session, Depends(get_session)]

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Alumno con id {id} no encontrado",
                }
            }
        },
    },
}


# CREATE
@router.post("/", response_model=AlumnoPublic, status_code=status.HTTP_201_CREATED)
def create_alumno(data: AlumnoCreate, Session: SessionDep):
    db_alumno = Alumno.model_validate(data)
    Session.add(db_alumno)
    Session.commit()
    Session.refresh(db_alumno)
    return db_alumno

# GET
@router.get("/", response_model=Page[AlumnoPublic])
def listar_alumnos(session: SessionDep):
    return paginate(session, select(Alumno).order_by(Alumno.id))

@router.get("/{id}", response_model=AlumnoPublicNested, responses=NOT_FOUND_RESPONSE)
def listar_alumno_id(id: int, session: SessionDep):
    alumno = session.get(Alumno, id)
    if not alumno:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    return alumno

# UPDATE
@router.put("/{id}", response_model=AlumnoPublic, responses=NOT_FOUND_RESPONSE)
def actualizar_alumno(id: int, data: AlumnoCreate, session: SessionDep):
    alumno_db = session.get(Alumno, id)
    if not alumno_db:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    alumno_data = data.model_dump(exclude_unset=True)
    alumno_db.sqlmodel_update(alumno_data)
    session.add(alumno_db)
    session.commit()
    session.refresh(alumno_db)
    return alumno_db

# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response=NOT_FOUND_RESPONSE)
def borrar_alumno(id: int, session: SessionDep):
    alumno = session.get(Alumno, id)
    if not alumno:
        raise HTTPException(
            status_code=NOT_FOUND_RESPONSE
        )
    session.delete(alumno)
    session.commit()
    return None


