import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import numpy_financial as npf
import tempfile
import os

# =====================
# EXTRACTION (Entrada de Dados)
# =====================
def entrada_dados():
    st.title("Investment Feasibility Analysis Project")

    st.subheader("Project Financial Data")
    prazo = st.number_input('Prazo do Projeto (anos)', min_value=1, max_value=50, value=5)
    valor_investimento = st.number_input('Valor do Investimento Inicial', value=50000.0)
    taxa_desconto = st.number_input('Taxa de Desconto (%)', min_value=0.0, max_value=100.0, value=10.0) / 100

    st.subheader("Fluxos de Caixa Projetados")
    fluxos_de_caixa = [-valor_investimento]  # investimento inicial
    for ano in range(1, prazo + 1):
        fluxo = st.number_input(f"Fluxo de Caixa no Ano {ano}", value=10000.0)
        fluxos_de_caixa.append(fluxo)

    fluxos_de_caixa = np.array(fluxos_de_caixa)
    return prazo, valor_investimento, taxa_desconto, fluxos_de_caixa

# =====================
# TRANSFORMATION (Cálculos)
# =====================
def calcular_vpl(fluxos_de_caixa, taxa_desconto):
    """Calcula o Valor Presente Líquido (VPL)"""
    return npf.npv(taxa_desconto, fluxos_de_caixa)

def calcular_tir(fluxos_de_caixa):
    """Calcula a Taxa Interna de Retorno (TIR)"""
    return npf.irr(fluxos_de_caixa)

def calcular_payback(fluxos_de_caixa):
    """Calcula o Payback, retornando o número de anos para o retorno do investimento"""
    acumulado = np.cumsum(fluxos_de_caixa)
    for i, valor in enumerate(acumulado):
        if valor >= 0:
            return i
    return None

def calcular_roi(valor_investimento, fluxos_de_caixa):
    """Calcula o Retorno sobre o Investimento (ROI)"""
    ganho_total = np.sum(fluxos_de_caixa[1:])  # Soma dos fluxos excluindo o investimento inicial
    roi = (ganho_total - valor_investimento) / valor_investimento
    return roi * 100  # Retorna em porcentagem

def calcular_margem_seguranca(vpl, valor_investimento):
    """Calcula a Margem de Segurança"""
    if valor_investimento != 0:
        margem = (vpl / valor_investimento) * 100
        return margem
    else:
        return None

# Função para centralizar cálculos
def calcular_viabilidade(fluxos_de_caixa, taxa_desconto, valor_investimento):
    vpl = calcular_vpl(fluxos_de_caixa, taxa_desconto)
    tir = calcular_tir(fluxos_de_caixa) * 100  # Converte TIR para percentual
    payback = calcular_payback(fluxos_de_caixa)
    roi = calcular_roi(valor_investimento, fluxos_de_caixa)
    margem_seguranca = calcular_margem_seguranca(vpl, valor_investimento)
    return vpl, tir, payback, roi, margem_seguranca

# =====================
# LOAD (Geração de Relatório e Visualização)
# =====================
def gerar_graficos(fluxos_de_caixa, taxa_desconto):
    """Gera gráficos dos fluxos de caixa e da análise de sensibilidade"""
    anos = list(range(len(fluxos_de_caixa)))
    acumulado = np.cumsum(fluxos_de_caixa)

    # Gerar os gráficos de fluxos de caixa
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(anos, fluxos_de_caixa, color='blue')
    ax1.set_xlabel('Ano')
    ax1.set_ylabel('Fluxo de Caixa')
    ax1.set_title('Fluxos de Caixa Projetados')
    ax1.grid(True)
    fig1.tight_layout()

    # Análise de Sensibilidade
    taxas = np.linspace(taxa_desconto - 0.1, taxa_desconto + 0.1, 20)
    vpl_sensibilidade = [calcular_vpl(fluxos_de_caixa, t) for t in taxas]

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(taxas * 100, vpl_sensibilidade, marker='o')
    ax2.axvline(x=taxa_desconto * 100, color='r', linestyle='--', label='Taxa de Desconto Atual')
    ax2.set_xlabel('Taxa de Desconto (%)')
    ax2.set_ylabel('VPL')
    ax2.set_title('Análise de Sensibilidade do VPL')
    ax2.grid(True)
    ax2.legend()
    fig2.tight_layout()

    # Salvar os gráficos temporariamente
    temp_dir = tempfile.mkdtemp()
    img1_path = f"{temp_dir}/fluxo_caixa.png"
    img2_path = f"{temp_dir}/sensibilidade.png"
    
    fig1.savefig(img1_path)
    fig2.savefig(img2_path)

    return fig1, fig2, img1_path, img2_path

