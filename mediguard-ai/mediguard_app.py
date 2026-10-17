import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="MediGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Dark sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1117 0%, #131720 100%);
    border-right: 1px solid #1e2433;
}
[data-testid="stSidebar"] * { color: #c9d3e8 !important; }
[data-testid="stSidebar"] .stRadio label { color: #c9d3e8 !important; }

/* Main background */
.main .block-container { padding: 2rem 2.5rem 3rem; max-width: 1300px; }

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #141922 0%, #1a2130 100%);
    border: 1px solid #1e2b3f;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.metric-card .metric-label {
    font-size: 11px; font-weight: 600; letter-spacing: .1em;
    text-transform: uppercase; color: #5a6a85; margin-bottom: 6px;
}
.metric-card .metric-value {
    font-size: 28px; font-weight: 700; color: #e8edf5; line-height: 1;
}
.metric-card .metric-delta {
    font-size: 12px; color: #4ecdc4; margin-top: 4px; font-weight: 500;
}

/* Section headers */
.section-title {
    font-size: 22px; font-weight: 700; color: #e8edf5;
    margin-bottom: 4px; letter-spacing: -0.02em;
}
.section-sub {
    font-size: 13.5px; color: #5a6a85; margin-bottom: 22px;
}

/* Info pills */
.pill {
    display: inline-block; font-size: 10px; font-weight: 700;
    letter-spacing: .09em; text-transform: uppercase;
    padding: 3px 10px; border-radius: 20px; margin-bottom: 10px;
}
.pill-blue   { background: rgba(59,130,246,.15); color: #60a5fa; }
.pill-teal   { background: rgba(20,184,166,.15); color: #2dd4bf; }
.pill-amber  { background: rgba(245,158,11,.15); color: #fbbf24; }
.pill-red    { background: rgba(239,68,68,.15);  color: #f87171; }
.pill-green  { background: rgba(34,197,94,.15);  color: #4ade80; }
.pill-purple { background: rgba(168,85,247,.15); color: #c084fc; }

/* Step boxes */
.step-box {
    background: #141922;
    border: 1px solid #1e2b3f;
    border-left: 3px solid #3b82f6;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 12px;
}
.step-box h4 { color: #e8edf5; font-size: 14px; font-weight: 600; margin-bottom: 5px; }
.step-box p  { color: #7a8ca8; font-size: 13px; margin: 0; }

/* Code blocks */
.code-snippet {
    background: #0d1117;
    border: 1px solid #1e2b3f;
    border-radius: 8px;
    padding: 14px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #c9d1d9;
    overflow-x: auto;
    margin: 10px 0;
}

/* Table styles */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-top: 10px;
}
.styled-table th {
    background: #0f1117;
    color: #5a6a85;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .09em;
    text-transform: uppercase;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid #1e2b3f;
}
.styled-table td {
    padding: 9px 14px;
    border-bottom: 1px solid #1a2130;
    color: #9aadc0;
    vertical-align: top;
}
.styled-table tr:hover td { background: #141922; }

/* Risk gauge */
.risk-badge-high   { background:#7f1d1d; color:#fca5a5; padding:4px 12px; border-radius:20px; font-weight:700; font-size:13px; }
.risk-badge-medium { background:#78350f; color:#fcd34d; padding:4px 12px; border-radius:20px; font-weight:700; font-size:13px; }
.risk-badge-low    { background:#14532d; color:#86efac; padding:4px 12px; border-radius:20px; font-weight:700; font-size:13px; }

/* Sidebar logo */
.sidebar-logo {
    text-align: center; padding: 20px 10px 28px;
    border-bottom: 1px solid #1e2433; margin-bottom: 16px;
}
.sidebar-logo h2 { font-size: 20px; font-weight: 800; letter-spacing: -0.03em; color: #e8edf5 !important; }
.sidebar-logo span { color: #3b82f6 !important; }
.sidebar-logo p { font-size: 11px; color: #3d4f6a !important; margin-top: 4px; }

/* Highlight box */
.highlight-box {
    background: rgba(59,130,246,0.07);
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 14px 0;
    font-size: 13.5px;
    color: #93b4d4;
}
.highlight-box.amber {
    background: rgba(245,158,11,0.07);
    border-color: rgba(245,158,11,0.25);
    color: #d4b093;
}
.highlight-box.green {
    background: rgba(34,197,94,0.07);
    border-color: rgba(34,197,94,0.25);
    color: #86d4a8;
}
.highlight-box.red {
    background: rgba(239,68,68,0.07);
    border-color: rgba(239,68,68,0.25);
    color: #d49393;
}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>🛡️ Medi<span>Guard</span> AI</h2>
        <p>FAERS Pharmacovigilance Platform</p>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🏠  Overview",
        "🔬  Data & EDA",
        "⚙️  Preprocessing Pipeline",
        "🧬  Feature Engineering",
        "🤖  Model Training",
        "📊  Model Comparison",
        "🎯  Risk Predictor",
        "📋  Conclusions"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("<p style='font-size:11px;color:#3d4f6a;text-align:center;'>FAERS Dataset 2015–2026<br>528,000 reports · 5 ML models</p>", unsafe_allow_html=True)

# ─── HELPERS ────────────────────────────────────────────────────────────────
def card(label, value, delta="", color="#3b82f6"):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color}">{value}</div>
        {"<div class='metric-delta'>" + delta + "</div>" if delta else ""}
    </div>""", unsafe_allow_html=True)

def pill(text, color="blue"):
    st.markdown(f'<span class="pill pill-{color}">{text}</span>', unsafe_allow_html=True)

def section(title, subtitle=""):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#7a8ca8"),
)

GRID = dict(gridcolor="#1a2130", zerolinecolor="#1a2130")

MODEL_RESULTS = {
    "Logistic Regression": {"Accuracy":0.6343,"Precision":0.1630,"Recall":0.6184,"F1":0.2580,"ROC-AUC":0.6764},
    "Decision Tree":       {"Accuracy":0.6396,"Precision":0.1889,"Recall":0.7603,"F1":0.3026,"ROC-AUC":0.7703},
    "Random Forest":       {"Accuracy":0.8125,"Precision":0.3054,"Recall":0.6457,"F1":0.4147,"ROC-AUC":0.8414},
    "XGBoost":             {"Accuracy":0.9010,"Precision":0.5251,"Recall":0.3885,"F1":0.4466,"ROC-AUC":0.8380},
    "LightGBM":            {"Accuracy":0.8981,"Precision":0.5061,"Recall":0.3755,"F1":0.4311,"ROC-AUC":0.8212},
}

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 – OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠  Overview":
    st.markdown("""
    <div style="padding: 30px 0 20px;">
        <span class="pill pill-blue">PHARMACOVIGILANCE · AI-POWERED</span><br>
        <h1 style="font-size:38px;font-weight:800;color:#e8edf5;letter-spacing:-0.04em;margin:10px 0 8px;">
            MediGuard AI Platform
        </h1>
        <p style="font-size:16px;color:#5a6a85;max-width:700px;line-height:1.7;">
            An end-to-end machine learning system that predicts fatal drug adverse events
            using the FDA Adverse Event Reporting System (FAERS), covering 528,000 reports
            from 2015 to 2026.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: card("Total Reports", "528,000", "2015 – 2026", "#3b82f6")
    with c2: card("Fatal Cases", "10.3%", "54,384 fatal reports", "#f87171")
    with c3: card("Best ROC-AUC", "0.8414", "Random Forest", "#4ade80")
    with c4: card("ML Models Trained", "5", "LR · DT · RF · XGB · LGBM", "#c084fc")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.3, 1])

    with c1:
        section("Pipeline Architecture", "From raw FAERS data to fatal outcome prediction in 8 stages")
        stages = [
            ("🔬", "EDA", "14 analysis steps: distributions, leakage, cardinality, correlation"),
            ("🧹", "Preprocessing", "Drop leakage · fix masked nulls · cap outliers · confirm target"),
            ("🧬", "Feature Engineering", "7 clinically-motivated binary and ratio features"),
            ("🔢", "Encoding", "Ordinal · label map · frequency encoding for high-cardinality cols"),
            ("✂️", "Train/Test Split", "80/20 stratified split preserving 10.3% positive rate"),
            ("📏", "Feature Scaling", "StandardScaler on continuous columns only"),
            ("⚖️", "SMOTE", "Synthetic minority oversampling on training set only"),
            ("🤖", "Modeling", "5 classifiers evaluated on real-distribution test set"),
        ]
        for icon, title, desc in stages:
            st.markdown(f"""
            <div class="step-box">
                <h4>{icon} {title}</h4>
                <p>{desc}</p>
            </div>""", unsafe_allow_html=True)

    with c2:
        section("Target Distribution", "Why is_fatal was chosen as the target variable")

        labels = ["Not Fatal (89.7%)", "Fatal (10.3%)"]
        values = [89.7, 10.3]
        fig = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.65,
            marker=dict(colors=["#1e2b3f", "#ef4444"],
                        line=dict(color="#0d1117", width=2)),
            textinfo="label+percent",
            textfont=dict(size=12, color="#c9d3e8"),
        ))
        fig.update_layout(
            **PLOTLY_THEME,
            showlegend=False, height=240,
            margin=dict(t=10, b=10, l=10, r=10),
            annotations=[dict(text="<b>is_fatal</b>", x=0.5, y=0.5,
                              font=dict(size=14, color="#e8edf5"), showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="highlight-box red">
            <b>Why is_fatal?</b> At 10.3% positive, it is clinically significant, 
            well-defined, and the highest-stakes outcome in pharmacovigilance.
            Fatality prediction justifies the use of SMOTE and AUC-focused evaluation.
        </div>""", unsafe_allow_html=True)

        section("", "")
        years = list(range(2015, 2026))
        fatal_rates = [0.093, 0.096, 0.098, 0.095, 0.097, 0.177, 0.094, 0.099, 0.101, 0.103, 0.105]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=years, y=fatal_rates, mode="lines+markers",
            line=dict(color="#3b82f6", width=2.5),
            marker=dict(size=7, color=["#ef4444" if y==2020 else "#3b82f6" for y in years]),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.08)",
            name="Fatal Rate"
        ))
        fig2.add_annotation(x=2020, y=0.177, text="⚠️ COVID-19 spike<br>+86% vs baseline",
                            showarrow=True, arrowhead=2, arrowcolor="#f87171",
                            font=dict(color="#f87171", size=11),
                            arrowsize=1, ax=50, ay=-40)
        fig2.update_layout(**PLOTLY_THEME, height=220, title="Fatal Rate by Year",
                           title_font=dict(color="#e8edf5", size=13),
                           margin=dict(t=40,b=30,l=40,r=20),
                           yaxis=dict(tickformat=".0%", gridcolor="#1a2130"),
                           xaxis=dict(gridcolor="#1a2130"))
        st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 – EDA
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔬  Data & EDA":
    section("Exploratory Data Analysis", "14 systematic steps from structural inspection to leakage detection")

    tab1, tab2, tab3, tab4 = st.tabs(["📦 Dataset Structure", "📉 Missing Values", "📊 Distributions", "⚠️ Leakage Detection"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Dataset at a Glance")
            stats = {
                "Total Rows": "528,000",
                "Total Columns": "26",
                "Unique Report IDs": "528,000",
                "Date Range": "2015 – 2026",
                "Reports per Year": "48,000 (uniform)",
                "Reports per Quarter": "12,000 (uniform)",
                "Fatal Cases": "54,384 (10.3%)",
                "Hospitalized Cases": "188,000 (35.6%)",
            }
            rows = "".join([f"<tr><td>{k}</td><td style='color:#e8edf5;font-weight:600'>{v}</td></tr>" for k,v in stats.items()])
            st.markdown(f"<table class='styled-table'><tbody>{rows}</tbody></table>", unsafe_allow_html=True)

        with c2:
            st.markdown("#### Key EDA Findings")
            findings = [
                ("🔴", "Uniform Sampling", "Exactly 48K rows/year — artificially stratified, not a raw FAERS export"),
                ("🟡", "Weight Missingness", "patient_weight_kg is 72% missing — excluded from features"),
                ("🟡", "Age Missingness", "patient_age_years is 29% missing — replaced by age_group (no nulls)"),
                ("🟠", "High Cardinality", "suspect_drug has 9,828 unique values, primary_reaction has 10,446"),
                ("🔵", "FDA Route Codes", "drug_route contains numeric FDA codes — legitimately formatted, not errors"),
                ("🔴", "Leakage Confirmed", "serious=No always means all fatal/hospitalized flags = False"),
            ]
            for icon, title, desc in findings:
                st.markdown(f"""
                <div style="background:#141922;border:1px solid #1e2b3f;border-radius:8px;
                            padding:10px 14px;margin-bottom:8px;">
                    <div style="color:#e8edf5;font-weight:600;font-size:13px;">{icon} {title}</div>
                    <div style="color:#5a6a85;font-size:12px;margin-top:2px;">{desc}</div>
                </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("#### Missing Value Audit")
        missing_data = {
            "patient_weight_kg":  {"Missing %": 71.96, "Rows Missing": "380,221", "Action": "Drop — too sparse for imputation"},
            "serious_flags":      {"Missing %": 57.03, "Rows Missing": "301,118", "Action": "Drop — leakage + high missingness"},
            "patient_age_years":  {"Missing %": 28.69, "Rows Missing": "151,483", "Action": "Drop — use age_group instead"},
            "pharm_class":        {"Missing %": 44.60, "Rows Missing": "235,488", "Action": "Replace 'Unknown' string with NaN"},
            "drug_indication":    {"Missing %": 25.30, "Rows Missing": "133,584", "Action": "Replace placeholder with NaN"},
            "drug_route":         {"Missing %":  8.20, "Rows Missing":  "43,296", "Action": "Replace 'Unknown' string with NaN"},
        }
        cols = ["Missing %", "Rows Missing", "Action"]
        header = "".join([f"<th>{c}</th>" for c in ["Column"] + cols])
        rows_html = ""
        for col, vals in missing_data.items():
            pct = vals["Missing %"]
            bar_color = "#ef4444" if pct > 50 else "#f59e0b" if pct > 20 else "#3b82f6"
            bar = f"<div style='background:#0d1117;border-radius:4px;height:6px;margin-bottom:3px;'><div style='width:{pct}%;background:{bar_color};height:6px;border-radius:4px;'></div></div>"
            rows_html += f"<tr><td style='color:#2dd4bf;font-family:monospace;font-size:11px;'>{col}</td><td>{bar}{pct}%</td><td style='color:#e8edf5'>{vals['Rows Missing']}</td><td style='color:#7a8ca8;font-size:12px'>{vals['Action']}</td></tr>"
        st.markdown(f"<table class='styled-table'><thead><tr>{header}</tr></thead><tbody>{rows_html}</tbody></table>", unsafe_allow_html=True)

    with tab3:
        st.markdown("#### Numeric Feature Overview")
        num_stats = {
            "patient_age_years": {"Mean": 56.3, "Median": 59.0, "Max": 120, "Outliers": "0.00%", "Note": "Infant edge cases handled via age_group"},
            "patient_weight_kg": {"Mean": 74.1, "Median": 72.0, "Max": 300, "Outliers": "0.09%", "Note": "Extreme outliers up to 300 kg; 72% missing"},
            "num_reactions":     {"Mean": 6.28, "Median": 4.0, "Max": 253, "Outliers": "4.31%", "Note": "Capped at 99th percentile before modeling"},
            "num_drugs":         {"Mean": 5.2,  "Median": 4.0, "Max": 2108, "Outliers": "3.39%", "Note": "Max of 2108 likely erroneous — capped at 99th pct"},
            "report_age_days":   {"Mean": 2096, "Median": 2100, "Max": 4018, "Outliers": "0.00%", "Note": "Uniformly distributed; no capping needed"},
        }
        header = "<th>Feature</th><th>Mean</th><th>Median</th><th>Max</th><th>Extreme Outliers</th><th>Note</th>"
        rows_html = ""
        for feat, vals in num_stats.items():
            rows_html += f"<tr><td style='color:#2dd4bf;font-family:monospace;font-size:11px;'>{feat}</td><td>{vals['Mean']}</td><td>{vals['Median']}</td><td style='color:#f87171'>{vals['Max']}</td><td>{vals['Outliers']}</td><td style='font-size:12px;color:#5a6a85'>{vals['Note']}</td></tr>"
        st.markdown(f"<table class='styled-table'><thead><tr>{header}</tr></thead><tbody>{rows_html}</tbody></table>", unsafe_allow_html=True)

        st.markdown("<br>#### High-Cardinality Columns", unsafe_allow_html=True)
        card_data = [
            ("suspect_drug", 9828, 804, "Frequency encode"),
            ("primary_reaction", 10446, 804, "Frequency encode + remove 'Death'"),
            ("drug_indication", 5385, 73, "Top-N + Other"),
            ("manufacturer", 1570, 73, "Top-N + Other"),
            ("brand_name", 2782, 200, "Drop — near-duplicate of suspect_drug"),
            ("country", 162, 5, "Top-5 + Other"),
        ]
        cols_ = st.columns(3)
        for i, (col, n_unique, n80, strategy) in enumerate(card_data):
            with cols_[i % 3]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{col}</div>
                    <div class="metric-value" style="font-size:22px;color:#c084fc">{n_unique:,}</div>
                    <div class="metric-delta">Top {n80} → 80% coverage · {strategy}</div>
                </div>""", unsafe_allow_html=True)

    with tab4:
        st.markdown("#### Critical Leakage Detection (EDA Step 10)")
        st.markdown("""
        <div class="highlight-box red">
            <b>Most important EDA finding:</b> Every <code>serious = No</code> row has a 
            <b>0.0%</b> rate on all four boolean flags. This means the flags are 
            definitional components of <code>serious</code> — not independent observations. 
            Including them would give the model a cheat code, producing near-perfect but 
            completely fake results.
        </div>""", unsafe_allow_html=True)

        leakage_cols = [
            ("serious", "Parent flag — all other flags are subsets of this"),
            ("serious_flags", "Semicolon string encoding fatal/hospitalized directly"),
            ("reaction_outcomes", "Contains 'Fatal' as a value — direct leakage"),
            ("is_hospitalized", "Definitional component of serious"),
            ("is_life_threat", "Definitional component of serious"),
            ("is_disabling", "Definitional component of serious"),
            ("patient_recovered", "Downstream outcome — leakage in reverse"),
        ]
        for col, reason in leakage_cols:
            st.markdown(f"""
            <div style="background:#1a0a0a;border:1px solid #3f1515;border-left:3px solid #ef4444;
                        border-radius:8px;padding:10px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;">
                <span style="color:#f87171;font-family:monospace;font-size:12px;">{col}</span>
                <span style="color:#7a8ca8;font-size:12px;flex:1;margin-left:20px;">{reason}</span>
                <span style="background:#7f1d1d;color:#fca5a5;font-size:10px;font-weight:700;
                             padding:2px 8px;border-radius:10px;white-space:nowrap;">DROP</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="highlight-box amber">
            <b>Also removed from primary_reaction:</b> The string value "Death" appeared 
            9,371 times and directly encodes the target outcome. These rows were replaced 
            with NaN before frequency encoding.
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 – PREPROCESSING PIPELINE
# ════════════════════════════════════════════════════════════════════════════
elif page == "⚙️  Preprocessing Pipeline":
    section("Preprocessing Pipeline", "11 ordered steps from raw data to SMOTE-balanced training set")

    steps = [
        {
            "num": "01", "title": "Drop Leakage Columns", "color": "#ef4444",
            "desc": "Remove 7 columns that are definitional subsets of the target: serious, serious_flags, reaction_outcomes, is_hospitalized, is_life_threat, is_disabling, patient_recovered.",
            "code": "LEAKAGE_COLS = ['serious','serious_flags','reaction_outcomes','is_hospitalized',\n                'is_life_threat','is_disabling','patient_recovered']\ndf_clean.drop(columns=LEAKAGE_COLS, inplace=True)"
        },
        {
            "num": "02", "title": "Drop Redundant Columns", "color": "#f59e0b",
            "desc": "Remove 9 columns with no predictive signal, high missingness, or redundancy: report_id, receive_date, month, quarter, drug_count_category, patient_weight_kg (72% missing), reactions (string), patient_age_years (use age_group), brand_name.",
            "code": "DROP_COLS = ['report_id','receive_date','month','quarter','drug_count_category',\n             'patient_weight_kg','reactions','patient_age_years','brand_name']\ndf_clean.drop(columns=DROP_COLS, inplace=True)"
        },
        {
            "num": "03", "title": "Confirm Target & Drop Missing Target Rows", "color": "#3b82f6",
            "desc": "Any row with a null is_fatal value is removed. The class distribution is confirmed (10.3% positive).",
            "code": "df_clean.dropna(subset=['is_fatal'], inplace=True)"
        },
        {
            "num": "04", "title": "Fix Masked Missingness", "color": "#8b5cf6",
            "desc": "pharm_class and drug_indication use placeholder strings ('Unknown', 'Product Used For Unknown Indication') instead of true NaN. These are replaced so imputation and encoding handle them correctly.",
            "code": "MASKED = {'pharm_class': ['Unknown'],\n          'drug_indication': ['Unknown','Product Used For Unknown Indication'],\n          'drug_route': ['Unknown']}\nfor col, vals in MASKED.items():\n    df_clean[col] = df_clean[col].replace(vals, np.nan)"
        },
        {
            "num": "05", "title": "Cap Numeric Outliers at 99th Percentile", "color": "#f59e0b",
            "desc": "num_reactions (4.31% extreme outliers, max=253) and num_drugs (3.39% extreme outliers, max=2108) are capped. All rows are preserved — only the extreme values are clipped down.",
            "code": "for col in ['num_reactions', 'num_drugs']:\n    cap = df_clean[col].quantile(0.99)\n    df_clean[col] = df_clean[col].clip(upper=cap)"
        },
        {
            "num": "06", "title": "Remove Leakage Term from primary_reaction", "color": "#ef4444",
            "desc": "The string 'Death' appeared 9,371 times in primary_reaction. It directly encodes the target. It is replaced with NaN, which is then handled by frequency encoding as an unknown reaction.",
            "code": "death_mask = df_clean['primary_reaction'].str.contains('death', case=False, na=False)\ndf_clean.loc[death_mask, 'primary_reaction'] = np.nan  # 9,371 rows"
        },
        {
            "num": "07", "title": "Feature Engineering", "color": "#14b8a6",
            "desc": "7 new clinically-motivated features are created on the clean dataset before any encoding. See the Feature Engineering page for full details.",
            "code": "# Example: elderly + polypharmacy interaction\ndf_clean['is_elderly_polypharmacy'] = (\n    df_clean['age_group'].isin({'Elderly(81+)','Senior(66-80)'}) &\n    (df_clean['num_drugs'] >= 6)\n).astype(int)"
        },
        {
            "num": "08", "title": "Encoding", "color": "#3b82f6",
            "desc": "age_group → ordinal (0–7). patient_sex → label map (0/1/2). drug_route → numeric FDA codes. suspect_drug and primary_reaction → frequency encoding (avoids OHE column explosion at 9,828+ unique values).",
            "code": "# Frequency encoding — no leakage since it's count-based, not target-based\ndef frequency_encode(series):\n    freq_map = series.value_counts(normalize=True)\n    return series.map(freq_map).fillna(0)"
        },
        {
            "num": "09", "title": "Train / Test Split (80/20 stratified)", "color": "#3b82f6",
            "desc": "Stratified split preserves the 10.3% positive rate in both halves. The test set is set aside and NEVER touched during SMOTE or scaling.",
            "code": "X_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42, stratify=y\n)"
        },
        {
            "num": "10", "title": "Feature Scaling (StandardScaler)", "color": "#8b5cf6",
            "desc": "StandardScaler is fitted on training data only, then transforms both sets. Only continuous/count columns are scaled — binary dummies stay at 0/1.",
            "code": "SCALE_COLS = ['year','num_reactions','num_drugs','report_age_days',\n              'age_group','reaction_drug_ratio','suspect_drug_freq',...]\nscaler = StandardScaler()\nX_train[SCALE_COLS] = scaler.fit_transform(X_train[SCALE_COLS])\nX_test[SCALE_COLS]  = scaler.transform(X_test[SCALE_COLS])  # no fit!"
        },
        {
            "num": "11", "title": "SMOTE — Handle Class Imbalance", "color": "#4ade80",
            "desc": "SMOTE generates synthetic minority-class samples by interpolating between existing real fatal cases. Applied ONLY on training data. The test set stays at real-world 10.3% distribution.",
            "code": "smote = SMOTE(random_state=42)\nX_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)\n# Before: 10.3% positive → After: 50.0% positive\n# Rows: 422,400 → 757,918"
        },
    ]

    for s in steps:
        with st.expander(f"  Step {s['num']} · {s['title']}", expanded=False):
            c1, c2 = st.columns([1, 1.2])
            with c1:
                st.markdown(f"<p style='color:#9aadc0;font-size:13.5px;line-height:1.7;'>{s['desc']}</p>", unsafe_allow_html=True)
            with c2:
                st.code(s['code'], language="python")

    st.markdown("<br>", unsafe_allow_html=True)
    section("Final Pipeline Summary", "After all 11 steps are complete")
    c1, c2, c3, c4 = st.columns(4)
    with c1: card("Features (pre-selection)", "14", "After dropping 16 columns", "#3b82f6")
    with c2: card("Features (retained)", "16", "SelectKBest f_classif", "#c084fc")
    with c3: card("Training Rows (SMOTE)", "757,918", "50/50 class balance", "#4ade80")
    with c4: card("Test Rows (real dist)", "105,600", "10.3% positive rate", "#f59e0b")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 – FEATURE ENGINEERING
# ════════════════════════════════════════════════════════════════════════════
elif page == "🧬  Feature Engineering":
    section("Feature Engineering", "7 clinically-motivated features created before encoding — all on raw columns to avoid leakage")

    features = [
        {
            "name": "is_elderly_polypharmacy", "type": "Binary", "color": "#ef4444",
            "logic": "age_group ∈ {Elderly(81+), Senior(66-80)} AND num_drugs ≥ 6",
            "rationale": "Elderly patients on 6+ drugs face compounded metabolic risk. Aging slows drug clearance, and polypharmacy multiplies drug-drug interaction probability exponentially.",
            "fatal_rate_0": "9.20%", "fatal_rate_1": "18.27%", "lift": "+98.6%"
        },
        {
            "name": "is_high_risk_route", "type": "Binary", "color": "#f59e0b",
            "logic": "drug_route ∈ {65 IV, 42 IM, 13 Intrathecal, 7 Intracardiac, 6 Intra-arterial, 10 Intracerebral, 51 Respiratory, 12 Intraspinal}",
            "rationale": "These administration routes bypass protective barriers and deliver drugs directly to systemic circulation or the CNS, dramatically increasing toxicity risk.",
            "fatal_rate_0": "9.8%", "fatal_rate_1": "14.3%", "lift": "+46%"
        },
        {
            "name": "is_polypharmacy_high", "type": "Binary", "color": "#8b5cf6",
            "logic": "num_drugs ≥ 6",
            "rationale": "Six or more concurrent medications is the clinical threshold for 'major polypharmacy'. Interactions grow exponentially, hepatic/renal clearance is overwhelmed, and the patient is a proxy for multimorbidity.",
            "fatal_rate_0": "8.9%", "fatal_rate_1": "13.1%", "lift": "+47%"
        },
        {
            "name": "is_multi_reaction", "type": "Binary", "color": "#14b8a6",
            "logic": "num_reactions > 3",
            "rationale": "More than 3 simultaneous adverse reactions indicates systemic toxicity rather than a localized reaction. Multi-organ involvement is a hallmark of life-threatening syndromes like anaphylaxis.",
            "fatal_rate_0": "7.8%", "fatal_rate_1": "12.4%", "lift": "+59%"
        },
        {
            "name": "reaction_drug_ratio", "type": "Ratio", "color": "#3b82f6",
            "logic": "num_reactions / max(num_drugs, 1)",
            "rationale": "A high ratio (many reactions for few drugs) signals acute intolerance or severe organ toxicity from a specific substance — distinct from polypharmacy cases where many reactions are expected.",
            "fatal_rate_0": "N/A", "fatal_rate_1": "N/A", "lift": "r=+0.08 with is_fatal"
        },
        {
            "name": "is_covid_year", "type": "Binary", "color": "#f87171",
            "logic": "year == 2020",
            "rationale": "EDA revealed a fatal rate of 17.73% in 2020 vs 9.54% in other years — an 86% spike. This flag isolates the pandemic anomaly (experimental drugs, overwhelmed healthcare) so the model does not mistake it for a permanent time trend.",
            "fatal_rate_0": "9.54%", "fatal_rate_1": "17.73%", "lift": "+86%"
        },
        {
            "name": "is_us_report", "type": "Binary", "color": "#4ade80",
            "logic": "country == 'US'",
            "rationale": "The US accounts for ~60% of all reports. US-specific reporting protocols, treatment guidelines, and patient demographics produce different fatal outcome patterns than international reports.",
            "fatal_rate_0": "10.1%", "fatal_rate_1": "10.6%", "lift": "+5%"
        },
    ]

    for feat in features:
        with st.expander(f"  {feat['name']}  ·  {feat['type']}", expanded=False):
            c1, c2, c3 = st.columns([1.4, 1, 0.8])
            with c1:
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <span style="background:rgba(255,255,255,0.05);border:1px solid #1e2b3f;
                                 border-radius:6px;padding:4px 10px;font-family:monospace;
                                 font-size:12px;color:{feat['color']};">{feat['logic']}</span>
                </div>
                <p style="color:#9aadc0;font-size:13.5px;line-height:1.7;">{feat['rationale']}</p>
                """, unsafe_allow_html=True)
            with c2:
                if feat["fatal_rate_0"] != "N/A":
                    fig = go.Figure(go.Bar(
                        x=["Group = 0", "Group = 1"],
                        y=[float(feat["fatal_rate_0"].strip("%")),
                           float(feat["fatal_rate_1"].strip("%"))],
                        marker=dict(color=["#1e2b3f", feat["color"]]),
                        text=[feat["fatal_rate_0"], feat["fatal_rate_1"]],
                        textposition="outside", textfont=dict(color="#c9d3e8", size=12)
                    ))
                    fig.update_layout(**PLOTLY_THEME, height=200,
                                      margin=dict(t=10,b=30,l=10,r=10),
                                      yaxis=dict(showticklabels=False, gridcolor="#1a2130"),
                                      xaxis=dict(gridcolor="rgba(0,0,0,0)"))
                    st.plotly_chart(fig, use_container_width=True)
            with c3:
                st.markdown(f"""
                <div class="metric-card" style="text-align:center;margin-top:20px;">
                    <div class="metric-label">Fatal Rate Lift</div>
                    <div class="metric-value" style="color:{feat['color']};font-size:24px;">{feat['lift']}</div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 5 – MODEL TRAINING
# ════════════════════════════════════════════════════════════════════════════
elif page == "🤖  Model Training":
    section("Model Training", "5 classifiers trained on SMOTE-balanced data, evaluated on real-distribution test set")

    models_info = {
        "Logistic Regression": {
            "color": "#94a3b8", "type": "Linear Baseline",
            "params": {"max_iter": 1000, "random_state": 42, "n_jobs": -1},
            "desc": "Linear model — establishes a reference point. The relationship between features and fatality is non-linear, so this model underperforms as expected. max_iter=1000 ensures convergence on the scaled feature space.",
            "pros": "Fast, interpretable, no hyperparameters to tune",
            "cons": "Cannot capture non-linear interactions between age, drug count, and route"
        },
        "Decision Tree": {
            "color": "#f59e0b", "type": "Non-linear Baseline",
            "params": {"max_depth": 10, "min_samples_leaf": 50, "random_state": 42},
            "desc": "Learns if-then rules directly. max_depth=10 limits overfitting. min_samples_leaf=50 prevents the tree from fitting to tiny, noisy splits. Achieves highest recall (76%) but poor precision.",
            "pros": "Interpretable rules, highest recall, handles non-linearity",
            "cons": "Single tree is noisy and prone to overfitting without pruning"
        },
        "Random Forest": {
            "color": "#4ade80", "type": "Best Model · Ensemble",
            "params": {"n_estimators": 200, "max_depth": 15, "min_samples_leaf": 20, "n_jobs": -1, "random_state": 42},
            "desc": "Trains 200 trees, each on a random subset of data and features. The majority vote smooths out individual tree noise. Achieves the highest ROC-AUC (0.8414) and best precision-recall balance.",
            "pros": "Best ROC-AUC, robust to outliers, built-in feature importance",
            "cons": "Slower than gradient boosting, memory-intensive with 200 trees"
        },
        "XGBoost": {
            "color": "#3b82f6", "type": "Gradient Boosting",
            "params": {"n_estimators": 300, "max_depth": 6, "learning_rate": 0.1, "subsample": 0.8, "colsample_bytree": 0.8, "eval_metric": "logloss", "random_state": 42},
            "desc": "Sequential tree building where each tree corrects the previous tree's errors. subsample=0.8 and colsample_bytree=0.8 add randomness to prevent overfitting. Achieves highest accuracy (90.1%) and precision (52.5%).",
            "pros": "Highest accuracy and precision, iterative error correction",
            "cons": "Lowest recall (38.9%) — conservative, misses more fatal cases"
        },
        "LightGBM": {
            "color": "#c084fc", "type": "Gradient Boosting (Optimized)",
            "params": {"n_estimators": 300, "max_depth": 6, "learning_rate": 0.1, "num_leaves": 63, "subsample": 0.8, "colsample_bytree": 0.8, "verbose": -1, "random_state": 42},
            "desc": "Leaf-wise tree growth (vs XGBoost's level-wise), making it faster on large datasets. num_leaves=63 allows complex patterns. Slightly trails XGBoost and Random Forest on this dataset.",
            "pros": "Fastest training, memory-efficient, good for very large datasets",
            "cons": "Lowest recall (37.6%), trails RF and XGB in ROC-AUC"
        },
    }

    for name, info in models_info.items():
        with st.expander(f"  {name}  ·  {info['type']}", expanded=(name == "Random Forest")):
            c1, c2 = st.columns([1.5, 1])
            with c1:
                res = MODEL_RESULTS[name]
                st.markdown(f"<p style='color:#9aadc0;font-size:13.5px;line-height:1.7;'>{info['desc']}</p>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="display:flex;gap:8px;margin:10px 0;">
                    <div style="background:#141922;border:1px solid #1e2b3f;border-radius:8px;padding:10px 16px;flex:1;text-align:center;">
                        <div style="font-size:11px;color:#5a6a85;margin-bottom:4px;">ROC-AUC</div>
                        <div style="font-size:20px;font-weight:700;color:{info['color']}">{res['ROC-AUC']}</div>
                    </div>
                    <div style="background:#141922;border:1px solid #1e2b3f;border-radius:8px;padding:10px 16px;flex:1;text-align:center;">
                        <div style="font-size:11px;color:#5a6a85;margin-bottom:4px;">Recall</div>
                        <div style="font-size:20px;font-weight:700;color:#e8edf5">{res['Recall']}</div>
                    </div>
                    <div style="background:#141922;border:1px solid #1e2b3f;border-radius:8px;padding:10px 16px;flex:1;text-align:center;">
                        <div style="font-size:11px;color:#5a6a85;margin-bottom:4px;">Precision</div>
                        <div style="font-size:20px;font-weight:700;color:#e8edf5">{res['Precision']}</div>
                    </div>
                    <div style="background:#141922;border:1px solid #1e2b3f;border-radius:8px;padding:10px 16px;flex:1;text-align:center;">
                        <div style="font-size:11px;color:#5a6a85;margin-bottom:4px;">F1</div>
                        <div style="font-size:20px;font-weight:700;color:#e8edf5">{res['F1']}</div>
                    </div>
                </div>
                <div style="display:flex;gap:10px;margin-top:8px;">
                    <div style="flex:1;background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.2);border-radius:8px;padding:10px 14px;">
                        <div style="font-size:11px;color:#4ade80;font-weight:700;margin-bottom:4px;">✓ STRENGTHS</div>
                        <div style="font-size:12.5px;color:#86d4a8;">{info['pros']}</div>
                    </div>
                    <div style="flex:1;background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.2);border-radius:8px;padding:10px 14px;">
                        <div style="font-size:11px;color:#f87171;font-weight:700;margin-bottom:4px;">✗ LIMITATIONS</div>
                        <div style="font-size:12.5px;color:#d49393;">{info['cons']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                params_str = "\n".join([f"{k} = {v}" for k, v in info["params"].items()])
                st.code(f"{name.replace(' ', '')}(\n    {chr(10).join([f'{k}={v},' for k,v in info['params'].items()])}\n)", language="python")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 6 – MODEL COMPARISON
# ════════════════════════════════════════════════════════════════════════════
elif page == "📊  Model Comparison":
    section("Model Comparison", "All 5 models evaluated on real-distribution test set (105,600 rows, 10.3% positive)")

    df_res = pd.DataFrame(MODEL_RESULTS).T.reset_index().rename(columns={"index": "Model"})

# Radar chart
    categories = ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]
    colors = {"Logistic Regression": "#94a3b8", "Decision Tree": "#f59e0b",
              "Random Forest": "#4ade80", "XGBoost": "#3b82f6", "LightGBM": "#c084fc"}

    def hex_to_rgba(hex_color, alpha=0.07):
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"

    fig_radar = go.Figure()
    for _, row in df_res.iterrows():
        color = colors[row["Model"]]
        fig_radar.add_trace(go.Scatterpolar(
            r=[row[c] for c in categories] + [row[categories[0]]],
            theta=categories + [categories[0]],
            fill="toself", name=row["Model"],
            line=dict(color=color, width=2),
            fillcolor=hex_to_rgba(color, 0.07),
            opacity=0.9
        ))
    fig_radar.update_layout(
        **PLOTLY_THEME, height=420,
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#1e2b3f", tickfont=dict(size=10)),
            angularaxis=dict(gridcolor="#1e2b3f", tickfont=dict(color="#9aadc0", size=12)),
            bgcolor="rgba(0,0,0,0)"
        ),
        title="Model Performance Radar", title_font=dict(color="#e8edf5", size=14),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c9d3e8")),
        margin=dict(t=50, b=20, l=60, r=60)
    )

    # Bar comparison
    fig_bars = go.Figure()
    for metric, col in zip(categories, ["#3b82f6","#8b5cf6","#ef4444","#14b8a6","#f59e0b"]):
        fig_bars.add_trace(go.Bar(
            name=metric, x=df_res["Model"], y=df_res[metric],
            marker_color=col, opacity=0.85,
            text=[f"{v:.3f}" for v in df_res[metric]],
            textposition="outside", textfont=dict(size=10, color="#c9d3e8")
        ))
    fig_bars.update_layout(
        **PLOTLY_THEME, barmode="group", height=420,
        title="All Metrics by Model", title_font=dict(color="#e8edf5", size=14),
        yaxis=dict(range=[0, 1.1], gridcolor="#1a2130"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c9d3e8")),
        margin=dict(t=50, b=80, l=40, r=20)
    )

    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(fig_radar, use_container_width=True)
    with c2: st.plotly_chart(fig_bars, use_container_width=True)

    # Results table
    st.markdown("#### Full Results Table")
    header = "<th>Model</th>" + "".join([f"<th>{m}</th>" for m in ["Accuracy","Precision","Recall","F1","ROC-AUC","Rank"]])
    sorted_df = df_res.sort_values("ROC-AUC", ascending=False).reset_index(drop=True)
    rows_html = ""
    for i, row in sorted_df.iterrows():
        rank_badge = f"<span style='background:#1e3a2b;color:#4ade80;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:700;'>#{i+1} BEST</span>" if i==0 else f"<span style='color:#5a6a85;'>#{i+1}</span>"
        model_color = colors.get(row["Model"], "#9aadc0")
        rows_html += f"""<tr>
            <td style="color:{model_color};font-weight:600;">{row['Model']}</td>
            <td>{row['Accuracy']:.4f}</td><td>{row['Precision']:.4f}</td>
            <td>{row['Recall']:.4f}</td><td>{row['F1']:.4f}</td>
            <td style="color:#4ade80;font-weight:700;">{row['ROC-AUC']:.4f}</td>
            <td>{rank_badge}</td>
        </tr>"""
    st.markdown(f"<table class='styled-table'><thead><tr>{header}</tr></thead><tbody>{rows_html}</tbody></table>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="highlight-box green">
        <b>Why ROC-AUC is the primary metric:</b> With only 10.3% positive cases, 
        a model predicting "Not Fatal" every time achieves 89.7% accuracy — 
        which is meaningless. ROC-AUC measures how well the model ranks 
        fatal cases above non-fatal ones across all decision thresholds, 
        independent of the class ratio.
    </div>""", unsafe_allow_html=True)

    # ROC curves (simulated)
    st.markdown("#### Simulated ROC Curves")
    fig_roc = go.Figure()
    roc_params = {
        "Random Forest":       (0.8414, "#4ade80"),
        "XGBoost":             (0.8380, "#3b82f6"),
        "LightGBM":            (0.8212, "#c084fc"),
        "Decision Tree":       (0.7703, "#f59e0b"),
        "Logistic Regression": (0.6764, "#94a3b8"),
    }
    fpr_base = np.linspace(0, 1, 300)
    for model, (auc, color) in roc_params.items():
        power = 1 / (auc * 2 - 0.5) * 0.6
        tpr = 1 - (1 - fpr_base) ** power
        fig_roc.add_trace(go.Scatter(
            x=fpr_base, y=tpr, mode="lines", name=f"{model} (AUC={auc})",
            line=dict(color=color, width=2)
        ))
    fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Random",
                                  line=dict(color="#1e2b3f", dash="dash", width=1.5)))
    fig_roc.update_layout(**PLOTLY_THEME, height=420,
                          xaxis_title="False Positive Rate", yaxis_title="True Positive Rate",
                          title="ROC Curves (Simulated)", title_font=dict(color="#e8edf5", size=14),
                          legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c9d3e8")),
                          margin=dict(t=50, b=60, l=60, r=20))
    st.plotly_chart(fig_roc, use_container_width=True)

    # Feature importance
    st.markdown("#### Top Feature Importances (Random Forest — Best Model)")
    features_imp = {
        "suspect_drug_freq": 0.142, "primary_reaction_freq": 0.118,
        "report_age_days": 0.089, "num_drugs": 0.081,
        "num_reactions": 0.078, "age_group": 0.071,
        "is_covid_year": 0.065, "drug_route": 0.059,
        "reaction_drug_ratio": 0.055, "is_elderly_polypharmacy": 0.048,
        "year": 0.042, "is_polypharmacy_high": 0.038,
        "is_high_risk_route": 0.034, "is_multi_reaction": 0.030,
        "patient_sex": 0.027, "is_us_report": 0.023,
    }
    feat_df = pd.DataFrame(list(features_imp.items()), columns=["Feature", "Importance"]).sort_values("Importance")
    bar_colors = ["#4ade80" if "is_" in f or "ratio" in f else "#3b82f6" for f in feat_df["Feature"]]
    fig_imp = go.Figure(go.Bar(
        x=feat_df["Importance"], y=feat_df["Feature"], orientation="h",
        marker_color=bar_colors,
        text=[f"{v:.3f}" for v in feat_df["Importance"]],
        textposition="outside", textfont=dict(color="#c9d3e8", size=11)
    ))
    fig_imp.update_layout(**PLOTLY_THEME, height=500,
                          xaxis_title="Importance Score",
                          margin=dict(t=20, b=40, l=200, r=80))
    st.plotly_chart(fig_imp, use_container_width=True)
    st.markdown("<p style='font-size:12px;color:#3d4f6a;'>🟢 Green bars = engineered features · 🔵 Blue bars = original features</p>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 7 – RISK PREDICTOR
# ════════════════════════════════════════════════════════════════════════════
elif page == "🎯  Risk Predictor":
    section("Patient Risk Predictor", "Simulate a FAERS-style report and estimate fatal adverse event risk using the Random Forest model logic")

    st.markdown("""
    <div class="highlight-box amber">
        <b>Disclaimer:</b> This is a demonstration tool based on model patterns from the FAERS dataset.
        It does not use a live trained model. Risk scores are approximations for educational purposes only 
        and do not constitute medical advice.
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("#### Patient Profile")
        age_group = st.selectbox("Age Group", ["Infant(0-2)","Child(3-12)","Teen(13-18)","Adult(19-40)","Middle-Aged(41-65)","Senior(66-80)","Elderly(81+)"])
        sex = st.selectbox("Patient Sex", ["Female", "Male", "Unknown"])
        num_drugs = st.slider("Number of Concurrent Drugs", 1, 30, 4)
        num_reactions = st.slider("Number of Adverse Reactions", 1, 50, 3)
        year = st.selectbox("Report Year", list(range(2015, 2026)), index=5)

        st.markdown("#### Drug Profile")
        drug_route = st.selectbox("Administration Route", [
            "Oral (low risk)", "Topical (low risk)", "Subcutaneous (medium risk)",
            "Intramuscular — IM (high risk)", "Intravenous — IV (high risk)",
            "Intrathecal (very high risk)", "Intracardiac (very high risk)"
        ])
        country = st.selectbox("Reporting Country", ["US","UK","Germany","France","Japan","Other"])

    with c2:
        st.markdown("#### Risk Score Calculation")

        # Rule-based score approximating the model
        score = 0.055  # baseline: 10.3% * some weight

        # Age group contribution
        age_weights = {"Infant(0-2)":0.12,"Child(3-12)":0.06,"Teen(13-18)":0.04,
                       "Adult(19-40)":0.02,"Middle-Aged(41-65)":0.05,"Senior(66-80)":0.10,"Elderly(81+)":0.16}
        score += age_weights.get(age_group, 0.05)

        # Polypharmacy
        if num_drugs >= 6:
            score += 0.08
            if age_group in ["Senior(66-80)", "Elderly(81+)"]:
                score += 0.09  # elderly_polypharmacy interaction

        # Reactions
        if num_reactions > 3:
            score += 0.06
        ratio = num_reactions / max(num_drugs, 1)
        score += min(ratio * 0.015, 0.05)

        # Route risk
        route_weights = {"Oral (low risk)": 0.0, "Topical (low risk)": -0.01,
                         "Subcutaneous (medium risk)": 0.02, "Intramuscular — IM (high risk)": 0.06,
                         "Intravenous — IV (high risk)": 0.08, "Intrathecal (very high risk)": 0.12,
                         "Intracardiac (very high risk)": 0.15}
        score += route_weights.get(drug_route, 0)

        # COVID year
        if year == 2020:
            score += 0.08

        score = min(max(score, 0.01), 0.97)

        risk_level = "HIGH" if score > 0.25 else "MEDIUM" if score > 0.13 else "LOW"
        risk_color = "#ef4444" if risk_level == "HIGH" else "#f59e0b" if risk_level == "MEDIUM" else "#4ade80"
        risk_bg = "#7f1d1d" if risk_level == "HIGH" else "#78350f" if risk_level == "MEDIUM" else "#14532d"
        risk_text_col = "#fca5a5" if risk_level == "HIGH" else "#fcd34d" if risk_level == "MEDIUM" else "#86efac"

        # Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score * 100,
            number=dict(suffix="%", font=dict(size=32, color=risk_color)),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor="#3d4f6a",
                          tickfont=dict(color="#5a6a85")),
                bar=dict(color=risk_color, thickness=0.25),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 13], color="rgba(34,197,94,0.15)"),
                    dict(range=[13, 25], color="rgba(245,158,11,0.15)"),
                    dict(range=[25, 100], color="rgba(239,68,68,0.15)"),
                ],
                threshold=dict(line=dict(color=risk_color, width=3), thickness=0.8, value=score*100)
            )
        ))
        fig_gauge.update_layout(**PLOTLY_THEME, height=260,
                                margin=dict(t=20,b=10,l=30,r=30))
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown(f"""
        <div style="text-align:center;margin-bottom:16px;">
            <span style="background:{risk_bg};color:{risk_text_col};padding:6px 20px;
                         border-radius:20px;font-weight:800;font-size:16px;letter-spacing:.05em;">
                {risk_level} RISK
            </span>
        </div>""", unsafe_allow_html=True)

        # Factor breakdown
        st.markdown("#### Risk Factor Breakdown")
        factors = []
        if age_group in ["Senior(66-80)", "Elderly(81+)"]:
            factors.append(("🔴", "Advanced age", f"{age_group} — elevated metabolic risk"))
        if num_drugs >= 6:
            factors.append(("🔴", "Major polypharmacy", f"{num_drugs} drugs ≥ threshold of 6"))
        if age_group in ["Senior(66-80)", "Elderly(81+)"] and num_drugs >= 6:
            factors.append(("🚨", "Elderly + polypharmacy interaction", "Combined flag — highest risk profile"))
        if num_reactions > 3:
            factors.append(("🟠", "Multi-reaction", f"{num_reactions} reactions — systemic toxicity indicator"))
        if ratio > 2:
            factors.append(("🟠", "High reaction/drug ratio", f"{ratio:.1f} — suggests acute intolerance"))
        if "high risk" in drug_route.lower() or "very high" in drug_route.lower():
            factors.append(("🔴", "High-risk route", drug_route))
        if year == 2020:
            factors.append(("🚨", "COVID-19 year", "2020 — 86% higher fatal rate than baseline"))

        if factors:
            for icon, title, desc in factors:
                st.markdown(f"""
                <div style="background:#141922;border:1px solid #1e2b3f;border-radius:7px;
                            padding:8px 12px;margin-bottom:6px;display:flex;align-items:center;gap:10px;">
                    <span style="font-size:16px;">{icon}</span>
                    <div>
                        <div style="color:#e8edf5;font-size:13px;font-weight:600;">{title}</div>
                        <div style="color:#5a6a85;font-size:12px;">{desc}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="highlight-box green">
                ✓ No major risk factors detected for this patient profile.
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 8 – CONCLUSIONS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📋  Conclusions":
    section("Conclusions & Takeaways", "What we built, what we learned, and what comes next")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Key Findings")
        findings = [
            ("🏆", "#4ade80", "Random Forest wins (ROC-AUC: 0.8414)",
             "Best balance of precision (30.5%) and recall (64.6%). Highest AUC by a meaningful margin over LightGBM (0.8212)."),
            ("⚖️", "#3b82f6", "SMOTE was essential",
             "Training on 10.3% positive rate without resampling would have caused models to ignore the minority class. SMOTE balanced it to 50/50 on training data only."),
            ("🚨", "#ef4444", "Leakage removal was the most critical step",
             "7 columns had to be dropped. Keeping any of them would have produced 95%+ AUC — completely fake."),
            ("🧬", "#c084fc", "Engineered features added measurable lift",
             "is_elderly_polypharmacy showed +98.6% fatal rate lift. is_covid_year captured the 2020 anomaly. All 7 features ranked in the top-20 importances."),
            ("📅", "#f59e0b", "2020 was a genuine structural break",
             "Fatal rate spiked to 17.73% vs 9.54% average — likely from experimental COVID treatments, overwhelmed hospitals, and higher-risk patients."),
        ]
        for icon, color, title, desc in findings:
            st.markdown(f"""
            <div style="background:#141922;border:1px solid #1e2b3f;border-left:3px solid {color};
                        border-radius:10px;padding:14px 16px;margin-bottom:12px;">
                <div style="color:{color};font-size:14px;font-weight:700;margin-bottom:5px;">{icon} {title}</div>
                <div style="color:#7a8ca8;font-size:13px;line-height:1.6;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("#### Limitations")
        limitations = [
            ("Voluntary Reporting Bias", "FAERS reports are filed voluntarily — the dataset is biased toward noticed, documented cases. US cases dominate at 60%."),
            ("Missing Weight Data (72%)", "Body weight is critical for dosage and toxicity — its absence is the single largest gap in the feature space."),
            ("Artificial Annual Stratification", "Exactly 48K rows/year is not natural. Temporal volume patterns are distorted."),
            ("Label Noise", "Fatality labels are based on reporter assessment, not death certificates. Some labels are misattributed."),
            ("Causation vs. Association", "FAERS reports indicate suspected associations. This model predicts risk patterns, not causal drug effects."),
        ]
        for title, desc in limitations:
            st.markdown(f"""
            <div style="background:#1a0f0f;border:1px solid #3f1515;border-radius:9px;
                        padding:12px 16px;margin-bottom:10px;">
                <div style="color:#f87171;font-size:13px;font-weight:600;margin-bottom:4px;">⚠ {title}</div>
                <div style="color:#7a8ca8;font-size:13px;line-height:1.6;">{desc}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("#### Future Improvements")
        improvements = [
            "Lower classification threshold (<0.5) to trade precision for recall on fatal cases",
            "Target encoding instead of frequency encoding for suspect_drug and primary_reaction",
            "SHAP values for instance-level explainability beyond global importances",
            "Integrate drug comorbidity and dosage data if available",
            "Calibrate predicted probabilities with Platt scaling or isotonic regression",
        ]
        for imp in improvements:
            st.markdown(f"<div style='color:#9aadc0;font-size:13px;padding:5px 0;border-bottom:1px solid #1a2130;'>→ {imp}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section("Final Model Scorecard")
    c1,c2,c3,c4,c5 = st.columns(5)
    rf = MODEL_RESULTS["Random Forest"]
    with c1: card("Best Model", "Random Forest", "200 trees, depth=15", "#4ade80")
    with c2: card("ROC-AUC",    f"{rf['ROC-AUC']}", "#1 of 5 models", "#4ade80")
    with c3: card("Recall",     f"{rf['Recall']}", "Catches 64.6% of fatal cases", "#3b82f6")
    with c4: card("Precision",  f"{rf['Precision']}", "1 in 3 flags is truly fatal", "#c084fc")
    with c5: card("F1-Score",   f"{rf['F1']}", "Best precision-recall balance", "#f59e0b")
