import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- Page Config ---
st.set_page_config(
    page_title="Milma Dairy Analytics",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Enhanced Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2.5rem !important; max-width: 1440px; }

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
}
[data-testid="stSidebar"] * { color: #f8fafc !important; }
[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 14px;
    padding: 6px;
    gap: 8px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: #64748b !important;
    padding: 0.6rem 1.5rem !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: #2563eb !important;
    color: white !important;
}

/* KPI Cards */
.kpi-card {
    border-radius: 20px;
    padding: 1.5rem;
    border: 1px solid rgba(255,255,255,0.8);
    box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.05);
    transition: all 0.2s ease;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1); }
.kpi-icon {
    width: 44px; height: 44px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; margin-bottom: 1rem;
}
.kpi-value { font-size: 1.8rem; font-weight: 800; letter-spacing: -1px; }

/* Header & Titles */
.top-header {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
    border-radius: 24px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    color: white;
}
.sec-title {
    font-size: 1rem; font-weight: 700; color: #1e293b;
    margin: 1.5rem 0 1rem;
    display: flex; align-items: center; gap: 10px;
}
.sec-title .line { flex: 1; height: 1px; background: #e2e8f0; }

.insight {
    background: #f1f5f9;
    border-left: 4px solid #2563eb;
    border-radius: 8px;
    padding: 1rem;
    font-size: 0.85rem;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def chart(height=320, margin=None, xaxis_title='', yaxis_title='', extra_margin_r=10, **kwargs):
    """Refactored helper to prevent key conflicts by merging axis configs."""
    m = margin or dict(l=10, r=extra_margin_r, t=20, b=10)
    
    # Base configuration
    layout = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Plus Jakarta Sans', color='#475569', size=11),
        height=height,
        margin=m,
        xaxis=dict(showgrid=False, tickfont=dict(size=11), title=xaxis_title),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=11), title=yaxis_title),
    )
    
    # Safely merge nested dictionaries like xaxis and yaxis if they exist in kwargs
    for axis in ['xaxis', 'yaxis']:
        if axis in kwargs:
            layout[axis].update(kwargs.pop(axis))
            
    layout.update(kwargs)
    return layout

CAT_COLORS = {'Curd': '#2563eb', 'Cheese': '#f59e0b', 'Paneer': '#10b981', 'Sambaram': '#8b5cf6', 'Yogurt': '#f43f5e'}

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    p = lambda f: os.path.join(base, f)
    # Using dummy loads for logic demonstration, replace with your pd.read_csv calls
    daily = pd.read_csv(p('dashboard_daily.csv'), parse_dates=['Date'])
    monthly_cat = pd.read_csv(p('dashboard_monthly_category.csv'))
    forecast = pd.read_csv(p('dashboard_forecast_2026.csv'), parse_dates=['Date'])
    # ... load other files similarly ...
    monthly_cat['Date'] = pd.to_datetime(monthly_cat['Year'].astype(str) + '-' + monthly_cat['Month'].astype(str).str.zfill(2) + '-01')
    return daily, monthly_cat, forecast # Add other variables as needed

# Assuming data is loaded
daily, monthly_cat, forecast = load_data() 
# (Note: In your real script, ensure all 7 variables are returned/unpacked)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<div style='text-align:center; padding: 20px 0;'><h2 style='margin:0;'>🥛 MILMA</h2><small>MRCMPU · KCMMF</small></div>", unsafe_allow_html=True)
    sel_cats = st.multiselect("Categories", sorted(daily['Category'].unique()), default=list(daily['Category'].unique()))
    sel_years = st.multiselect("Years", sorted(daily['Year'].unique()), default=list(daily['Year'].unique()))

fd = daily[daily['Category'].isin(sel_cats) & daily['Year'].isin(sel_years)]

# --- Header ---
st.markdown("""
<div class='top-header'>
    <div style='text-transform: uppercase; letter-spacing: 2px; font-size: 0.7rem; opacity: 0.8; font-weight: 700;'>Sales Intelligence Portal</div>
    <h1 style='margin: 10px 0 5px 0; font-size: 2.2rem;'>Milma Fermented Dairy Analytics</h1>
    <div style='opacity: 0.7; font-size: 0.9rem;'>Performance Tracking & Demand Forecasting (2021–2026)</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🎯 Menu", "🔮 Forecast"])

with tab1:
    if not fd.empty:
        # KPIs
        c1, c2, c3, c4, c5 = st.columns(5)
        metrics = [
            ("💰", "Revenue", f"₹{fd['Total_Amount'].sum()/1e6:.1f}M", "#eff6ff", "#2563eb"),
            ("⚖️", "Volume", f"{fd['Group_Qty_Kg'].sum()/1000:.1f}T", "#f0fdf4", "#16a34a"),
            ("📊", "Avg Rate", f"₹{fd['Avg_Rate'].mean():.1f}", "#fffbeb", "#d97706"),
            ("🏷️", "SKUs", str(fd['Product'].nunique()), "#faf5ff", "#7c3aed"),
            ("📅", "Days", str(fd['Date'].nunique()), "#fff1f2", "#e11d48")
        ]
        for col, (icon, lab, val, bg, txt) in zip([c1, c2, c3, c4, c5], metrics):
            col.markdown(f"""<div class='kpi-card' style='background:{bg};'><div class='kpi-icon' style='background:white;'>{icon}</div>
            <div style='font-size:0.7rem; font-weight:700; color:#64748b; text-transform:uppercase;'>{lab}</div>
            <div class='kpi-value' style='color:{txt};'>{val}</div></div>""", unsafe_allow_html=True)

        st.markdown("<div class='sec-title'>Performance Breakdown <span class='line'></span></div>", unsafe_allow_html=True)
        col_left, col_right = st.columns([3, 2])
        
        with col_left:
            # FIXED: Top 10 Products by Revenue
            top10 = fd.groupby(['Category','Product'])['Total_Amount'].sum().reset_index().nlargest(10,'Total_Amount')
            fig4 = go.Figure(go.Bar(
                x=top10['Total_Amount']/1000, y=top10['Product'], orientation='h',
                marker=dict(color=[CAT_COLORS.get(c,'#64748b') for c in top10['Category']], opacity=0.9),
                text=[f'₹{v/1000:.0f}K' for v in top10['Total_Amount']], textposition='outside'
            ))
            # Pass the custom yaxis config THROUGH the helper function
            fig4.update_layout(**chart(
                height=400, 
                xaxis_title='Revenue (₹ Thousands)', 
                extra_margin_r=80,
                yaxis=dict(autorange='reversed', showgrid=False) 
            ))
            st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

        with col_right:
            cat_rev = fd.groupby('Category')['Total_Amount'].sum().reset_index()
            fig2 = go.Figure(go.Pie(
                labels=cat_rev['Category'], values=cat_rev['Total_Amount'], hole=0.7,
                marker=dict(colors=[CAT_COLORS.get(c) for c in cat_rev['Category']], line=dict(color='white', width=2))
            ))
            fig2.update_layout(**chart(height=400), showlegend=True)
            st.plotly_chart(fig2, use_container_width=True)

# ... (Include other tabs with similar refactored chart calls) ...

st.markdown(f"<div style='text-align:center; padding:40px; color:#94a3b8; font-size:0.8rem;'>{st.get_option('page_title')} · Version 2.1 · 2026 Internal Report</div>", unsafe_allow_html=True)
