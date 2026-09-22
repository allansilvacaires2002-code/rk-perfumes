from datetime import datetime
import os
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="RK Perfumes - ERP",
    page_icon="🧴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CONFIGURAÇÃO DO BANCO DE DADOS SQLITE ---
DB_FILE = "rk_perfumes.db"


def criar_conexao():
  return sqlite3.connect(DB_FILE, check_same_thread=False)


def inicializar_banco():
  conn = criar_conexao()
  cursor = conn.cursor()

  # Tabela de Produtos / Estoque
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            codigo TEXT PRIMARY KEY,
            nome TEXT,
            categoria TEXT,
            preco_custo TEXT,
            preco_venda TEXT,
            lucro_unitario TEXT,
            margem TEXT,
            estoque INTEGER,
            status TEXT
        )
    """)

  # Tabela de Clientes
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente TEXT PRIMARY KEY,
            nome TEXT,
            telefone TEXT,
            cep TEXT,
            rua TEXT,
            numero TEXT,
            bairro TEXT,
            cidade TEXT
        )
    """)

  # Tabela de Vendas
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            cliente TEXT,
            perfume TEXT,
            quantidade INTEGER,
            valor_total REAL,
            forma_pagamento TEXT,
            status_pagamento TEXT,
            lucro REAL
        )
    """)
  conn.commit()
  conn.close()


# Executa a criação das tabelas ao iniciar
inicializar_banco()


# Funções de Carregamento de Dados do Banco SQL
def carregar_produtos():
  conn = criar_conexao()
  df = pd.read_sql_query("SELECT * FROM produtos", conn)
  conn.close()
  return df


def carregar_clientes():
  conn = criar_conexao()
  df = pd.read_sql_query("SELECT * FROM clientes", conn)
  conn.close()
  return df


def carregar_vendas():
  conn = criar_conexao()
  df = pd.read_sql_query("SELECT * FROM vendas", conn)
  if "id" in df.columns:
    df = df.drop(columns=["id"])
  conn.close()
  return df


# Estilização CSS completa para o Modo Escuro Profundo e correção de botões
st.markdown(
    """
    <style>
        /* Fundo principal da aplicação */
        .stApp {
            background-color: #0d1117 !important;
            color: #ffffff !important;
            font-family: 'Inter', sans-serif;
        }
        
        /* Barra lateral (Sidebar) escura */
        section[data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 1px solid #30363d;
        }
        
        section[data-testid="stSidebar"] .stRadio label {
            color: #e6edf3 !important;
            font-weight: 500;
        }

        /* Topo / Header */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }

        /* Cartões de Métricas (Dashboard) em modo escuro */
        div.metric-card {
            background-color: #161b22 !important;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
            border-left: 5px solid #00b074;
            margin-bottom: 15px;
            border-top: 1px solid #30363d;
            border-right: 1px solid #30363d;
            border-bottom: 1px solid #30363d;
        }
        
        div.metric-card h4 {
            color: #8b949e !important;
            font-size: 13px;
            margin-bottom: 8px;
            font-weight: 600;
            text-transform: uppercase;
        }

        div.metric-card h2 {
            color: #ffffff !important;
            font-size: 26px;
            font-weight: 700;
            margin: 0;
        }

        /* Títulos e textos gerais */
        h1, h2, h3, h4, p, span, label {
            color: #ffffff !important;
        }

        /* CORREÇÃO DOS BOTÕES (Garante cor verde esmeralda e texto branco legível) */
        div.stButton > button, 
        div.stFormSubmitButton > button {
            background-color: #00b074 !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            border: none !important;
            font-weight: 600 !important;
        }
        
        div.stButton > button:hover, 
        div.stFormSubmitButton > button:hover {
            background-color: #00915f !important;
            color: #ffffff !important;
        }

        /* Campos de texto e inputs escuros */
        input, select, textarea {
            background-color: #21262d !important;
            color: #ffffff !important;
            border: 1px solid #30363d !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Inicialização do Estado de Autenticação
if "autenticado" not in st.session_state:
  st.session_state.autenticado = False

# --- TELA DE LOGIN ---
if not st.session_state.autenticado:
  st.markdown(
      "<h1 style='text-align: center; color: #00b074 !important;'>🧴 RK"
      " Perfumes</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h3 style='text-align: center; color: #8b949e !important;'>Acesso ao"
      " Sistema de Gestão</h3>",
      unsafe_allow_html=True,
  )
  st.write("")

  col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
  with col_l2:
    with st.form("form_login"):
      usuario_input = st.text_input("Utilizador")
      senha_input = st.text_input("Palavra-passe", type="password")
      submit_login = st.form_submit_button("Entrar no Painel")

      if submit_login:
        if usuario_input == "RK" and senha_input == "2026":
          st.session_state.autenticado = True
          st.success("Login efetuado com sucesso!")
          st.rerun()
        else:
          st.error("Utilizador ou palavra-passe incorretos!")
  st.stop()

# Carregar dados atuais do banco SQL
df_produtos = carregar_produtos()
df_clientes = carregar_clientes()
df_vendas = carregar_vendas()

# --- BARRA LATERAL ---
with st.sidebar:
  st.markdown("### 🧴 **RK Perfumes**")
  st.caption("Sistema de Gestão Comercial")
  st.divider()
  menu_opcao = st.radio(
      "Ir para:",
      [
          "Dashboard",
          "Estoque",
          "Clientes",
          "Vendas",
      ],
      label_visibility="collapsed",
  )
  st.divider()
  st.caption("Utilizador: **RK** | Banco SQL Ativo")
  if st.button("Terminar Sessão"):
    st.session_state.autenticado = False
    st.rerun()

# --- CONTEÚDO PRINCIPAL ---

if menu_opcao == "Dashboard":
  st.markdown("## 📊 Resumo / Dashboard Executivo")
  st.markdown(
      "Visão completa e consolidada do desempenho do seu negócio de perfumes."
  )

  st.divider()
  st.subheader("📅 Filtro de Período (Mês de Análise)")

  meses_disponiveis = ["Mês Atual"]
  if not df_vendas.empty:
    lista_meses = (
        df_vendas["data_hora"]
        .apply(lambda x: str(x).split()[0][3:])
        .unique()
        .tolist()
    )
    for m in lista_meses:
      if m not in meses_disponiveis:
        meses_disponiveis.append(m)

  col_sel1, col_sel2 = st.columns([1, 2])
  with col_sel1:
    mes_selecionado = st.selectbox(
        "Selecione o Mês para ver o faturamento:", meses_disponiveis
    )

  df_filtrado = df_vendas.copy()
  if not df_filtrado.empty:
    if mes_selecionado == "Mês Atual":
      mes_corrente = datetime.now().strftime("%m/%Y")
      df_filtrado = df_filtrado[
          df_filtrado["data_hora"].str.contains(mes_corrente)
      ]
    else:
      df_filtrado = df_filtrado[
          df_filtrado["data_hora"].str.contains(mes_selecionado)
      ]

  faturamento_total = (
      df_filtrado["valor_total"].sum() if not df_filtrado.empty else 0.0
  )
  lucro_liquido = df_filtrado["lucro"].sum() if not df_filtrado.empty else 0.0
  total_vendas = len(df_filtrado) if not df_filtrado.empty else 0
  total_clientes = len(df_clientes)

  mais_vendido = "Nenhuma venda"
  if not df_filtrado.empty and "perfume" in df_filtrado.columns:
    mais_vendido = (
        df_filtrado["perfume"].mode()[0]
        if not df_filtrado["perfume"].empty
        else "N/A"
    )

  col1, col2, col3 = st.columns(3)
  with col1:
    st.markdown(
        f"""<div class="metric-card"><h4>Faturamento ({mes_selecionado})</h4><h2>R$ {faturamento_total:.2f}</h2></div>""",
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f"""<div class="metric-card"><h4>Lucro Líquido ({mes_selecionado})</h4><h2>R$ {lucro_liquido:.2f}</h2></div>""",
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        f"""<div class="metric-card"><h4>Vendas no Período</h4><h2>{total_vendas}</h2></div>""",
        unsafe_allow_html=True,
    )

  col4, col5 = st.columns(2)
  with col4:
    st.markdown(
        f"""<div class="metric-card"><h4>Perfume Mais Vendido</h4><h2>{mais_vendido}</h2></div>""",
        unsafe_allow_html=True,
    )
  with col5:
    st.markdown(
        f"""<div class="metric-card" style="border-left-color: #3b82f6;"><h4>Clientes Cadastrados</h4><h2>{total_clientes}</h2></div>""",
        unsafe_allow_html=True,
    )

  st.divider()

  st.subheader("💵 Fechamento de Caixa por Forma de Pagamento")
  if not df_vendas.empty and "forma_pagamento" in df_vendas.columns:
    col_filtro1, col_filtro2 = st.columns([1, 2])
    with col_filtro1:
      tipo_periodo_caixa = st.selectbox(
          "Filtrar Fechamento por:", ["Hoje (Dia)", "Mês Atual (Geral)"]
      )

    df_caixa = df_vendas.copy()
    if tipo_periodo_caixa == "Hoje (Dia)":
      hoje_str = datetime.now().strftime("%d/%m/%Y")
      df_caixa["ApenasData"] = df_caixa["data_hora"].apply(
          lambda x: str(x).split()[0]
      )
      df_caixa = df_caixa[df_caixa["ApenasData"] == hoje_str]
    else:
      mes_corrente = datetime.now().strftime("%m/%Y")
      df_caixa = df_caixa[df_caixa["data_hora"].str.contains(mes_corrente)]

    if not df_caixa.empty:
      caixa_por_pagamento = (
          df_caixa.groupby("forma_pagamento")["valor_total"]
          .sum()
          .reset_index()
      )
      caixa_por_pagamento.columns = [
          "Forma de Pagamento",
          "Total Arrecadado (R$)",
      ]
      caixa_por_pagamento["Total Arrecadado (R$)"] = caixa_por_pagamento[
          "Total Arrecadado (R$)"
      ].apply(lambda x: f"R$ {x:.2f}")

      st.dataframe(caixa_por_pagamento, use_container_width=True)
    else:
      st.warning("Nenhuma venda registada para este período.")
  else:
    st.info("Ainda não há vendas registadas.")

  st.divider()
  st.subheader("⚠️ Alerta de Estoque Baixo")
  if not df_produtos.empty:
    estoque_baixo = df_produtos[
        df_produtos["status"].isin(["Estoque Baixo", "Esgotado"])
    ]
    if not estoque_baixo.empty:
      for index, row in estoque_baixo.iterrows():
        st.warning(
            f"🚨 **{row['nome']}** ({row['estoque']} un. - {row['status']})"
        )
    else:
      st.success("✅ Todos os produtos estão com níveis saudáveis de estoque!")
  else:
    st.info("Nenhum produto cadastrado.")

  st.divider()
  st.subheader(f"📋 Histórico de Vendas ({mes_selecionado})")
  if not df_filtrado.empty:
    st.dataframe(df_filtrado, use_container_width=True)
  else:
    st.info(f"Nenhuma venda registada para '{mes_selecionado}'.")

elif menu_opcao == "Estoque":
  st.markdown("## 🧴 Controle de Estoque Profissional")
  acao_produto = st.radio(
      "O que você deseja fazer no estoque?",
      ["Cadastrar Novo Produto", "Editar Produto", "Remover Produto"],
      horizontal=True,
      key="radio_estoque",
  )
  st.divider()

  if acao_produto == "Cadastrar Novo Produto":
    proximo_cod_num = len(df_produtos) + 1
    codigo_automatico = f"PROD-{proximo_cod_num:03d}"

    with st.form("form_produto", clear_on_submit=True):
      st.info(
          f"🆔 **Código Automático gerado para o novo produto:**"
          f" {codigo_automatico}"
      )

      col1, col2, col3 = st.columns(3)
      with col1:
        nome_prod = st.text_input("Nome / Marca / Linha (Ex: Essencial Oud)")
        cat_prod = st.selectbox(
            "Categoria", ["Masculino", "Feminino", "Unissex"]
        )
      with col2:
        preco_custo = st.number_input(
            "Preço de Custo (R$)", min_value=0.0, format="%.2f"
        )
        preco_venda = st.number_input(
            "Preço de Venda (R$)", min_value=0.0, format="%.2f"
        )
      with col3:
        qtd_estoque = st.number_input(
            "Quantidade em Estoque", min_value=0, step=1
        )

      if st.form_submit_button("Cadastrar Produto") and nome_prod:
        lucro_unit = preco_venda - preco_custo
        margem_perc = (
            (lucro_unit / preco_custo) * 100
            if preco_custo > 0
            else (100.0 if preco_venda > 0 else 0.0)
        )
        status = (
            "Disponível"
            if qtd_estoque > 3
            else ("Estoque Baixo" if qtd_estoque > 0 else "Esgotado")
        )

        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO produtos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                codigo_automatico,
                nome_prod,
                cat_prod,
                f"R$ {preco_custo:.2f}",
                f"R$ {preco_venda:.2f}",
                f"R$ {lucro_unit:.2f}",
                f"{margem_perc:.1f}%",
                qtd_estoque,
                status,
            ),
        )
        conn.commit()
        conn.close()

        st.success("Perfume cadastrado e salvo no banco SQL com sucesso!")
        st.rerun()

  elif acao_produto == "Editar Produto":
    if not df_produtos.empty:
      with st.form("form_editar_produto"):
        produto_editar = st.selectbox(
            "Selecione o perfume para alterar dados", df_produtos["nome"].tolist()
        )
        prod_atual = df_produtos[df_produtos["nome"] == produto_editar].iloc[0]
        custo_limpo = float(
            str(prod_atual["preco_custo"])
            .replace("R$", "")
            .replace(",", ".")
            .strip()
        )
        venda_limpo = float(
            str(prod_atual["preco_venda"])
            .replace("R$", "")
            .replace(",", ".")
            .strip()
        )

        col1, col2, col3 = st.columns(3)
        with col1:
          novo_nome = st.text_input("Nome do Perfume", value=prod_atual["nome"])
          nova_cat = st.selectbox(
              "Categoria",
              ["Masculino", "Feminino", "Unissex"],
              index=(
                  ["Masculino", "Feminino", "Unissex"].index(
                      prod_atual["categoria"]
                  )
                  if prod_atual["categoria"]
                  in ["Masculino", "Feminino", "Unissex"]
                  else 0
              ),
          )
        with col2:
          novo_custo = st.number_input(
              "Preço de Custo (R$)",
              min_value=0.0,
              value=custo_limpo,
              format="%.2f",
          )
          nova_venda = st.number_input(
              "Preço de Venda (R$)",
              min_value=0.0,
              value=venda_limpo,
              format="%.2f",
          )
        with col3:
          novo_qtd = st.number_input(
              "Quantidade em Estoque",
              min_value=0,
              value=int(prod_atual["estoque"]),
              step=1,
          )

        if st.form_submit_button("Guardar Alterações do Produto"):
          lucro_unit = nova_venda - novo_custo
          margem_perc = (
              (lucro_unit / novo_custo) * 100
              if novo_custo > 0
              else (100.0 if nova_venda > 0 else 0.0)
          )
          status = (
              "Disponível"
              if novo_qtd > 3
              else ("Estoque Baixo" if novo_qtd > 0 else "Esgotado")
          )

          conn = criar_conexao()
          cursor = conn.cursor()
          cursor.execute(
              """
                UPDATE produtos SET nome = ?, categoria = ?, preco_custo = ?, preco_venda = ?, lucro_unitario = ?, margem = ?, estoque = ?, status = ? WHERE codigo = ?
            """,
              (
                  novo_nome,
                  nova_cat,
                  f"R$ {novo_custo:.2f}",
                  f"R$ {nova_venda:.2f}",
                  f"R$ {lucro_unit:.2f}",
                  f"{margem_perc:.1f}%",
                  novo_qtd,
                  status,
                  prod_atual["codigo"],
              ),
          )
          conn.commit()
          conn.close()

          st.success("Produto atualizado e salvo no banco SQL!")
          st.rerun()
    else:
      st.info("Nenhum produto cadastrado para editar.")

  elif acao_produto == "Remover Produto":
    if not df_produtos.empty:
      with st.form("form_remover_produto"):
        prod_para_remover = st.selectbox(
            "Selecione o produto que deseja excluir", df_produtos["nome"].tolist()
        )
        if st.form_submit_button("Excluir Produto Selecionado"):
          conn = criar_conexao()
          cursor = conn.cursor()
          cursor.execute("DELETE FROM produtos WHERE nome = ?", (prod_para_remover,))
          conn.commit()
          conn.close()
          st.success("Produto removido do banco SQL com sucesso!")
          st.rerun()
    else:
      st.info("Nenhum produto cadastrado para remover.")

  st.divider()
  st.subheader("📦 Produtos Disponíveis em Estoque")
  if not df_produtos.empty:
    st.dataframe(df_produtos, use_container_width=True)
  else:
    st.info("Nenhum produto cadastrado no estoque.")

