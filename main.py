import pip
import xlsxwriter


import numpy as np
import streamlit as st
import pandas as pd
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="Calculadora de Média", layout="centered")

# Título da aplicação
st.title("Calculadora de Média para Alunos de Engenharia")

# Entrada de número de notas
number = st.number_input("Quantas notas deseja inserir?", min_value=1, step=1)
nota = []

# Coleta das notas
st.subheader("Insira as notas")
for ii in range(int(number)):
    nota.append(st.number_input(f"Nota {ii+1}:", min_value=0.0, max_value=10.0, step=0.1))

# Calcula a média e a nota mínima para o exame
if nota:
    nota = np.array(nota)
    media_notas = nota.mean()
    nota_minima = max(0, (5 - media_notas * 0.6) / 0.4)

    # Exibe a média e a nota mínima
    st.subheader("Resultados")
    st.write(f"**Média das notas:** {media_notas:.2f}")
    st.write(f"**Nota mínima necessária no exame:** {nota_minima:.2f}")

    # Botão para gerar e baixar o arquivo Excel
    if st.button("Baixar Resultados como Excel"):
        # Cria um DataFrame com os dados
        df = pd.DataFrame({
            "Nota": nota,
            "Média": [media_notas] * len(nota),
            "Nota Mínima no Exame": [nota_minima] * len(nota)
        })

        # Converte o DataFrame para bytes para download
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Resultados")
            writer.close()
            output.seek(0)

        # Configura o botão de download
        st.download_button(
            label="Baixar Excel",
            data=output,
            file_name="Resultados_Calculo_Media.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
