"""Utility helpers for ClienteFlow."""
from __future__ import annotations

import os
from typing import Iterable

import streamlit as st


def normalize_tags(value: str | None) -> str | None:
    """Normalize tags into a comma separated string."""
    if not value:
        return None
    parts = [part.strip() for part in value.split(",") if part.strip()]
    if not parts:
        return None
    return ", ".join(parts)


def normalize_phone(value: str | None) -> str | None:
    """Normalize phone with trimmed spaces."""
    if not value:
        return None
    return " ".join(str(value).split())


def get_credentials() -> tuple[str, str]:
    """Get login credentials from environment or defaults."""
    user = os.getenv("CLIENTEFLOW_USER") or os.getenv("USER") or "admin"
    password = os.getenv("CLIENTEFLOW_PASS") or os.getenv("PASS") or "admin"
    return user, password


def login_gate() -> bool:
    """Render login form and return auth status."""
    if st.session_state.get("auth"):
        return True

    user_env, pass_env = get_credentials()
    st.subheader("Login")
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

    if submitted:
        if username == user_env and password == pass_env:
            st.session_state["auth"] = True
            st.success("Login ok")
            st.rerun()
        else:
            st.error("Credenciais invalidas")
    return False


def require_auth() -> None:
    """Stop page rendering if user is not authenticated."""
    if not st.session_state.get("auth"):
        st.warning("Faça login na pagina inicial para continuar.")
        st.stop()


def sidebar_header(title: str) -> None:
    """Render a common sidebar header with logout."""
    st.sidebar.title(title)
    if st.session_state.get("auth"):
        if st.sidebar.button("Logout"):
            st.session_state["auth"] = False
            st.rerun()


def format_tags(tags: str | None) -> str:
    """Format tags for display."""
    return tags or "-"


def list_to_display(values: Iterable[str]) -> str:
    """Join list values for display."""
    return ", ".join(values)