elif menu_opcao == "Clientes":
  st.markdown("## 👥 Gestão de Clientes")
  acao_cliente = st.radio(
      "O que você deseja fazer?",
      ["Cadastrar Novo Cliente", "Editar Cliente", "Remover Cliente"],
      horizontal=True,
  )
  st.divider()

  if acao_cliente == "Cadastrar Novo Cliente":
    proximo_id_num = len(df_clientes) + 1
    id_automatico = f"CLI-{proximo_id_num:03d}"
    with st.form("form_cliente", clear_on_submit=True):
      st.info(f"🆔 **ID Gerado:** {id_automatico}")
      col1, col2 = st.columns(2)
      with col1:
        nome_cliente = st.text_input("Nome Completo")
        tel_cliente = st.text_input("Telefone / WhatsApp")
        cep_cliente = st.text_input("CEP")
        rua_cliente = st.text_input("Rua / Avenida")
      with col2:
        num_cliente = st.text_input("Número da Casa / Apto")
        bairro_cliente = st.text_input("Bairro")
        cidade_cliente = st.text_input("Cidade")

      if st.form_submit_button("Salvar Cliente") and nome_cliente:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                id_automatico,
                nome_cliente,
                tel_cliente,
                cep_cliente,
                rua_cliente,
                num_cliente,
                bairro_cliente,
                cidade_cliente,
            ),
        )
        conn.commit()
        conn.close()

        st.success(f"Cliente '{nome_cliente}' salvo no banco SQL com sucesso!")
        st.rerun()

  elif acao_cliente == "Editar Cliente":
    if not df_clientes.empty:
      with st.form("form_editar_cliente"):
        cliente_editar = st.selectbox(
            "Selecione o cliente para alterar dados", df_clientes["nome"].tolist()
        )
        cli_atual = df_clientes[df_clientes["nome"] == cliente_editar].iloc[0]

        col_e1, col_e2 = st.columns(2)
        with col_e1:
          novo_nome = st.text_input("Nome Completo", value=cli_atual["nome"])
          novo_tel = st.text_input("Telefone / WhatsApp", value=cli_atual["telefone"])
          novo_cep = st.text_input("CEP", value=cli_atual["cep"])
          nova_rua = st.text_input("Rua / Avenida", value=cli_atual["rua"])
        with col_e2:
          novo_num = st.text_input("Número", value=cli_atual["numero"])
          novo_bairro = st.text_input("Bairro", value=cli_atual["bairro"])
          nova_cidade = st.text_input("Cidade", value=cli_atual["cidade"])

        if st.form_submit_button("Guardar Alterações"):
          conn = criar_conexao()
          cursor = conn.cursor()
          cursor.execute(
              """
                UPDATE clientes SET nome = ?, telefone = ?, cep = ?, rua = ?, numero = ?, bairro = ?, cidade = ? WHERE id_cliente = ?
            """,
              (
                  novo_nome,
                  novo_tel,
                  novo_cep,
                  nova_rua,
                  novo_num,
                  novo_bairro,
                  nova_cidade,
                  cli_atual["id_cliente"],
              ),
          )
          conn.commit()
          conn.close()

          st.success("Dados do cliente atualizados no banco SQL!")
          st.rerun()
    else:
      st.info("Nenhum cliente cadastrado para editar.")

  elif acao_cliente == "Remover Cliente":
    if not df_clientes.empty:
      with st.form("form_remover_cliente"):
        cliente_para_remover = st.selectbox(
            "Selecione o cliente que deseja excluir", df_clientes["nome"].tolist()
        )
        if st.form_submit_button("Excluir Cliente Selecionado"):
          conn = criar_conexao()
          cursor = conn.cursor()
          cursor.execute(
              "DELETE FROM clientes WHERE nome = ?", (cliente_para_remover,)
          )
          conn.commit()
          conn.close()
          st.success("Cliente removido do banco SQL com sucesso!")
          st.rerun()
    else:
      st.info("Nenhum cliente cadastrado para remover.")

  st.divider()
  st.subheader("📖 Lista de Clientes Registrados")
  if not df_clientes.empty:
    st.dataframe(df_clientes, use_container_width=True)
  else:
    st.info("Nenhum cliente cadastrado ainda.")

