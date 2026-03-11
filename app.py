import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Milma Dairy Analytics",
    page_icon="🥛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #f0f4fa !important;
    color: #1a2540 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem !important; max-width: 1400px; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a2463 0%, #1b3a8a 60%, #1e4db7 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] label {
    color: rgba(255,255,255,0.6) !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stMultiSelect > div > div,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: rgba(255,255,255,0.18) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 12px;
    padding: 5px 6px;
    gap: 3px;
    border: 1px solid #e2e8f4;
    box-shadow: 0 1px 6px rgba(10,36,99,0.07);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    color: #64748b !important;
    padding: 0.5rem 1.3rem !important;
    border: none !important;
    transition: all 0.15s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0a2463, #2563eb) !important;
    color: white !important;
    box-shadow: 0 2px 10px rgba(10,36,99,0.3) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.2rem !important; }

.top-header {
    background: linear-gradient(135deg, #0a2463 0%, #1e4db7 55%, #3b82f6 100%);
    border-radius: 20px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.4rem;
    position: relative;
    overflow: hidden;
}
.top-header::before {
    content: '';
    position: absolute;
    width: 350px; height: 350px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
    top: -130px; right: -50px;
}
.top-header::after {
    content: '';
    position: absolute;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.035);
    bottom: -70px; left: 30%;
}
.header-badge {
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.22);
    color: rgba(255,255,255,0.88);
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    display: inline-block; margin-bottom: 0.7rem;
}
.header-title {
    font-size: 1.8rem; font-weight: 800;
    color: white; margin: 0 0 0.3rem;
    letter-spacing: -0.5px;
}
.header-sub { color: rgba(255,255,255,0.62); font-size: 0.82rem; }

.kpi-card {
    border-radius: 16px;
    padding: 1.3rem 1.4rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 12px rgba(10,36,99,0.07);
    transition: transform 0.15s, box-shadow 0.15s;
    position: relative; overflow: hidden;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(10,36,99,0.13); }
.kpi-icon {
    width: 40px; height: 40px; border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem; margin-bottom: 0.85rem;
}
.kpi-label {
    font-size: 0.68rem; font-weight: 700; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem;
}
.kpi-value { font-size: 1.6rem; font-weight: 800; line-height: 1.05; letter-spacing: -0.5px; }

