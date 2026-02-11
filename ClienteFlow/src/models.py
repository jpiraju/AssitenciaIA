"""SQLAlchemy models for ClienteFlow."""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Cliente(Base):
    """Client entity."""

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(200))
    telefone: Mapped[str | None] = mapped_column(String(50))
    empresa: Mapped[str | None] = mapped_column(String(200))
    cargo: Mapped[str | None] = mapped_column(String(200))
    tags: Mapped[str | None] = mapped_column(String(300))
    observacoes: Mapped[str | None] = mapped_column(Text)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    contatos: Mapped[list[Contato]] = relationship(
        "Contato",
        back_populates="cliente",
        cascade="all, delete-orphan",
        order_by="Contato.data_hora.desc()",
    )


class Contato(Base):
    """Contact entity."""

    __tablename__ = "contatos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey("clientes.id"))
    data_hora: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    canal: Mapped[str] = mapped_column(String(20), nullable=False)
    assunto: Mapped[str] = mapped_column(String(200), nullable=False)
    notas: Mapped[str | None] = mapped_column(Text)
    proximo_contato: Mapped[date | None] = mapped_column(Date)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cliente: Mapped[Cliente] = relationship("Cliente", back_populates="contatos")
