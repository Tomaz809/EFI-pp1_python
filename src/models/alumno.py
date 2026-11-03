from typing import TYPE_CHECKING, Annotated, Optional
from sqlmodel import Field, Relationship, SQLModel
from src.models.carrera import CarreraPublic

if TYPE_CHECKING:
    from src.models.carrera import Carrera


class AlumnoBase(SQLModel):
    nombre: Annotated[str, Field(min_length=1, max_length=80)]
    apellido: Annotated[str, Field(min_length=1, max_length=80)]
    dni: Annotated[str, Field(min_length=7, max_length=12)]
    email: Annotated[str, Field(min_length=5, max_length=100)]
    legajo: Annotated[int, Field(ge=0, le=99999)]


class Alumno(AlumnoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    dni: Annotated[str, Field(min_length=7, max_length=12, unique=True, index=True)]
    email: Annotated[str, Field(min_length=5, max_length=100, unique=True, index=True)]
    legajo: Annotated[int, Field(ge=0, le=99999, unique=True, index=True)]
    carrera_id: Optional[int] = Field(
        default=None,
        foreign_key="carrera.id",
        ondelete="SET NULL",
    )

    carrera: Optional["Carrera"] = Relationship(back_populates="alumnos")


class AlumnoCreate(AlumnoBase):
    carrera_id: Optional[int] = None

class AlumnoUpdate(SQLModel):
    nombre: Annotated[str, Field(min_length=1, max_length=80)] | None = None
    apellido: Annotated[str, Field(min_length=1, max_length=80)] | None = None
    dni: Annotated[str, Field(min_length=7, max_length=12)] | None = None
    email: Annotated[str, Field(min_length=5, max_length=100)] | None = None
    legajo: Annotated[int, Field(ge=0, le=99999)] | None = None
    carrera_id: Optional[int] = None


class AlumnoPublic(AlumnoBase):
    id: int
    carrera_id: Optional[int] = None


class AlumnoPublicNested(AlumnoPublic):
    carrera: Optional[CarreraPublic] = None