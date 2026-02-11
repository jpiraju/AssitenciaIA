"""Agenda page."""
from __future__ import annotations

from datetime import datetime

import streamlit as st
from pydantic import ValidationError

from src.db import init_db
from src.export import contacts_to_csv
from src.schemas import ContactCreate
from src.services import create_contact, list_clients, list_contacts
from src.utils import require_auth, sidebar_header

init_db()
require_auth()
sidebar_header("ClienteFlow")

st.title("Agenda")

clients = list_clients()
client_map = {client.nome: client.id for client in clients}
client_names = ["Todos"] + list(client_map.keys())

col1, col2, col3 = st.columns(3)
usar_inicio = col1.checkbox("Filtrar por data inicio")
start_date = col1.date_input(
    "Data inicio", value=datetime.now().date(), disabled=not usar_inicio
)
usar_fim = col2.checkbox("Filtrar por data fim")
end_date = col2.date_input(
    "Data fim", value=datetime.now().date(), disabled=not usar_fim
)
canal = col3.selectbox(
    "Canal",
    options=["Todos", "telefone", "email", "whatsapp", "reuniao", "outro"],
)

cliente_nome = st.selectbox("Cliente", options=client_names)

selected_cliente_id = None
if cliente_nome != "Todos":
    selected_cliente_id = client_map.get(cliente_nome)

contacts = list_contacts(
    cliente_id=selected_cliente_id,
    data_inicio=start_date if usar_inicio else None,
    data_fim=end_date if usar_fim else None,
    canal=None if canal == "Todos" else canal,
)

st.subheader("Contatos")
if not contacts:
    st.info("Nenhum contato encontrado")
else:
    rows = [
        {
            "data_hora": contato.data_hora.strftime("%Y-%m-%d %H:%M"),
            "cliente": contato.cliente.nome if contato.cliente else "",
            "canal": contato.canal,
            "assunto": contato.assunto,
            "proximo_contato": contato.proximo_contato.strftime("%Y-%m-%d")
            if contato.proximo_contato
            else "",
        }
        for contato in contacts
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)

    csv_data = contacts_to_csv(contacts)
    st.download_button(
        "Exportar CSV (contatos filtrados)",
        data=csv_data,
        file_name="contatos.csv",
        mime="text/csv",
    )

with st.expander("Novo contato"):
    if not clients:
        st.info("Cadastre um cliente antes de criar contatos")
    else:
        with st.form("form_agenda_contato"):
            cliente_select = st.selectbox(
                "Cliente", options=client_names[1:]
            )
            col_a, col_b = st.columns(2)
            data_contato = col_a.date_input("Data", value=datetime.now().date())
            hora_contato = col_b.time_input("Hora", value=datetime.now().time())
            canal_form = st.selectbox(
                "Canal",
                options=["telefone", "email", "whatsapp", "reuniao", "outro"],
            )
            assunto = st.text_input("Assunto*")
            notas = st.text_area("Notas")
            usar_proximo = st.checkbox("Definir proximo contato")
            proximo_contato = None
            if usar_proximo:
                proximo_contato = st.date_input("Proximo contato")
            submitted = st.form_submit_button("Registrar")

        if submitted:
            try:
                data_hora = datetime.combine(data_contato, hora_contato)
                create_contact(
                    ContactCreate(
                        cliente_id=client_map[cliente_select],
                        data_hora=data_hora,
                        canal=canal_form,
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
