# Dashboard de Vendas com Streamlit

Este projeto é um dashboard interativo de vendas construído com Python e Streamlit. Ele permite visualizar KPIs, gráficos de faturamento por dia, cidade e canal de venda, além de uma tabela com os produtos mais vendidos.

## Estrutura do Projeto

- `app.py`: Código fonte principal do dashboard.
- `vendas_exemplo.csv`: Arquivo de dados de exemplo.
- `requirements.txt`: Lista de dependências do projeto.

## Pré-requisitos

- Python 3.8 ou superior instalado.

## Como Executar

Siga os passos abaixo para configurar o ambiente e rodar o dashboard.

### 1. Criar um Ambiente Virtual

Abra o terminal (PowerShell ou CMD) na pasta do projeto e execute:

```bash
# Windows
python -m venv venv
```

### 2. Ativar o Ambiente Virtual

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
.\venv\Scripts\activate.bat
```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 4. Executar o Dashboard

Inicie o servidor do Streamlit:

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no seu navegador padrão.

## Funcionalidades

- **Upload de Arquivo**: Carregue seu próprio arquivo CSV de vendas.
- **Filtros**: Filtre os dados por data, cidade, canal de venda e categoria.
- **KPIs**: Visualize Faturamento Total, Número de Pedidos e Ticket Médio.
- **Gráficos Interativos**: Acompanhe a evolução das vendas e distribuição por cidade e canal.
- **Top Produtos**: Veja a lista dos produtos com maior receita.

## Como subir para o GitHub

Siga este passo a passo para colocar seu projeto no GitHub.

### 1. Criar o arquivo .gitignore
Certifique-se de que existe um arquivo chamado `.gitignore` na raiz do projeto com o seguinte conteúdo (para não enviar arquivos desnecessários):
```
venv/
__pycache__/
*.pyc
```

### 2. Inicializar o Git
Abra o terminal na pasta do projeto e rode:

```bash
git init
```

### 3. Adicionar os arquivos
Prepare os arquivos para serem salvos:

```bash
git add .
```

### 4. Salvar a versão (Commit)
Salve o estado atual do projeto:

```bash
git commit -m "Primeira versão do dashboard de vendas"
```

### 5. Criar o repositório no GitHub
1. Acesse [github.com/new](https://github.com/new) (faça login se necessário).
2. Dê um nome para o repositório (ex: `dashboard-vendas`).
3. Deixe como "Public" ou "Private".
4. **Não** marque nenhuma opção de "Initialize this repository with..." (README, gitignore, license), pois já temos isso localmente.
5. Clique em **Create repository**.

### 6. Conectar e Enviar
Copie os comandos que aparecerão na tela do GitHub na seção **"…or push an existing repository from the command line"**. Eles serão parecidos com isso:

```bash
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/dashboard-vendas.git
git push -u origin main
```

Cole esses comandos no seu terminal e dê Enter. Se pedir senha, use seu Token de Acesso Pessoal (PAT) ou autentique via navegador se o Git solicitar.

Pronto! Seu projeto estará online.
