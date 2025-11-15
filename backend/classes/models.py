from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(Text, nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

class Recurso(Base):
    __tablename__ = "recursos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    data_criacao: Mapped[datetime] = mapped_column( DateTime(timezone=True), server_default=func.now() )
    git_repo_url: Mapped[str] = mapped_column(Text, nullable=True)

class RecursoAtivo(Base):
    __tablename__ = "recursos_ativos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    recurso_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recurso_alvo: Mapped[str] = mapped_column(Text, nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    data_criacao: Mapped[datetime] = mapped_column( DateTime(timezone=True), server_default=func.now() )