.sec-title {
    font-size: 0.92rem; font-weight: 700; color: #0f172a;
    margin-bottom: 0.85rem;
    display: flex; align-items: center; gap: 0.4rem;
}
.sec-title .line { flex:1; height:1px; background: linear-gradient(to right,#e2e8f4,transparent); }

.insight {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border-left: 4px solid #2563eb;
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1rem;
    font-size: 0.81rem; color: #1e3a6e; line-height: 1.6;
    margin: 0.4rem 0 0.9rem;
}
.insight b { color: #1d4ed8; }

.footer {
    text-align: center; padding: 1.4rem 0 0.5rem;
    color: #94a3b8; font-size: 0.7rem;
    border-top: 1px solid #e2e8f4; margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans', color='#334155', size=11),
)

def chart(height=320, margin=None, xaxis_title=None, yaxis_title=None,
          extra_margin_r=4, **kwargs):
    """Helper that builds a layout dict without duplicate key conflicts."""
    m = margin or dict(l=4, r=extra_margin_r, t=10, b=10)
    layout = dict(
        **CHART_LAYOUT,
        height=height,
        margin=m,
        xaxis=dict(showgrid=False, tickfont=dict(size=11),
                   title=xaxis_title or ''),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(size=11),
                   title=yaxis_title or ''),
    )
    layout.update(kwargs)
    return layout

CAT_COLORS = {
    'Curd': '#2563eb', 'Cheese': '#f59e0b',
    'Paneer': '#10b981', 'Sambaram': '#8b5cf6', 'Yogurt': '#f43f5e',
}
PALETTE = ['#2563eb','#f59e0b','#10b981','#8b5cf6','#f43f5e','#06b6d4','#84cc16']

@st.cache_data
def load():
    base = os.path.dirname(os.path.abspath(__file__))
    def p(f): return os.path.join(base, f)
    daily        = pd.read_csv(p('dashboard_daily.csv'), parse_dates=['Date'])
    monthly_cat  = pd.read_csv(p('dashboard_monthly_category.csv'))
    monthly_prod = pd.read_csv(p('dashboard_monthly_product.csv'))
    menu         = pd.read_csv(p('dashboard_menu_engineering.csv'))
    annual       = pd.read_csv(p('dashboard_annual_kpis.csv'))
    seasonal     = pd.read_csv(p('dashboard_seasonal.csv'))
    forecast     = pd.read_csv(p('dashboard_forecast_2026.csv'), parse_dates=['Date'])
    monthly_cat['Date'] = pd.to_datetime(
        monthly_cat['Year'].astype(str) + '-' + monthly_cat['Month'].astype(str).str.zfill(2) + '-01'
    )
    return daily, monthly_cat, monthly_prod, menu, annual, seasonal, forecast

daily, monthly_cat, monthly_prod, menu, annual, seasonal, forecast = load()
CATEGORIES = sorted(daily['Category'].unique())
YEARS      = sorted(daily['Year'].unique())

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.6rem 0 1.2rem;text-align:center;'>
        <div style='font-size:2.2rem;margin-bottom:0.4rem;'>🥛</div>
        <div style='font-size:1.25rem;font-weight:800;color:white;letter-spacing:-0.3px;'>MILMA</div>
        <div style='font-size:0.62rem;color:rgba(255,255,255,0.45);letter-spacing:2px;margin-top:3px;'>MRCMPU · KCMMF</div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.1);margin:0 0 1.2rem;'>
    """, unsafe_allow_html=True)

    sel_cats  = st.multiselect("Categories", CATEGORIES, default=CATEGORIES)
    sel_years = st.multiselect("Years", YEARS, default=YEARS)

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.1);margin:1.2rem 0;'>
    <div style='font-size:0.67rem;color:rgba(255,255,255,0.38);line-height:1.7;text-align:center;'>
        Temporal Sales Behavior Analysis<br>of Fermented Dairy Products<br><br>
        <span style='color:rgba(255,255,255,0.6);font-weight:600;'>Vaidyan Subin Thomas</span><br>
        24203030 · M.Sc. Data Analytics<br>Rajagiri College · 2024–2026
    </div>
    """, unsafe_allow_html=True)

