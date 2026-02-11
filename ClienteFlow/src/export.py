"""CSV export helpers."""
from __future__ import annotations

import csv
import io

from src.models import Cliente, Contato


def clients_to_csv(clients: list[Cliente]) -> str:
    """Export clients to CSV string."""
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "id",
            "nome",
            "email",
            "telefone",
            "empresa",
            "cargo",
            "tags",
            "observacoes",
            "criado_em",
            "atualizado_em",
        ],
    )
    writer.writeheader()
    for client in clients:
        writer.writerow(
            {
                "id": client.id,
                "nome": client.nome,
                "email": client.email or "",
                "telefone": client.telefone or "",
                "empresa": client.empresa or "",
                "cargo": client.cargo or "",
                "tags": client.tags or "",
                "observacoes": client.observacoes or "",
                "criado_em": client.criado_em.isoformat(),
                "atualizado_em": client.atualizado_em.isoformat()
                if client.atualizado_em
                else "",
            }
        )
    return output.getvalue()


def contacts_to_csv(contacts: list[Contato]) -> str:
    """Export contacts to CSV string."""
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "id",
            "cliente_id",
            "cliente_nome",
            "data_hora",
            "canal",
            "assunto",
            "notas",
            "proximo_contato",
            "criado_em",
        ],
    )
    writer.writeheader()
    for contact in contacts:
        writer.writerow(
            {
                "id": contact.id,
                "cliente_id": contact.cliente_id,
                "cliente_nome": contact.cliente.nome if contact.cliente else "",
                "data_hora": contact.data_hora.isoformat(),
                "canal": contact.canal,
                "assunto": contact.assunto,
                "notas": contact.notas or "",
                "proximo_contato": contact.proximo_contato.isoformat()
                if contact.proximo_contato
                else "",
                "criado_em": contact.criado_em.isoformat(),
            }
        )
    return output.getvalue()
