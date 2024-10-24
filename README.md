# projeto_an-lise_viabilidade_projetos
Estrutura lógica em que disponibiliza ao usuário que realize a adição dos dados para a realização de uma análise de viabilidade de projetos.

# Investment Feasibility Analysis Project

Este é um aplicativo Streamlit para análise de viabilidade de investimentos, fornecendo cálculos financeiros como VPL, TIR, ROI e análise de payback, além de gerar um relatório em PDF com os resultados.

## Funcionalidades

- Entrada de dados financeiros do projeto
- Cálculo do Valor Presente Líquido (VPL)
- Cálculo da Taxa Interna de Retorno (TIR)
- Cálculo do Retorno sobre o Investimento (ROI)
- Análise de payback
- Margem de segurança
- Geração de gráficos financeiros
- Geração de relatório em PDF

## Requisitos

- Python 3.x
- Bibliotecas: `streamlit`, `numpy`, `matplotlib`, `fpdf`, `numpy_financial`, `tempfile`, `os`

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
Copy
Navegue até o diretório do projeto:
cd seu_repositorio
Copy
Instale as dependências:
pip install -r requirements.txt
Copy
Uso
Execute o aplicativo com o seguinte comando:

streamlit run seu_arquivo.py
Copy
Substitua seu_arquivo.py pelo nome do arquivo que contém o código do aplicativo.

Como Funciona
Entrada de Dados: O usuário insere o prazo do projeto, valor do investimento, taxa de desconto e fluxos de caixa projetados.
Cálculos de Viabilidade: Com base nos dados inseridos, o aplicativo calcula o VPL, TIR, ROI, payback e margem de segurança.
Visualização: Os gráficos dos fluxos de caixa e da análise de sensibilidade são gerados e exibidos.
Relatório PDF: O usuário pode gerar e baixar um relatório em PDF que resume a análise.
Contribuição
Sinta-se à vontade para contribuir com melhorias ao projeto. Para iniciar, siga estas etapas:

Faça um fork do projeto
Crie uma branch para sua feature (git checkout -b feature/sua-feature)
Commit suas alterações (git commit -m 'Adicione sua feature')
Push para a branch (git push origin feature/sua-feature)
Abra um Pull Request
Licença
Este projeto é licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.

Este README fornece uma visão geral, instruções de instalação e como usar o projeto. Ajuste as informações conforme necessário para refletir seu projeto específico. ```