fd = daily[daily['Category'].isin(sel_cats) & daily['Year'].isin(sel_years)]
fm = monthly_cat[monthly_cat['Category'].isin(sel_cats) & monthly_cat['Year'].isin(sel_years)]
fa = annual[annual['Category'].isin(sel_cats) & annual['Year'].isin(sel_years)]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='top-header'>
    <div class='header-badge'>Fermented Dairy · Sales Intelligence</div>
    <div class='header-title'>Milma Sales Analytics Dashboard</div>
    <div class='header-sub'>Malabar Regional Co-operative Milk Producers Union · 2021–2025 · 5 Product Categories</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊  Overview", "📈  Trends", "🎯  Menu Engineering", "🔮  2026 Forecast"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 · OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    total_rev  = fd['Total_Amount'].sum()
    total_qty  = fd['Group_Qty_Kg'].sum()
    avg_rate   = fd['Avg_Rate'].mean()
    n_products = fd['Product'].nunique()
    n_days     = fd['Date'].nunique()

    kpis = [
        ("💰", "Total Revenue",  f"₹{total_rev/1e6:.1f}M",  "#eff6ff", "#dbeafe", "#2563eb"),
        ("⚖️", "Total Volume",   f"{total_qty/1000:.1f}T",  "#f0fdf4", "#dcfce7", "#16a34a"),
        ("📊", "Avg Rate / Kg",  f"₹{avg_rate:.2f}",        "#fffbeb", "#fef3c7", "#d97706"),
        ("🏷️", "SKUs Tracked",   str(n_products),           "#faf5ff", "#ede9fe", "#7c3aed"),
        ("📅", "Selling Days",   str(n_days),               "#fff1f2", "#ffe4e6", "#e11d48"),
    ]
    cols = st.columns(5)
    for col, (icon, label, val, bg, icon_bg, color) in zip(cols, kpis):
        with col:
            st.markdown(f"""
            <div class='kpi-card' style='background:{bg};'>
                <div class='kpi-icon' style='background:{icon_bg};'>{icon}</div>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value' style='color:{color};'>{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("<div class='sec-title'>📦 Revenue by Category <span class='line'></span></div>", unsafe_allow_html=True)
        cat_rev = fd.groupby('Category')['Total_Amount'].sum().reset_index().sort_values('Total_Amount')
        fig = go.Figure(go.Bar(
            x=cat_rev['Total_Amount']/1e6, y=cat_rev['Category'], orientation='h',
            marker=dict(color=[CAT_COLORS.get(c,'#64748b') for c in cat_rev['Category']],
                        line=dict(width=0), opacity=0.9),
            text=[f'₹{v/1e6:.1f}M' for v in cat_rev['Total_Amount']],
            textposition='outside', textfont=dict(size=12, color='#334155'),
        ))
        fig.update_layout(**chart(height=280, xaxis_title='Revenue (₹ Millions)', extra_margin_r=70))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_b:
        st.markdown("<div class='sec-title'>🥧 Revenue Share <span class='line'></span></div>", unsafe_allow_html=True)
        top_cat = cat_rev.sort_values('Total_Amount',ascending=False).iloc[0]['Category']
        fig2 = go.Figure(go.Pie(
            labels=cat_rev['Category'], values=cat_rev['Total_Amount'], hole=0.62,
            marker=dict(colors=[CAT_COLORS.get(c,'#64748b') for c in cat_rev['Category']],
                        line=dict(color='white', width=3)),
            textinfo='label+percent', textfont=dict(size=11),
            pull=[0.04 if c == top_cat else 0 for c in cat_rev['Category']],
        ))
        fig2.update_layout(**chart(height=280), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='sec-title'>🌡️ Summer Hump — Curd Monthly Revenue Heatmap <span class='line'></span></div>", unsafe_allow_html=True)
    curd_hm = monthly_cat[monthly_cat['Category']=='Curd']
    if not curd_hm.empty:
        pivot = curd_hm.pivot_table(index='Year', columns='Month', values='Total_Revenue', aggfunc='sum')
        mn = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        pivot.columns = [mn[m-1] for m in pivot.columns if m <= 12]
        fig3 = go.Figure(go.Heatmap(
            z=pivot.values/1000, x=pivot.columns.tolist(), y=pivot.index.tolist(),
            colorscale=[[0,'#eff6ff'],[0.25,'#93c5fd'],[0.6,'#2563eb'],[1,'#1e3a8a']],
            text=np.round(pivot.values/1000,0).astype(int),
            texttemplate='<b>%{text}K</b>', textfont=dict(size=10),
            colorbar=dict(title='₹K', tickfont=dict(size=10), thickness=12)
        ))
        fig3.update_layout(**chart(height=240))
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
        st.markdown("""<div class='insight'>
        🌞 <b>Summer Hump:</b> Curd revenue spikes <b>40%+ above baseline</b> in Apr–Jun.
        Katti Moru 500ml surges <b>195–340%</b> during peak months.
        Pre-position cold-chain capacity by <b>March Week 3</b>.
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sec-title'>🏆 Top 10 Products by Revenue <span class='line'></span></div>", unsafe_allow_html=True)
    top10 = fd.groupby(['Category','Product'])['Total_Amount'].sum().reset_index().nlargest(10,'Total_Amount')
    fig4 = go.Figure(go.Bar(
        x=top10['Total_Amount']/1000, y=top10['Product'], orientation='h',
        marker=dict(color=[CAT_COLORS.get(c,'#64748b') for c in top10['Category']],
                    line=dict(width=0), opacity=0.9),
        text=[f'₹{v/1000:.0f}K' for v in top10['Total_Amount']],
        textposition='outside', textfont=dict(size=11),
    ))
    fig4.update_layout(**chart(height=340, xaxis_title='Revenue (₹ Thousands)', extra_margin_r=80),
        yaxis=dict(autorange='reversed', tickfont=dict(size=11), showgrid=False))
    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 · TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    sel_cat_trend = st.selectbox("Select Category", sel_cats, key='trend_cat')
    sub = fm[fm['Category']==sel_cat_trend].sort_values('Date')
    mn  = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    st.markdown(f"<div class='sec-title'>📈 Year-over-Year Monthly Revenue — {sel_cat_trend} <span class='line'></span></div>", unsafe_allow_html=True)
    fig5 = go.Figure()
    yr_pal = ['#0a2463','#1e4db7','#3b82f6','#60a5fa','#93c5fd']
    for i, yr in enumerate(sorted(sub['Year'].unique())):
        yd = sub[sub['Year']==yr].sort_values('Month')
        fig5.add_trace(go.Scatter(
            x=[mn[m-1] for m in yd['Month']], y=yd['Total_Revenue']/1000,
            name=str(yr), mode='lines+markers',
            line=dict(color=yr_pal[i%len(yr_pal)], width=2.5),
            marker=dict(size=7, line=dict(color='white', width=1.5))
        ))
    fig5.add_vrect(x0='Mar', x1='Jun', fillcolor='#fef3c7', opacity=0.5,
                   layer='below', line_width=0,
                   annotation_text='☀️ Peak Season', annotation_position='top left',
                   annotation_font=dict(size=11, color='#92400e'))
    fig5.update_layout(**chart(height=380, xaxis_title='Month', yaxis_title='Revenue (₹ Thousands)'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
        hovermode='x unified')
    st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='sec-title'>📊 Annual Revenue by Category <span class='line'></span></div>", unsafe_allow_html=True)
        ann = fa.groupby(['Year','Category'])['Total_Revenue'].sum().reset_index()
        fig6 = px.bar(ann, x='Year', y='Total_Revenue', color='Category',
                      color_discrete_map=CAT_COLORS, barmode='stack', template='none',
                      labels={'Total_Revenue':'Revenue (₹)'})
        fig6.update_traces(marker_line_width=0)
        fig6.update_layout(**chart(height=320, yaxis_title='Revenue (₹)'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                        bgcolor='rgba(0,0,0,0)', font=dict(size=10), title=''))
        st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("<div class='sec-title'>🌊 Average Seasonal Pattern <span class='line'></span></div>", unsafe_allow_html=True)
        sea = monthly_cat[monthly_cat['Category'].isin(sel_cats)].groupby(
            ['Category','Month'])['Total_Revenue'].mean().reset_index()
        sea['Month_Name'] = sea['Month'].apply(lambda m: mn[m-1])
        fig7 = px.line(sea, x='Month_Name', y='Total_Revenue', color='Category',
                       color_discrete_map=CAT_COLORS, markers=True, template='none',
                       labels={'Total_Revenue':'Avg Revenue (₹)','Month_Name':''})
        fig7.add_vrect(x0='Mar', x1='Jun', fillcolor='#fef3c7', opacity=0.5,
                       layer='below', line_width=0)
        fig7.update_traces(line_width=2.5, marker=dict(size=6, line=dict(color='white',width=1.5)))
        fig7.update_layout(**chart(height=320, yaxis_title='Avg Revenue (₹)'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                        bgcolor='rgba(0,0,0,0)', font=dict(size=10), title=''),
            hovermode='x unified')
        st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='sec-title'>🔍 Product-Level Monthly Trend <span class='line'></span></div>", unsafe_allow_html=True)
    prods_in_cat = daily[daily['Category']==sel_cat_trend]['Product'].unique().tolist()
    sel_prods = st.multiselect("Select Products", prods_in_cat, default=prods_in_cat[:3], key='pd')
    if sel_prods:
        pts = daily[daily['Product'].isin(sel_prods)].groupby(
            ['Product', pd.Grouper(key='Date', freq='ME')])['Total_Amount'].sum().reset_index()
        fig8 = px.line(pts, x='Date', y='Total_Amount', color='Product',
                       template='none', labels={'Total_Amount':'Revenue (₹)','Date':''})
        fig8.update_traces(line_width=2.5)
        fig8.update_layout(**chart(height=320, yaxis_title='Revenue (₹)'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                        bgcolor='rgba(0,0,0,0)', font=dict(size=10), title=''),
            hovermode='x unified')
        st.plotly_chart(fig8, use_container_width=True, config={'displayModeBar': False})

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 · MENU ENGINEERING
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    QUAD_COLORS = {
        'Star ⭐':               '#2563eb',
        'Push Item 🔄':         '#10b981',
        'Premium Puzzle 💎':    '#f59e0b',
        'Efficiency Target 📉': '#f43f5e',
    }
    menu_f = menu[menu['Category'].isin(sel_cats)]

    st.markdown("<div class='sec-title'>🎯 Product Portfolio Quadrant <span class='line'></span></div>", unsafe_allow_html=True)
    fig9 = px.scatter(
        menu_f, x='Total_Qty_Kg', y='Total_Revenue',
        color='Quadrant', size='Total_Revenue', size_max=52,
        hover_name='Product',
        hover_data={'Category':True,'Avg_Rate':':.2f','Total_Qty_Kg':':,.0f','Quadrant':False},
        color_discrete_map=QUAD_COLORS, template='none',
        labels={'Total_Qty_Kg':'Volume (Kg)','Total_Revenue':'Revenue (₹)'}
    )
    fig9.update_traces(marker=dict(line=dict(color='white',width=2), opacity=0.85))
    fig9.update_layout(**chart(height=440, xaxis_title='Volume (Kg)', yaxis_title='Revenue (₹)'),
        legend=dict(title='', orientation='h', yanchor='bottom', y=1.02,
                    xanchor='right', x=1, bgcolor='rgba(0,0,0,0)', font=dict(size=11)))
    st.plotly_chart(fig9, use_container_width=True, config={'displayModeBar': False})

    STRATEGIES = {
        'Star ⭐':               ('Maximize Availability',  '✅ Priority cold-storage & retail placement. These are revenue anchors — never run out of stock.'),
        'Push Item 🔄':         ('Boost Margin',           '🔼 High volume but low unit value. Bundle with premium SKUs or introduce slight price increments.'),
        'Premium Puzzle 💎':    ('Improve Visibility',     '💡 High value, low reach. Targeted urban promotions and gifting channel activations.'),
        'Efficiency Target 📉': ('Review Viability',       '⚠️ Low volume and value. Consider institutional-only supply, or phased discontinuation.'),
    }
    cols2 = st.columns(2)
    for i, (quad, (action, detail)) in enumerate(STRATEGIES.items()):
        pq = menu_f[menu_f['Quadrant']==quad]
        with cols2[i%2]:
            with st.expander(f"{quad}  ·  {action}  ({len(pq)} products)", expanded=i<2):
                st.markdown(f"<div class='insight'>{detail}</div>", unsafe_allow_html=True)
                if len(pq):
                    disp = pq[['Category','Product','Total_Revenue','Total_Qty_Kg','Avg_Rate']].copy()
                    disp.columns = ['Category','Product','Revenue (₹)','Volume (Kg)','Rate (₹/Kg)']
                    disp['Revenue (₹)']  = disp['Revenue (₹)'].apply(lambda x: f'₹{x:,.0f}')
                    disp['Volume (Kg)']  = disp['Volume (Kg)'].apply(lambda x: f'{x:,.1f}')
                    disp['Rate (₹/Kg)']  = disp['Rate (₹/Kg)'].apply(lambda x: f'₹{x:.2f}')
                    st.dataframe(disp.reset_index(drop=True), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 · FORECAST
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""<div class='insight'>
    🤖 <b>Temporal Fusion Transformer (TFT)</b> trained on weekly sales (2021–2025).
    Forecast covers <b>52 weeks of 2026</b> across <b>12 SKUs</b> —
    incorporating seasonality, summer hump patterns, and product-level momentum.
    </div>""", unsafe_allow_html=True)

    sel_fc = st.multiselect("Products to display", forecast['Product'].unique().tolist(),
                             default=forecast['Product'].unique().tolist()[:5], key='fc')
    fc_f = forecast[forecast['Product'].isin(sel_fc)]

    st.markdown("<div class='sec-title'>🔮 2026 Weekly Revenue Forecast <span class='line'></span></div>", unsafe_allow_html=True)
    fig10 = go.Figure()
    for i, prod in enumerate(sel_fc):
        pd_ = fc_f[fc_f['Product']==prod].sort_values('Date')
        fig10.add_trace(go.Scatter(
            x=pd_['Date'], y=pd_['Forecast_Revenue']/1000,
            name=prod, mode='lines',
            line=dict(color=PALETTE[i%len(PALETTE)], width=2.5)
        ))
    fig10.add_vrect(x0='2026-04-01', x1='2026-06-30',
                    fillcolor='#fef3c7', opacity=0.6, layer='below', line_width=0,
                    annotation_text='☀️ Summer Peak', annotation_position='top left',
                    annotation_font=dict(size=11, color='#92400e'))
    fig10.update_layout(**chart(height=400, yaxis_title='Forecast Revenue (₹ Thousands)', extra_margin_r=150),
        legend=dict(orientation='v', x=1.01, y=1, bgcolor='rgba(0,0,0,0)', font=dict(size=10)),
        hovermode='x unified')
    st.plotly_chart(fig10, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='sec-title'>📅 Monthly Forecast Rollup <span class='line'></span></div>", unsafe_allow_html=True)
    fc_m = fc_f.copy()
    fc_m['Month']      = fc_m['Date'].dt.month
    fc_m['Month_Name'] = fc_m['Date'].dt.strftime('%b')
    rollup = fc_m.groupby(['Month','Month_Name'])['Forecast_Revenue'].sum().reset_index().sort_values('Month')
    fig11 = go.Figure(go.Bar(
        x=rollup['Month_Name'], y=rollup['Forecast_Revenue']/1000,
        marker=dict(color=['#ef4444' if m in [4,5,6] else '#2563eb' for m in rollup['Month']],
                    line=dict(width=0), opacity=0.9),
        text=[f'₹{v/1000:.0f}K' for v in rollup['Forecast_Revenue']],
        textposition='outside', textfont=dict(size=11),
    ))
    fig11.update_layout(**chart(height=320, yaxis_title='Forecast Revenue (₹K)',
                                margin=dict(l=4,r=4,t=26,b=10)),
        annotations=[dict(x=0.5, y=1.07, xref='paper', yref='paper', showarrow=False,
                          text='🔴 Red bars = Summer Peak (Apr–Jun)',
                          font=dict(size=10, color='#94a3b8'))])
    st.plotly_chart(fig11, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div class='sec-title'>📦 2026 Dynamic Logistics Playbook <span class='line'></span></div>", unsafe_allow_html=True)
    pb = pd.DataFrame({
        'Timing':       ['Jan W3','Feb W1','Mar W1','Mar W3','Apr W1','May W1',
                         'Jun W1','Jul W1','Sep W1','Oct W1','Nov W1','Dec W3'],
        'Action':       ['Baseline stock review','Begin pre-season Curd ramp-up',
                         '+20% cold-storage for Curd','Activate secondary routes',
                         '🔴 PEAK — Max cold-chain allocation','Summer surge daily monitoring',
                         'Maintain peak; plan wind-down','Post-peak stabilization',
                         'Onam prep: +15% Sambaram','Q4 baseline restock',
                         'Push — Premium SKU promotions','Annual review & model retrain'],
        'Key Products': ['Cheese Slice 100g, Paneer 200g','Skimmed Milk Curd 525g, DTM Curd',
                         'Curd 525g, Katti Moru 500ml','Katti Moru 1L, Special Curd 500g',
                         'All Curd variants, Sambaram 180ml','Katti Moru 500ml (340%+ surge)',
                         'All Curd; begin Cheese push','Cheese Slice, Paneer, Premium Curd',
                         'Sambaram 180ml, Nellikka 250ml','Cheese Slice 100g, Paneer 200g',
                         'Probiotic Set Curd 1kg, Cheese Spread','All categories']
    })
    st.dataframe(pb, use_container_width=True, hide_index=True)
    st.markdown("""<div class='insight'>
    ⏱️ <b>14-day advance notice</b> built into every action — letting procurement,
    cold-chain, and distribution teams pre-position before each demand event.
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
    Milma Fermented Dairy Sales Analytics · Vaidyan Subin Thomas (24203030) ·
    M.Sc. Computer Science (Data Analytics) · Rajagiri College of Social Sciences · 2024–2026
</div>
""", unsafe_allow_html=True)
