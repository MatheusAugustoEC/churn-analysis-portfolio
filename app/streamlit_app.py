import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import sys
import os
import io

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from bigquery_client import run_query

st.set_page_config(
    page_title="Churn Analytics",
    page_icon="🔴",
    layout="wide"
)

# Sidebar
st.sidebar.title("🔴 Churn Analytics")
pagina = st.sidebar.radio("", ["📊 Visão Geral", "🔍 Predição Individual", "👥 Clientes em Risco"])

# Carrega dados
@st.cache_data
def load_data():
    return run_query("SELECT * FROM `churn_dataset.churn_predictions`")

df = load_data()

if pagina == "📊 Visão Geral":
    st.title("📊 Visão Geral")
    
    # KPIs
    total_clientes = len(df)
    taxa_churn = df['churn_real'].mean() * 100
    alto_risco = len(df[df['risco'] == 'Alto'])
    receita_risco = df[df['risco'] == 'Alto']['MonthlyCharges'].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Clientes", f"{total_clientes:,}")
    col2.metric("Taxa de Churn", f"{taxa_churn:.1f}%")
    col3.metric("Clientes em Risco Alto", f"{alto_risco:,}")
    col4.metric("Receita em Risco", f"$ {receita_risco:,.2f}")
    st.divider()

    # Gráfico 1 — Distribuição de Risco
    risco_counts = df['risco'].value_counts()
    fig1 = go.Figure(go.Pie(
        labels=risco_counts.index,
        values=risco_counts.values,
        hole=0.4,
        marker_colors=['#C06B6B', '#D4A96A', '#5B8DB8'],
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Clientes: %{value}<br>Proporção: %{percent}<extra></extra>'
    ))
    fig1.update_layout(title='Distribuição de Risco de Churn', template='plotly_white')

    # Gráfico 2 — Churn por Contrato
    churn_contrato = df.groupby('Contract')['churn_real'].mean() * 100
    fig2 = go.Figure(go.Bar(
        x=churn_contrato.index,
        y=churn_contrato.values,
        marker_color='#5B8DB8',
        text=[f'{v:.1f}%' for v in churn_contrato.values],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Taxa de Churn: %{y:.1f}%<extra></extra>'
    ))
    fig2.update_layout(title='Taxa de Churn por Contrato', template='plotly_white',
                       yaxis_title='Taxa de Churn (%)', yaxis=dict(range=[0, churn_contrato.max() * 1.2]))

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3 — Churn por Internet
    churn_internet = df.groupby('InternetService')['churn_real'].mean() * 100
    fig3 = go.Figure(go.Bar(
        x=churn_internet.index,
        y=churn_internet.values,
        marker_color='#5B8DB8',
        text=[f'{v:.1f}%' for v in churn_internet.values],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Taxa de Churn: %{y:.1f}%<extra></extra>'
    ))
    fig3.update_layout(title='Taxa de Churn por Serviço de Internet', template='plotly_white',
                       yaxis_title='Taxa de Churn (%)', yaxis=dict(range=[0, churn_internet.max() * 1.2]))

    # Gráfico 4 — Churn por Tenure
    churn_tenure = df.groupby('tenure')['churn_real'].mean() * 100
    fig4 = go.Figure(go.Scatter(
        x=churn_tenure.index,
        y=churn_tenure.values,
        mode='lines+markers',
        line=dict(color='#5B8DB8', width=2),
        marker=dict(size=4),
        hovertemplate='<b>Mês %{x}</b><br>Taxa de Churn: %{y:.1f}%<extra></extra>'
    ))
    fig4.update_layout(
        title='Taxa de Churn por Tempo de Permanência',
        template='plotly_white',
        xaxis_title='Meses',
        yaxis_title='Taxa de Churn (%)',
        hovermode='x unified'
    )

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig3, use_container_width=True)
    col2.plotly_chart(fig4, use_container_width=True)


