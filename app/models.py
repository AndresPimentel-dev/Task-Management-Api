from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from typing import List

from app.database import Base

class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String())
    hashed_password: Mapped[str] = mapped_column(String)

    workspace: Mapped[List["Workspace"]] = relationship(back_populates="owner")

class Workspace(Base):
    __tablename__ = "workspace"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())

    owner_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    owner: Mapped["User"] = relationship(back_populates="workspace")

class Task(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    status: Mapped[str] = mapped_column(String())

    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspace.id"))
    assignee_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

