from sqlmodel import CheckConstraint, Field, SQLModel


class CorrelativaBase(SQLModel):
    materia_id: int = Field(
        foreign_key="materia.id",
        ondelete="CASCADE",
        primary_key=True,
    )
    correlativa_id: int = Field(
        foreign_key="materia.id",
        ondelete="CASCADE",
        primary_key=True,
    )


class Correlativa(CorrelativaBase, table=True):
    __table_args__ = (
        CheckConstraint(
            "materia_id != correlativa_id",
            name="check_correlativa_no_self_reference",
        ),
    )


class CorrelativaCreate(CorrelativaBase):
    pass


class CorrelativaPublic(CorrelativaBase):
    pass