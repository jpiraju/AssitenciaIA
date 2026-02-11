"""Clientes page."""
from __future__ import annotations

from datetime import datetime, time as time_cls

import streamlit as st
from pydantic import ValidationError

from src.db import init_db
from src.export import clients_to_csv
from src.schemas import ClientCreate, ClientUpdate, ContactCreate
from src.services import (
    create_client,
    create_contact,
    delete_client,
    get_client,
    list_clients,
    update_client,
)
from src.utils import require_auth, sidebar_header

init_db()
require_auth()
sidebar_header("ClienteFlow")

st.title("Clientes")

col1, col2, col3 = st.columns(3)
search = col1.text_input("Busca (nome/email/telefone/empresa/tags)")
empresa = col2.text_input("Filtro por empresa")
tags = col3.text_input("Filtro por tags")

clients = list_clients(search=search, empresa=empresa, tags=tags)

with st.expander("Novo cliente"):
    with st.form("form_novo_cliente"):
        nome = st.text_input("Nome*")
        email = st.text_input("Email")
        telefone = st.text_input("Telefone")
        empresa_novo = st.text_input("Empresa")
        cargo = st.text_input("Cargo")
        tags_novo = st.text_input("Tags (tag1, tag2)")
        observacoes = st.text_area("Observacoes")
        submitted = st.form_submit_button("Salvar")

    if submitted:
        try:
            create_client(
                ClientCreate(
                    nome=nome,
                    email=email,
                    telefone=telefone,
                    empresa=empresa_novo,
                    cargo=cargo,
                    tags=tags_novo,
                    observacoes=observacoes,
                )
            )
            st.success("Cliente criado")
            st.rerun()
        except ValidationError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Erro ao criar cliente: {exc}")

st.subheader("Lista de clientes")

if not clients:
    st.info("Nenhum cliente encontrado")
else:
    table = [
        {
            "id": client.id,
            "nome": client.nome,
            "email": client.email or "",
            "telefone": client.telefone or "",
            "empresa": client.empresa or "",
            "tags": client.tags or "",
            "atualizado_em": client.atualizado_em.strftime("%Y-%m-%d %H:%M"),
        }
        for client in clients
    ]
    st.dataframe(table, use_container_width=True, hide_index=True)

    csv_data = clients_to_csv(clients)
    st.download_button(
        "Exportar CSV (clientes filtrados)",
        data=csv_data,
        file_name="clientes.csv",
        mime="text/csv",
    )

    selected_id = st.selectbox(
        "Selecionar cliente para ver detalhes",
        options=[client.id for client in clients],
        format_func=lambda cid: next(
            (c.nome for c in clients if c.id == cid),
            str(cid),
        ),
    )

    if selected_id:
        client = get_client(selected_id)
        if not client:
            st.warning("Cliente nao encontrado")
        else:
            st.subheader("Detalhe do cliente")
            col_a, col_b = st.columns(2)
            col_a.markdown(f"**Nome:** {client.nome}")
            col_a.markdown(f"**Email:** {client.email or '-'}")
            col_a.markdown(f"**Telefone:** {client.telefone or '-'}")
            col_b.markdown(f"**Empresa:** {client.empresa or '-'}")
            col_b.markdown(f"**Cargo:** {client.cargo or '-'}")
            col_b.markdown(f"**Tags:** {client.tags or '-'}")
            st.markdown(f"**Observacoes:** {client.observacoes or '-'}")

            st.markdown("### Contatos do cliente")
            if not client.contatos:
                st.info("Nenhum contato registrado")
            else:
                contact_rows = [
                    {
                        "data_hora": contato.data_hora.strftime("%Y-%m-%d %H:%M"),
                        "canal": contato.canal,
                        "assunto": contato.assunto,
                        "notas": contato.notas or "",
                        "proximo_contato": contato.proximo_contato.strftime("%Y-%m-%d")
                        if contato.proximo_contato
                        else "",
                    }
                    for contato in client.contatos
                ]
                st.dataframe(contact_rows, use_container_width=True, hide_index=True)

            st.markdown("### Registrar contato")
            with st.form("form_novo_contato"):
                col_c, col_d = st.columns(2)
                data_contato = col_c.date_input("Data", value=datetime.now().date())
                hora_contato = col_d.time_input("Hora", value=datetime.now().time())
                canal = st.selectbox(
                    "Canal",
                    options=["telefone", "email", "whatsapp", "reuniao", "outro"],
                )
                assunto = st.text_input("Assunto*")
                notas = st.text_area("Notas")
                usar_proximo = st.checkbox("Definir proximo contato")
                proximo_contato = None
                if usar_proximo:
                    proximo_contato = st.date_input("Proximo contato")
                submitted_contact = st.form_submit_button("Registrar contato")

            if submitted_contact:
                try:
                    data_hora = datetime.combine(data_contato, hora_contato)
                    create_contact(
                        ContactCreate(
                            cliente_id=client.id,
                            data_hora=data_hora,
                            canal=canal,
                            assunto=assunto,
                            notas=notas,
                            proximo_contato=proximo_contato,
                        )
                    )
                    st.success("Contato registrado")
                    st.rerun()
                except ValidationError as exc:
                    st.error(str(exc))
                except Exception as exc:
                    st.error(f"Erro ao registrar contato: {exc}")

            st.markdown("### Editar cliente")
            with st.form("form_editar_cliente"):
                nome_edit = st.text_input("Nome*", value=client.nome)
                email_edit = st.text_input("Email", value=client.email or "")
                telefone_edit = st.text_input("Telefone", value=client.telefone or "")
                empresa_edit = st.text_input("Empresa", value=client.empresa or "")
                cargo_edit = st.text_input("Cargo", value=client.cargo or "")
                tags_edit = st.text_input("Tags", value=client.tags or "")
                observacoes_edit = st.text_area(
                    "Observacoes", value=client.observacoes or ""
                )
                submitted_edit = st.form_submit_button("Salvar alteracoes")

            if submitted_edit:
                try:
                    update_client(
                        client.id,
                        ClientUpdate(
                            nome=nome_edit,
                            email=email_edit,
                            telefone=telefone_edit,
                            empresa=empresa_edit,
                            cargo=cargo_edit,
                            tags=tags_edit,
                            observacoes=observacoes_edit,
                        ),
                    )
                    st.success("Cliente atualizado")
                    st.rerun()
                except ValidationError as exc:
                    st.error(str(exc))
                except Exception as exc:
                    st.error(f"Erro ao atualizar cliente: {exc}")

            st.markdown("### Excluir cliente")
            confirmar = st.checkbox("Confirmo a exclusao deste cliente")
            if st.button("Excluir cliente", disabled=not confirmar):
                try:
                    ok = delete_client(client.id)
                    if ok:
                        st.success("Cliente excluido")
                        st.rerun()
                    else:
                        st.error("Cliente nao encontrado")
                except Exception as exc:
                    st.error(f"Erro ao excluir: {exc}")
