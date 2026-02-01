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

# ─── Enhanced Custom CSS ───────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(25px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}

.fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
}

.slide-in-left {
  animation: slideInLeft 0.6s ease-out forwards;
}

.kpi-card {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  position: relative;
  overflow: hidden;
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s;
}

.kpi-card:hover::before {
  left: 100%;
}

.kpi-card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.pulse-once {
  animation: pulse 1.8s ease-in-out;
}

.section-header {
  color: #1b5e20;
  font-size: 1.95rem !important;
  margin: 2.5rem 0 1.2rem 0 !important;
  font-weight: 700;
  letter-spacing: -0.02em;
  position: relative;
  padding-left: 16px;
}

.section-header::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 5px;
  height: 70%;
  background: linear-gradient(180deg, #4caf50, #1b5e20);
  border-radius: 3px;
}

.main-title {
  background: linear-gradient(135deg, #1b5e20 0%, #4caf50 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.subtitle {
  background: linear-gradient(90deg, #666 0%, #999 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 500;
}

.metric-container {
  background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  border: 1px solid rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.metric-container:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.stButton>button {
  border-radius: 12px !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
  border: 2px solid transparent !important;
}

.stButton>button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
}

.sidebar .stMultiSelect {
  margin-bottom: 1.5rem;
}

.sidebar .element-container {
  animation: slideInLeft 0.5s ease-out;
}

/* Plotly chart containers */
.js-plotly-plot {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #4caf50, #1b5e20);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #45a049, #145214);
}

.divider-fancy {
  height: 3px;
  background: linear-gradient(90deg, transparent, #4caf50, transparent);
  border: none;
  margin: 2rem 0;
  border-radius: 2px;
}

.info-badge {
  display: inline-block;
  padding: 0.4rem 0.9rem;
  background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #1b5e20;
  margin: 0.3rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

.chart-container {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 16px rgba(0,0,0,0.06);
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.04);
}

.chart-container:hover {
  box-shadow: 0 8px 28px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# ─── Enhanced Header ───────────────────────────────────
st.markdown(
    '<h1 style="text-align:center; margin-bottom:0.3rem;" class="pulse-once main-title">'
    '🥬 Vegetable Consumer Survey Dashboard</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p style="text-align:center; font-size:1.2rem; margin-top:0;" class="fade-in-up subtitle">'
    'Buying habits • Price sensitivity • Trust • Traceability interest</p>',
    unsafe_allow_html=True
)

st.markdown('<hr class="divider-fancy">', unsafe_allow_html=True)

# ─── Load data with better loading feedback ────────────
@st.cache_data
def load_data():
    path = "Sheet2.xlsx"    
    with st.spinner("🔄 Reading responses & preparing insights... 🥕📈"):
        time.sleep(0.7)  # pleasant micro-delay
        try:
            df = pd.read_excel(path)
        except Exception as e:
            st.error(f"❌ Cannot read file\n{str(e)}")
            st.stop()

    # ── renaming logic same as before ──────────────────
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
        st.error("❌ No expected columns found. Check Excel column names.")
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

# ─── Enhanced Sidebar ──────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="text-align:center; padding: 1rem 0 1.5rem 0;">'
        '<h2 style="color:#1b5e20; margin:0; font-size: 2rem;">🎛️ Filters</h2>'
        '</div>', 
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="slide-in-left">', unsafe_allow_html=True)
    
    freq_opts = sorted(df["Purchase_Frequency"].dropna().astype(str).unique()) if "Purchase_Frequency" in df else []
    freq_sel = st.multiselect("📊 Purchase Frequency", freq_opts, default=freq_opts)

    src_opts = sorted(df["Purchase_Source"].dropna().astype(str).unique()) if "Purchase_Source" in df else []
    src_sel = st.multiselect("🏪 Purchase Source", src_opts, default=src_opts)

    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔄 Reset all filters", type="primary", use_container_width=True):
        st.rerun()
    
    st.markdown("<br>"*2, unsafe_allow_html=True)
    
    # Sidebar stats
    st.markdown(
        '<div style="background: linear-gradient(135deg, #e8f5e9, #c8e6c9); '
        'padding: 1rem; border-radius: 12px; margin-top: 1rem;">'
        f'<p style="margin:0; color: #1b5e20; font-weight: 600; text-align: center;">'
        f'📈 Total Responses<br><span style="font-size: 2rem; font-weight: 700;">{len(df)}</span></p>'
        '</div>',
        unsafe_allow_html=True
    )

# ─── Filtered data ─────────────────────────────────────
f_df = df.copy()
if freq_sel: f_df = f_df[f_df["Purchase_Frequency"].isin(freq_sel)]
if src_sel:  f_df = f_df[f_df["Purchase_Source"].isin(src_sel)]

# ─── Enhanced KPIs ─────────────────────────────────────
st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">🎯 Key Highlights</h2>', unsafe_allow_html=True)

cols = st.columns(4, gap="medium")

n = len(f_df)

p_prem = round(100 * (f_df["Willing_Premium"]     == "Yes").mean(), 1) if n > 0 and "Willing_Premium"     in f_df else 0
p_trac = round(100 * (f_df["Traceability_Interest"] == "Yes").mean(), 1) if n > 0 and "Traceability_Interest" in f_df else 0
p_try  = round(100 * (f_df["Trial_Intent"]         == "Yes").mean(), 1) if n > 0 and "Trial_Intent"        in f_df else 0

def kpi_style(pct):
    if pct >= 70: 
        bg = "linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)"
        clr = "#1b5e20"
        icon = "🟢"
    elif pct >= 45: 
        bg = "linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%)"
        clr = "#f57f17"
        icon = "🟡"
    else: 
        bg = "linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%)"
        clr = "#c62828"
        icon = "🔴"
    return bg, clr, icon

with cols[0]:
    st.markdown(
        '<div class="metric-container fade-in-up" style="text-align:center">'
        f'<div style="font-size:3rem; margin-bottom: 0.5rem;">📊</div>'
        f'<div style="font-size:1.1rem; color:#666; font-weight:600">Total Responses</div>'
        f'<div style="font-size:3rem; font-weight:800; color:#1b5e20; margin-top:0.5rem">{n:,}</div>'
        '</div>', 
        unsafe_allow_html=True
    )

with cols[1]:
    bg, clr, icon = kpi_style(p_prem)
    st.markdown(
        f'<div class="kpi-card fade-in-up" style="background:{bg};padding:1.6rem 1.2rem;text-align:center">'
        f'<div style="font-size:2.5rem; margin-bottom:0.5rem">{icon}</div>'
        f'<div style="font-size:1.05rem; color:{clr}; opacity:0.85; font-weight:600">Willing to Pay More</div>'
        f'<div style="font-size:3.2rem;font-weight:800;margin:0.6rem 0; color:{clr}">{p_prem}%</div>'
        f'<div style="font-size:0.85rem; color:{clr}; opacity:0.7">Premium Products</div>'
        f'</div>', 
        unsafe_allow_html=True
    )

with cols[2]:
    bg, clr, icon = kpi_style(p_trac)
    st.markdown(
        f'<div class="kpi-card fade-in-up" style="background:{bg};padding:1.6rem 1.2rem;text-align:center">'
        f'<div style="font-size:2.5rem; margin-bottom:0.5rem">{icon}</div>'
        f'<div style="font-size:1.05rem; color:{clr}; opacity:0.85; font-weight:600">Want Traceability</div>'
        f'<div style="font-size:3.2rem;font-weight:800;margin:0.6rem 0; color:{clr}">{p_trac}%</div>'
        f'<div style="font-size:0.85rem; color:{clr}; opacity:0.7">Track Farm Source</div>'
        f'</div>', 
        unsafe_allow_html=True
    )

with cols[3]:
    bg, clr, icon = kpi_style(p_try)
    st.markdown(
        f'<div class="kpi-card fade-in-up" style="background:{bg};padding:1.6rem 1.2rem;text-align:center">'
        f'<div style="font-size:2.5rem; margin-bottom:0.5rem">{icon}</div>'
        f'<div style="font-size:1.05rem; color:{clr}; opacity:0.85; font-weight:600">Would Try Service</div>'
        f'<div style="font-size:3.2rem;font-weight:800;margin:0.6rem 0; color:{clr}">{p_try}%</div>'
        f'<div style="font-size:0.85rem; color:{clr}; opacity:0.7">New Platform Intent</div>'
        f'</div>', 
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# ─── Enhanced Charts section ───────────────────────────
st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
st.markdown('<hr class="divider-fancy">', unsafe_allow_html=True)

colA, colB = st.columns(2, gap="large")

with colA:
    if "Purchase_Frequency" in f_df and not f_df.empty:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.pie(
            f_df, names="Purchase_Frequency",
            hole=0.5,
            title="<b>Purchase Frequency</b>",
            color_discrete_sequence=px.colors.qualitative.G10,
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont_size=13,
            marker=dict(line=dict(color='white', width=3))
        )
        fig.update_layout(
            title_font_size=22,
            title_font_color="#1b5e20",
            title_font_family="Inter",
            margin=dict(t=80, b=40),
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=-0.15, 
                xanchor="center", 
                x=0.5,
                font=dict(size=12)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with colB:
    if "Purchase_Source" in f_df and not f_df.empty:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.bar(
            f_df["Purchase_Source"].value_counts().reset_index(),
            x="count", y="Purchase_Source",
            orientation="h",
            title="<b>Main Purchase Channels</b>",
            color="count",
            color_continuous_scale=["#c8e6c9", "#66bb6a", "#2e7d32", "#1b5e20"]
        )
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=2
        )
        fig.update_layout(
            showlegend=False,
            title_font_size=22,
            title_font_color="#1b5e20",
            title_font_family="Inter",
            margin=dict(t=80, b=40),
            xaxis_title="<b>Responses</b>",
            yaxis_title="",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(gridcolor='rgba(0,0,0,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Decision factors ──────────────────────────────────
st.markdown('<h2 class="section-header fade-in-up">💡 What matters most when buying vegetables</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="info-badge">📌 Multiple answers possible — count of mentions</p>',
    unsafe_allow_html=True
)

if "Decision_Factors" in f_df:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    keywords = ["Price", "Freshness", "Quality", "Trust", "Convenience", "Local", "Organic", "Packaging"]
    counts = {k: f_df["Decision_Factors"].str.contains(k, case=False, na=False).sum() for k in keywords}
    df_count = pd.DataFrame(counts.items(), columns=["Factor","Count"]).sort_values("Count", ascending=False)

    fig = px.bar(
        df_count, x="Count", y="Factor",
        orientation="h", text="Count",
        color="Count", 
        color_continuous_scale=["#fff9c4", "#ffeb3b", "#fdd835", "#f9a825", "#f57f17"]
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=14,
        marker_line_color='white',
        marker_line_width=2
    )
    fig.update_layout(
        margin=dict(t=30, b=30, l=20, r=80), 
        coloraxis_showscale=False,
        xaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=13)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Trust × Premium ───────────────────────────────────
if all(c in f_df for c in ["Source_Importance", "Willing_Premium"]):
    st.markdown('<h2 class="section-header fade-in-up">🤝 Source importance vs Willingness to pay premium</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = px.histogram(
        f_df,
        x="Source_Importance",
        color="Willing_Premium",
        barmode="group",
        color_discrete_sequence=["#66bb6a", "#ffb74d", "#ef5350"],
        category_orders={"Willing_Premium": ["Yes","Maybe","No"]}
    )
    fig.update_traces(
        marker_line_color='white',
        marker_line_width=2
    )
    fig.update_layout(
        legend_title_text="<b>Willing to pay more?</b>",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(gridcolor='rgba(0,0,0,0.05)', title="<b>Source Importance</b>"),
        yaxis=dict(gridcolor='rgba(0,0,0,0.05)', title="<b>Count</b>"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=13),
        margin=dict(t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────
st.markdown('<hr class="divider-fancy">', unsafe_allow_html=True)
st.markdown(
    f'<p style="text-align:center; color:#999; font-size:0.9rem; padding: 1rem 0;">'
    f'Dashboard powered by Streamlit 📊 • Last updated: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}</p>',
    unsafe_allow_html=True
)