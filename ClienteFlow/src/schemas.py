"""Pydantic schemas and validation rules."""
from __future__ import annotations

from datetime import date, datetime
import re

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

PHONE_PATTERN = re.compile(r"^[0-9+()\- ]+$")
ALLOWED_CANAIS = {"telefone", "email", "whatsapp", "reuniao", "outro"}


class ClientBase(BaseModel):
    nome: str = Field(min_length=1)
    email: EmailStr | None = None
    telefone: str | None = None
    empresa: str | None = None
    cargo: str | None = None
    tags: str | None = None
    observacoes: str | None = None

    @field_validator("email", mode="before")
    @classmethod
    def empty_email_to_none(cls, value):
        if value in (None, ""):
            return None
        return value

    @field_validator("telefone", mode="before")
    @classmethod
    def empty_phone_to_none(cls, value):
        if value in (None, ""):
            return None
        return str(value).strip()

    @field_validator("telefone")
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value
        if not PHONE_PATTERN.match(value):
            raise ValueError("Telefone invalido")
        return value


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    nome: str | None = None


class ContactBase(BaseModel):
    cliente_id: int
    data_hora: datetime
    canal: str
    assunto: str
    notas: str | None = None
    proximo_contato: date | None = None

    @field_validator("canal")
    @classmethod
    def validate_canal(cls, value):
        if value not in ALLOWED_CANAIS:
            raise ValueError("Canal invalido")
        return value

    @model_validator(mode="after")
    def validate_dates(self):
        if self.proximo_contato and self.proximo_contato < self.data_hora.date():
            raise ValueError("Proximo contato deve ser depois da data do contato")
        return self


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    cliente_id: int | None = None
    data_hora: datetime | None = None
    canal: str | None = None
    assunto: str | None = None