elif pagina == "🔍 Predição Individual":
    st.title("🔍 Predição Individual")
    st.write("Preencha os dados do cliente para prever a probabilidade de churn.")

    col1, col2, col3 = st.columns(3)

    with col1:
        tenure = st.number_input("Tempo de Permanência (meses)", min_value=0, max_value=72, value=12)
        monthly_charges = st.number_input("Mensalidade ($)", min_value=0.0, max_value=200.0, value=50.0)
        contract = st.selectbox("Tipo de Contrato", ["Month-to-month", "One_year", "Two_year"])
        internet_service = st.selectbox("Serviço de Internet", 
            ["DSL", "Fiber optic", "No"],
            format_func=lambda x: x)

    with col2:
        gender = st.selectbox("Gênero", ["Male", "Female"])
        senior_citizen = st.selectbox("Idoso", ["Não", "Sim"])
        partner = st.selectbox("Parceiro", ["Não", "Sim"])
        dependents = st.selectbox("Dependentes", ["Não", "Sim"])

    with col3:
        phone_service = st.selectbox("Serviço Telefônico", ["Não", "Sim"])
        multiple_lines = st.selectbox("Múltiplas Linhas", ["Não", "Sim"])
        paperless_billing = st.selectbox("Fatura Digital", ["Não", "Sim"])
        payment_method = st.selectbox("Método de Pagamento", [
            "Bank_transfer_automatic",
            "Credit_card_automatic", 
            "Electronic_check",
            "Mailed_check"
        ], format_func=lambda x: x.replace("_", " "))

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        online_security = st.selectbox("Segurança Online", ["Não", "Sim"])
        online_backup = st.selectbox("Backup Online", ["Não", "Sim"])
    with col2:
        device_protection = st.selectbox("Proteção de Dispositivo", ["Não", "Sim"])
        tech_support = st.selectbox("Suporte Técnico", ["Não", "Sim"])
    with col3:
        streaming_tv = st.selectbox("Streaming TV", ["Não", "Sim"])
        streaming_movies = st.selectbox("Streaming Filmes", ["Não", "Sim"])

    if st.button("Analisar Risco de Churn"):
        payload = {
            "SeniorCitizen": 1 if senior_citizen == "Sim" else 0,
            "Partner": 1 if partner == "Sim" else 0,
            "Dependents": 1 if dependents == "Sim" else 0,
            "tenure": float(tenure),
            "PhoneService": 1 if phone_service == "Sim" else 0,
            "PaperlessBilling": 1 if paperless_billing == "Sim" else 0,
            "MonthlyCharges": float(monthly_charges),
            "gender_Male": 1 if gender == "Male" else 0,
            "MultipleLines_Yes": 1 if multiple_lines == "Sim" else 0,
            "InternetService_Fiber_optic": 1 if internet_service == "Fiber optic" else 0,
            "InternetService_No": 1 if internet_service == "No" else 0,
            "OnlineSecurity_Yes": 1 if online_security == "Sim" else 0,
            "OnlineBackup_Yes": 1 if online_backup == "Sim" else 0,
            "DeviceProtection_Yes": 1 if device_protection == "Sim" else 0,
            "TechSupport_Yes": 1 if tech_support == "Sim" else 0,
            "StreamingTV_Yes": 1 if streaming_tv == "Sim" else 0,
            "StreamingMovies_Yes": 1 if streaming_movies == "Sim" else 0,
            "Contract_One_year": 1 if contract == "One_year" else 0,
            "Contract_Two_year": 1 if contract == "Two_year" else 0,
            "PaymentMethod_Credit_card_automatic": 1 if payment_method == "Credit_card_automatic" else 0,
            "PaymentMethod_Electronic_check": 1 if payment_method == "Electronic_check" else 0,
            "PaymentMethod_Mailed_check": 1 if payment_method == "Mailed_check" else 0
        }

        response = requests.post("http://localhost:8000/predict", json=payload)
        resultado = response.json()

        prob = resultado['probabilidade_churn'] * 100
        risco = resultado['risco']
        cor = '#C06B6B' if risco == 'Alto' else '#D4A96A' if risco == 'Médio' else '#5B8DB8'

        st.markdown(f"""
        <div style='background-color:{cor}20; border-left: 5px solid {cor}; padding: 20px; border-radius: 5px;'>
            <h2 style='color:{cor}'>Risco {risco}</h2>
            <h3>Probabilidade de Churn: {prob:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)


elif pagina == "👥 Clientes em Risco":
    st.title("👥 Clientes em Risco")

    risco_filtro = st.selectbox(
    "Filtrar por Nível de Risco",
    options=["Todos", "Alto", "Médio", "Baixo"]
    )

    df_filtrado = df if risco_filtro == "Todos" else df[df['risco'] == risco_filtro]
    df_filtrado = df_filtrado.sort_values('probabilidade_churn', ascending=False).reset_index(drop=True)

    # Métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes Filtrados", f"{len(df_filtrado):,}")
    col2.metric("Probabilidade Média", f"{df_filtrado['probabilidade_churn'].mean() / 100 :.1%}")
    col3.metric("Receita em Risco", f"$ {df_filtrado['MonthlyCharges'].sum():,.2f}")

    st.divider()

    # Tabela
    st.dataframe(
        df_filtrado[['customerID', 'probabilidade_churn', 'risco', 'MonthlyCharges', 'Contract', 'tenure', 'InternetService']].rename(columns={
            'customerID': 'ID Cliente',
            'probabilidade_churn': 'Prob. Churn',
            'risco': 'Risco',
            'MonthlyCharges': 'Mensalidade ($)',
            'Contract': 'Contrato',
            'tenure': 'Meses',
            'InternetService': 'Internet'
        }),
        use_container_width=True,
        hide_index=True
    )

    # Download
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name="clientes_em_risco.csv",
        mime="text/csv"
    )

    buffer = io.BytesIO()
    df_filtrado.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    st.download_button(
        label="📥 Baixar Excel",
        data=buffer,
        file_name="clientes_em_risco.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )