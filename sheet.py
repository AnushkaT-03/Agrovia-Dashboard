import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import time

# ─── Page config ───────────────────────────────────────
st.set_page_config(
    page_title="Vegetable Consumer Insights",
    page_icon="🥬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Clean & Interactive CSS ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Smooth animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}

.animated { animation: fadeIn 0.6s ease-out; }
.slide-in { animation: slideIn 0.5s ease-out; }

/* Clean background */
.stApp {
    background: linear-gradient(135deg, #f8fdf9 0%, #ffffff 100%);
}

/* KPI Cards - Clean & Modern */
.kpi-card {
    background: white;
    border-radius: 20px;
    padding: 2rem 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 2px solid transparent;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #4caf50, #81c784);
    transform: scaleX(0);
    transition: transform 0.4s ease;
}

.kpi-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 40px rgba(76, 175, 80, 0.2);
    border-color: #4caf50;
}

.kpi-card:hover::after {
    transform: scaleX(1);
}

/* Section headers - Clean style */
.section-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #2e7d32;
    margin: 3rem 0 1.5rem 0;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.section-title::before {
    content: '';
    width: 6px;
    height: 40px;
    background: linear-gradient(180deg, #4caf50, #2e7d32);
    border-radius: 10px;
}

/* Chart containers - Clean white cards */
.chart-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
    transition: all 0.3s ease;
    border: 1px solid rgba(0, 0, 0, 0.03);
    margin-bottom: 2rem;
}

.chart-card:hover {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    transform: translateY(-4px);
}

/* Sidebar styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f1f8f4 0%, #ffffff 100%);
}

.sidebar-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #2e7d32;
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 3px solid #4caf50;
}

/* Improved multiselect */
.stMultiSelect [data-baseweb="select"] {
    border-radius: 12px;
    border: 2px solid #e0e0e0;
    transition: all 0.3s ease;
}

.stMultiSelect [data-baseweb="select"]:hover {
    border-color: #4caf50;
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
}

/* Button styling */
.stButton>button {
    border-radius: 14px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2) !important;
    background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%) !important;
    border: none !important;
}

.stButton>button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3) !important;
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #1b5e20 0%, #4caf50 50%, #81c784 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}

.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #666;
    font-weight: 500;
    margin-bottom: 3rem;
}

/* Metric text styling */
.metric-value {
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1;
    margin: 1rem 0;
}

.metric-label {
    font-size: 1rem;
    font-weight: 600;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-sublabel {
    font-size: 0.85rem;
    color: #999;
    margin-top: 0.5rem;
}

/* Badge styling */
.info-badge {
    display: inline-block;
    padding: 0.6rem 1.2rem;
    background: white;
    border: 2px solid #4caf50;
    border-radius: 30px;
    font-size: 0.9rem;
    font-weight: 600;
    color: #2e7d32;
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
}

/* Divider */
.clean-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
    margin: 3rem 0;
    border: none;
}

