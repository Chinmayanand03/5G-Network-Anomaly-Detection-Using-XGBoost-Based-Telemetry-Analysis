import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="5G Anomaly Detection",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    /* =========================================================
       PROFESSIONAL CLOUD / E-COMMERCE STYLE 5G UI
       Same dashboard structure, upgraded visual system
       ========================================================= */

    :root {
        --navy: #071426;
        --navy-2: #0b1f38;
        --blue: #1683ff;
        --cyan: #20d9ff;
        --violet: #7c5cff;
        --green: #16c784;
        --orange: #ff9f43;
        --red: #ff4d6d;
        --card: rgba(255,255,255,0.075);
        --card-border: rgba(255,255,255,0.13);
        --text: #f5f8ff;
        --muted: #aebbd0;
    }

    .stApp {
        background:
            radial-gradient(circle at 5% 0%, rgba(32,217,255,0.18), transparent 26%),
            radial-gradient(circle at 95% 5%, rgba(124,92,255,0.20), transparent 28%),
            radial-gradient(circle at 55% 80%, rgba(22,131,255,0.12), transparent 34%),
            linear-gradient(135deg, #061321 0%, #091a30 45%, #071426 100%);
        color: var(--text);
    }

    .main .block-container {
        max-width: 1210px;
        padding-top: 1.8rem;
        padding-bottom: 4rem;
    }

    /* Top navigation style */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        padding: 14px 18px;
        margin-bottom: 24px;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        background: rgba(7,20,38,0.76);
        backdrop-filter: blur(18px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.24);
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 15px;
        font-weight: 800;
        letter-spacing: 0.2px;
    }

    .brand-dot {
        width: 11px;
        height: 11px;
        border-radius: 50%;
        background: #20d9ff;
        box-shadow: 0 0 18px #20d9ff;
    }

    .status-pill {
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(22,199,132,0.12);
        border: 1px solid rgba(22,199,132,0.30);
        color: #7ff0bf;
        font-size: 12px;
        font-weight: 800;
    }

    /* Hero */
    .hero {
        position: relative;
        overflow: hidden;
        padding: 30px 32px;
        margin-bottom: 28px;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.12);
        background:
            radial-gradient(circle at 88% 20%, rgba(32,217,255,0.25), transparent 22%),
            radial-gradient(circle at 68% 100%, rgba(124,92,255,0.24), transparent 35%),
            linear-gradient(120deg, rgba(15,45,77,0.96), rgba(8,25,48,0.96));
        box-shadow: 0 25px 70px rgba(0,0,0,0.30);
    }

    .hero::after {
        content: "";
        position: absolute;
        right: -100px;
        top: -110px;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        border: 1px solid rgba(32,217,255,0.22);
        box-shadow:
            0 0 0 35px rgba(32,217,255,0.035),
            0 0 0 75px rgba(32,217,255,0.025);
    }

    .hero-kicker {
        color: #5fe6ff;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 9px;
    }

    .hero-title {
        font-size: clamp(34px, 5vw, 58px);
        line-height: 1.02;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(90deg, #ffffff 0%, #a9f4ff 48%, #9d8cff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        margin-top: 14px;
        max-width: 760px;
        color: #c8d5e8;
        font-size: 16px;
        line-height: 1.65;
    }

    .hero-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        margin-top: 20px;
    }

    .hero-tag {
        padding: 8px 12px;
        border-radius: 999px;
        color: #eafcff;
        font-size: 11px;
        font-weight: 800;
        background: rgba(32,217,255,0.09);
        border: 1px solid rgba(32,217,255,0.20);
    }

    /* Section headings */
    .section-title {
        display: flex;
        align-items: center;
        gap: 11px;
        margin: 30px 0 14px;
        font-size: 24px;
        font-weight: 900;
        color: #ffffff;
    }

    .section-title::before {
        content: "";
        width: 5px;
        height: 27px;
        border-radius: 8px;
        background: linear-gradient(180deg, #20d9ff, #7c5cff);
        box-shadow: 0 0 14px rgba(32,217,255,0.55);
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        min-height: 118px;
        padding: 20px 21px;
        border-radius: 18px;
        border: 1px solid var(--card-border);
        background:
            linear-gradient(145deg, rgba(255,255,255,0.10), rgba(255,255,255,0.035));
        box-shadow: 0 12px 32px rgba(0,0,0,0.20);
        transition: transform .18s ease, border-color .18s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(32,217,255,0.38);
    }

    div[data-testid="stMetricLabel"] {
        color: #aebbd0 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: .7px;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 900 !important;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        min-height: 46px;
        border: 0;
        border-radius: 12px;
        color: white;
        font-weight: 850;
        letter-spacing: .15px;
        background: linear-gradient(100deg, #087ff5, #17c7ff);
        box-shadow: 0 9px 24px rgba(8,127,245,0.24);
        transition: transform .15s ease, box-shadow .15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 13px 30px rgba(32,217,255,0.30);
        color: white;
    }

    /* Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.13) !important;
        border-radius: 11px !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="select"] * {
        color: #f4f8ff !important;
    }

    /* Tables */
    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.11);
        box-shadow: 0 14px 35px rgba(0,0,0,0.18);
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-weight: 800;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #20d9ff !important;
    }

    /* Alerts / result boxes */
    .result-normal {
        padding: 20px 22px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(22,199,132,0.16), rgba(22,199,132,0.05));
        border: 1px solid rgba(22,199,132,0.34);
        box-shadow: 0 12px 30px rgba(22,199,132,0.08);
    }

    .result-abnormal {
        padding: 20px 22px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(255,77,109,0.18), rgba(255,77,109,0.05));
        border: 1px solid rgba(255,77,109,0.38);
        box-shadow: 0 12px 30px rgba(255,77,109,0.10);
    }

    .result-title {
        font-size: 20px;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .result-text {
        color: #c8d5e8;
        font-size: 13px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 20% 0%, rgba(32,217,255,0.12), transparent 30%),
            linear-gradient(180deg, #071526, #091c32);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] .stRadio label {
        border-radius: 10px;
        padding: 5px 8px;
    }

    /* Footer */
    .footer {
        margin-top: 48px;
        padding: 18px 0 5px;
        color: #7f91aa;
        font-size: 12px;
        text-align: center;
        border-top: 1px solid rgba(255,255,255,0.08);
    }

    /* Hide Streamlit chrome */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Overview layout matching the reference design */
    .overview-metric {
        min-height: 92px;
        padding: 17px 19px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.12);
        background: linear-gradient(145deg, rgba(255,255,255,0.075), rgba(255,255,255,0.035));
        box-shadow: 0 10px 25px rgba(0,0,0,0.14);
        border-left: 4px solid #20d9ff;
    }

    .overview-metric.metric-normal { border-left-color: #16c784; }
    .overview-metric.metric-abnormal { border-left-color: #ff4d7d; }
    .overview-metric.metric-accuracy { border-left-color: #9b72ff; }

    .overview-metric-label {
        color: #8fb3d4;
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .overview-metric-value {
        color: #ffffff;
        font-size: 25px;
        line-height: 1;
        font-weight: 900;
    }

    .overview-subtitle {
        font-size: 19px;
        margin-top: 24px;
        margin-bottom: 9px;
    }

    .overview-subtitle::before {
        width: 4px;
        height: 22px;
    }

    .class-stat-block {
        padding: 0 0 8px 0;
    }

    .class-stat-title {
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .class-stat-value {
        color: #ffffff;
        font-size: 24px;
        line-height: 1;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .class-stat-caption {
        color: #aebbd0;
        font-size: 12px;
        margin-bottom: 3px;
    }

    .normal-text { color: #4dffb0; }
    .abnormal-text { color: #ff4d7d; }
    .cyan-text { color: #20d9ff; }
    .violet-text { color: #9d80ff; }

    .detection-title {
        margin-top: 22px;
    }

    .context-card {
        padding: 15px 16px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.12);
        background: linear-gradient(145deg, rgba(255,255,255,0.075), rgba(255,255,255,0.035));
        color: #c7d9ec;
        font-size: 12px;
        line-height: 1.65;
    }

    .samples-title {
        margin-top: 28px;
    }

    .section-description {
        color: #9fc2de;
        font-size: 12px;
        line-height: 1.55;
        margin: -3px 0 18px;
    }

    @media (max-width: 900px) {
        .hero { padding: 24px; }
        .hero-title { font-size: 36px; }
    }

    /* Technical assessment cards */
    .assessment-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 16px;
        margin-bottom: 8px;
    }

    .assessment-card {
        min-height: 330px;
        padding: 25px 27px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 18px 45px rgba(0,0,0,0.22);
        background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.025));
    }

    .assessment-normal {
        border-top: 4px solid #22c55e;
    }

    .assessment-abnormal {
        border-top: 4px solid #ff4d7d;
    }

    .assessment-label {
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 1.5px;
        color: #8eeaff;
        margin-bottom: 8px;
    }

    .assessment-normal .assessment-label {
        color: #5ee6a5;
    }

    .assessment-abnormal .assessment-label {
        color: #ff86a4;
    }

    .assessment-title {
        font-size: 23px;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 12px;
    }

    .assessment-card p,
    .assessment-card li,
    .action-card p,
    .note-card {
        color: #c6d5e8;
        font-size: 14px;
        line-height: 1.65;
    }

    .assessment-card ul {
        padding-left: 20px;
        margin: 12px 0;
    }

    .assessment-card li {
        margin-bottom: 7px;
    }

    .assessment-action {
        margin-top: 18px;
        padding: 13px 15px;
        border-radius: 12px;
        background: rgba(32,217,255,0.07);
        border: 1px solid rgba(32,217,255,0.16);
    }

    .action-card {
        min-height: 205px;
        padding: 21px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.11);
        background: linear-gradient(145deg, rgba(16,46,76,0.75), rgba(7,22,40,0.75));
        box-shadow: 0 14px 35px rgba(0,0,0,0.18);
    }

    .action-number {
        color: #20d9ff;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 1.5px;
    }

    .action-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 900;
        margin: 7px 0 8px;
    }

    .note-card {
        margin-top: 18px;
        padding: 16px 18px;
        border-radius: 14px;
        border-left: 4px solid #20d9ff;
        background: rgba(32,217,255,0.06);
    }

    .feature-compare-wrap {
        overflow-x: auto;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        background: rgba(7,24,39,0.82);
        box-shadow: 0 14px 35px rgba(0,0,0,0.18);
    }

    .feature-compare {
        width: 100%;
        border-collapse: collapse;
        color: #dcecff;
        font-size: 12px;
    }

    .feature-compare th {
        padding: 10px 12px;
        text-align: left;
        color: #9fc2de;
        font-weight: 800;
        background: rgba(255,255,255,0.055);
        border-bottom: 1px solid rgba(255,255,255,0.10);
    }

    .feature-compare td {
        padding: 8px 12px;
        border-bottom: 1px solid rgba(255,255,255,0.075);
    }

    .feature-compare tr:last-child td {
        border-bottom: none;
    }

    .feature-compare td:nth-child(4) {
        color: #7de9ff;
        font-weight: 800;
    }

    @media (max-width: 900px) {
        .assessment-grid {
            grid-template-columns: 1fr;
        }
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# FILE PATHS
# ============================================================

DATA_PATH = "data/features/all_runs_features.csv"
MODEL_PATH = "models/xgboost_model.pkl"
FEATURE_PATH = "models/feature_columns.txt"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


# ============================================================
# LOAD FEATURES
# ============================================================

@st.cache_data
def load_features():
    with open(FEATURE_PATH, "r") as f:
        return [line.strip() for line in f if line.strip()]


df = load_data()
model = load_model()
feature_columns = load_features()


# ============================================================
# BASIC VALUES
# ============================================================

total_samples = len(df)
normal_count = int((df["label"] == 0).sum())
abnormal_count = int((df["label"] == 1).sum())

abnormal_rate = (
    abnormal_count / total_samples * 100
    if total_samples > 0 else 0
)

try:
    X_all = df[feature_columns]
    y_all = df["label"]
    predictions_all = model.predict(X_all)
    accuracy = (predictions_all == y_all).mean() * 100
except Exception:
    accuracy = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📡 5G Monitor")

    st.markdown(
        """
        **Network Anomaly Detection**

        XGBoost-based telemetry analysis
        """
    )

    st.divider()

    st.markdown("### Dashboard")

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Telemetry Analysis",
            "Feature Importance",
            "Anomaly Detection",
            "Dataset"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Dataset Status")

    st.success("Dataset loaded")

    st.metric(
        "Telemetry Windows",
        total_samples
    )

    st.metric(
        "Abnormal Rate",
        f"{abnormal_rate:.1f}%"
    )

    st.divider()

    st.caption(
        "5G Network Telemetry Anomaly Detection & Classification\n"
        "Member 3 Streamlit Dashboard"
    )


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-kicker">5G NETWORK TELEMETRY • MACHINE LEARNING • SECURITY ANALYTICS</div>
    <div class="hero-title">5G Network Telemetry Anomaly Detection &amp; Classification</div>
    <div class="hero-subtitle">
        XGBoost-based classification of network telemetry windows using packet,
        protocol, signaling, and timing features.
    </div>
    <div class="hero-tags">
        <span class="hero-tag">TELEMETRY ANALYSIS</span>
        <span class="hero-tag">XGBOOST CLASSIFICATION</span>
        <span class="hero-tag">NORMAL / ABNORMAL</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    # ========================================================
    # NETWORK OVERVIEW
    # ========================================================
    st.markdown(
        '<div class="section-title">Network Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Summary of the collected 5G telemetry windows and their normal/abnormal classification distribution.'
        '</div>',
        unsafe_allow_html=True
    )

    overview_metrics = st.columns(4)

    with overview_metrics[0]:
        st.markdown(
            f'''<div class="overview-metric metric-total">
                <div class="overview-metric-label">TOTAL WINDOWS</div>
                <div class="overview-metric-value">{total_samples}</div>
            </div>''',
            unsafe_allow_html=True
        )

    with overview_metrics[1]:
        st.markdown(
            f'''<div class="overview-metric metric-normal">
                <div class="overview-metric-label">NORMAL WINDOWS</div>
                <div class="overview-metric-value">{normal_count}</div>
            </div>''',
            unsafe_allow_html=True
        )

    with overview_metrics[2]:
        st.markdown(
            f'''<div class="overview-metric metric-abnormal">
                <div class="overview-metric-label">ABNORMAL WINDOWS</div>
                <div class="overview-metric-value">{abnormal_count}</div>
            </div>''',
            unsafe_allow_html=True
        )

    with overview_metrics[3]:
        accuracy_text = f"{accuracy:.1f}%" if accuracy is not None else "N/A"
        st.markdown(
            f'''<div class="overview-metric metric-accuracy">
                <div class="overview-metric-label">DATASET-FIT ACCURACY</div>
                <div class="overview-metric-value">{accuracy_text}</div>
            </div>''',
            unsafe_allow_html=True
        )

    # ========================================================
    # TRAFFIC CLASSIFICATION + CLASS STATISTICS
    # ========================================================
    traffic_col, stats_col = st.columns([0.92, 1.08], gap="medium")

    with traffic_col:
        st.markdown(
            '<div class="section-title overview-subtitle">Traffic Classification</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(5.65, 4.75))
        fig.patch.set_facecolor("#071827")
        ax.set_facecolor("#071827")

        values = [normal_count, abnormal_count]
        labels = ["Normal", "Abnormal"]
        colors = ["#16c784", "#ff4d7d"]

        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            colors=colors,
            startangle=90,
            counterclock=False,
            autopct=lambda p: f"{p:.1f}%",
            pctdistance=0.69,
            labeldistance=1.08,
            wedgeprops=dict(width=0.30, edgecolor="#071827", linewidth=3),
            textprops=dict(color="#dcecff", fontsize=11, fontweight="bold")
        )

        for autotext in autotexts:
            autotext.set_color("#ffffff")
            autotext.set_fontsize(13)
            autotext.set_fontweight("bold")

        ax.text(
            0, 0.06, str(total_samples),
            ha="center", va="center",
            color="#ffffff", fontsize=25, fontweight="900"
        )
        ax.text(
            0, -0.14, "Telemetry Windows",
            ha="center", va="center",
            color="#aebbd0", fontsize=9.5
        )

        legend_labels = [
            f"Normal  •  {normal_count}",
            f"Abnormal  •  {abnormal_count}"
        ]
        ax.legend(
            wedges,
            legend_labels,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.08),
            ncol=2,
            frameon=False,
            labelcolor="#c9d8eb",
            fontsize=10
        )

        ax.set_title(
            "Normal vs Abnormal Telemetry",
            color="#ffffff",
            fontsize=18,
            fontweight="bold",
            pad=12
        )
        ax.set_aspect("equal")
        fig.tight_layout(pad=0.7)

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with stats_col:
        st.markdown(
            '<div class="section-title overview-subtitle">Class Statistics</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'''<div class="class-stat-block">
                <div class="class-stat-title normal-text">Normal traffic</div>
                <div class="class-stat-value">{normal_count}</div>
                <div class="class-stat-caption">telemetry windows</div>
            </div>''',
            unsafe_allow_html=True
        )

        st.markdown(
            f'''<div class="class-stat-block">
                <div class="class-stat-title abnormal-text">Abnormal traffic</div>
                <div class="class-stat-value">{abnormal_count}</div>
                <div class="class-stat-caption">telemetry windows</div>
            </div>''',
            unsafe_allow_html=True
        )

        st.markdown(
            f'''<div class="class-stat-block">
                <div class="class-stat-title cyan-text">Abnormal rate</div>
                <div class="class-stat-value">{abnormal_rate:.2f}%</div>
                <div class="class-stat-caption">of the dataset</div>
            </div>''',
            unsafe_allow_html=True
        )

        st.markdown(
            f'''<div class="class-stat-block">
                <div class="class-stat-title violet-text">Telemetry features</div>
                <div class="class-stat-value">{len(feature_columns)}</div>
                <div class="class-stat-caption">features supplied to XGBoost</div>
            </div>''',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title overview-subtitle detection-title">Detection Context</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '''<div class="context-card">
                The classifier uses a feature vector derived from packet volume,
                packet-length statistics, protocol counts, 5G signaling activity and
                packet timing. Classification should be interpreted together with
                the telemetry distribution and network logs.
            </div>''',
            unsafe_allow_html=True
        )

    # ========================================================
    # SAMPLES BY RUN
    # ========================================================
    st.markdown(
        '<div class="section-title samples-title">Samples by Run</div>',
        unsafe_allow_html=True
    )

    runs = list(df["run_id"].dropna().astype(str).unique())
    normal_by_run = []
    abnormal_by_run = []

    for run in runs:
        run_mask = df["run_id"].astype(str) == run
        normal_by_run.append(int((run_mask & (df["label"] == 0)).sum()))
        abnormal_by_run.append(int((run_mask & (df["label"] == 1)).sum()))

    x = np.arange(len(runs))
    width = 0.36

    fig, ax = plt.subplots(figsize=(12.2, 4.6))
    fig.patch.set_facecolor("#071827")
    ax.set_facecolor("#0b0f17")

    ax.bar(
        x - width / 2,
        abnormal_by_run,
        width,
        label="Abnormal",
        color="#7cc0ee"
    )
    ax.bar(
        x + width / 2,
        normal_by_run,
        width,
        label="Normal",
        color="#0877ce"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(runs, rotation=90, color="#dcecff", fontsize=9)
    ax.tick_params(axis="y", colors="#dcecff", labelsize=9)
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", color="#7f91aa", alpha=0.22, linewidth=0.8)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.02, -0.24),
        ncol=2,
        frameon=False,
        labelcolor="#dcecff",
        fontsize=9
    )

    fig.tight_layout(pad=1.1)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # ========================================================
    # NETWORK ASSESSMENT
    # ========================================================
    st.markdown(
        '<div class="section-title assessment-section-title">Network Assessment</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Interpretation of the telemetry classes and practical actions for investigating abnormal 5G traffic.'
        '</div>',
        unsafe_allow_html=True
    )

    assessment_features = [
        "packet_count",
        "mean_packet_length",
        "http2_count",
        "pfcp_count",
        "ngap_count",
        "initial_ue_count",
        "uplink_nas_count",
        "mean_interarrival_ms"
    ]
    assessment_features = [f for f in assessment_features if f in df.columns]
    class_means = df.groupby("label")[assessment_features].mean() if assessment_features else pd.DataFrame()

    def mean_value(label_value, feature):
        try:
            return float(class_means.loc[label_value, feature])
        except Exception:
            return None

    packet_normal = mean_value(0, "packet_count")
    packet_abnormal = mean_value(1, "packet_count")
    iat_normal = mean_value(0, "mean_interarrival_ms")
    iat_abnormal = mean_value(1, "mean_interarrival_ms")

    packet_statement = (
        f"Packet volume is substantially higher in abnormal windows ({packet_abnormal:.2f} mean vs {packet_normal:.2f} normal)."
        if packet_normal is not None and packet_abnormal is not None
        else "Packet-volume statistics provide an important separation signal."
    )

    iat_statement = (
        "Inter-arrival timing is more compressed in abnormal windows."
        if iat_normal is not None and iat_abnormal is not None and iat_abnormal < iat_normal
        else "Inter-arrival timing is included as a traffic-density signal when available."
    )

    normal_pct = (normal_count / total_samples * 100) if total_samples else 0
    abnormal_pct = (abnormal_count / total_samples * 100) if total_samples else 0

    assessment_cols = st.columns(2, gap="small")

    with assessment_cols[0]:
        st.markdown(
            f'''<div class="assessment-card assessment-normal">
                <div class="assessment-label">NORMAL TRAFFIC</div>
                <div class="assessment-title">Baseline-consistent telemetry</div>
                <p>This dataset contains <b>{normal_count}</b> normal telemetry windows ({normal_pct:.1f}% of the dataset).</p>
                <ul>
                    <li>Observed feature values remain closer to the learned normal distribution.</li>
                    <li>Protocol and 5G signaling activity is comparatively less pronounced.</li>
                    <li>{iat_statement}</li>
                    <li>The overall feature profile is closer to the learned normal class.</li>
                </ul>
                <div class="assessment-action"><b>Operational meaning:</b> continue monitoring. No immediate anomaly response is indicated when the model probability remains low.</div>
            </div>''',
            unsafe_allow_html=True
        )

    with assessment_cols[1]:
        st.markdown(
            f'''<div class="assessment-card assessment-abnormal">
                <div class="assessment-label">ABNORMAL TRAFFIC</div>
                <div class="assessment-title">Deviation from the learned baseline</div>
                <p>This dataset contains <b>{abnormal_count}</b> abnormal telemetry windows ({abnormal_pct:.1f}% of the dataset).</p>
                <ul>
                    <li>{packet_statement}</li>
                    <li>HTTP/2, PFCP and NGAP activity can increase the separation between the classes.</li>
                    <li>UE registration and NAS signaling activity may be more pronounced.</li>
                    <li>Shorter inter-arrival intervals indicate more concentrated traffic when supported by the data.</li>
                </ul>
                <div class="assessment-action"><b>Operational meaning:</b> verify whether the increase is legitimate load or a signaling anomaly before taking corrective action.</div>
            </div>''',
            unsafe_allow_html=True
        )

    # ========================================================
    # WHY THE MODEL SEPARATES THE CLASSES
    # ========================================================
    st.markdown(
        '<div class="section-title">Why the Model Separates the Classes</div>',
        unsafe_allow_html=True
    )

    feature_explanation = [
        "packet_count",
        "mean_packet_length",
        "http2_count",
        "pfcp_count",
        "ngap_count",
        "initial_ue_count",
        "uplink_nas_count",
        "pdu_setup_req_count",
        "pdu_setup_resp_count",
        "ue_release_count",
        "mean_interarrival_ms"
    ]
    feature_explanation = [f for f in feature_explanation if f in df.columns]

    comparison = df.groupby("label")[feature_explanation].mean().T if feature_explanation else pd.DataFrame()

    rows = []
    for feature in feature_explanation:
        normal_mean = float(comparison.loc[feature, 0]) if 0 in comparison.columns else np.nan
        abnormal_mean = float(comparison.loc[feature, 1]) if 1 in comparison.columns else np.nan

        if np.isfinite(normal_mean) and np.isfinite(abnormal_mean) and normal_mean != 0:
            change = (abnormal_mean - normal_mean) / abs(normal_mean) * 100
            change_text = f"{change:+.1f}%"
        else:
            change_text = "N/A"

        rows.append((
            feature,
            f"{normal_mean:.2f}" if np.isfinite(normal_mean) else "N/A",
            f"{abnormal_mean:.2f}" if np.isfinite(abnormal_mean) else "N/A",
            change_text
        ))

    if rows:
        table_html = '''<div class="feature-compare-wrap"><table class="feature-compare"><thead><tr><th>Telemetry Feature</th><th>Normal Mean</th><th>Abnormal Mean</th><th>Abnormal vs Normal</th></tr></thead><tbody>'''
        for feature, normal_mean, abnormal_mean, change_text in rows:
            table_html += f"<tr><td>{feature}</td><td>{normal_mean}</td><td>{abnormal_mean}</td><td>{change_text}</td></tr>"
        table_html += "</tbody></table></div>"
        st.markdown(table_html, unsafe_allow_html=True)

    # ========================================================
    # ABNORMAL TRAFFIC: INVESTIGATION & REMEDIATION
    # ========================================================
    st.markdown(
        '<div class="section-title">Abnormal Traffic: Investigation &amp; Remediation</div>',
        unsafe_allow_html=True
    )

    action_cols = st.columns(3, gap="small")

    with action_cols[0]:
        st.markdown(
            '''<div class="action-card">
                <div class="action-number">01</div>
                <div class="action-title">Validate the event</div>
                <p>Check the corresponding PCAP, run ID, timestamp window and core-network logs. Confirm that the traffic increase is real and not an extraction or measurement issue.</p>
            </div>''',
            unsafe_allow_html=True
        )

    with action_cols[1]:
        st.markdown(
            '''<div class="action-card">
                <div class="action-number">02</div>
                <div class="action-title">Identify the source</div>
                <p>Examine signaling activity around registration, NAS, NGAP, HTTP/2 and PFCP. Look for repeated requests, unusual bursts, unexpected UE behaviour or a sudden increase from one source.</p>
            </div>''',
            unsafe_allow_html=True
        )

    with action_cols[2]:
        st.markdown(
            '''<div class="action-card">
                <div class="action-number">03</div>
                <div class="action-title">Apply the response</div>
                <p>If the event is confirmed as malicious or harmful, apply rate limiting, source isolation or traffic filtering where appropriate, then continue monitoring the telemetry trend.</p>
            </div>''',
            unsafe_allow_html=True
        )

    st.markdown(
        '''<div class="note-card"><b>Interpretation note:</b> An “Abnormal” prediction indicates that the telemetry window differs from the learned normal pattern. It does not by itself prove an attack. Use packet captures, network logs and model probability to determine the operational cause.</div>''',
        unsafe_allow_html=True
    )

# ============================================================
# TELEMETRY ANALYSIS
# ============================================================

elif page == "Telemetry Analysis":

    st.markdown(
        '<div class="section-title">5G Telemetry Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Comparison of telemetry behaviour between normal and abnormal traffic.'
        '</div>',
        unsafe_allow_html=True
    )

    comparison_features = [
        "packet_count",
        "mean_packet_length",
        "sctp_count",
        "http2_count",
        "pfcp_count",
        "ngap_count",
        "initial_ue_count",
        "uplink_nas_count",
        "pdu_setup_req_count",
        "pdu_setup_resp_count",
        "ue_release_count",
        "mean_interarrival_ms"
    ]

    available_features = [
        f for f in comparison_features
        if f in df.columns
    ]

    summary = df.groupby("label")[available_features].mean().T

    summary = summary.rename(
        columns={
            0: "Normal",
            1: "Abnormal"
        }
    )

    if "Normal" in summary.columns and "Abnormal" in summary.columns:
        summary["Difference"] = (
            summary["Abnormal"] - summary["Normal"]
        )

    st.dataframe(
        summary.round(2),
        use_container_width=True
    )

    st.markdown(
        '<div class="section-title">Select a Telemetry Feature</div>',
        unsafe_allow_html=True
    )

    selected_feature = st.selectbox(
        "Feature",
        available_features
    )

    normal_values = df[df["label"] == 0][selected_feature]
    abnormal_values = df[df["label"] == 1][selected_feature]

    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    fig.patch.set_facecolor("#071827")
    ax.set_facecolor("#071827")

    bp = ax.boxplot(
        [normal_values, abnormal_values],
        positions=[1, 2],
        widths=0.48,
        patch_artist=True,
        tick_labels=["Normal", "Abnormal"],
        showmeans=True,
        meanprops=dict(
            marker="D",
            markerfacecolor="#ffffff",
            markeredgecolor="#20d9ff",
            markersize=5
        ),
        flierprops=dict(
            marker="o",
            markerfacecolor="#20d9ff",
            markeredgecolor="#ffffff",
            markersize=5,
            alpha=0.9
        ),
        medianprops=dict(
            color="#ffffff",
            linewidth=2.5
        ),
        whiskerprops=dict(
            color="#7dd3fc",
            linewidth=1.8
        ),
        capprops=dict(
            color="#7dd3fc",
            linewidth=1.8
        )
    )

    bp["boxes"][0].set_facecolor("#16c784")
    bp["boxes"][1].set_facecolor("#ff4d7d")

    for box in bp["boxes"]:
        box.set_alpha(0.72)
        box.set_edgecolor("#dff8ff")
        box.set_linewidth(1.5)

    ax.set_title(
        f"{selected_feature}: Normal vs Abnormal",
        color="#ffffff",
        fontsize=16,
        fontweight="bold",
        pad=14
    )

    ax.set_ylabel(
        selected_feature,
        color="#b9dff0",
        fontsize=11
    )

    ax.set_xticks([1, 2])
    ax.set_xticklabels(
        ["Normal", "Abnormal"],
        color="#dff8ff",
        fontsize=11,
        fontweight="bold"
    )

    ax.tick_params(
        axis="y",
        colors="#b9dff0",
        labelsize=10
    )

    ax.grid(
        axis="y",
        alpha=0.16,
        color="#7dd3fc",
        linewidth=0.8
    )

    for spine in ax.spines.values():
        spine.set_color("#21465d")
        spine.set_linewidth(1.2)

    # Add a little breathing room so the highest whisker/outlier is never
    # pressed against the top edge of the chart.
    all_values = np.concatenate([
        normal_values.dropna().to_numpy(),
        abnormal_values.dropna().to_numpy()
    ])

    if len(all_values) > 0:
        ymin = float(np.nanmin(all_values))
        ymax = float(np.nanmax(all_values))
        pad = max((ymax - ymin) * 0.08, 1.0)
        ax.set_ylim(ymin - pad, ymax + pad)

    fig.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

elif page == "Feature Importance":

    st.markdown(
        '<div class="section-title">XGBoost Feature Importance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Features ranked according to their contribution to the trained model.'
        '</div>',
        unsafe_allow_html=True
    )

    importance = model.feature_importances_

    importance_df = pd.DataFrame({
        "Feature": feature_columns,
        "Importance": importance
    })

    importance_df = importance_df.sort_values(
        "Importance",
        ascending=False
    )

    top_features = importance_df.head(10)

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#071827")
    ax.set_facecolor("#071827")

    plot_data = top_features.sort_values(
        "Importance"
    )

    bars = ax.barh(
        plot_data["Feature"],
        plot_data["Importance"],
        color="#00cfff"
    )

    for bar in bars:
        bar.set_alpha(0.82)

    ax.set_xlabel(
        "Importance",
        color="#b9dff0"
    )

    ax.set_title(
        "Top 10 XGBoost Features",
        color="#ffffff",
        fontweight="bold",
        pad=14
    )

    ax.tick_params(
        colors="#b9dff0"
    )

    for spine in ax.spines.values():
        spine.set_color("#21465d")

    ax.grid(
        axis="x",
        alpha=0.14,
        color="#7dd3fc"
    )

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.dataframe(
        importance_df,
        use_container_width=True
    )


# ============================================================
# ANOMALY DETECTION
# ============================================================

elif page == "Anomaly Detection":

    st.markdown(
        '<div class="section-title">Anomaly Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Use the trained XGBoost model to classify an existing telemetry window.'
        '</div>',
        unsafe_allow_html=True
    )

    sample_index = st.slider(
        "Select telemetry window",
        min_value=0,
        max_value=len(df) - 1,
        value=0
    )

    sample = df.iloc[[sample_index]]

    st.markdown("### Selected Telemetry Window")

    display_columns = [
        c for c in [
            "run_id",
            "window",
            "packet_count",
            "mean_packet_length",
            "http2_count",
            "ngap_count",
            "initial_ue_count",
            "uplink_nas_count",
            "label"
        ]
        if c in sample.columns
    ]

    st.dataframe(
        sample[display_columns],
        use_container_width=True
    )

    if st.button(
        "🔍 Analyze Selected Window",
        use_container_width=True
    ):

        X_sample = sample[feature_columns]

        prediction = model.predict(X_sample)[0]

        probability = model.predict_proba(X_sample)[0]

        abnormal_probability = probability[1]

        actual_label = sample["label"].iloc[0]

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            if prediction == 1:

                st.markdown(
                    """
                    <div class="prediction-abnormal">
                        <div class="prediction-title">
                            🚨 ABNORMAL
                        </div>
                        <p>Potential anomalous network traffic detected.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="prediction-normal">
                        <div class="prediction-title">
                            ✓ NORMAL
                        </div>
                        <p>No anomaly detected by the model.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col2:

            st.metric(
                "Abnormal Probability",
                f"{abnormal_probability:.2%}"
            )

            st.metric(
                "Actual Label",
                "Abnormal" if actual_label == 1 else "Normal"
            )


# ============================================================
# DATASET
# ============================================================

elif page == "Dataset":

    st.markdown(
        '<div class="section-title">Telemetry Dataset</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Complete extracted telemetry feature dataset.'
        '</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=600
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <b>5G Network Telemetry Anomaly Detection &amp; Classification</b><br>
        Telemetry-based anomaly classification using XGBoost<br>
        Network Security &amp; Analytics Dashboard
    </div>
    """,
    unsafe_allow_html=True
)
