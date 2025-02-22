# Análise Climática para Cultivo de Café no Brasil

Esta aplicação utiliza dados climáticos (temperatura e de umidade) para analisar a viabilidade do cultivo de café em diferentes estados do Brasil. A aplicação exibe métricas climáticas, gráficos de temperatura e umidade, e um mapa geográfico com um heatmap das temperaturas médias.

## Estrutura do Código

- `app.py`: Arquivo principal da aplicação que contém a lógica para obter dados climáticos, processar e exibir as informações usando Streamlit.


## Funcionalidades

- Seleção de estado brasileiro para análise climática.
- Exibição de métricas de temperatura média, máxima e mínima, e umidade média, máxima e mínima dos últimos 30 dias.
- Gráficos de temperatura e umidade ao longo dos últimos 30 dias.
- Mapa geográfico com um heatmap das temperaturas médias por estado.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python:
  - streamlit
  - requests
  - pandas
  - plotly
  - geopandas

## Instalação

1. Clone o repositório para sua máquina local:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. Crie um ambiente virtual de acordo com seu Sistema Operacional (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  
    venv\Scripts\activate
    ```

3. Instale os pacotes necessários:
    ```bash
    pip install -r requirements.txt
    ```

## Como Iniciar

1. Execute a aplicação Streamlit:
    ```bash
    streamlit run app.py
    ```

2. Acesse a aplicação no navegador através do endereço:
    ```
    http://localhost:8501
    ```

## Estrutura do Código

- `app.py`: Contém a lógica principal da aplicação, incluindo:
  - Definição das coordenadas dos estados brasileiros.
  - Função para obter dados climáticos da API Open-Meteo.
  - Função para carregar dados geográficos dos estados brasileiros.
  - Interface com Streamlit para exibir métricas, gráficos e mapa geográfico.

## Exemplo de Uso

1. Selecione um estado brasileiro no dropdown.
2. Visualize as métricas de temperatura e umidade dos últimos 30 dias.
3. Explore os gráficos de temperatura e umidade.
4. Veja o mapa geográfico com o heatmap das temperaturas médias por estado.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.