def gerar_relatorio(vpl, tir, payback, roi, margem_seguranca, fluxos_de_caixa, taxa_desconto):
    """Gera o relatório com as principais métricas de viabilidade do projeto e gráficos"""
    pdf = FPDF()
    pdf.add_page()

    # Título do Relatório
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, 'Relatório de Viabilidade de Investimento', ln=True, align='C')

    # Resultados da Análise
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Valor Presente Líquido (VPL): R${vpl:.2f}", ln=True)
    pdf.cell(200, 10, f"Taxa Interna de Retorno (TIR): {tir:.2f}%", ln=True)
    pdf.cell(200, 10, f"Retorno sobre o Investimento (ROI): {roi:.2f}%", ln=True)
    if margem_seguranca is not None:
        pdf.cell(200, 10, f"Margem de Segurança: {margem_seguranca:.2f}%", ln=True)
    else:
        pdf.cell(200, 10, "Margem de Segurança: Não disponível", ln=True)

    if payback is not None:
        pdf.cell(200, 10, f"Período de Payback: {payback} anos", ln=True)
    else:
        pdf.cell(200, 10, "Período de Payback: Não alcançado", ln=True)

    # Recomendação com base nos resultados
    pdf.ln(10)
    if vpl > 0 and tir > taxa_desconto * 100:
        pdf.cell(200, 10, 'Recomendação: O projeto é viável e deve ser considerado para execução.', ln=True)
    else:
        pdf.cell(200, 10, 'Recomendação: O projeto não parece ser viável. É recomendada uma revisão nos fluxos de caixa.', ln=True)

    # Explicação detalhada antes dos gráficos
    pdf.ln(10)
    pdf.multi_cell(200, 10, "Explicações:\n"
                             "O Valor Presente Líquido (VPL) mostra quanto o projeto gera em valor presente "
                             "considerando uma taxa de desconto aplicada aos fluxos de caixa projetados. Um VPL positivo indica "
                             "que o projeto é lucrativo.\n"
                             "A Taxa Interna de Retorno (TIR) representa a taxa de desconto na qual o VPL se iguala a zero, "
                             "servindo como uma medida da rentabilidade do projeto.\n"
                             "O Retorno sobre o Investimento (ROI) demonstra o quanto o projeto retorna em relação ao valor "
                             "investido inicialmente.\n"
                             "O Payback refere-se ao tempo que leva para o valor investido ser recuperado pelos fluxos de caixa "
                             "gerados.\n"
                             "A Margem de Segurança é a proporção de segurança entre o VPL e o valor do investimento.")

    # Gerar e adicionar gráficos ao PDF
    _, _, img1_path, img2_path = gerar_graficos(fluxos_de_caixa, taxa_desconto)
    pdf.image(img1_path, x=10, y=None, w=180)  # Adicionar gráfico dos fluxos de caixa
    pdf.image(img2_path, x=10, y=None, w=180)  # Adicionar gráfico de sensibilidade

    # Salvar o PDF temporariamente
    temp_pdf_path = os.path.join(tempfile.gettempdir(), "relatorio_viabilidade.pdf")
    pdf.output(temp_pdf_path)
    
    # Limpar arquivos temporários
    os.remove(img1_path)
    os.remove(img2_path)

    return temp_pdf_path

def main():
    # Entrada dos dados e cálculos
    prazo, valor_investimento, taxa_desconto, fluxos_de_caixa = entrada_dados()
    vpl, tir, payback, roi, margem_seguranca = calcular_viabilidade(fluxos_de_caixa, taxa_desconto, valor_investimento)
    
    # Mostrar gráficos na interface
    st.subheader("Gráficos")
    fig1, fig2, _, _ = gerar_graficos(fluxos_de_caixa, taxa_desconto)
    st.pyplot(fig1)
    st.pyplot(fig2)

    # Geração do PDF
    if st.button("Gerar Relatório em PDF"):
        temp_pdf_path = gerar_relatorio(vpl, tir, payback, roi, margem_seguranca, fluxos_de_caixa, taxa_desconto)
        with open(temp_pdf_path, "rb") as f:
            st.download_button("Baixar Relatório", f, "relatorio_viabilidade.pdf")

if __name__ == "__main__":
    main()