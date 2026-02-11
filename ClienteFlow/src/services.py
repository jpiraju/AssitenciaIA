"""Service layer for database operations."""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import or_
from sqlalchemy.orm import selectinload

from src.db import get_session
from src.models import Cliente, Contato
from src.schemas import ClientCreate, ClientUpdate, ContactCreate, ContactUpdate
from src.utils import normalize_phone, normalize_tags


def create_client(data: ClientCreate) -> Cliente:
    """Create a new client."""
    payload = data.model_dump()
    payload["telefone"] = normalize_phone(payload.get("telefone"))
    payload["tags"] = normalize_tags(payload.get("tags"))
    with get_session() as session:
        client = Cliente(**payload)
        session.add(client)
        session.flush()
        session.refresh(client)
        return client


def list_clients(
    search: str | None = None,
    empresa: str | None = None,
    tags: str | None = None,
) -> list[Cliente]:
    """List clients with optional filters."""
    with get_session() as session:
        query = session.query(Cliente)
        if search:
            like = f"%{search}%"
            query = query.filter(
                or_(
                    Cliente.nome.ilike(like),
                    Cliente.email.ilike(like),
                    Cliente.telefone.ilike(like),
                    Cliente.empresa.ilike(like),
                    Cliente.tags.ilike(like),
                )
            )
        if empresa:
            query = query.filter(Cliente.empresa.ilike(f"%{empresa}%"))
        if tags:
            query = query.filter(Cliente.tags.ilike(f"%{tags}%"))
        return query.order_by(Cliente.nome.asc()).all()


def get_client(client_id: int) -> Cliente | None:
    """Get client by id with contacts."""
    with get_session() as session:
        return (
            session.query(Cliente)
            .options(selectinload(Cliente.contatos))
            .filter(Cliente.id == client_id)
            .first()
        )


def update_client(client_id: int, data: ClientUpdate) -> Cliente | None:
    """Update client data."""
    with get_session() as session:
        client = session.query(Cliente).filter(Cliente.id == client_id).first()
        if not client:
            return None
        payload = data.model_dump(exclude_unset=True)
        if "telefone" in payload:
            payload["telefone"] = normalize_phone(payload.get("telefone"))
        if "tags" in payload:
            payload["tags"] = normalize_tags(payload.get("tags"))
        for key, value in payload.items():
            setattr(client, key, value)
        session.flush()
        session.refresh(client)
        return client


def delete_client(client_id: int) -> bool:
    """Delete a client and cascade contacts."""
    with get_session() as session:
        client = session.query(Cliente).filter(Cliente.id == client_id).first()
        if not client:
            return False
        session.delete(client)
        return True


def create_contact(data: ContactCreate) -> Contato:
    """Create a new contact."""
    payload = data.model_dump()
    with get_session() as session:
        contact = Contato(**payload)
        session.add(contact)
        session.flush()
        session.refresh(contact)
        return contact


def list_contacts(
    cliente_id: int | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    canal: str | None = None,
) -> list[Contato]:
    """List contacts with filters."""
    with get_session() as session:
        query = session.query(Contato).options(selectinload(Contato.cliente))
        if cliente_id:
            query = query.filter(Contato.cliente_id == cliente_id)
        if data_inicio:
            query = query.filter(Contato.data_hora >= datetime.combine(data_inicio, datetime.min.time()))
        if data_fim:
            query = query.filter(Contato.data_hora <= datetime.combine(data_fim, datetime.max.time()))
        if canal:
            query = query.filter(Contato.canal == canal)
        return query.order_by(Contato.data_hora.desc()).all()


def update_contact(contact_id: int, data: ContactUpdate) -> Contato | None:
    """Update a contact."""
    with get_session() as session:
        contact = session.query(Contato).filter(Contato.id == contact_id).first()
        if not contact:
            return None
        payload = data.model_dump(exclude_unset=True)
        for key, value in payload.items():
            setattr(contact, key, value)
        session.flush()
        session.refresh(contact)
        return contact


def delete_contact(contact_id: int) -> bool:
    """Delete a contact."""
    with get_session() as session:
        contact = session.query(Contato).filter(Contato.id == contact_id).first()
        if not contact:
            return False
        session.delete(contact)
        return True
