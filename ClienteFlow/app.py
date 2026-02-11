"""Streamlit entrypoint for ClienteFlow."""
from __future__ import annotations

import logging

import streamlit as st

from src.db import init_db
from src.utils import login_gate, sidebar_header

logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="ClienteFlow", layout="wide")
init_db()
sidebar_header("ClienteFlow")

st.title("ClienteFlow")
st.write("Cadastro de Clientes + Agenda de Contato")

if not login_gate():
    st.stop()

st.success("Autenticado")
st.markdown(
    "Use o menu lateral para acessar Clientes, Agenda e Ajuda. "
    "Os dados ficam em data/app.db."
)
