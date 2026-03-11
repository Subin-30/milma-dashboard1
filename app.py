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

# --- Contrast-Optimized CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #f8fafc !important;
    color: #0f172a !important; /* Forces black/dark text for the main body */
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2.5rem !important; max-width: 1440px; }

/* Sidebar Styling - Keeps white text for dark background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
}
[data-testid="stSidebar"] * { color: #ffffff !important; }
[data-testid="stSidebar"] label {
    color: #cbd5e1 !important; /* Light gray for sidebar labels */
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Tab Styling - Black text for inactive, White for active */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 14px;
    padding: 6px;
    gap: 8px;
    border: 1px solid #e2e8f0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: #1e293b !important; /* Explicitly dark text */
    padding: 0.6rem 1.5rem !important;
}
.stTabs [aria-selected="true"] {
    background: #2563eb !important;
    color: white !important; /* Active tab stays white */
}

/* Section Title - Deep Black for visibility */
.sec-title {
    font-size: 1.1rem; 
    font-weight: 800; 
    color: #000000 !important; 
    margin: 2rem 0 1rem;
    display: flex; 
    align-items: center; 
    gap: 10px;
}
.sec-title .line { flex: 1; height: 1px; background: #cbd5e1; }

/* Insight Box - Dark text on light blue */
.insight {
    background: #eff6ff;
    border-left: 5px solid #2563eb;
    border-radius: 8px;
    padding: 1.2rem;
    font-size: 0.9rem;
    color: #1e3a8a !important;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# --- Refactored Chart Helper (Black Text Labels) ---
def chart(height=320, margin=None, xaxis_title='', yaxis_title='', extra_margin_r=10, **kwargs):
    m = margin or dict(l=10, r=extra_margin_r, t=25, b=10)
    
    # Base configuration using Dark Slate/Black for all diagram text
    layout = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Plus Jakarta Sans', color='#000000', size=12), # Forces black font
        height=height,
        margin=m,
        xaxis=dict(
            showgrid=False, 
            tickfont=dict(size=11, color='#000000'), 
            title=dict(text=xaxis_title, font=dict(color='#000000')),
            linecolor='#cbd5e1'
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#e2e8f0', 
            tickfont=dict(size=11, color='#000000'), 
            title=dict(text=yaxis_title, font=dict(color='#000000')),
            zerolinecolor='#cbd5e1'
        ),
    )
    
    # Conflict resolution for yaxis/xaxis overrides
    for axis in ['xaxis', 'yaxis']:
        if axis in kwargs:
            layout[axis].update(kwargs.pop(axis))
            
    layout.update(kwargs)
    return layout

# ... [Keep your existing load_data() and data processing logic here] ...

# --- Tab 1 Overview Implementation ---
with tab1:
    if not fd.empty:
        # KPI Row
        st.markdown("<div class='sec-title'>Key Performance Indicators <span class='line'></span></div>", unsafe_allow_html=True)
        # (Metric logic here...)

        # Charts Row
        col_a, col_b = st.columns([3, 2])
        
        with col_a:
            st.markdown("<div class='sec-title'>Top 10 Products <span class='line'></span></div>", unsafe_allow_html=True)
            top10 = fd.groupby(['Category','Product'])['Total_Amount'].sum().reset_index().nlargest(10,'Total_Amount')
            fig4 = go.Figure(go.Bar(
                x=top10['Total_Amount']/1000, 
                y=top10['Product'], 
                orientation='h',
                marker=dict(color='#2563eb', opacity=0.8),
                text=[f'₹{v/1000:.0f}K' for v in top10['Total_Amount']],
                textposition='outside',
                textfont=dict(color='#000000') # Forces bar labels to black
            ))
            
            # FIXED: Merge override into chart function
            fig4.update_layout(**chart(
                height=400, 
                xaxis_title='Revenue (₹ Thousands)',
                yaxis=dict(autorange='reversed', showgrid=False)
            ))
            st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

        with col_b:
            st.markdown("<div class='sec-title'>Revenue Share <span class='line'></span></div>", unsafe_allow_html=True)
            cat_rev = fd.groupby('Category')['Total_Amount'].sum().reset_index()
            fig2 = go.Figure(go.Pie(
                labels=cat_rev['Category'], 
                values=cat_rev['Total_Amount'], 
                hole=0.6,
                textinfo='label+percent',
                textfont=dict(color='#000000') # Forces pie labels to black
            ))
            fig2.update_layout(**chart(height=400), showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
