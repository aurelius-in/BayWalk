from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from db.session import Base


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    targets: Mapped[dict] = mapped_column(JSON)
    scene_ref: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="created")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Run(Base):
    __tablename__ = "runs"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(String, index=True)
    kind: Mapped[str] = mapped_column(String)  # plan or generate
    state: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Artifact(Base):
    __tablename__ = "artifacts"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(String, index=True)
    kind: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
