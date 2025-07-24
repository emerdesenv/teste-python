import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configurações iniciais
st.set_page_config(page_title="Radar de Desempenho", layout="centered")
st.markdown("<h1 style='text-align: center; color: #0E76A8;'>📊 Desempenho dos Alunos</h1>", unsafe_allow_html=True)
st.markdown("**Envie o arquivo de notas (.xlsx) usando o campo abaixo:**")

# Upload do arquivo
arquivo = st.file_uploader(label="", type=['xlsx'], help="Tamanho máximo: 200MB • Formato XLSX")

# Função para gráfico radar
def gerar_grafico_radar(titulo, labels, valores):
    valores += [valores[0]]
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True).tolist()

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, valores, 'o-', linewidth=2, color="#1f77b4")
    ax.fill(angles, valores, alpha=0.25, color="#a6c8e0")

    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=12)
    ax.set_title(titulo, fontsize=16, pad=35, color="#333333")
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.spines['polar'].set_color('#444')
    ax.spines['polar'].set_linewidth(1)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=10)

    st.pyplot(fig)

# Função para processar a aba N1
def processar_aba_n1(arquivo):
    df = pd.read_excel(arquivo, sheet_name="N1")
    colunas_metricas = ["Atividades em Sala", "Desafios", "Soft Skills"]

    if "Aluno" not in df.columns:
        st.error("❌ A aba N1 precisa conter a coluna 'Aluno'.")
        st.stop()

    return df, colunas_metricas

# Função para processar a aba N2
def processar_aba_n2(arquivo):
    df = pd.read_excel(arquivo, sheet_name="N2")
    colunas_metricas = [
        "Planejamento e Gestão",
        "Colaboração e Comunicação",
        "Desenvolvimento Técnico",
        "Documentação",
        "Testes e Validação"
    ]

    if "Aluno" not in df.columns:
        st.error("❌ A aba N2 precisa conter a coluna 'Aluno'.")
        st.stop()

    return df, colunas_metricas

# Quando o arquivo for enviado
if arquivo is not None:
    abas = pd.ExcelFile(arquivo).sheet_names
    aba_escolhida = st.selectbox("Selecione a aba com os dados:", abas)

    # Carregamento conforme a aba
    if aba_escolhida == "N1":
        df, colunas_metricas = processar_aba_n1(arquivo)
    elif aba_escolhida == "N2":
        df, colunas_metricas = processar_aba_n2(arquivo)
    else:
        st.warning("⚠️ Aba não reconhecida.")
        st.stop()

    # Validação das colunas esperadas
    if not all(col in df.columns for col in colunas_metricas):
        st.error(f"❌ A aba selecionada não contém todas as colunas esperadas: {colunas_metricas}")
        st.stop()

    # Seleção de aluno
    aluno = st.selectbox("Selecione um aluno:", df["Aluno"])
    dados_aluno = df[df["Aluno"] == aluno].iloc[0]

    # ✅ Trilha
    if "Trilhas" in df.columns:
        trilha = str(dados_aluno["Trilhas"]).strip().lower()
        if trilha == "ok":
            st.success("✅ Todas as trilhas foram concluídas com sucesso!")
        else:
            st.warning("⚠️ O aluno ainda não concluiu todas as trilhas.")

    # ✅ Nota EAD
    if "EAD/Nota" in df.columns:
        try:
            nota_ead = float(str(dados_aluno["EAD/Nota"]).replace(",", ".").strip())
            if nota_ead == 10.0:
                st.success("✅ EAD concluído com nota máxima!")
            elif nota_ead < 6.0:
                st.warning(f"⚠️ Nota de EAD inferior a 6: {nota_ead}")
            else:
                st.info(f"ℹ️ Nota de EAD: {nota_ead}")
        except Exception as e:
            st.warning(f"⚠️ Não foi possível ler a nota de EAD. Detalhes: {e}")

    # 🎯 Gráfico radar
    dados_grafico = dados_aluno[colunas_metricas]
    gerar_grafico_radar(f"Desempenho de: {aluno}", list(dados_grafico.index), list(dados_grafico.values))

else:
    st.info("Por favor, envie um arquivo Excel com os dados dos alunos.")
