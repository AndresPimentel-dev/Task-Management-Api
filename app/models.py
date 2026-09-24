from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UsersTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String)

    workspaces: Mapped[list["WorkspacesTable"]] = relationship(back_populates="owner")

class WorkspacesTable(Base):
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(50))

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["UsersTable"] = relationship(back_populates="workspaces")
    tasks: Mapped[list["TasksTable"]] = relationship(back_populates="workspace")

class TasksTable(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))

    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    workspace: Mapped["WorkspacesTable"] = relationship(back_populates="tasks")