elif menu_opcao == "Vendas":
  st.markdown("## 🛍️ Registo Profissional de Vendas")
  if df_produtos.empty or df_clientes.empty:
    st.warning(
        "⚠️ Cadastre ao menos um **Produto** e um **Cliente** antes de"
        " registrar vendas."
    )
  else:
    with st.form("form_venda_dinamica", clear_on_submit=True):
      col1, col2 = st.columns(2)
      with col1:
        cliente_venda = st.selectbox("Cliente", df_clientes["nome"].tolist())
        perfume_venda = st.selectbox("Perfume Vendido", df_produtos["nome"].tolist())
        qtd_venda = st.number_input("Quantidade", min_value=1, value=1, step=1)

      with col2:
        st.markdown("### 💳 Forma e Valor do Pagamento")
        metodo_principal = st.selectbox(
            "Selecione a forma de pagamento",
            [
                "Pix",
                "Dinheiro",
                "Cartão de Débito",
                "Cartão de Crédito",
            ],
        )

        valor_recebido = st.number_input(
            "Valor Pago / Recebido (R$)", min_value=0.0, format="%.2f"
        )

        detalhe_pagamento = metodo_principal
        status_pag = "Pago"

        if metodo_principal == "Cartão de Crédito":
          tipo_cartao = st.radio(
              "Tipo de Crédito", ["À vista", "Parcelado"], horizontal=True
          )
          if tipo_cartao == "Parcelado":
            parcelas = st.selectbox(
                "Número de Parcelas",
                [
                    "2x",
                    "3x",
                    "4x",
                    "5x",
                    "6x",
                    "7x",
                    "8x",
                    "9x",
                    "10x",
                    "11x",
                    "12x",
                ],
            )
            detalhe_pagamento = f"Cartão de Crédito (Parcelado {parcelas})"
          else:
            detalhe_pagamento = f"Cartão de Crédito (À vista)"
          status_pag = "Pago no Crédito"

        elif metodo_principal == "Cartão de Débito":
          detalhe_pagamento = "Cartão de Débito"
          status_pag = "Pago no Débito"

        elif metodo_principal == "Pix":
          detalhe_pagamento = "Pix"
          status_pag = "Pago no Pix"

        elif metodo_principal == "Dinheiro":
          detalhe_pagamento = "Dinheiro"
          status_pag = "Pago em Dinheiro"

      if st.form_submit_button("Finalizar e Registrar Venda"):
        prod_row = df_produtos[df_produtos["nome"] == perfume_venda].iloc[0]
        estoque_atual = int(prod_row["estoque"])

        if qtd_venda > estoque_atual:
          st.error(
              f"⚠️ Stock insuficiente! Apenas {estoque_atual} unidades"
              f" disponíveis de '{perfume_venda}'."
          )
        else:
          novo_estoque = estoque_atual - qtd_venda
          novo_status_estoque = (
              "Disponível"
              if novo_estoque > 3
              else ("Estoque Baixo" if novo_estoque > 0 else "Esgotado")
          )

          p_venda_str = prod_row["preco_venda"]
          p_lucro_str = prod_row["lucro_unitario"]

          p_venda = float(
              str(p_venda_str).replace("R$", "").replace(",", ".").strip()
          )
          p_lucro = float(
              str(p_lucro_str).replace("R$", "").replace(",", ".").strip()
          )

          val_total = qtd_venda * p_venda
          val_efetivo = valor_recebido if valor_recebido > 0 else val_total
          lucro_total = qtd_venda * p_lucro
          data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

          conn = criar_conexao()
          cursor = conn.cursor()

          cursor.execute(
              """
                UPDATE produtos SET estoque = ?, status = ? WHERE nome = ?
            """,
              (novo_estoque, novo_status_estoque, perfume_venda),
          )

          cursor.execute(
              """
                INSERT INTO vendas (data_hora, cliente, perfume, quantidade, valor_total, forma_pagamento, status_pagamento, lucro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
              (
                  data_hora_atual,
                  cliente_venda,
                  perfume_venda,
                  qtd_venda,
                  val_efetivo,
                  detalhe_pagamento,
                  status_pag,
                  lucro_total,
              ),
          )

          conn.commit()
          conn.close()

          st.success(
              "Venda registada com sucesso e salva no banco de dados SQL!"
              f" (Restam {novo_estoque} no stock)"
          )
          st.rerun()

  st.divider()
  st.subheader("📜 Histórico Geral de Vendas")
  if not df_vendas.empty:
    st.dataframe(df_vendas, use_container_width=True)
  else:
    st.info("Nenhuma venda registada até o momento.")
