import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# --- Page Config ---
st.set_page_config(
    page_title="Milma Dairy Analytics",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded" # Forces sidebar to start open
)

# --- Enhanced CSS for Visibility ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

/* Main Body Background and Font */
.stApp {
    background-color: #f8fafc !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* SIDEBAR FIX: Dark background, White text */
[data-testid="stSidebar"] {
    background-color: #0f172a !important; /* Deep navy/black */
    border-right: 1px solid #1e293b;
    min-width: 280px !important;
}

/* Sidebar Text & Labels */
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
[data-testid="stSidebar"] label {
    font-weight: 700 !important;
    color: #94a3b8 !important; /* Muted gray for labels */
    text-transform: uppercase;
    font-size: 0.75rem;
}

/* Main Content Text Visibility */
h1, h2, h3, p, span {
    color: #0f172a !important;
}

/* Header Banner */
.top-header {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    color: white !important;
}
.top-header * { color: white !important; }

/* KPI Cards */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

/* Tab Contrast */
.stTabs [data-baseweb="tab"] {
    color: #475569 !important;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    color: #2563eb !important;
    border-bottom-color: #2563eb !important;
}
</style>
""", unsafe_allow_html=True)

# --- Refactored Chart Helper (Forces Black Text) ---
def chart_style(fig, height=400, x_title="", y_title="", is_horizontal=False):
    fig.update_layout(
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#000000', family="Plus Jakarta Sans", size=12),
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            title=x_title,
            showgrid=False,
            tickfont=dict(color='#000000'),
            titlefont=dict(color='#000000')
        ),
        yaxis=dict(
            title=y_title,
            showgrid=True,
            gridcolor='#e2e8f0',
            tickfont=dict(color='#000000'),
            titlefont=dict(color='#000000'),
            autorange='reversed' if is_horizontal else None
        )
    )
    return fig

# --- Sidebar Content ---
with st.sidebar:
    st.markdown("### 🥛 MILMA SETTINGS")
    st.write("---")
    # Categories and Years filters go here
    # Example:
    # sel_cats = st.multiselect("Categories", ["Curd", "Paneer", "Cheese"])
    st.info("Sidebar is now high-contrast.")

# --- Main Dashboard ---
st.markdown("""
<div class='top-header'>
    <small>SALES INTELLIGENCE PORTAL</small>
    <h1>Milma Fermented Dairy Analytics</h1>
    <p>Performance Tracking & Demand Forecasting (2021–2026)</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🎯 Menu", "🔮 Forecast"])

with tab1:
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.subheader("Performance Breakdown")
        # Example Horizontal Bar Chart
        fig = go.Figure(go.Bar(
            x=[1018, 259, 27, 26, 21],
            y=["Skimmed Milk Curd", "Curd 500g", "Toned Milk", "Butter Milk", "Katti Moru"],
            orientation='h',
            marker_color='#2563eb',
            text=["₹1018M", "₹259K", "₹27K", "₹26K", "₹21K"],
            textposition='outside',
            textfont=dict(color='#000000') # Forces bar text to Black
        ))
        st.plotly_chart(chart_style(fig, is_horizontal=True), use_container_width=True)

    with col_right:
        st.subheader("Market Share")
        fig_pie = go.Figure(go.Pie(
            labels=["Curd", "Butter Milk", "Others"],
            values=[94, 4, 2],
            hole=0.6,
            textinfo='label+percent',
            textfont=dict(color='#000000') # Forces pie labels to Black
        ))
        st.plotly_chart(chart_style(fig_pie), use_container_width=True)
