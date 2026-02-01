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

# ─── Dark Mode Clean CSS ───────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background: #0a0e27;
    color: #e0e0e0;
}

/* Hide unnecessary Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Smooth fade animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.animated { animation: fadeIn 0.5s ease-out; }

/* KPI Cards - Dark minimal */
.kpi-card {
    background: linear-gradient(135deg, #1a1f3a 0%, #14182b 100%);
    border-radius: 16px;
    padding: 1.8rem 1.5rem;
    border: 1px solid rgba(76, 175, 80, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #4caf50, transparent);
    opacity: 0;
    transition: opacity 0.3s;
}

.kpi-card:hover {
    transform: translateY(-5px);
    border-color: rgba(76, 175, 80, 0.5);
    box-shadow: 0 8px 32px rgba(76, 175, 80, 0.15);
}

.kpi-card:hover::before {
    opacity: 1;
}

/* Chart containers */
.chart-box {
    background: #14182b;
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 2rem;
    transition: all 0.3s ease;
}

.chart-box:hover {
    border-color: rgba(76, 175, 80, 0.3);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

/* Sidebar dark */
section[data-testid="stSidebar"] {
    background: #0f1229;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

section[data-testid="stSidebar"] > div {
    background: #0f1229;
}

/* Multiselect dark */
.stMultiSelect > div > div {
    background: #1a1f3a;
    border-color: rgba(76, 175, 80, 0.3);
    color: #e0e0e0;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(135deg, #4caf50, #45a049) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3) !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4) !important;
}

/* Section title */
.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #4caf50;
    margin: 2.5rem 0 1.5rem 0;
    padding-left: 1rem;
    border-left: 4px solid #4caf50;
}

/* Metric styling */
.metric-value {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
    margin: 0.8rem 0;
}

.metric-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-sublabel {
    font-size: 0.75rem;
    color: #666;
    margin-top: 0.3rem;
}

/* Info badge */
.info-tag {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: rgba(76, 175, 80, 0.15);
    border: 1px solid rgba(76, 175, 80, 0.3);
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #66bb6a;
}

/* Scrollbar dark */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #0a0e27;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #4caf50, #2e7d32);
    border-radius: 10px;
    border: 2px solid #0a0e27;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #66bb6a, #4caf50);
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(76, 175, 80, 0.3), transparent);
    margin: 2rem 0;
    border: none;
}

/* Remove padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 100%;
}

/* Plotly dark theme */
.js-plotly-plot {
    border-radius: 12px;
}

/* Sidebar stats */
.sidebar-stat {
    background: linear-gradient(135deg, #1a1f3a, #14182b);
    border: 1px solid rgba(76, 175, 80, 0.3);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    margin-top: 2rem;
}

/* Filter status */
.stAlert {
    background: rgba(76, 175, 80, 0.1);
    border: 1px solid rgba(76, 175, 80, 0.3);
    color: #66bb6a;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────
st.markdown(
    '<h1 style="text-align:center; font-size:2.5rem; font-weight:800; color:#4caf50; margin-bottom:0.5rem;" class="animated">'
    'Vegetable Consumer Insights</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p style="text-align:center; font-size:1rem; color:#999; margin-bottom:2rem;" class="animated">'
    'Survey Analytics Dashboard</p>',
    unsafe_allow_html=True
)

# ─── Load data ─────────────────────────────────────────
@st.cache_data
def load_data():
    path = "Sheet2.xlsx"    
    try:
        df = pd.read_excel(path)
    except Exception as e:
        st.error(f"Error: {str(e)}")
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
        st.error("No valid columns found.")
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
    st.markdown('<h2 style="color:#4caf50; text-align:center; margin-bottom:2rem;">Filters</h2>', unsafe_allow_html=True)
    
    freq_opts = sorted(df["Purchase_Frequency"].dropna().astype(str).unique()) if "Purchase_Frequency" in df else []
    freq_sel = st.multiselect("Purchase Frequency", freq_opts, default=freq_opts)

    src_opts = sorted(df["Purchase_Source"].dropna().astype(str).unique()) if "Purchase_Source" in df else []
    src_sel = st.multiselect("Purchase Source", src_opts, default=src_opts)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Reset Filters", use_container_width=True):
        st.rerun()
    
    # Sidebar stats
    st.markdown(
        '<div class="sidebar-stat">'
        '<div style="font-size:0.8rem; color:#999; margin-bottom:0.5rem;">TOTAL RESPONSES</div>'
        f'<div style="font-size:2.2rem; font-weight:800; color:#4caf50;">{len(df)}</div>'
        '</div>',
        unsafe_allow_html=True
    )

# ─── Filtered data ─────────────────────────────────────
f_df = df.copy()
if freq_sel: f_df = f_df[f_df["Purchase_Frequency"].isin(freq_sel)]
if src_sel:  f_df = f_df[f_df["Purchase_Source"].isin(src_sel)]

if len(f_df) < len(df):
    st.info(f"Showing {len(f_df)} of {len(df)} responses")

# ─── KPIs ──────────────────────────────────────────────
st.markdown('<div class="animated">', unsafe_allow_html=True)

cols = st.columns(4, gap="medium")

n = len(f_df)
p_prem = round(100 * (f_df["Willing_Premium"] == "Yes").mean(), 1) if n > 0 and "Willing_Premium" in f_df else 0
p_trac = round(100 * (f_df["Traceability_Interest"] == "Yes").mean(), 1) if n > 0 and "Traceability_Interest" in f_df else 0
p_try = round(100 * (f_df["Trial_Intent"] == "Yes").mean(), 1) if n > 0 and "Trial_Intent" in f_df else 0

def get_color(pct):
    if pct >= 70: return "#4caf50"
    elif pct >= 45: return "#ff9800"
    else: return "#f44336"

with cols[0]:
    st.markdown(
        '<div class="kpi-card">'
        '<div style="text-align:center">'
        '<div class="metric-label">Filtered</div>'
        f'<div class="metric-value" style="color:#4caf50">{n}</div>'
        '<div class="metric-sublabel">Responses</div>'
        '</div></div>', 
        unsafe_allow_html=True
    )

with cols[1]:
    clr = get_color(p_prem)
    st.markdown(
        '<div class="kpi-card">'
        '<div style="text-align:center">'
        '<div class="metric-label">Premium Ready</div>'
        f'<div class="metric-value" style="color:{clr}">{p_prem}%</div>'
        '<div class="metric-sublabel">Pay more</div>'
        '</div></div>', 
        unsafe_allow_html=True
    )

with cols[2]:
    clr = get_color(p_trac)
    st.markdown(
        '<div class="kpi-card">'
        '<div style="text-align:center">'
        '<div class="metric-label">Want Traceability</div>'
        f'<div class="metric-value" style="color:{clr}">{p_trac}%</div>'
        '<div class="metric-sublabel">Track source</div>'
        '</div></div>', 
        unsafe_allow_html=True
    )

with cols[3]:
    clr = get_color(p_try)
    st.markdown(
        '<div class="kpi-card">'
        '<div style="text-align:center">'
        '<div class="metric-label">Trial Intent</div>'
        f'<div class="metric-value" style="color:{clr}">{p_try}%</div>'
        '<div class="metric-sublabel">Try service</div>'
        '</div></div>', 
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# ─── Charts ────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Purchase Patterns</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    if "Purchase_Frequency" in f_df and not f_df.empty:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        
        fig = px.pie(
            f_df, 
            names="Purchase_Frequency",
            hole=0.6,
            color_discrete_sequence=['#1b5e20', '#2e7d32', '#388e3c', '#4caf50', '#66bb6a', '#81c784']
        )
        
        fig.update_traces(
            textposition='outside',
            textinfo='percent+label',
            textfont=dict(size=12, color='#e0e0e0'),
            marker=dict(line=dict(color='#0a0e27', width=3))
        )
        
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            annotations=[dict(
                text=f'<b>{n}</b><br><span style="font-size:0.8em">responses</span>',
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False,
                font=dict(color='#4caf50')
            )],
            height=400
        )
        
        st.markdown('<h3 style="color:#e0e0e0; font-size:1.1rem; margin-bottom:1rem; font-weight:600">Frequency</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, key="freq")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if "Purchase_Source" in f_df and not f_df.empty:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        
        source_data = f_df["Purchase_Source"].value_counts().reset_index()
        source_data.columns = ['Source', 'Count']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=source_data["Count"],
            y=source_data["Source"],
            orientation='h',
            text=source_data["Count"],
            textposition='outside',
            textfont=dict(size=12, color='#e0e0e0'),
            marker=dict(
                color=source_data["Count"],
                colorscale=[[0, '#1b5e20'], [1, '#81c784']],
                line=dict(color='#0a0e27', width=2)
            ),
            hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=60),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                showgrid=True,
                color='#e0e0e0'
            ),
            yaxis=dict(
                categoryorder='total ascending',
                color='#e0e0e0'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12, color='#e0e0e0'),
            height=400
        )
        
        st.markdown('<h3 style="color:#e0e0e0; font-size:1.1rem; margin-bottom:1rem; font-weight:600">Purchase Channels</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, key="source")
        st.markdown('</div>', unsafe_allow_html=True)

# ─── Decision Factors ──────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Decision Factors</h2>', unsafe_allow_html=True)

if "Decision_Factors" in f_df:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    
    keywords = ["Price", "Freshness", "Quality", "Trust", "Convenience", "Local", "Organic", "Packaging"]
    counts = {k: f_df["Decision_Factors"].str.contains(k, case=False, na=False).sum() for k in keywords}
    df_count = pd.DataFrame(counts.items(), columns=["Factor","Count"]).sort_values("Count", ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_count["Count"],
        y=df_count["Factor"],
        orientation='h',
        text=df_count["Count"],
        textposition='outside',
        textfont=dict(size=13, color='#e0e0e0', weight='bold'),
        marker=dict(
            color=df_count["Count"],
            colorscale=[[0, '#ff6f00'], [0.5, '#ff9800'], [1, '#ffc107']],
            line=dict(color='#0a0e27', width=2)
        ),
        hovertemplate='<b>%{y}</b><br>Mentions: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=80),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=True,
            color='#e0e0e0'
        ),
        yaxis=dict(color='#e0e0e0'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=13, color='#e0e0e0'),
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True, key="factors")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Trust Analysis ────────────────────────────────────
if all(c in f_df for c in ["Source_Importance", "Willing_Premium"]):
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Trust vs Premium</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    
    fig = px.histogram(
        f_df,
        x="Source_Importance",
        color="Willing_Premium",
        barmode="group",
        color_discrete_map={
            "Yes": "#4caf50",
            "Maybe": "#ff9800",
            "No": "#f44336"
        },
        category_orders={"Willing_Premium": ["Yes","Maybe","No"]}
    )
    
    fig.update_traces(
        marker_line_color='#0a0e27',
        marker_line_width=2,
        opacity=0.9
    )
    
    fig.update_layout(
        legend=dict(
            title="Pay Premium?",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='#e0e0e0')
        ),
        xaxis=dict(
            title="Source Importance",
            gridcolor='rgba(255,255,255,0.05)',
            color='#e0e0e0'
        ),
        yaxis=dict(
            title="Responses",
            gridcolor='rgba(255,255,255,0.05)',
            color='#e0e0e0'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='#e0e0e0'),
        margin=dict(t=60, b=40, l=40, r=40),
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True, key="trust")
    st.markdown('</div>', unsafe_allow_html=True)