/* Sidebar stat card */
.sidebar-stat {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 16px rgba(76, 175, 80, 0.15);
    border: 2px solid #4caf50;
    margin-top: 2rem;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

::-webkit-scrollbar-track {
    background: #f5f5f5;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #4caf50, #2e7d32);
    border-radius: 10px;
    border: 2px solid #f5f5f5;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #66bb6a, #1b5e20);
}

/* Remove default streamlit padding */
.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Plotly charts clean background */
.js-plotly-plot {
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────
st.markdown('<h1 class="main-title animated">🥬 Vegetable Consumer Survey</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle animated">Comprehensive insights into buying habits, price sensitivity, and trust factors</p>', unsafe_allow_html=True)

# ─── Load data ─────────────────────────────────────────
@st.cache_data
def load_data():
    path = "Sheet2.xlsx"    
    with st.spinner("📊 Loading survey data..."):
        time.sleep(0.5)
        try:
            df = pd.read_excel(path)
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.stop()

    rename = {}
    for c in df.columns:
        low = str(c).lower().strip()
        if "timestamp" in low: rename[c] = "Timestamp"
        elif "how often" in low: rename[c] = "Purchase_Frequency"
        elif "where do you usually buy" in low: rename[c] = "Purchase_Source"
        elif "what matters most" in low: rename[c] = "Decision_Factors"
        elif any(x in low for x in ["₹10","10–15","10-15","premium"]): rename[c] = "Willing_Premium"
        elif any(x in low for x in ["harvest","trace","source location"]): rename[c] = "Traceability_Interest"
        elif "how important" in low: rename[c] = "Source_Importance"
        elif "try it at least once" in low: rename[c] = "Trial_Intent"

    df = df.rename(columns=rename)

    keep = ["Purchase_Frequency","Purchase_Source","Decision_Factors",
            "Willing_Premium","Traceability_Interest","Source_Importance","Trial_Intent"]
    existing = [c for c in keep if c in df.columns]
    if not existing:
        st.error("❌ No expected columns found. Check Excel file.")
        st.stop()

    df = df[existing].copy()

    def clean_ynm(x):
        if pd.isna(x): return None
        s = str(x).strip()
        if any(w in s for w in ["Yes","होय","हाय"]): return "Yes"
        if any(w in s for w in ["Maybe","कदाचित"]): return "Maybe"
        if any(w in s for w in ["No","नाही","न"]): return "No"
        return s

    for col in ["Willing_Premium","Traceability_Interest","Trial_Intent"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_ynm)

    return df

df = load_data()

# ─── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title slide-in">🎛️ Filters</div>', unsafe_allow_html=True)
    
    freq_opts = sorted(df["Purchase_Frequency"].dropna().astype(str).unique()) if "Purchase_Frequency" in df else []
    freq_sel = st.multiselect("📊 Purchase Frequency", freq_opts, default=freq_opts, key="freq")

    src_opts = sorted(df["Purchase_Source"].dropna().astype(str).unique()) if "Purchase_Source" in df else []
    src_sel = st.multiselect("🏪 Purchase Source", src_opts, default=src_opts, key="src")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()
    with col2:
        apply_btn = st.button("✅ Apply", type="primary", use_container_width=True)
    
    # Sidebar stats
    st.markdown(
        '<div class="sidebar-stat">'
        '<div style="font-size: 0.9rem; color: #666; font-weight: 600; margin-bottom: 0.5rem;">TOTAL RESPONSES</div>'
        f'<div style="font-size: 2.5rem; font-weight: 800; color: #2e7d32;">{len(df)}</div>'
        '<div style="font-size: 0.8rem; color: #999; margin-top: 0.3rem;">Survey participants</div>'
        '</div>',
        unsafe_allow_html=True
    )

# ─── Filtered data ─────────────────────────────────────
f_df = df.copy()
if freq_sel: f_df = f_df[f_df["Purchase_Frequency"].isin(freq_sel)]
if src_sel:  f_df = f_df[f_df["Purchase_Source"].isin(src_sel)]

# Show filter status
if len(f_df) < len(df):
    st.info(f"📌 Showing {len(f_df)} of {len(df)} responses based on your filters")

# ─── KPIs ──────────────────────────────────────────────
st.markdown('<div class="animated">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🎯 Key Performance Indicators</h2>', unsafe_allow_html=True)

cols = st.columns(4, gap="large")

n = len(f_df)

p_prem = round(100 * (f_df["Willing_Premium"]     == "Yes").mean(), 1) if n > 0 and "Willing_Premium"     in f_df else 0
p_trac = round(100 * (f_df["Traceability_Interest"] == "Yes").mean(), 1) if n > 0 and "Traceability_Interest" in f_df else 0
p_try  = round(100 * (f_df["Trial_Intent"]         == "Yes").mean(), 1) if n > 0 and "Trial_Intent"        in f_df else 0

def get_color(pct):
    if pct >= 70: return "#2e7d32", "🟢"
    elif pct >= 45: return "#f57f17", "🟡"
    else: return "#c62828", "🔴"

with cols[0]:
    st.markdown(
        '<div class="kpi-card">'
        '<div style="text-align:center">'
        '<div style="font-size:3.5rem; margin-bottom: 0.8rem;">📊</div>'
        '<div class="metric-label">Active Filters</div>'
        f'<div class="metric-value" style="color:#2e7d32">{n:,}</div>'
        '<div class="metric-sublabel">Responses</div>'
        '</div></div>', 
        unsafe_allow_html=True
    )

with cols[1]:
    clr, icon = get_color(p_prem)
    st.markdown(
        '<div class="kpi-card">'
        '<div style="text-align:center">'
        f'<div style="font-size:3rem; margin-bottom:0.5rem">{icon}</div>'
        '<div class="metric-label">Premium Willingness</div>'
        f'<div class="metric-value" style="color:{clr}">{p_prem}%</div>'
        '<div class="metric-sublabel">Pay more for quality</div>'
        '</div></div>', 
        unsafe_allow_html=True
    )

with cols[2]:
    clr, icon = get_color(p_trac)
    st.markdown(
        '<div class="kpi-card">'
        '<div style="text-align:center">'
        f'<div style="font-size:3rem; margin-bottom:0.5rem">{icon}</div>'
        '<div class="metric-label">Traceability Interest</div>'
        f'<div class="metric-value" style="color:{clr}">{p_trac}%</div>'
        '<div class="metric-sublabel">Want source tracking</div>'
        '</div></div>', 
        unsafe_allow_html=True
    )

with cols[3]:
    clr, icon = get_color(p_try)
    st.markdown(
        '<div class="kpi-card">'
        '<div style="text-align:center">'
        f'<div style="font-size:3rem; margin-bottom:0.5rem">{icon}</div>'
        '<div class="metric-label">Trial Intent</div>'
        f'<div class="metric-value" style="color:{clr}">{p_try}%</div>'
        '<div class="metric-sublabel">Would try new service</div>'
        '</div></div>', 
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# ─── Charts Row 1 ──────────────────────────────────────
st.markdown('<hr class="clean-divider">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📈 Purchase Patterns</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    if "Purchase_Frequency" in f_df and not f_df.empty:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        
        fig = px.pie(
            f_df, 
            names="Purchase_Frequency",
            hole=0.55,
            color_discrete_sequence=['#1b5e20', '#2e7d32', '#388e3c', '#4caf50', '#66bb6a', '#81c784']
        )
        
        fig.update_traces(
            textposition='outside',
            textinfo='percent+label',
            textfont_size=14,
            marker=dict(line=dict(color='white', width=4)),
            pull=[0.05] * len(f_df["Purchase_Frequency"].unique())
        )
        
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                font=dict(size=13)
            ),
            margin=dict(t=40, b=40, l=40, r=160),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[dict(
                text=f'<b>{n}</b><br>responses',
                x=0.5, y=0.5,
                font_size=18,
                showarrow=False,
                font=dict(color='#2e7d32')
            )]
        )
        
        st.markdown('<h3 style="color:#2e7d32; font-size:1.4rem; margin-bottom:1rem; font-weight:700">Purchase Frequency Distribution</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, key="freq_chart")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if "Purchase_Source" in f_df and not f_df.empty:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        
        source_data = f_df["Purchase_Source"].value_counts().reset_index()
        source_data.columns = ['Source', 'Count']
        
        fig = px.bar(
            source_data,
            x="Count",
            y="Source",
            orientation="h",
            text="Count",
            color="Count",
            color_continuous_scale=['#c8e6c9', '#81c784', '#4caf50', '#2e7d32', '#1b5e20']
        )
        
        fig.update_traces(
            textposition='outside',
            textfont_size=14,
            marker_line_color='white',
            marker_line_width=3,
            hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=False,
            margin=dict(t=40, b=40, l=20, r=80),
            xaxis=dict(
                title="Number of Responses",
                gridcolor='rgba(0,0,0,0.05)',
                showgrid=True
            ),
            yaxis=dict(
                title="",
                categoryorder='total ascending'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=13)
        )
        
        st.markdown('<h3 style="color:#2e7d32; font-size:1.4rem; margin-bottom:1rem; font-weight:700">Main Purchase Channels</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, key="source_chart")
        st.markdown('</div>', unsafe_allow_html=True)

# ─── Decision Factors ──────────────────────────────────
st.markdown('<hr class="clean-divider">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">💡 Decision Factors Analysis</h2>', unsafe_allow_html=True)
st.markdown('<span class="info-badge">📌 Multiple selections allowed per respondent</span>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

if "Decision_Factors" in f_df:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    keywords = ["Price", "Freshness", "Quality", "Trust", "Convenience", "Local", "Organic", "Packaging"]
    counts = {k: f_df["Decision_Factors"].str.contains(k, case=False, na=False).sum() for k in keywords}
    df_count = pd.DataFrame(counts.items(), columns=["Factor","Count"]).sort_values("Count", ascending=True)
    
    fig = go.Figure()
    
    colors = ['#fff59d', '#ffee58', '#fdd835', '#fbc02d', '#f9a825', '#f57f17', '#e65100', '#bf360c']
    
    fig.add_trace(go.Bar(
        x=df_count["Count"],
        y=df_count["Factor"],
        orientation='h',
        text=df_count["Count"],
        textposition='outside',
        textfont=dict(size=15, color='#2e7d32', weight='bold'),
        marker=dict(
            color=df_count["Count"],
            colorscale=[[0, colors[0]], [1, colors[-1]]],
            line=dict(color='white', width=3)
        ),
        hovertemplate='<b>%{y}</b><br>Mentions: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=100),
        xaxis=dict(
            title="<b>Number of Mentions</b>",
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True
        ),
        yaxis=dict(title=""),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True, key="factors_chart")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Trust Analysis ────────────────────────────────────
if all(c in f_df for c in ["Source_Importance", "Willing_Premium"]):
    st.markdown('<hr class="clean-divider">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">🤝 Trust vs. Premium Willingness</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    fig = px.histogram(
        f_df,
        x="Source_Importance",
        color="Willing_Premium",
        barmode="group",
        color_discrete_map={
            "Yes": "#4caf50",
            "Maybe": "#ffa726",
            "No": "#ef5350"
        },
        category_orders={"Willing_Premium": ["Yes","Maybe","No"]}
    )
    
    fig.update_traces(
        marker_line_color='white',
        marker_line_width=3,
        opacity=0.9
    )
    
    fig.update_layout(
        legend=dict(
            title="<b>Pay Premium?</b>",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=13)
        ),
        xaxis=dict(
            title="<b>Source Importance Rating</b>",
            gridcolor='rgba(0,0,0,0.05)'
        ),
        yaxis=dict(
            title="<b>Number of Responses</b>",
            gridcolor='rgba(0,0,0,0.05)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=13),
        margin=dict(t=80, b=60, l=60, r=40),
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True, key="trust_chart")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────
st.markdown('<hr class="clean-divider">', unsafe_allow_html=True)
st.markdown(
    f'<p style="text-align:center; color:#999; font-size:0.95rem; padding: 1.5rem 0;">'
    f'✨ Built with Streamlit • Last updated: {pd.Timestamp.now().strftime("%B %d, %Y at %H:%M")}</p>',
    unsafe_allow_html=True
)