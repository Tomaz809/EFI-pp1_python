from typing import Annotated, Optional
from sqlmodel import SQLModel, Field
from .materia import MateriaPublic

class CarreraBase(SQLModel):
    nombre: Annotated[str, Field(max_length=100)]
    codigo: Annotated[int, Field(max_length=4)]

class Carrera(CarreraBase, table=True):
    id: Annotated[int, Field(primary_key=True)]

class CarreraPublic(CarreraBase):
    id: int

class CarreraPublicNested(CarreraPublic):
    materia: Optional[MateriaPublic]=None

class CarreraCreate(CarreraBase):
    pass