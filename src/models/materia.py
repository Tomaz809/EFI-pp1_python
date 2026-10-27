from typing import Annotated, Optional, list
from sqlmodel import Relationship, SQLModel, Field
from models.carrera import Carrera


class MateriaBase(SQLModel):
    nombre_materia: Annotated[str, Field(max_length=50)]
    codigo: Annotated[int, Field(ge=0, le=9999)]
    año: Annotated[int, Field(ge=1, le=9)]
    cuatrimestral: bool


class Materia(MateriaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    codigo: Annotated[int, Field(ge=0, le=9999, unique=True, index=True)]
    carrera_id: Optional[int] = Field(
        default=None,
        foreign_key="carrera.id",
        ondelete="SET NULL",
    )

    carrera: Optional["Carrera"] = Relationship(back_populates="materias")


class MateriaPublic(MateriaBase):
    id: int
    carrera_id: Optional[int] = None


class MateriaPublicNested(MateriaPublic):
    correlativas: list[MateriaPublic] = Field(default_factory=list)


class MateriaCreate(MateriaBase):
    carrera_id: Optional[int] = None


class MateriaUpdate(SQLModel):
    nombre_materia: Annotated[str, Field(min_length=1, max_length=50)] | None = None
    codigo: Annotated[int, Field(ge=0, le=9999)] | None = None
    año: Annotated[int, Field(ge=1, le=9)] | None = None
    cuatrimestral: bool | None = None
    carrera_id: Optional[int] = None