from typing import Annotated, Optional
from sqlmodel import SQLModel, Field, Relationship
from models.carrera import CarreraPublic, Carrera


class AlumnoBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=80)
    apellido: str = Field(min_length=1, max_length=80)
    dni: str = Field(min_length=7, max_length=12)
    email: str = Field(min_length=5, max_length=100)
    legajo: int = Field(ge=0, le=99999)


class Alumno(AlumnoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    dni: str = Field(min_length=7, max_length=12, unique=True, index=True)
    email: str = Field(min_length=5, max_length=100, unique=True, index=True)
    legajo: int = Field(ge=0, le=99999, unique=True, idex=True)
    carrera_id: Optional[int] = Field(
        default=None,
        foreign_key="carrera.id",
        ondelete="SET NULL",
    )

    carrera: Optional["Carrera"] = Relationship(back_populates="alumnos")


class AlumnoCreate(AlumnoBase):
    carrera_id: Optional[int] = None

class AlumnoUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=80)
    apellido: Optional[str] = Field(default=None, min_length=1, max_length=80)
    dni: Optional[str] = Field(default=None, min_length=7, max_length=12)
    email: Optional[str] = Field(default=None, min_length=5, max_length=100)
    legajo: Optional[int] = Field(default=None, ge=0, le=99999)
    carrera_id: Optional[int] = None


class AlumnoPublic(AlumnoBase):
    id: int
    carrera_id: Optional[int] = None


class AlumnoPublicNested(AlumnoPublic):
    carrera: Optional[CarreraPublic] = None