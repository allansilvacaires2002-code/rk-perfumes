from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="2B Perfumes - ERP",
    page_icon="🧴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilização CSS completa para o Modo Escuro Profundo
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0d1117 !important;
            color: #ffffff !important;
            font-family: 'Inter', sans-serif;
        }
        section[data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 1px solid #30363d;
        }
        section[data-testid="stSidebar"] .stRadio label {
            color: #e6edf3 !important;
            font-weight: 500;
        }
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }
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
        h1, h2, h3, h4, p, span, label {
            color: #ffffff !important;
        }
        .stButton>button {
            background-color: #00b074 !important;
            color: white !important;
            border-radius: 8px;
            padding: 8px 16px;
            border: none;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #00915f !important;
        }
        input, select, textarea {
            background-color: #21262d !important;
            color: #ffffff !important;
            border: 1px solid #30363d !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Inicialização e verificação de integridade das tabelas na sessão
if (
    "produtos" not in st.session_state
    or len(st.session_state.produtos.columns) != 9
):
  st.session_state.produtos = pd.DataFrame(
      columns=[
          "Código",
          "Nome do Perfume",
          "Categoria",
          "Preço de Custo",
          "Preço de Venda",
          "Lucro Unitário",
          "Margem (%)",
          "Estoque",
          "Status",
      ]
  )

if (
    "clientes" not in st.session_state
    or len(st.session_state.clientes.columns) != 8
):
  st.session_state.clientes = pd.DataFrame(
      columns=[
          "ID do Cliente",
          "Nome Completo",
          "Telefone",
          "CEP",
          "Rua/Avenida",
          "Número",
          "Bairro",
          "Cidade",
      ]
  )

if (
    "vendas" not in st.session_state
    or "Forma de Pagamento" not in st.session_state.vendas.columns
):
  st.session_state.vendas = pd.DataFrame(
      columns=[
          "Data e Hora",
          "Cliente",
          "Perfume",
          "Quantidade",
          "Valor Total",
          "Forma de Pagamento",
          "Status Pagamento",
          "Lucro",
      ]
  )

# --- BARRA LATERAL ---
with st.sidebar:
  st.markdown("### 🧴 **2B Perfumes**")
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
  st.caption("Usuário: **2B** | ERP Ativo")

# --- CONTEÚDO PRINCIPAL ---

if menu_opcao == "Dashboard":
  st.markdown("## 📊 Resumo / Dashboard Executivo")
  st.markdown(
      "Visão completa e consolidada do desempenho do seu negócio de perfumes."
  )

  faturamento_total = (
      st.session_state.vendas["Valor Total"].sum()
      if not st.session_state.vendas.empty
      else 0.0
  )
  lucro_liquido = (
      st.session_state.vendas["Lucro"].sum()
      if not st.session_state.vendas.empty
      else 0.0
  )
  total_vendas = (
      len(st.session_state.vendas) if not st.session_state.vendas.empty else 0
  )
  total_clientes = len(st.session_state.clientes)

  mais_vendido = "Nenhuma venda"
  if (
      not st.session_state.vendas.empty
      and "Perfume" in st.session_state.vendas.columns
  ):
    mais_vendido = (
        st.session_state.vendas["Perfume"].mode()[0]
        if not st.session_state.vendas["Perfume"].empty
        else "N/A"
    )

  col1, col2, col3 = st.columns(3)
  with col1:
    st.markdown(
        f"""<div class="metric-card"><h4>Faturamento Total</h4><h2>R$ {faturamento_total:.2f}</h2></div>""",
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f"""<div class="metric-card"><h4>Lucro Líquido</h4><h2>R$ {lucro_liquido:.2f}</h2></div>""",
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        f"""<div class="metric-card"><h4>Total de Vendas</h4><h2>{total_vendas}</h2></div>""",
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

  # --- FECHAMENTO DE CAIXA ---
  st.subheader("💵 Fechamento de Caixa por Forma de Pagamento")
  if (
      not st.session_state.vendas.empty
      and "Forma de Pagamento" in st.session_state.vendas.columns
  ):
    caixa_por_pagamento = (
        st.session_state.vendas.groupby("Forma de Pagamento")["Valor Total"]
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

    col_caixa_tabela, col_caixa_info = st.columns([2, 1])
    with col_caixa_tabela:
      st.dataframe(caixa_por_pagamento, use_container_width=True)
    with col_caixa_info:
      st.info(
          "💡 **Fechamento:** Totais agrupados por forma de pagamento para"
          " facilitar a conferência do caixa[cite: 1, 2]."
      )
  else:
    st.info(
        "Ainda não há vendas registradas para montar o fechamento de caixa."
    )

  st.divider()

  col_graf, col_alert = st.columns([2, 1])
  with col_graf:
    st.subheader("📈 Desempenho Profissional de Vendas")
    if not st.session_state.vendas.empty:
      df_temp = st.session_state.vendas.copy()
      df_temp["Dia"] = df_temp["Data e Hora"].apply(lambda x: str(x).split()[0])
      df_vendas_graf = (
          df_temp.groupby("Dia")["Valor Total"].sum().reset_index()
      )

      fig = go.Figure()
      fig.add_trace(
          go.Bar(
              x=df_vendas_graf["Dia"],
              y=df_vendas_graf["Valor Total"],
              name="Faturamento (R$)",
              marker_color="#00b074",
              opacity=0.85,
          )
      )
      fig.add_trace(
          go.Scatter(
              x=df_vendas_graf["Dia"],
              y=df_vendas_graf["Valor Total"],
              name="Tendência",
              mode="lines+markers",
              line=dict(color="#f59e0b", width=3),
              marker=dict(size=8),
          )
      )
      fig.update_layout(
          plot_bgcolor="#161b22",
          paper_bgcolor="#0d1117",
          font=dict(color="#ffffff"),
          margin=dict(l=10, r=10, t=30, b=10),
          legend=dict(
              orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
          ),
          xaxis=dict(showgrid=False),
          yaxis=dict(showgrid=True, gridcolor="#30363d"),
      )
      st.plotly_chart(fig, use_container_width=True)
    else:
      st.info("Ainda não há dados suficientes para exibir o gráfico profissional.")

  with col_alert:
    st.subheader("⚠️ Alerta de Estoque Baixo")
    if not st.session_state.produtos.empty:
      estoque_baixo = st.session_state.produtos[
          st.session_state.produtos["Status"].isin(
              ["Estoque Baixo", "Esgotado"]
          )
      ]
      if not estoque_baixo.empty:
        for index, row in estoque_baixo.iterrows():
          st.warning(
              f"🚨 **{row['Nome do Perfume']}** ({row['Estoque']} un. -"
              f" {row['Status']})"
          )
      else:
        st.success(
            "✅ Todos os produtos estão com níveis saudáveis de estoque!"
        )
    else:
      st.info("Nenhum produto cadastrado.")

  st.divider()
  st.subheader("📋 Histórico Geral de Vendas")
  if not st.session_state.vendas.empty:
    st.dataframe(st.session_state.vendas, use_container_width=True)
  else:
    st.info("Nenhuma venda registrada até o momento.")

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
    st.markdown("### ➕ Cadastrar Novo Produto")
    with st.form("form_produto", clear_on_submit=True):
      col1, col2, col3 = st.columns(3)
      with col1:
        cod_prod = st.text_input("Código do Produto")
        nome_prod = st.text_input("Nome / Marca / Linha (Ex: Essencial Oud)")
      with col2:
        cat_prod = st.selectbox(
            "Categoria", ["Masculino", "Feminino", "Unissex"]
        )
        preco_custo = st.number_input(
            "Preço de Custo (R$)", min_value=0.0, format="%.2f"
        )
      with col3:
        preco_venda = st.number_input(
            "Preço de Venda (R$)", min_value=0.0, format="%.2f"
        )
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
        novo_df = pd.DataFrame(
            [[
                cod_prod,
                nome_prod,
                cat_prod,
                f"R$ {preco_custo:.2f}",
                f"R$ {preco_venda:.2f}",
                f"R$ {lucro_unit:.2f}",
                f"{margem_perc:.1f}%",
                qtd_estoque,
                status,
            ]],
            columns=st.session_state.produtos.columns,
        )
        st.session_state.produtos = pd.concat(
            [st.session_state.produtos, novo_df], ignore_index=True
        )
        st.success("Perfume cadastrado com sucesso[cite: 1, 2]!")
        st.rerun()

  elif acao_produto == "Editar Produto":
    st.markdown("### ✏️ Editar Produto")
    if not st.session_state.produtos.empty:
      with st.form("form_editar_produto"):
        produto_editar = st.selectbox(
            "Selecione o perfume para alterar dados",
            st.session_state.produtos["Nome do Perfume"].tolist(),
        )
        prod_atual = st.session_state.produtos[
            st.session_state.produtos["Nome do Perfume"] == produto_editar
        ].iloc[0]
        custo_limpo = float(
            str(prod_atual["Preço de Custo"])
            .replace("R$", "")
            .replace(",", ".")
            .strip()
        )
        venda_limpo = float(
            str(prod_atual["Preço de Venda"])
            .replace("R$", "")
            .replace(",", ".")
            .strip()
        )

        col1, col2, col3 = st.columns(3)
        with col1:
          novo_cod = st.text_input("Código do Produto", value=prod_atual["Código"])
          novo_nome = st.text_input(
              "Nome do Perfume", value=prod_atual["Nome do Perfume"]
          )
        with col2:
          nova_cat = st.selectbox(
              "Categoria",
              ["Masculino", "Feminino", "Unissex"],
              index=(
                  ["Masculino", "Feminino", "Unissex"].index(
                      prod_atual["Categoria"]
                  )
                  if prod_atual["Categoria"]
                  in ["Masculino", "Feminino", "Unissex"]
                  else 0
              ),
          )
          novo_custo = st.number_input(
              "Preço de Custo (R$)",
              min_value=0.0,
              value=custo_limpo,
              format="%.2f",
          )
        with col3:
          nova_venda = st.number_input(
              "Preço de Venda (R$)",
              min_value=0.0,
              value=venda_limpo,
              format="%.2f",
          )
          novo_qtd = st.number_input(
              "Quantidade em Estoque",
              min_value=0,
              value=int(prod_atual["Estoque"]),
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
          idx = st.session_state.produtos[
              st.session_state.produtos["Nome do Perfume"] == produto_editar
          ].index[0]
          st.session_state.produtos.at[idx, "Código"] = novo_cod
          st.session_state.produtos.at[idx, "Nome do Perfume"] = novo_nome
          st.session_state.produtos.at[idx, "Categoria"] = nova_cat
          st.session_state.produtos.at[idx, "Preço de Custo"] = (
              f"R$ {novo_custo:.2f}"
          )
          st.session_state.produtos.at[idx, "Preço de Venda"] = (
              f"R$ {nova_venda:.2f}"
          )
          st.session_state.produtos.at[idx, "Lucro Unitário"] = (
              f"R$ {lucro_unit:.2f}"
          )
          st.session_state.produtos.at[idx, "Margem (%)"] = (
              f"{margem_perc:.1f}%"
          )
          st.session_state.produtos.at[idx, "Estoque"] = novo_qtd
          st.session_state.produtos.at[idx, "Status"] = status
          st.success("Produto atualizado com sucesso[cite: 1, 2]!")
          st.rerun()
    else:
      st.info("Nenhum produto cadastrado para editar.")

  elif acao_produto == "Remover Produto":
    st.markdown("### 🗑️ Remover Produto")
    if not st.session_state.produtos.empty:
      with st.form("form_remover_produto"):
        prod_para_remover = st.selectbox(
            "Selecione o produto que deseja excluir",
            st.session_state.produtos["Nome do Perfume"].tolist(),
        )
        if st.form_submit_button("Excluir Produto Selecionado"):
          st.session_state.produtos = st.session_state.produtos[
              st.session_state.produtos["Nome do Perfume"] != prod_para_remover
          ].reset_index(drop=True)
          st.success("Produto removido com sucesso[cite: 1, 2]!")
          st.rerun()
    else:
      st.info("Nenhum produto cadastrado para remover.")

  st.divider()
  st.subheader("📦 Produtos Disponíveis em Estoque")
  if not st.session_state.produtos.empty:
    st.dataframe(st.session_state.produtos, use_container_width=True)
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
    proximo_id_num = len(st.session_state.clientes) + 1
    id_automatico = f"CLI-{proximo_id_num:03d}"
    st.markdown("### ➕ Cadastrar Novo Cliente")
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
        novo_cli = pd.DataFrame(
            [[
                id_automatico,
                nome_cliente,
                tel_cliente,
                cep_cliente,
                rua_cliente,
                num_cliente,
                bairro_cliente,
                cidade_cliente,
            ]],
            columns=st.session_state.clientes.columns,
        )
        st.session_state.clientes = pd.concat(
            [st.session_state.clientes, novo_cli], ignore_index=True
        )
        st.success(f"Cliente '{nome_cliente}' cadastrado com sucesso[cite: 1, 2]!")
        st.rerun()

  elif acao_cliente == "Editar Cliente":
    st.markdown("### ✏️ Editar Cliente")
    if not st.session_state.clientes.empty:
      with st.form("form_editar_cliente"):
        cliente_editar = st.selectbox(
            "Selecione o cliente para alterar dados",
            st.session_state.clientes["Nome Completo"].tolist(),
        )
        cli_atual = st.session_state.clientes[
            st.session_state.clientes["Nome Completo"] == cliente_editar
        ].iloc[0]

        col_e1, col_e2 = st.columns(2)
        with col_e1:
          novo_nome = st.text_input(
              "Nome Completo", value=cli_atual["Nome Completo"]
          )
          novo_tel = st.text_input(
              "Telefone / WhatsApp", value=cli_atual["Telefone"]
          )
          novo_cep = st.text_input("CEP", value=cli_atual["CEP"])
          nova_rua = st.text_input("Rua / Avenida", value=cli_atual["Rua/Avenida"])
        with col_e2:
          novo_num = st.text_input("Número", value=cli_atual["Número"])
          novo_bairro = st.text_input("Bairro", value=cli_atual["Bairro"])
          nova_cidade = st.text_input("Cidade", value=cli_atual["Cidade"])

        if st.form_submit_button("Guardar Alterações"):
          idx = st.session_state.clientes[
              st.session_state.clientes["Nome Completo"] == cliente_editar
          ].index[0]
          st.session_state.clientes.at[idx, "Nome Completo"] = novo_nome
          st.session_state.clientes.at[idx, "Telefone"] = novo_tel
          st.session_state.clientes.at[idx, "CEP"] = novo_cep
          st.session_state.clientes.at[idx, "Rua/Avenida"] = nova_rua
          st.session_state.clientes.at[idx, "Número"] = novo_num
          st.session_state.clientes.at[idx, "Bairro"] = novo_bairro
          st.session_state.clientes.at[idx, "Cidade"] = nova_cidade
          st.success("Dados do cliente atualizados com sucesso[cite: 1, 2]!")
          st.rerun()
    else:
      st.info("Nenhum cliente cadastrado para editar.")

  elif acao_cliente == "Remover Cliente":
    st.markdown("### 🗑️ Remover Cliente")
    if not st.session_state.clientes.empty:
      with st.form("form_remover_cliente"):
        cliente_para_remover = st.selectbox(
            "Selecione o cliente que deseja excluir",
            st.session_state.clientes["Nome Completo"].tolist(),
            key="rem_cli",
        )
        if st.form_submit_button("Excluir Cliente Selecionado"):
          st.session_state.clientes = st.session_state.clientes[
              st.session_state.clientes["Nome Completo"] != cliente_para_remover
          ].reset_index(drop=True)
          st.success(
              f"Cliente '{cliente_para_remover}' removido com sucesso[cite: 1, 2]!"
          )
          st.rerun()
    else:
      st.info("Nenhum cliente cadastrado para remover.")

  st.divider()
  st.subheader("📖 Lista de Clientes Registrados")
  if not st.session_state.clientes.empty:
    st.dataframe(st.session_state.clientes, use_container_width=True)
  else:
    st.info("Nenhum cliente cadastrado ainda.")

elif menu_opcao == "Vendas":
  st.markdown("## 🛍️ Registo Profissional de Vendas")
  if st.session_state.produtos.empty or st.session_state.clientes.empty:
    st.warning(
        "⚠️ Cadastre ao menos um **Produto** e um **Cliente** antes de"
        " registrar vendas."
    )
  else:
    with st.form("form_venda_dinamica", clear_on_submit=True):
      col1, col2 = st.columns(2)
      with col1:
        cliente_venda = st.selectbox(
            "Cliente", st.session_state.clientes["Nome Completo"].tolist()
        )
        perfume_venda = st.selectbox(
            "Perfume Vendido",
            st.session_state.produtos["Nome do Perfume"].tolist(),
        )
        qtd_venda = st.number_input(
            "Quantidade", min_value=1, value=1, step=1
        )

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
            detalhe_pagamento = "Cartão de Crédito (À vista)"
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
        idx_prod = st.session_state.produtos[
            st.session_state.produtos["Nome do Perfume"] == perfume_venda
        ].index[0]
        estoque_atual = int(st.session_state.produtos.at[idx_prod, "Estoque"])

        if qtd_venda > estoque_atual:
          st.error(
              f"⚠️ Stock insuficiente! Apenas {estoque_atual} unidades"
              f" disponíveis de '{perfume_venda}'."
          )
        else:
          novo_estoque = estoque_atual - qtd_venda
          st.session_state.produtos.at[idx_prod, "Estoque"] = novo_estoque

          novo_status_estoque = (
              "Disponível"
              if novo_estoque > 3
              else ("Estoque Baixo" if novo_estoque > 0 else "Esgotado")
          )
          st.session_state.produtos.at[idx_prod, "Status"] = (
              novo_status_estoque
          )

          data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

          prod_row = st.session_state.produtos.loc[idx_prod]
          p_venda_str = prod_row["Preço de Venda"]
          p_lucro_str = prod_row["Lucro Unitário"]

          p_venda = float(
              str(p_venda_str).replace("R$", "").replace(",", ".").strip()
          )
          p_lucro = float(
              str(p_lucro_str).replace("R$", "").replace(",", ".").strip()
          )

          val_total = qtd_venda * p_venda
          val_efetivo = valor_recebido if valor_recebido > 0 else val_total
          lucro_total = qtd_venda * p_lucro

          nova_venda = pd.DataFrame(
              [[
                  data_hora_atual,
                  cliente_venda,
                  perfume_venda,
                  qtd_venda,
                  val_efetivo,
                  detalhe_pagamento,
                  status_pag,
                  lucro_total,
              ]],
              columns=st.session_state.vendas.columns,
          )
          st.session_state.vendas = pd.concat(
              [st.session_state.vendas, nova_venda], ignore_index=True
          )

          st.success(
              "Venda registada com sucesso, stock atualizado e caixa"
              f" sincronizado[cite: 1, 2]! (Restam {novo_estoque} no stock)"
          )
          st.rerun()

  st.divider()
  st.subheader("📜 Histórico Geral de Vendas")
  if not st.session_state.vendas.empty:
    st.dataframe(st.session_state.vendas, use_container_width=True)
  else:
    st.info("Nenhuma venda realizada.")
