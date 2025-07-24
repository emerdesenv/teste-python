import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configura página
st.set_page_config(page_title="Radar de Desempenho", layout="centered")

# Título estilizado
st.markdown("<h1 style='text-align: center; color: #0E76A8;'>📊 Desempenho dos Alunos</h1>", unsafe_allow_html=True)

# Upload do arquivo Excel
arquivo = st.file_uploader("Envie o arquivo de notas (.xlsx):", type=["xlsx"])

if arquivo is not None:
    # Lê a planilha específica
    df = pd.read_excel(arquivo, sheet_name="N2")

    # Colunas que queremos no radar
    colunas_metrica = [
        "Planejamento e Gestão",
        "Colaboração e Comunicação",
        "Desenvolvimento Técnico",
        "Documentação",
        "Testes e Validação"
    ]

    # Dropdown centralizado com os alunos
    aluno = st.selectbox("Selecione um aluno:", df["Aluno"])

    # Filtra os dados para o aluno selecionado, pegando só as colunas das métricas
    dados = df.loc[df["Aluno"] == aluno, colunas_metrica].iloc[0]

    labels = list(dados.index)
    valores = list(dados.values)

    # Fecha o gráfico adicionando o primeiro valor ao final para fechar o radar
    valores += [valores[0]]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += [angles[0]]

    # Cores e estilo
    cor_linha = "#1f77b4"
    cor_preenchimento = "#a6c8e0"

    # Cria gráfico
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, valores, 'o-', linewidth=2, color=cor_linha)
    ax.fill(angles, valores, alpha=0.25, color=cor_preenchimento)

    # Estiliza labels e grade
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=12)
    ax.set_title(f"Desempenho de: {aluno}", fontsize=16, pad=35, color="#333333")
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.spines['polar'].set_color('#444')
    ax.spines['polar'].set_linewidth(1)

    # Ajusta a escala do gráfico
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=10)

    # Mostra gráfico
    st.pyplot(fig)
else:
    st.info("Por favor, envie um arquivo Excel com os dados dos alunos.")