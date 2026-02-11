"""Ajuda page."""
from __future__ import annotations

import streamlit as st

from src.db import init_db
from src.utils import require_auth, sidebar_header

init_db()
require_auth()
sidebar_header("ClienteFlow")

st.title("Ajuda")

st.markdown(
    """
Como usar
- Use o menu lateral para navegar entre Clientes, Agenda e Ajuda.
- Em Clientes, voce pode cadastrar, editar, excluir e abrir o detalhe de um cliente.
- Em Agenda, registre contatos vinculados a um cliente e filtre por periodo/canal/cliente.

Validacoes
- Nome do cliente e assunto do contato sao obrigatorios.
- Email precisa estar no formato correto.
- Telefone aceita digitos e os caracteres +() - e espaco.
- Proximo contato nao pode ser antes da data do contato.

Exportacao CSV
- Use os botoes de exportacao nas telas de Clientes e Agenda.
- O arquivo gerado reflete os filtros atuais da tela.

Banco de dados
- O SQLite fica em data/app.db.
- Para resetar, apague o arquivo data/app.db e recarregue o app.

Dicas e atalhos
- Use a busca por texto para filtrar por nome, email, telefone, empresa e tags.
- Use tags separadas por virgula para agrupar clientes.
"""
)
