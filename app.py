import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Milma Fermented Dairy — Sales Analytics",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #003580 0%, #0057b8 60%, #1a78d4 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}
.main-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.main-header h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.9rem;
    color: white;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.main-header p {
    color: rgba(255,255,255,0.75);
    font-size: 0.85rem;
    margin: 0;
    font-weight: 300;
}
.milma-badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    display: inline-block;
    margin-bottom: 0.6rem;
}

/* KPI Cards */
.kpi-card {
    background: white;
    border: 1px solid #e8edf5;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,53,128,0.06);
    transition: box-shadow 0.2s;
}
.kpi-card:hover { box-shadow: 0 4px 16px rgba(0,53,128,0.12); }
.kpi-card .accent-bar {
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 12px 0 0 12px;
}
.kpi-card .label {
    font-size: 0.72rem;
    font-weight: 500;
    color: #8a95a3;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.4rem;
}
.kpi-card .value {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #0d1b2a;
    line-height: 1.1;
}
.kpi-card .delta {
    font-size: 0.78rem;
    margin-top: 0.3rem;
    font-weight: 500;
}
.delta-up   { color: #16a34a; }
.delta-down { color: #dc2626; }

/* Section headers */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #0d1b2a;
    margin: 0.5rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, #e2e8f0, transparent);
    margin-left: 0.5rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #f8fafd;
    border-right: 1px solid #e2e8f0;
}
[data-testid="stSidebar"] .sidebar-logo {
    text-align: center;
    padding: 1rem 0;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #f1f5f9;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

/* Insight box */
.insight-box {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border: 1px solid #bfdbfe;
    border-left: 4px solid #2563eb;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin: 0.8rem 0;
    font-size: 0.84rem;
    color: #1e3a5f;
    line-height: 1.5;
}
.insight-box strong { color: #1d4ed8; }

/* Footer */
.footer {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
    color: #94a3b8;
    font-size: 0.75rem;
    border-top: 1px solid #f1f5f9;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ── Data Loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    def p(f): return os.path.join(base, f)
    daily    = pd.read_csv(p('dashboard_daily.csv'), parse_dates=['Date'])
    monthly_cat  = pd.read_csv(p('dashboard_monthly_category.csv'))
    monthly_prod = pd.read_csv(p('dashboard_monthly_product.csv'))
    menu     = pd.read_csv(p('dashboard_menu_engineering.csv'))
    annual   = pd.read_csv(p('dashboard_annual_kpis.csv'))
    seasonal = pd.read_csv(p('dashboard_seasonal.csv'))
    forecast = pd.read_csv(p('dashboard_forecast_2026.csv'), parse_dates=['Date'])
    monthly_cat['Date'] = pd.to_datetime(
        monthly_cat['Year'].astype(str) + '-' + monthly_cat['Month'].astype(str).str.zfill(2) + '-01'
    )
    return daily, monthly_cat, monthly_prod, menu, annual, seasonal, forecast

daily, monthly_cat, monthly_prod, menu, annual, seasonal, forecast = load_data()

CATEGORIES = sorted(daily['Category'].unique().tolist())
YEARS = sorted(daily['Year'].unique().tolist())
CAT_COLORS = {
    'Curd':     '#0057b8',
    'Cheese':   '#f59e0b',
    'Paneer':   '#10b981',
    'Sambaram': '#8b5cf6',
    'Yogurt':   '#ef4444',
}

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1rem 0 1.5rem'>
        <div style='font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800;
                    color:#003580; letter-spacing:-0.5px;'>🥛 MILMA</div>
        <div style='font-size:0.7rem; color:#64748b; margin-top:2px; letter-spacing:1px;'>
            MRCMPU · KCMMF
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🔍 Filters**")
    sel_cats = st.multiselect(
        "Categories", CATEGORIES,
        default=CATEGORIES,
        help="Select one or more product categories"
    )
    sel_years = st.multiselect(
        "Years", YEARS,
        default=YEARS,
        help="Select years to include"
    )

    st.markdown("---")
    st.markdown("**📄 About**")
    st.caption(
        "Temporal Sales Behavior Analysis of Fermented Dairy Products · "
        "M.Sc. Data Analytics · Rajagiri College · 2024–2026"
    )
    st.caption("Vaidyan Subin Thomas · 24203030")

# ── Filtered data ──────────────────────────────────────────────────────────────
fd = daily[daily['Category'].isin(sel_cats) & daily['Year'].isin(sel_years)]
fm = monthly_cat[monthly_cat['Category'].isin(sel_cats) & monthly_cat['Year'].isin(sel_years)]
fa = annual[annual['Category'].isin(sel_cats) & annual['Year'].isin(sel_years)]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='main-header'>
    <span class='milma-badge'>MALABAR MILMA · KCMMF</span>
    <h1>🥛 Fermented Dairy Sales Analytics</h1>
    <p>Temporal Sales Behavior Analysis · 2021–2025 · Curd · Cheese · Paneer · Sambaram · Yogurt</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", "📈 Trends", "🎯 Menu Engineering", "🔮 2026 Forecast"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:

    # ── KPI Cards ──────────────────────────────────────────────────────────────
    total_rev  = fd['Total_Amount'].sum()
    total_qty  = fd['Group_Qty_Kg'].sum()
    avg_rate   = fd['Avg_Rate'].mean()
    n_products = fd['Product'].nunique()
    n_days     = fd['Date'].nunique()

    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        (c1, "Total Revenue", f"₹{total_rev/1e6:.2f}M", "#0057b8", ""),
        (c2, "Total Volume",  f"{total_qty/1000:.1f}T", "#10b981", ""),
        (c3, "Avg Rate/Kg",   f"₹{avg_rate:.2f}",       "#f59e0b", ""),
        (c4, "SKUs Tracked",  str(n_products),           "#8b5cf6", ""),
        (c5, "Selling Days",  str(n_days),               "#ef4444", ""),
    ]
    for col, label, val, color, delta in kpis:
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='accent-bar' style='background:{color}'></div>
                <div class='label'>{label}</div>
                <div class='value'>{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Revenue by Category ────────────────────────────────────────────────────
    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        st.markdown("<div class='section-title'>📦 Revenue by Category</div>", unsafe_allow_html=True)
        cat_rev = fd.groupby('Category')['Total_Amount'].sum().reset_index().sort_values('Total_Amount')
        fig = go.Figure(go.Bar(
            x=cat_rev['Total_Amount'] / 1e6,
            y=cat_rev['Category'],
            orientation='h',
            marker_color=[CAT_COLORS.get(c, '#64748b') for c in cat_rev['Category']],
            text=[f'₹{v/1e6:.2f}M' for v in cat_rev['Total_Amount']],
            textposition='outside',
        ))
        fig.update_layout(
            height=300, margin=dict(l=0, r=60, t=10, b=30),
            xaxis_title='Revenue (₹ Millions)',
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
            font=dict(family='DM Sans')
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>🥧 Revenue Share</div>", unsafe_allow_html=True)
        fig2 = go.Figure(go.Pie(
            labels=cat_rev['Category'],
            values=cat_rev['Total_Amount'],
            hole=0.55,
            marker_colors=[CAT_COLORS.get(c, '#64748b') for c in cat_rev['Category']],
            textinfo='label+percent',
            textfont_size=11,
        ))
        fig2.update_layout(
            height=300, margin=dict(l=0, r=0, t=10, b=10),
            showlegend=False,
            paper_bgcolor='white',
            font=dict(family='DM Sans')
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Summer Hump Heatmap ────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🌡️ Summer Hump — Curd Monthly Revenue Heatmap</div>",
                unsafe_allow_html=True)

    curd_hm = monthly_cat[monthly_cat['Category'] == 'Curd'].copy()
    if not curd_hm.empty:
        pivot = curd_hm.pivot_table(index='Year', columns='Month', values='Total_Revenue', aggfunc='sum')
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        pivot.columns = [month_names[m-1] for m in pivot.columns if m <= 12]

        fig3 = go.Figure(go.Heatmap(
            z=pivot.values / 1000,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale='YlOrRd',
            text=np.round(pivot.values / 1000, 0).astype(int),
            texttemplate='%{text}K',
            textfont_size=10,
            colorbar=dict(title='₹K', tickfont=dict(size=10))
        ))
        fig3.update_layout(
            height=260, margin=dict(l=0, r=0, t=10, b=30),
            xaxis_title='Month', yaxis_title='Year',
            plot_bgcolor='white', paper_bgcolor='white',
            font=dict(family='DM Sans')
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""
        <div class='insight-box'>
        🌞 <strong>Summer Hump Effect:</strong> Curd revenue surges <strong>40%+ above baseline</strong>
        during April–June. Katti Moru 500ml shows 195–340% surge during peak months.
        Cold-chain capacity must be pre-positioned by <strong>March Week 3</strong>.
        </div>
        """, unsafe_allow_html=True)

    # ── Top Products ───────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🏆 Top 10 Products by Revenue</div>", unsafe_allow_html=True)
    top10 = fd.groupby(['Category','Product'])['Total_Amount'].sum().reset_index()
    top10 = top10.sort_values('Total_Amount', ascending=False).head(10)

    fig4 = go.Figure(go.Bar(
        x=top10['Total_Amount'] / 1000,
        y=top10['Product'],
        orientation='h',
        marker_color=[CAT_COLORS.get(c, '#64748b') for c in top10['Category']],
        text=[f'₹{v/1000:.0f}K' for v in top10['Total_Amount']],
        textposition='outside',
    ))
    fig4.update_layout(
        height=360, margin=dict(l=0, r=80, t=10, b=30),
        xaxis_title='Revenue (₹ Thousands)',
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        yaxis=dict(autorange='reversed'),
        font=dict(family='DM Sans')
    )
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:

    st.markdown("<div class='section-title'>📈 Year-over-Year Monthly Revenue</div>",
                unsafe_allow_html=True)

    sel_cat_trend = st.selectbox("Select Category", sel_cats, key='trend_cat')
    sub = fm[fm['Category'] == sel_cat_trend].sort_values('Date')

    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    fig5 = go.Figure()
    year_colors = ['#003580','#0057b8','#3b82f6','#93c5fd','#bfdbfe']
    years_in_sub = sorted(sub['Year'].unique())

    for i, yr in enumerate(years_in_sub):
        yr_data = sub[sub['Year'] == yr].sort_values('Month')
        fig5.add_trace(go.Scatter(
            x=[month_names[m-1] for m in yr_data['Month']],
            y=yr_data['Total_Revenue'] / 1000,
            name=str(yr),
            mode='lines+markers',
            line=dict(color=year_colors[i % len(year_colors)], width=2.5),
            marker=dict(size=7)
        ))

    fig5.add_vrect(x0='Mar', x1='Jun', fillcolor='orange', opacity=0.08,
                   annotation_text='Summer Peak', annotation_position='top left')
    fig5.update_layout(
        height=380, margin=dict(l=0, r=0, t=20, b=30),
        xaxis_title='Month', yaxis_title='Revenue (₹ Thousands)',
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        legend_title='Year',
        font=dict(family='DM Sans'),
        hovermode='x unified'
    )
    st.plotly_chart(fig5, use_container_width=True)

    # ── Annual Growth ──────────────────────────────────────────────────────────
    col_x, col_y = st.columns(2)

    with col_x:
        st.markdown("<div class='section-title'>📊 Annual Revenue Growth</div>",
                    unsafe_allow_html=True)
        ann = fa.groupby('Year')['Total_Revenue'].sum().reset_index()
        ann['YoY_Pct'] = ann['Total_Revenue'].pct_change() * 100
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(
            x=ann['Year'], y=ann['Total_Revenue']/1e6,
            marker_color='#0057b8', name='Revenue',
            text=[f'₹{v/1e6:.2f}M' for v in ann['Total_Revenue']],
            textposition='outside'
        ))
        fig6.update_layout(
            height=300, margin=dict(l=0, r=0, t=20, b=30),
            yaxis_title='₹ Millions', plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
            font=dict(family='DM Sans'), showlegend=False
        )
        st.plotly_chart(fig6, use_container_width=True)

    with col_y:
        st.markdown("<div class='section-title'>📦 Volume vs Revenue (Scatter)</div>",
                    unsafe_allow_html=True)
        cat_scatter = fd.groupby('Category').agg(
            Revenue=('Total_Amount','sum'), Volume=('Group_Qty_Kg','sum')
        ).reset_index()
        fig7 = px.scatter(
            cat_scatter, x='Volume', y='Revenue',
            text='Category', size='Revenue', size_max=50,
            color='Category',
            color_discrete_map=CAT_COLORS,
            template='plotly_white'
        )
        fig7.update_traces(textposition='top center', textfont_size=11)
        fig7.update_layout(
            height=300, margin=dict(l=0, r=0, t=20, b=30),
            showlegend=False, font=dict(family='DM Sans'),
            xaxis_title='Volume (Kg)', yaxis_title='Revenue (₹)'
        )
        st.plotly_chart(fig7, use_container_width=True)

    # ── Seasonal Pattern ───────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🌊 Seasonal Revenue Pattern by Category</div>",
                unsafe_allow_html=True)

    seasonal_avg = monthly_cat[monthly_cat['Category'].isin(sel_cats)].groupby(
        ['Category','Month'])['Total_Revenue'].mean().reset_index()
    seasonal_avg['Month_Name'] = seasonal_avg['Month'].apply(lambda m: month_names[m-1])

    fig8 = px.line(
        seasonal_avg, x='Month_Name', y='Total_Revenue',
        color='Category', color_discrete_map=CAT_COLORS,
        markers=True, template='plotly_white',
        labels={'Total_Revenue': 'Avg Monthly Revenue (₹)', 'Month_Name': 'Month'}
    )
    fig8.add_vrect(x0='Mar', x1='Jun', fillcolor='orange', opacity=0.07,
                   annotation_text='Peak Season', annotation_position='top left')
    fig8.update_layout(
        height=340, margin=dict(l=0, r=0, t=20, b=30),
        font=dict(family='DM Sans'), hovermode='x unified',
        legend_title='Category'
    )
    st.plotly_chart(fig8, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MENU ENGINEERING
# ══════════════════════════════════════════════════════════════════════════════
with tab3:

    st.markdown("<div class='section-title'>🎯 Menu Engineering — Product Portfolio Quadrant</div>",
                unsafe_allow_html=True)

    menu_filtered = menu[menu['Category'].isin(sel_cats)]

    quad_colors = {
        'Star ⭐':              '#16a34a',
        'Push Item 🔄':        '#2563eb',
        'Premium Puzzle 💎':   '#d97706',
        'Efficiency Target 📉':'#dc2626',
    }

    fig9 = px.scatter(
        menu_filtered,
        x='Total_Qty_Kg', y='Total_Revenue',
        color='Quadrant',
        size='Total_Revenue',
        size_max=55,
        hover_name='Product',
        hover_data={'Category': True, 'Avg_Rate': ':.2f', 'Quadrant': False},
        facet_col='Category',
        facet_col_wrap=3,
        color_discrete_map=quad_colors,
        template='plotly_white',
        labels={'Total_Qty_Kg': 'Volume (Kg)', 'Total_Revenue': 'Revenue (₹)'}
    )
    fig9.update_layout(
        height=520, margin=dict(l=0, r=0, t=40, b=10),
        legend_title='Quadrant',
        font=dict(family='DM Sans')
    )
    st.plotly_chart(fig9, use_container_width=True)

    # ── Classification Table ───────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📋 Product Classifications & Strategy</div>",
                unsafe_allow_html=True)

    strategy = {
        'Star ⭐':              '✅ Maximize availability. Priority cold-storage & retail placement.',
        'Push Item 🔄':        '🔼 Bundle with premium SKUs. Slight price increase opportunity.',
        'Premium Puzzle 💎':   '💡 Boost visibility. Targeted promotions in urban channels.',
        'Efficiency Target 📉':'⚠️ Review viability. Consider institutional-only supply or phase-out.',
    }

    for quad, strat in strategy.items():
        prods = menu_filtered[menu_filtered['Quadrant'] == quad]
        if len(prods) == 0:
            continue
        color = quad_colors.get(quad, '#64748b')
        with st.expander(f"{quad} — {len(prods)} products", expanded=(quad == 'Star ⭐')):
            st.markdown(f"<div class='insight-box'>{strat}</div>", unsafe_allow_html=True)
            display = prods[['Category','Product','Total_Revenue','Total_Qty_Kg','Avg_Rate']].copy()
            display.columns = ['Category','Product','Revenue (₹)','Volume (Kg)','Avg Rate (₹/Kg)']
            display['Revenue (₹)'] = display['Revenue (₹)'].apply(lambda x: f'₹{x:,.0f}')
            display['Volume (Kg)'] = display['Volume (Kg)'].apply(lambda x: f'{x:,.1f}')
            display['Avg Rate (₹/Kg)'] = display['Avg Rate (₹/Kg)'].apply(lambda x: f'₹{x:.2f}')
            st.dataframe(display.reset_index(drop=True), use_container_width=True, hide_index=True)

    # ── Revenue Distribution ───────────────────────────────────────────────────
    st.markdown("<div class='section-title'>💰 Revenue by Quadrant</div>", unsafe_allow_html=True)
    quad_rev = menu_filtered.groupby('Quadrant')['Total_Revenue'].sum().reset_index()
    fig10 = go.Figure(go.Pie(
        labels=quad_rev['Quadrant'],
        values=quad_rev['Total_Revenue'],
        hole=0.5,
        marker_colors=[quad_colors.get(q, '#64748b') for q in quad_rev['Quadrant']],
        textinfo='label+percent',
    ))
    fig10.update_layout(
        height=300, margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor='white', font=dict(family='DM Sans'), showlegend=False
    )
    st.plotly_chart(fig10, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — 2026 FORECAST
# ══════════════════════════════════════════════════════════════════════════════
with tab4:

    st.markdown("""
    <div class='insight-box'>
    🤖 <strong>TFT Model:</strong> Temporal Fusion Transformer trained on weekly sales data (2021–2025).
    Forecasts incorporate <strong>seasonality</strong>, <strong>summer hump pattern</strong>,
    and <strong>product-level trends</strong> for all 12 tracked SKUs.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>🔮 2026 Weekly Revenue Forecast</div>",
                unsafe_allow_html=True)

    sel_products = st.multiselect(
        "Select Products to Display",
        forecast['Product'].unique().tolist(),
        default=forecast['Product'].unique().tolist()[:4],
        key='forecast_prods'
    )

    forecast_filtered = forecast[forecast['Product'].isin(sel_products)]

    fig11 = go.Figure()
    prod_colors = px.colors.qualitative.Set1
    for i, prod in enumerate(sel_products):
        pdata = forecast_filtered[forecast_filtered['Product'] == prod].sort_values('Date')
        fig11.add_trace(go.Scatter(
            x=pdata['Date'],
            y=pdata['Forecast_Revenue'] / 1000,
            name=prod,
            mode='lines+markers',
            line=dict(color=prod_colors[i % len(prod_colors)], width=2),
            marker=dict(size=5)
        ))

    # Summer peak shading
    fig11.add_vrect(
        x0='2026-04-01', x1='2026-06-30',
        fillcolor='orange', opacity=0.1,
        annotation_text='☀️ Summer Peak', annotation_position='top left',
        annotation_font_size=11
    )
    fig11.update_layout(
        height=420, margin=dict(l=0, r=0, t=20, b=30),
        xaxis_title='Week', yaxis_title='Forecast Revenue (₹ Thousands)',
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        legend=dict(orientation='v', x=1.01, y=1),
        font=dict(family='DM Sans'), hovermode='x unified'
    )
    st.plotly_chart(fig11, use_container_width=True)

    # ── Monthly Forecast Rollup ────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📅 Monthly Forecast Summary — 2026</div>",
                unsafe_allow_html=True)

    fc_monthly = forecast_filtered.copy()
    fc_monthly['Month'] = fc_monthly['Date'].dt.month
    fc_monthly['Month_Name'] = fc_monthly['Date'].dt.strftime('%b')
    fc_rollup = fc_monthly.groupby(['Month','Month_Name'])['Forecast_Revenue'].sum().reset_index()
    fc_rollup = fc_rollup.sort_values('Month')

    bar_colors = ['#ef4444' if m in [4,5,6] else '#0057b8' for m in fc_rollup['Month']]
    fig12 = go.Figure(go.Bar(
        x=fc_rollup['Month_Name'],
        y=fc_rollup['Forecast_Revenue'] / 1000,
        marker_color=bar_colors,
        text=[f'₹{v/1000:.0f}K' for v in fc_rollup['Forecast_Revenue']],
        textposition='outside'
    ))
    fig12.update_layout(
        height=320, margin=dict(l=0, r=0, t=20, b=30),
        yaxis_title='Forecast Revenue (₹ Thousands)',
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        font=dict(family='DM Sans'),
        annotations=[dict(
            x=0.5, y=1.05, xref='paper', yref='paper',
            text='🔴 Red = Summer Peak (Apr–Jun)', showarrow=False, font=dict(size=11, color='#94a3b8')
        )]
    )
    st.plotly_chart(fig12, use_container_width=True)

    # ── Logistics Playbook ─────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📦 2026 Dynamic Logistics Playbook</div>",
                unsafe_allow_html=True)

    playbook_data = {
        'Timing':       ['Jan W3','Feb W1','Mar W1','Mar W3','Apr W1','May W1',
                         'Jun W1','Jul W1','Sep W1','Oct W1','Nov W1','Dec W3'],
        'Action':       ['Baseline stock review','Begin pre-season Curd ramp-up',
                         '+20% cold-storage for Curd','Activate secondary routes',
                         '🔴 PEAK ALERT — Max cold-chain','Summer surge monitoring',
                         'Maintain peak; plan wind-down','Post-peak stabilization',
                         'Onam prep: +15% Sambaram','Q4 baseline restock',
                         'Promotional push — Premium SKUs','Annual data compilation'],
        'Key Products': ['Cheese Slice 100g, Paneer 200g',
                         'Skimmed Milk Curd 525g, DTM Curd 500g',
                         'Curd 525g, Katti Moru 500ml',
                         'Katti Moru 1L, Special Curd 500g',
                         'All Curd variants, Sambaram 180ml',
                         'Katti Moru 500ml (340%+ surge)',
                         'All Curd; begin Cheese push',
                         'Cheese Slice, Paneer, Premium Curd',
                         'Sambaram 180ml, Nellikka 250ml',
                         'Cheese Slice 100g, Paneer 200g',
                         'Probiotic Set Curd 1kg, Cheese Spread',
                         'All categories']
    }
    pb_df = pd.DataFrame(playbook_data)
    st.dataframe(pb_df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class='insight-box'>
    ⏱️ <strong>14-day advance notice</strong> is built into every playbook action —
    allowing procurement, cold-chain, and distribution teams to pre-position before each demand event.
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    Milma Fermented Dairy Sales Analytics · Vaidyan Subin Thomas (24203030) ·
    M.Sc. Computer Science (Data Analytics) · Rajagiri College of Social Sciences · 2024–2026
</div>
""", unsafe_allow_html=True)
