from typing import Annotated, Optional
from sqlmodel import Relationship, SQLModel, Field
from .carrera import Carrera
from .correlativa import CorrelativaPublic

class MateriaBase(SQLModel):
    nombre_materia: Annotated[str, Field(max_length=50)]
    codigo: Annotated[int, Field(max_length=4)]
    año: Annotated[int, Field(max_length=1)]
    cuatrimestral: bool

class Materia(MateriaBase, table=True):
    id: Annotated[int, Field(primary_key=True)]

    carrera: Optional[Carrera] = Relationship(back_populates="carreras")

class MateriaPublic(MateriaBase):
    id: int

class MateriaPublicNested(MateriaPublic):
    correlativa: Optional[CorrelativaPublic]=None

class MateriaCreate(MateriaBase):
    pass

    

