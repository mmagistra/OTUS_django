from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    def __repr__(self) -> str:
        return str(self)

    id: Mapped[int] = mapped_column(primary_key=True)
