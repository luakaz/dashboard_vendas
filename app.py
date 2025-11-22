import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Configuration ---
st.set_page_config(
    page_title="Dashboard de Vendas",
    layout="wide"
)

# --- Constants ---
DEFAULT_DATA_PATH = "vendas_exemplo.csv"

# --- Helper Functions ---

@st.cache_data
def load_data(file) -> pd.DataFrame:
    """
    Loads data from a CSV file (or file-like object) into a pandas DataFrame.
    
    Args:
        file: The file path or file-like object to read.
        
    Returns:
        pd.DataFrame: The loaded DataFrame with 'data_venda' converted to datetime.
    """
    try:
        df = pd.read_csv(file)
        # Ensure date column is datetime
        if 'data_venda' in df.columns:
            df['data_venda'] = pd.to_datetime(df['data_venda'])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return pd.DataFrame()

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renders sidebar filters and applies them to the DataFrame.
    
    Args:
        df: The original DataFrame.
        
    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    st.sidebar.header("Filtros")
    
    # Date Range Filter
    if 'data_venda' in df.columns and not df.empty:
        min_date = df['data_venda'].min().date()
        max_date = df['data_venda'].max().date()
        
        # Default to full range
        date_range = st.sidebar.date_input(
            "Intervalo de Datas",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
        
        # Handle cases where date_input returns a single date (during selection)
        if len(date_range) == 2:
            start_date, end_date = date_range
            # Filter by date
            df = df[(df['data_venda'].dt.date >= start_date) & (df['data_venda'].dt.date <= end_date)]
        elif len(date_range) == 1:
            # If only one date is selected, filter by that specific date (or wait, but filtering is safer)
            start_date = date_range[0]
            df = df[df['data_venda'].dt.date == start_date]

    # City Filter
    if 'cidade' in df.columns:
        cities = sorted(df['cidade'].unique())
        selected_cities = st.sidebar.multiselect("Cidade", cities)
        if selected_cities:
            df = df[df['cidade'].isin(selected_cities)]
            
    # Channel Filter
    if 'canal_venda' in df.columns:
        channels = sorted(df['canal_venda'].unique())
        selected_channels = st.sidebar.multiselect("Canal de Venda", channels)
        if selected_channels:
            df = df[df['canal_venda'].isin(selected_channels)]
            
    # Category Filter
    if 'categoria_produto' in df.columns:
        categories = sorted(df['categoria_produto'].unique())
        selected_categories = st.sidebar.multiselect("Categoria de Produto", categories)
        if selected_categories:
            df = df[df['categoria_produto'].isin(selected_categories)]
            
    return df

def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Computes Key Performance Indicators (KPIs) from the DataFrame.
    
    Args:
        df: The DataFrame to compute KPIs from.
        
    Returns:
        dict: A dictionary containing 'total_revenue', 'order_count', and 'avg_ticket'.
    """
    if df.empty:
        return {
            "total_revenue": 0.0,
            "order_count": 0,
            "avg_ticket": 0.0
        }
        
    total_revenue = df['valor_total'].sum()
    order_count = df['id_pedido'].nunique()
    avg_ticket = total_revenue / order_count if order_count > 0 else 0.0
    
    return {
        "total_revenue": total_revenue,
        "order_count": order_count,
        "avg_ticket": avg_ticket
    }

def plot_revenue_by_day(df: pd.DataFrame):
    """
    Plots a line chart of revenue by day.
    """
    if df.empty:
        st.info("Sem dados para exibir o gráfico de faturamento por dia.")
        return

    daily_revenue = df.groupby('data_venda')['valor_total'].sum().reset_index()
    fig = px.line(
        daily_revenue, 
        x='data_venda', 
        y='valor_total',
        title="Faturamento por Dia",
        labels={'data_venda': 'Data', 'valor_total': 'Faturamento (R$)'}
    )
    st.plotly_chart(fig)

def plot_revenue_by_city(df: pd.DataFrame):
    """
    Plots a horizontal bar chart of revenue by city.
    """
    if df.empty:
        st.info("Sem dados para exibir o gráfico de faturamento por cidade.")
        return

    city_revenue = df.groupby('cidade')['valor_total'].sum().reset_index()
    city_revenue = city_revenue.sort_values(by='valor_total', ascending=True) # Sort for bar chart logic (bottom to top)
    
    fig = px.bar(
        city_revenue,
        x='valor_total',
        y='cidade',
        orientation='h',
        title="Faturamento por Cidade",
        labels={'valor_total': 'Faturamento (R$)', 'cidade': 'Cidade'}
    )
    st.plotly_chart(fig)

def plot_revenue_by_channel(df: pd.DataFrame):
    """
    Plots a pie/donut chart of revenue by sales channel.
    """
    if df.empty:
        st.info("Sem dados para exibir o gráfico de faturamento por canal.")
        return

    channel_revenue = df.groupby('canal_venda')['valor_total'].sum().reset_index()
    
    fig = px.pie(
        channel_revenue,
        names='canal_venda',
        values='valor_total',
        title="Faturamento por Canal de Venda",
        hole=0.4 # Donut chart
    )
    st.plotly_chart(fig)

def build_top_products_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds a DataFrame for the top products by revenue.
    
    Args:
        df: The source DataFrame.
        
    Returns:
        pd.DataFrame: Aggregated DataFrame with product, order count, and total revenue.
    """
    if df.empty:
        return pd.DataFrame()
        
    top_products = df.groupby('produto').agg(
        pedidos=('id_pedido', 'nunique'),
        faturamento=('valor_total', 'sum')
    ).reset_index()
    
    top_products = top_products.sort_values(by='faturamento', ascending=False)
    return top_products

# --- Main Function ---

def main():
    st.title("Dashboard de Vendas")
    
    # 1. Data Loading
    uploaded_file = st.sidebar.file_uploader("Carregar arquivo CSV", type=["csv"])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    elif os.path.exists(DEFAULT_DATA_PATH):
        # st.sidebar.info(f"Carregando arquivo padrão: {DEFAULT_DATA_PATH}")
        df = load_data(DEFAULT_DATA_PATH)
    else:
        st.warning("Por favor, faça o upload de um arquivo CSV para começar.")
        return

    if df.empty:
        st.error("O arquivo carregado está vazio ou inválido.")
        return

    # Validate required columns
    required_columns = ['data_venda', 'id_pedido', 'cidade', 'canal_venda', 'categoria_produto', 'produto', 'valor_total']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"O arquivo está faltando as seguintes colunas obrigatórias: {', '.join(missing_columns)}")
        return

    # 2. Filters
    df_filtered = apply_filters(df)
    
    if df_filtered.empty:
        st.warning("Não há dados para os filtros selecionados.")
        return

    # 3. KPIs
    kpis = compute_kpis(df_filtered)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Faturamento Total", f"R$ {kpis['total_revenue']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col2.metric("Número de Pedidos", kpis['order_count'])
    col3.metric("Ticket Médio", f"R$ {kpis['avg_ticket']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.markdown("---")

    # 4. Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        plot_revenue_by_day(df_filtered)
        
    with col_right:
        plot_revenue_by_city(df_filtered)
        
    st.markdown("---")
    
    col_pie, col_table = st.columns([1, 2]) # Adjust ratio as needed
    
    with col_pie:
        plot_revenue_by_channel(df_filtered)
        
    with col_table:
        st.subheader("Top Produtos por Receita")
        top_products_df = build_top_products_table(df_filtered)
        
        # Formatting for display
        if not top_products_df.empty:
            st.dataframe(
                top_products_df.head(10).style.format({
                    "faturamento": "R$ {:,.2f}"
                }),
                hide_index=True
            )
        else:
            st.info("Sem dados de produtos.")

if __name__ == "__main__":
    main()
