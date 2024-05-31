# Painel de Clima e Trânsito

Este é um projeto que utiliza Dash para criar um painel interativo de clima e trânsito. O painel permite visualizar dados de clima e tráfego em gráficos e mapas.

## Pré-requisitos

Para executar este projeto, você precisará dos seguintes componentes:

- Pentaho Data Integration (Kettle - PDI)
- Python 3
- Servidor MySQL
- Pacotes Python:
  - dash
  - plotly
  - pandas
  - sqlalchemy
  - mysql-connector-python
  - python-dotenv

## Instalação

### Pentaho Data Integration

1. Baixe e instale o Pentaho Data Integration (Kettle) a partir do [site oficial](https://privatefilesbucket-community-edition.s3.us-west-2.amazonaws.com/9.4.0.0-343/ce/client-tools/pdi-ce-9.4.0.0-343.zip).
2. Extraia o conteúdo do arquivo baixado para um diretório de sua escolha.
3. Adicione a variável de ambiente 'PENTAHO_JAVA_HOME' apontando para versão 8 do Java Development Kit (JDK).

### Servidor MySQL

1. Baixe e instale o MySQL Server a partir do [site oficial](https://dev.mysql.com/downloads/mysql/).
2. Siga as instruções de instalação e configure uma senha para o usuário root.

### Configuração do Pentaho Data Integration

1. No diretório de instalação do Pentaho, encontre o arquivo `kettle.properties`.
2. Abra o arquivo `kettle.properties` em um editor de texto.
3. Preencha as seguintes variáveis com as informações do seu banco de dados:

    ```properties
    DB_HOST=host
    DB_NAME=db_name
    DB_PORT=port
    DB_USERNAME=user
    DB_PASSWORD=senha
    ```

### Projeto Python

1. Clone este repositório:

    ```sh
    git clone https://github.com/gschw4b/weather_traffic_project.git
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):

    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais do banco de dados:

    ```bash
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_HOST=localhost
    DB_NAME=nome_do_banco
    ```

5. Execute o script SQL para criar a estrutura do banco de dados:

    ```sh
    mysql -u root -p < model.sql
    ```

## Uso

1. Execute o job `root.kjb` usando o Spoon do Pentaho, para realizar a Extração, Transformação e Carga dos dados:

    ```sh
    /path/to/data-integration/spoon.sh -file=path/to/root.kjb  # No Windows, use `spoon.bat` em vez de `spoon.sh`
    ```

2. Execute a aplicação, para gerar o dashboard interativo:

    ```sh
    python data_visualization.py
    ```

3. Abra seu navegador e acesse `http://127.0.0.1:8050/` para visualizar o dashboard.

## Estrutura do Projeto

- `data_visualization.py`: Arquivo principal contendo o código da aplicação Dash.
- `requirements.txt`: Lista de dependências do projeto.
- `model.sql`: Script SQL para criação da estrutura do banco de dados.
- `root.kjb`: Job orquestrador responsável por executar as transformações responsáveis (Pentaho Data Integration).
- `get-weather.ktr`: Transformação responsável pela carga de Clima (Pentaho Data Integration).
- `get-traffic.ktr`: Transformação responsável pela carga de Tráfego (Pentaho Data Integration).
- `.env`: Arquivo de variáveis de ambiente (não incluído no repositório).
- `README.md`: Este arquivo, contendo informações sobre o projeto.