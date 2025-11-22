'import pandas as pd
import plotly.express as px

def test_cumulative_logic():
    # Create dummy data
    data = {
        'data_venda': pd.to_datetime(['2023-01-15', '2023-01-20', '2023-02-10', '2023-02-25', '2023-03-05']),
        'valor_total': [100, 200, 150, 250, 300]
    }
    df = pd.DataFrame(data)
    
    # Logic from app.py
    df_chart = df.copy()
    df_chart['mes_ano'] = df_chart['data_venda'].dt.to_period('M').astype(str)
    
    monthly_revenue = df_chart.groupby('mes_ano')['valor_total'].sum().reset_index()
    monthly_revenue['faturamento_acumulado'] = monthly_revenue['valor_total'].cumsum()
    
    print("Monthly Revenue:")
    print(monthly_revenue)
    
    # Expected values:
    # Jan: 100+200 = 300. Cum: 300
    # Feb: 150+250 = 400. Cum: 300+400 = 700
    # Mar: 300. Cum: 700+300 = 1000
    
    expected_cum = [300, 700, 1000]
    assert monthly_revenue['faturamento_acumulado'].tolist() == expected_cum
    print("Verification Successful!")

if __name__ == "__main__":
    test_cumulative_logic()
