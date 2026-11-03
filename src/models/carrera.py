from typing import TYPE_CHECKING, Annotated
from sqlmodel import Field, Relationship, SQLModel
from src.models.materia import MateriaPublic

if TYPE_CHECKING:
    from src.models.alumno import Alumno
    from src.models.materia import Materia


class CarreraBase(SQLModel):
    nombre: Annotated[str, Field(max_length=100)]
    codigo: Annotated[int, Field(ge=0, le=9999)]

class Carrera(CarreraBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    codigo: Annotated[int, Field(ge=0, le=9999, unique=True, index=True)]
    materias: list["Materia"] = Relationship(back_populates="carrera")
    alumnos: list["Alumno"] = Relationship(back_populates="carrera")

class AlumnoEnCarrera(SQLModel):
    id: int
    nombre: str
    apellido: str
    dni: str

class CarreraPublic(CarreraBase):
    id: int

class CarreraPublicNested(CarreraPublic):
    materias: list[MateriaPublic] = Field(default_factory=list)
    alumnos: list[AlumnoEnCarrera] = Field(default_factory=list)

class CarreraCreate(CarreraBase):
    pass

class CarreraUpdate(SQLModel):
    nombre: Annotated[str, Field(min_length=1, max_length=50)] | None = None
    codigo: Annotated[int, Field(ge=0, le=9999)] | None = None