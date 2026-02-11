# ClienteFlow

Objetivo
- Aplicacao simples para Cadastro de Clientes + Agenda de Contato.
- Interface em Streamlit, dados locais em SQLite, operacoes via SQLAlchemy.

Requisitos
- Python 3.11+

Instalacao
1) Abra um terminal na pasta do projeto.
2) Crie e ative um ambiente virtual:
   - python -m venv .venv
   - source .venv/bin/activate
3) Instale as dependencias:
   - pip install -r requirements.txt

Execucao
- streamlit run app.py

Como usar
- Na pagina inicial, faca login (padrao admin/admin).
- Use o menu lateral para acessar Clientes, Agenda e Ajuda.
- Cadastre clientes e registre contatos vinculados.

Fake login
- Credenciais padrao: admin/admin.
- Pode sobrescrever via variaveis de ambiente:
  - CLIENTEFLOW_USER e CLIENTEFLOW_PASS
  - USER e PASS (se nao definido o prefixo CLIENTEFLOW)

Exportacao CSV
- Clientes: use "Exportar CSV" na tela de Clientes (exporta dados filtrados).
- Contatos: use "Exportar CSV" na tela de Agenda (exporta dados filtrados).

Como gerar CSV
- Aplique filtros na tela desejada.
- Clique no botao de exportacao para baixar o arquivo.

Banco de dados
- Local: data/app.db
- Para resetar o banco: apague data/app.db e reinicie o app.

Estrutura de pastas
- data/app.db
- docs/prints/print1.png
- docs/prints/print2.png
- docs/prints/print3.png
- src/
- pages/
- app.py

Prints
- Coloque as imagens em docs/prints/:
  - docs/prints/print1.png
  - docs/prints/print2.png
  - docs/prints/print3.png


"""
