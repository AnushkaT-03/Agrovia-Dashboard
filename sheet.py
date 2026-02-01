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

# ─── Custom CSS for animations ─────────────────────────
st.markdown("""
<style>
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

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.04); }
  100% { transform: scale(1); }
}

.fade-in-up {
  animation: fadeInUp 0.9s ease-out forwards;
}

.kpi-card {
  transition: all 0.3s ease;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.12);
}

.pulse-once {
  animation: pulse 1.6s ease-in-out;
}

.section-header {
  color: #1b5e20;
  font-size: 1.85rem !important;
  margin: 2rem 0 1rem 0 !important;
  font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────
st.markdown(
    '<h1 style="text-align:center; color:#1b5e20; margin-bottom:0.3rem;" class="pulse-once">'
    '🥬 Vegetable Consumer Survey Dashboard</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p style="text-align:center; color:#555; font-size:1.18rem; margin-top:0;" class="fade-in-up">'
    'Buying habits • Price sensitivity • Trust • Traceability interest</p>',
    unsafe_allow_html=True
)

# ─── Load data with better loading feedback ────────────
@st.cache_data
def load_data():
    path = r"C:\Users\anush\OneDrive\Desktop\Agrovia\Sheet2.xlsx"
    with st.spinner("Reading responses & preparing insights... 🥕📈"):
        time.sleep(0.7)  # pleasant micro-delay
        try:
            df = pd.read_excel(path)
        except Exception as e:
            st.error(f"Cannot read file\n{str(e)}")
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
        st.error("No expected columns found. Check Excel column names.")
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

# ─── Sidebar (small visual upgrade) ────────────────────
with st.sidebar:
    st.markdown('<h3 style="color:#1b5e20;">Filters</h3>', unsafe_allow_html=True)
    
    freq_opts = sorted(df["Purchase_Frequency"].dropna().astype(str).unique()) if "Purchase_Frequency" in df else []
    freq_sel = st.multiselect("Purchase Frequency", freq_opts, default=freq_opts)

    src_opts = sorted(df["Purchase_Source"].dropna().astype(str).unique()) if "Purchase_Source" in df else []
    src_sel = st.multiselect("Purchase Source", src_opts, default=src_opts)

    st.markdown("<br>"*2, unsafe_allow_html=True)
    if st.button("⟲ Reset all filters", type="primary", use_container_width=True):
        st.rerun()

# ─── Filtered data ─────────────────────────────────────
f_df = df.copy()
if freq_sel: f_df = f_df[f_df["Purchase_Frequency"].isin(freq_sel)]
if src_sel:  f_df = f_df[f_df["Purchase_Source"].isin(src_sel)]

# ─── KPIs with animation ───────────────────────────────
st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">Key Highlights</h2>', unsafe_allow_html=True)

cols = st.columns(4, gap="medium")

n = len(f_df)

p_prem = round(100 * (f_df["Willing_Premium"]     == "Yes").mean(), 1) if n > 0 and "Willing_Premium"     in f_df else 0
p_trac = round(100 * (f_df["Traceability_Interest"] == "Yes").mean(), 1) if n > 0 and "Traceability_Interest" in f_df else 0
p_try  = round(100 * (f_df["Trial_Intent"]         == "Yes").mean(), 1) if n > 0 and "Trial_Intent"        in f_df else 0

def kpi_style(pct):
    if pct >= 70: bg, clr = "#e8f5e9", "#1b5e20"
    elif pct >= 45: bg, clr = "#fff8e1", "#f57f17"
    else: bg, clr = "#ffebee", "#c62828"
    return f"background:{bg};color:{clr};"

with cols[0]:
    st.metric("Total Responses", f"{n:,}")

with cols[1]:
    st.markdown(
        f'<div class="kpi-card fade-in-up" style="{kpi_style(p_prem)};padding:1.4rem 1rem;text-align:center">'
        f'<div style="font-size:1.15rem;opacity:0.9">Willing to pay more</div>'
        f'<div style="font-size:2.8rem;font-weight:700;margin:0.4rem 0">{p_prem}%</div>'
        f'</div>', unsafe_allow_html=True
    )

with cols[2]:
    st.markdown(
        f'<div class="kpi-card fade-in-up" style="{kpi_style(p_trac)};padding:1.4rem 1rem;text-align:center">'
        f'<div style="font-size:1.15rem;opacity:0.9">Want traceability</div>'
        f'<div style="font-size:2.8rem;font-weight:700;margin:0.4rem 0">{p_trac}%</div>'
        f'</div>', unsafe_allow_html=True
    )

with cols[3]:
    st.markdown(
        f'<div class="kpi-card fade-in-up" style="{kpi_style(p_try)};padding:1.4rem 1rem;text-align:center">'
        f'<div style="font-size:1.15rem;opacity:0.9">Would try service</div>'
        f'<div style="font-size:2.8rem;font-weight:700;margin:0.4rem 0">{p_try}%</div>'
        f'</div>', unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# ─── Charts section ────────────────────────────────────
st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
st.divider()

colA, colB = st.columns(2, gap="large")

with colA:
    if "Purchase_Frequency" in f_df and not f_df.empty:
        fig = px.pie(
            f_df, names="Purchase_Frequency",
            hole=0.45,
            title="Purchase Frequency",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            title_font_size=20,
            margin=dict(t=70, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)

with colB:
    if "Purchase_Source" in f_df and not f_df.empty:
        fig = px.bar(
            f_df["Purchase_Source"].value_counts().reset_index(),
            x="count", y="Purchase_Source",
            orientation="h",
            title="Main Purchase Channels",
            color="count",
            color_continuous_scale="Greens"
        )
        fig.update_layout(
            showlegend=False,
            title_font_size=20,
            margin=dict(t=70, b=30),
            xaxis_title="Responses",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Rest of the dashboard remains the same ────────────
# Decision factors
st.markdown('<h2 class="section-header fade-in-up">What matters most when buying vegetables</h2>', unsafe_allow_html=True)
st.caption("Multiple answers possible — count of mentions")

if "Decision_Factors" in f_df:
    keywords = ["Price", "Freshness", "Quality", "Trust", "Convenience", "Local", "Organic", "Packaging"]
    counts = {k: f_df["Decision_Factors"].str.contains(k, case=False, na=False).sum() for k in keywords}
    df_count = pd.DataFrame(counts.items(), columns=["Factor","Count"]).sort_values("Count", ascending=False)

    fig = px.bar(
        df_count, x="Count", y="Factor",
        orientation="h", text="Count",
        color="Count", color_continuous_scale="YlGn"
    )
    fig.update_traces(textposition="auto")
    fig.update_layout(margin=dict(t=30,b=20), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# Trust × Premium
if all(c in f_df for c in ["Source_Importance", "Willing_Premium"]):
    st.markdown('<h2 class="section-header fade-in-up">Source importance vs Willingness to pay premium</h2>', unsafe_allow_html=True)
    
    fig = px.histogram(
        f_df,
        x="Source_Importance",
        color="Willing_Premium",
        barmode="group",
        color_discrete_sequence=["#66bb6a", "#ffb74d", "#ef5350"],
        category_orders={"Willing_Premium": ["Yes","Maybe","No"]}
    )
    fig.update_layout(legend_title_text="Willing to pay more?")
    st.plotly_chart(fig, use_container_width=True)

st.caption(f"Dashboard • Updated {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")