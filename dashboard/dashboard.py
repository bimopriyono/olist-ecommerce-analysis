from pathlib import Path
<<<<<<< HEAD
import html

=======
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# 1. KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Olist | E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# 2. MEMUAT DATA
# =========================================================

@st.cache_data
def load_data():
    main = pd.read_csv(BASE_DIR / "main_data.csv")
    category = pd.read_csv(BASE_DIR / "category_items.csv")
    rfm = pd.read_csv(BASE_DIR / "rfm_data.csv")

    date_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for col in date_columns:
        if col in main.columns:
            main[col] = pd.to_datetime(main[col], errors="coerce")

    if "order_purchase_timestamp" in category.columns:
        category["order_purchase_timestamp"] = pd.to_datetime(
            category["order_purchase_timestamp"], errors="coerce"
        )

    if "last_purchase" in rfm.columns:
        rfm["last_purchase"] = pd.to_datetime(
            rfm["last_purchase"], errors="coerce"
        )

    if "is_late" in main.columns:
        main["is_late"] = main["is_late"].fillna(False).astype(bool)

    return main, category, rfm


try:
    main_df, category_df, rfm_df = load_data()

except FileNotFoundError:
    st.error(
        "File data dashboard tidak ditemukan. Pastikan "
        "main_data.csv, category_items.csv, dan rfm_data.csv "
        "berada di folder dashboard."
    )
    st.stop()


# =========================================================
# 3. CUSTOM CSS
# =========================================================


st.markdown("""
<style>

<<<<<<< HEAD
/* ---------- WARNA DASAR ---------- */

:root {
    --navy: #17243F;
    --navy-light: #243454;
    --purple: #5145CD;
    --purple-light: #756BFA;
    --background: #EAF0FA;
    --card: #FFFFFF;
    --text: #172554;
    --muted: #64748B;
    --border: #DCE5F2;
=======
/* =====================================================
   1. BACKGROUND UTAMA
===================================================== */

.stApp {
    background-color: #E8EDF7;
    color: #1E293B;
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
}

.stApp,
[data-testid="stAppViewContainer"] {
<<<<<<< HEAD
    background: var(--background);
    color: var(--text);
=======
    background-color: #E8EDF7;
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1600px;
    padding-top: 1.8rem;
    padding-bottom: 2.5rem;
}

<<<<<<< HEAD
/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #17243F 0%,
        #1B2948 100%
    );
=======

/* =====================================================
   2. SIDEBAR NAVY
===================================================== */

section[data-testid="stSidebar"] {
    background-color: #17243F;
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
    border-right: 1px solid #263653;
}

section[data-testid="stSidebar"] > div {
    padding: 1.7rem 1.1rem;
}

<<<<<<< HEAD
/* Teks sidebar */
section[data-testid="stSidebar"] * {
    color: #EAF0FF;
=======
/* Semua teks sidebar */
section[data-testid="stSidebar"] * {
    color: #E8EEF9;
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
}

/* Judul sidebar */
section[data-testid="stSidebar"] h1 {
    color: #FFFFFF !important;
<<<<<<< HEAD
    font-size: 1.55rem !important;
    font-weight: 800 !important;
}

/* Deskripsi sidebar */
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #B9C7E0 !important;
}

/* Garis pemisah sidebar */
section[data-testid="stSidebar"] hr {
    border-color: #43516D;
    margin-top: 1.2rem;
    margin-bottom: 1.2rem;
}

/* Label navigasi */
=======
    font-size: 1.55rem;
    font-weight: 800;
}

/* Subjudul sidebar */
section[data-testid="stSidebar"] p {
    color: #B8C5DC !important;
}

/* Judul bagian navigasi dan filter */
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

/* Label navigasi */
section[data-testid="stSidebar"] label {
    color: #E8EEF9 !important;
    font-weight: 600;
}

/* Jarak antar pilihan navigasi */
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 7px;
}

/* Tampilan pilihan navigasi */
section[data-testid="stSidebar"] div[role="radiogroup"] label {
<<<<<<< HEAD
    background: transparent;
    border: 1px solid transparent;
=======
    background-color: #202F4D;
    border: 1px solid #344563;
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
    border-radius: 10px;
    padding: 10px 12px;
    transition: all 0.2s ease;
}

/* Efek hover navigasi */
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
<<<<<<< HEAD
    background: #293A61;
    border-color: #5366A0;
}

/* Teks navigasi */
section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: #E8EEFC !important;
    font-weight: 550;
}
=======
    background-color: #344477;
    border-color: #7774E8;
}

/* Warna teks navigasi */
section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: #E8EEF9 !important;
}

/* Garis sidebar */
section[data-testid="stSidebar"] hr {
    border-color: #3B4A65;
}

/* Caption sidebar */
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #AAB9D1 !important;
}


/* =====================================================
   3. FILTER SIDEBAR
===================================================== */

/* Kotak tanggal */
section[data-testid="stSidebar"] input {
    background-color: #263653 !important;
    color: #FFFFFF !important;
    border: 1px solid #526482 !important;
    border-radius: 8px !important;
}

/* Kotak multiselect */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #263653 !important;
    border-color: #526482 !important;
}

/* Teks pilihan multiselect */
section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #FFFFFF !important;
}

/* Ikon filter */
section[data-testid="stSidebar"] svg {
    color: #DCE5F5;
}


/* =====================================================
   4. TEKS UTAMA
===================================================== */
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6

/* Navigasi aktif */
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(
        100deg,
        #5145CD,
        #6558E8
    );
    border-color: #766CF1;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
}

/* Radio button */
section[data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
    color: #F8FAFF !important;
}

/* ---------- FILTER SIDEBAR ---------- */

section[data-testid="stSidebar"] label {
    color: #E5ECFA !important;
    font-weight: 550;
}

section[data-testid="stSidebar"] input {
    background: #202F4D !important;
    color: #FFFFFF !important;
    border-color: #536482 !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #202F4D !important;
    border-color: #536482 !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: #E8EDFF !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #26365B !important;
}

/* ---------- AREA KONTEN ---------- */

h1, h2, h3, h4 {
    color: #172554 !important;
    font-weight: 750 !important;
}

p {
<<<<<<< HEAD
    color: #40516F;
=======
    color: #334155;
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
}

[data-testid="stCaptionContainer"] {
    color: #64748B;
}

<<<<<<< HEAD
/* ---------- HEADER DASHBOARD ---------- */

.main-header {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        115deg,
        #F7F8FF 0%,
        #E8ECFF 55%,
        #DDE5FC 100%
    );
    border: 1px solid #D8E0F4;
    border-radius: 18px;
    padding: 29px 34px;
    margin-bottom: 20px;
    box-shadow: 0 4px 14px rgba(32, 48, 89, 0.06);
}

.header-content {
    position: relative;
    z-index: 2;
}

.header-line {
    width: 65px;
    height: 7px;
    background: linear-gradient(
        90deg,
        #5145CD,
        #8278FF
    );
    border-radius: 20px;
    margin-bottom: 12px;
}

.main-header h1 {
    color: #111B49 !important;
    font-size: 2.15rem !important;
    font-weight: 850 !important;
    line-height: 1.2;
    margin: 0;
}

.main-header p {
    color: #50648C !important;
    font-size: 1.02rem;
    margin: 10px 0 0 0;
}

.header-decoration {
    position: absolute;
    right: 35px;
    top: 18px;
    font-size: 5.2rem;
    opacity: 0.18;
}

/* ---------- KARTU KPI ---------- */

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #DCE5F2;
    border-radius: 15px;
    padding: 17px 18px;
    min-height: 150px;
    height: 100%;
    box-shadow: 0 3px 10px rgba(23, 37, 84, 0.045);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 7px 18px rgba(23, 37, 84, 0.09);
}

.kpi-top {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 10px;
}

.kpi-icon {
    width: 46px;
    height: 46px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.45rem;
}

.icon-purple {
    background: #EEEAFE;
}

.icon-blue {
    background: #E4EDFF;
}

.icon-green {
    background: #DDF8EC;
}

.icon-orange {
    background: #FFF0D7;
}

.kpi-label {
    color: #455779;
    font-size: 0.91rem;
    font-weight: 650;
}

.kpi-value {
    color: #111B49;
=======

/* =====================================================
   5. HEADER HALAMAN
===================================================== */

.main-header {
    background: linear-gradient(
        120deg,
        #E1E7FF 0%,
        #EEF1FF 55%,
        #E6ECFA 100%
    );
    border: 1px solid #D4DDF3;
    padding: 30px 34px;
    border-radius: 17px;
    margin-bottom: 25px;
    box-shadow: 0 4px 14px rgba(30, 41, 59, 0.06);
    position: relative;
    overflow: hidden;
}

.main-header h1 {
    color: #172554 !important;
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    line-height: 1.3;
}

.main-header p {
    color: #475B80 !important;
    margin-top: 10px;
    margin-bottom: 0;
    font-size: 0.98rem;
}


/* =====================================================
   6. KARTU KPI
===================================================== */

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE3EF;
    border-radius: 14px;
    padding: 21px 19px;
    min-height: 125px;
    box-shadow: 0 3px 10px rgba(23, 37, 84, 0.05);
    transition: all 0.2s ease;
}

/* Hover kartu */
[data-testid="stMetric"]:hover {
    border-color: #A5B4FC;
    box-shadow: 0 5px 15px rgba(49, 46, 129, 0.10);
}

/* Label KPI */
[data-testid="stMetricLabel"] {
    color: #53627D !important;
    font-size: 0.9rem;
    font-weight: 650;
}

[data-testid="stMetricLabel"] p {
    color: #53627D !important;
}

/* Angka KPI */
[data-testid="stMetricValue"] {
    color: #172554 !important;
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
    font-size: 1.65rem;
    font-weight: 850;
    line-height: 1.2;
    overflow-wrap: anywhere;
}

<<<<<<< HEAD
.kpi-description {
    color: #71809B;
    font-size: 0.82rem;
    margin-top: 7px;
    line-height: 1.4;
}

/* ---------- KARTU GRAFIK ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #DCE5F2;
    border-radius: 15px;
    box-shadow: 0 3px 10px rgba(23, 37, 84, 0.04);
}

.chart-heading {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 8px;
}

.chart-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 43px;
    height: 43px;
    border-radius: 12px;
    background: #ECEBFF;
    color: #5145CD;
    font-size: 1.35rem;
}

.chart-heading h3 {
    color: #172554 !important;
    font-size: 1.15rem !important;
    font-weight: 750 !important;
    margin: 0;
}

/* ---------- PLOTLY ---------- */

[data-testid="stPlotlyChart"] {
    background: transparent;
}

.js-plotly-plot .plotly .main-svg {
    font-family: Arial, sans-serif;
}

/* ---------- TABEL ---------- */

[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border: 1px solid #DCE5F2;
=======
/* Delta KPI */
[data-testid="stMetricDelta"] {
    color: #475569 !important;
}


/* =====================================================
   7. GRAFIK
===================================================== */

[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE3EF;
    border-radius: 14px;
    padding: 10px;
    box-shadow: 0 3px 10px rgba(23, 37, 84, 0.04);
}


/* =====================================================
   8. TABEL
===================================================== */

[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE3EF;
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
    border-radius: 12px;
    overflow: hidden;
}

<<<<<<< HEAD
/* ---------- ALERT DAN TOMBOL ---------- */

[data-testid="stAlert"] {
    border-radius: 11px;
}
=======

/* =====================================================
   9. TOMBOL DAN ALERT
===================================================== */
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6

.stButton button {
    border-radius: 9px;
    font-weight: 650;
}

<<<<<<< HEAD
/* ---------- FOOTER ---------- */

.dashboard-footer {
    text-align: center;
    color: #8290A8;
    font-size: 0.8rem;
    padding: 25px 10px 5px;
}

/* ---------- RESPONSIVE ---------- */
=======
[data-testid="stAlert"] {
    border-radius: 10px;
}


/* =====================================================
   10. GARIS PEMISAH
===================================================== */

hr {
    border-color: #D5DDEC;
}


/* =====================================================
   11. RESPONSIVE
===================================================== */
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6

@media (max-width: 768px) {

    .block-container {
        padding: 1rem 1rem 2rem;
    }

    .main-header {
        padding: 22px;
    }

    .main-header h1 {
        font-size: 1.55rem !important;
    }

    .header-decoration {
        display: none;
    }

    .kpi-card {
        min-height: 130px;
    }

    .kpi-value {
        font-size: 1.35rem;
    }

}

</style>
""", unsafe_allow_html=True)



# =========================================================
# 4. FUNGSI BANTUAN
# =========================================================

def format_brl(value):
    return f"R$ {value:,.2f}"



def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="main-header">
            <div class="header-content">
                <div class="header-line"></div>
                <h1>{html.escape(title)}</h1>
                <p>{html.escape(subtitle)}</p>
            </div>
            <div class="header-decoration">🛒</div>
        </div>
        """,
        unsafe_allow_html=True
    )


<<<<<<< HEAD
def kpi_card(icon, label, value, description, icon_class):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-icon {icon_class}">{icon}</div>
                <div class="kpi-label">{html.escape(str(label))}</div>
            </div>
            <div class="kpi-value">{html.escape(str(value))}</div>
            <div class="kpi-description">
                {html.escape(str(description))}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def chart_heading(icon, title):
    st.markdown(
        f"""
        <div class="chart-heading">
            <div class="chart-icon">{icon}</div>
            <h3>{html.escape(title)}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


def style_chart(fig, height=390):
=======

def style_chart(fig, height=400):
>>>>>>> e8758c7d9bf0a819353c326c00a5221d26931ab6
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            color="#405579",
            size=12
        ),
        title_font=dict(
            color="#172554",
            size=17
        ),
        margin=dict(
            l=35,
            r=20,
            t=25,
            b=35
        ),
        height=height,
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_color="#172554",
            bordercolor="#DCE5F2"
        ),
        legend=dict(
            font=dict(color="#536785"),
            bgcolor="rgba(255,255,255,0)"
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E8EDF6",
        zeroline=False,
        linecolor="#DCE5F2",
        tickfont=dict(color="#536785")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E8EDF6",
        zeroline=False,
        linecolor="#DCE5F2",
        tickfont=dict(color="#536785")
    )

    return fig


def add_overview_metrics(data):
    revenue = data["revenue"].fillna(0).sum()
    order_count = data["order_id"].nunique()
    customer_count = data["customer_unique_id"].nunique()
    aov = revenue / order_count if order_count else 0

    cols = st.columns(4)

    with cols[0]:
        kpi_card(
            "🪙", "Total Revenue", format_brl(revenue),
            "Total pendapatan dari pesanan delivered", "icon-purple"
        )

    with cols[1]:
        kpi_card(
            "🛒", "Total Orders", f"{order_count:,}",
            "Jumlah pesanan delivered", "icon-blue"
        )

    with cols[2]:
        kpi_card(
            "👥", "Unique Customers", f"{customer_count:,}",
            "Jumlah pelanggan unik", "icon-green"
        )

    with cols[3]:
        kpi_card(
            "🏷️", "Average Order Value", format_brl(aov),
            "Rata-rata nilai pesanan", "icon-orange"
        )


def add_metrics(items):
    cols = st.columns(len(items))

    for col, item in zip(cols, items):
        with col:
            kpi_card(*item)


# =========================================================
# 5. SIDEBAR DAN FILTER
# =========================================================

st.sidebar.markdown(
    """
    <div style="padding: 5px 0 12px;">
        <div style="font-size: 1.65rem; font-weight: 850; color: white;">
            🛍️ Olist Analytics
        </div>
        <div style="font-size: 0.9rem; color: #B9C7E0; margin-top: 7px;">
            E-Commerce Business Intelligence
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

page_options = [
    "📊  Overview",
    "👤  Customer Analytics",
    "🚚  Delivery Analytics",
    "⬡  Product Analytics"
]

page_selected = st.sidebar.radio(
    "NAVIGASI",
    page_options,
    label_visibility="visible"
)

page_map = {
    "📊  Overview": "Overview",
    "👤  Customer Analytics": "Customer Analytics",
    "🚚  Delivery Analytics": "Delivery Analytics",
    "⬡  Product Analytics": "Product Analytics"
}

page = page_map[page_selected]

st.sidebar.divider()
st.sidebar.subheader("FILTER DATA")

valid_dates = main_df["order_purchase_timestamp"].dropna()

if valid_dates.empty:
    st.error("Tidak ada tanggal transaksi yang valid.")
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

date_range = st.sidebar.date_input(
    "📅 Periode Transaksi",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

states = sorted(
    main_df["customer_state"].dropna().unique().tolist()
)

selected_states = st.sidebar.multiselect(
    "📍 Wilayah Pelanggan",
    options=states,
    default=states
)


# =========================================================
# 6. FILTER DATA
# =========================================================

filtered_main = main_df[
    main_df["order_purchase_timestamp"].dt.date.between(
        start_date, end_date
    )
    & main_df["customer_state"].isin(selected_states)
].copy()

filtered_category = category_df[
    category_df["order_purchase_timestamp"].dt.date.between(
        start_date, end_date
    )
    & category_df["customer_state"].isin(selected_states)
].copy()

filtered_rfm = rfm_df[
    rfm_df["customer_state"].isin(selected_states)
].copy()

delivered = filtered_main[
    filtered_main["order_status"].eq("delivered")
].copy()


# =========================================================
# 7. OVERVIEW
# =========================================================

if page == "Overview":

    page_header(
        "E-Commerce Business Overview",
        "Ringkasan performa penjualan Olist berdasarkan pesanan yang telah delivered."
    )

    add_overview_metrics(delivered)

    if delivered.empty:
        st.warning("Tidak ada pesanan delivered pada filter yang dipilih.")
        st.stop()

    st.write("")

    monthly = (
        delivered.assign(
            month=delivered[
                "order_purchase_timestamp"
            ].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("month", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique")
        )
    )

    left, right = st.columns(2, gap="medium")

    with left:
        with st.container(border=True):
            chart_heading("📊", "Tren Pendapatan Bulanan")

            fig = px.area(
                monthly,
                x="month",
                y="revenue",
                markers=True,
                labels={
                    "month": "Bulan",
                    "revenue": "Pendapatan (BRL)"
                },
                color_discrete_sequence=["#5145CD"]
            )

            fig.update_traces(
                line=dict(width=3, color="#5145CD"),
                marker=dict(size=7, color="#5145CD"),
                fillcolor="rgba(81,69,205,0.12)"
            )

            style_chart(fig, 390)
            st.plotly_chart(fig, use_container_width=True)

    with right:
        with st.container(border=True):
            chart_heading("🛒", "Jumlah Pesanan Bulanan")

            fig = px.bar(
                monthly,
                x="month",
                y="orders",
                labels={
                    "month": "Bulan",
                    "orders": "Jumlah Pesanan"
                },
                color_discrete_sequence=["#7167F0"]
            )

            fig.update_traces(
                marker_line_width=0,
                opacity=0.95
            )

            style_chart(fig, 390)
            st.plotly_chart(fig, use_container_width=True)

    st.write("")

    with st.container(border=True):
        chart_heading("🚚", "Distribusi Status Pesanan")

        status = (
            filtered_main["order_status"]
            .value_counts()
            .rename_axis("status")
            .reset_index(name="orders")
        )

        status_colors = {
            "delivered": "#2DBE83",
            "shipped": "#4285F4",
            "invoiced": "#F5B82E",
            "processing": "#8257E5",
            "canceled": "#EF5368",
            "unavailable": "#A3ADBD",
            "approved": "#27A6A1",
            "created": "#64748B"
        }

        fig = px.pie(
            status,
            names="status",
            values="orders",
            hole=0.55,
            color="status",
            color_discrete_map=status_colors
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#FFFFFF", width=2))
        )

        style_chart(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Revenue dihitung dari penjumlahan harga produk (price) "
        "pada pesanan berstatus delivered. Biaya pengiriman "
        "(freight_value) tidak dimasukkan ke dalam revenue produk."
    )


# =========================================================
# 8. CUSTOMER ANALYTICS - RFM
# =========================================================

elif page == "Customer Analytics":

    page_header(
        "Customer Analytics",
        "Analisis karakteristik dan segmentasi pelanggan menggunakan RFM."
    )

    st.caption(
        "RFM dihitung berdasarkan seluruh periode transaksi delivered "
        "yang tersedia. Filter wilayah diterapkan pada pelanggan, "
        "sedangkan filter tanggal tidak menghitung ulang skor RFM."
    )

    if filtered_rfm.empty:
        st.warning("Tidak ada pelanggan pada wilayah yang dipilih.")
        st.stop()

    total_customers = filtered_rfm["customer_unique_id"].nunique()
    total_monetary = filtered_rfm["monetary"].sum()
    avg_frequency = filtered_rfm["frequency"].mean()
    avg_recency = filtered_rfm["recency"].mean()

    add_metrics([
        ("👥", "Total Pelanggan", f"{total_customers:,}",
         "Jumlah pelanggan unik", "icon-purple"),
        ("💰", "Total Monetary", format_brl(total_monetary),
         "Total nilai pembelian", "icon-green"),
        ("🛍️", "Rata-rata Frequency", f"{avg_frequency:.2f}",
         "Rata-rata jumlah transaksi", "icon-blue"),
        ("📅", "Rata-rata Recency", f"{avg_recency:.1f} hari",
         "Jarak sejak pembelian terakhir", "icon-orange")
    ])

    segment_order = [
        "Champions",
        "Loyal Customers",
        "Potential Loyalists",
        "Needs Attention",
        "At Risk",
        "Hibernating"
    ]

    summary = (
        filtered_rfm.groupby("segment", as_index=False)
        .agg(
            customers=("customer_unique_id", "nunique"),
            monetary=("monetary", "sum"),
            avg_recency=("recency", "mean"),
            avg_frequency=("frequency", "mean")
        )
    )

    left, right = st.columns(2, gap="medium")

    with left:
        with st.container(border=True):
            chart_heading("👥", "Jumlah Pelanggan per Segmen")

            fig = px.bar(
                summary,
                x="segment",
                y="customers",
                category_orders={"segment": segment_order},
                labels={
                    "segment": "Segmen",
                    "customers": "Jumlah Pelanggan"
                },
                color_discrete_sequence=["#635BDB"]
            )

            fig.update_layout(xaxis_tickangle=-25)
            style_chart(fig, 390)
            st.plotly_chart(fig, use_container_width=True)

    with right:
        with st.container(border=True):
            chart_heading("💰", "Kontribusi Monetary per Segmen")

            fig = px.bar(
                summary,
                x="segment",
                y="monetary",
                category_orders={"segment": segment_order},
                labels={
                    "segment": "Segmen",
                    "monetary": "Monetary (BRL)"
                },
                color_discrete_sequence=["#8278F5"]
            )

            fig.update_layout(xaxis_tickangle=-25)
            style_chart(fig, 390)
            st.plotly_chart(fig, use_container_width=True)

    st.write("")

    with st.container(border=True):
        chart_heading("📋", "Ringkasan Segmen RFM")

        st.dataframe(
            summary.sort_values("monetary", ascending=False),
            use_container_width=True,
            hide_index=True
        )

    with st.container(border=True):
        chart_heading("👤", "Daftar Pelanggan")

        st.dataframe(
            filtered_rfm[
                [
                    "customer_unique_id",
                    "customer_state",
                    "recency",
                    "frequency",
                    "monetary",
                    "R_score",
                    "F_score",
                    "M_score",
                    "segment"
                ]
            ]
            .sort_values("monetary", ascending=False)
            .head(100),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("""
    **Rekomendasi strategi pelanggan**

    - **Champions dan Loyal Customers:** pertahankan melalui program loyalitas dan penghargaan pelanggan.
    - **Potential Loyalists:** tingkatkan frekuensi pembelian melalui promosi yang relevan.
    - **At Risk dan Hibernating:** lakukan kampanye reaktivasi untuk mendorong pelanggan kembali bertransaksi.
    """)


# =========================================================
# 9. DELIVERY ANALYTICS
# =========================================================

elif page == "Delivery Analytics":

    page_header(
        "Delivery Performance",
        "Evaluasi ketepatan waktu pengiriman berdasarkan tanggal aktual dan estimasi."
    )

    delivery = delivered.dropna(
        subset=[
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    ).copy()

    if delivery.empty:
        st.warning(
            "Tidak ada data pengiriman lengkap pada filter yang dipilih."
        )
        st.stop()

    total_delivery = delivery["order_id"].nunique()
    late_orders = int(delivery["is_late"].sum())

    late_rate = (
        late_orders / total_delivery * 100
        if total_delivery else 0
    )

    on_time_rate = 100 - late_rate
    avg_days = delivery["delivery_days"].mean()

    add_metrics([
        ("📦", "Pesanan Dianalisis", f"{total_delivery:,}",
         "Pesanan dengan data pengiriman lengkap", "icon-purple"),
        ("⏰", "Late Delivery Rate", f"{late_rate:.2f}%",
         "Persentase pesanan terlambat", "icon-orange"),
        ("✅", "On-Time Rate", f"{on_time_rate:.2f}%",
         "Persentase pesanan tepat waktu", "icon-green"),
        ("🚚", "Rata-rata Durasi", f"{avg_days:.1f} hari",
         "Rata-rata waktu pengiriman", "icon-blue")
    ])

    state_delivery = (
        delivery.groupby("customer_state", as_index=False)
        .agg(
            total_orders=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
            avg_delivery_days=("delivery_days", "mean")
        )
    )

    state_delivery["late_rate"] = (
        state_delivery["late_orders"]
        / state_delivery["total_orders"] * 100
    )

    state_delivery = state_delivery[
        state_delivery["total_orders"] >= 100
    ].sort_values("late_rate", ascending=True)

    with st.container(border=True):
        chart_heading("📍", "Tingkat Keterlambatan per State")

        fig = px.bar(
            state_delivery,
            x="late_rate",
            y="customer_state",
            orientation="h",
            hover_data=[
                "total_orders",
                "late_orders",
                "avg_delivery_days"
            ],
            labels={
                "late_rate": "Keterlambatan (%)",
                "customer_state": "State",
                "total_orders": "Total Pesanan",
                "late_orders": "Pesanan Terlambat",
                "avg_delivery_days": "Rata-rata Durasi (hari)"
            },
            color="late_rate",
            color_continuous_scale=["#A5B4FC", "#5145CD"]
        )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        style_chart(fig, 480)
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        chart_heading("⏱️", "Distribusi Ketepatan Waktu Pengiriman")

        delivery["delivery_status"] = delivery["is_late"].map(
            {
                True: "Terlambat",
                False: "Tepat Waktu"
            }
        )

        status = (
            delivery["delivery_status"]
            .value_counts()
            .rename_axis("status")
            .reset_index(name="orders")
        )

        fig = px.pie(
            status,
            names="status",
            values="orders",
            hole=0.58,
            color="status",
            color_discrete_map={
                "Terlambat": "#EF5368",
                "Tepat Waktu": "#2DBE83"
            }
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#FFFFFF", width=2))
        )

        style_chart(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        chart_heading("📋", "Detail Pengiriman per State")

        st.dataframe(
            state_delivery.sort_values(
                "late_rate", ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 10. PRODUCT ANALYTICS
# =========================================================

elif page == "Product Analytics":

    page_header(
        "Product Analytics",
        "Analisis kategori produk berdasarkan pendapatan dan jumlah item terjual."
    )

    if filtered_category.empty:
        st.warning(
            "Tidak ada item delivered pada filter yang dipilih."
        )
        st.stop()

    category_summary = (
        filtered_category.groupby("category", as_index=False)
        .agg(
            revenue=("price", "sum"),
            items_sold=("order_item_id", "count")
        )
        .sort_values("revenue", ascending=False)
    )

    total_items = category_summary["items_sold"].sum()
    top_category = category_summary.iloc[0]["category"]

    add_metrics([
        ("📦", "Kategori Produk",
         f"{category_summary['category'].nunique():,}",
         "Jumlah kategori produk", "icon-purple"),
        ("🛒", "Item Terjual", f"{total_items:,}",
         "Jumlah item yang terjual", "icon-blue"),
        ("🏆", "Kategori Tertinggi", top_category,
         "Kategori dengan pendapatan terbesar", "icon-orange")
    ])

    top10 = category_summary.head(10).sort_values(
        "revenue", ascending=True
    )

    with st.container(border=True):
        chart_heading("🏆", "Top 10 Kategori berdasarkan Pendapatan")

        fig = px.bar(
            top10,
            x="revenue",
            y="category",
            orientation="h",
            labels={
                "revenue": "Pendapatan Produk (BRL)",
                "category": "Kategori"
            },
            color="revenue",
            color_continuous_scale=["#A5B4FC", "#5145CD"]
        )

        style_chart(fig, 470)
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        chart_heading("📈", "Perbandingan Pendapatan dan Item Terjual")

        fig = px.scatter(
            category_summary,
            x="items_sold",
            y="revenue",
            hover_name="category",
            size="revenue",
            labels={
                "items_sold": "Jumlah Item Terjual",
                "revenue": "Pendapatan (BRL)"
            },
            color="revenue",
            color_continuous_scale=["#A5B4FC", "#5145CD"]
        )

        style_chart(fig, 430)
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        chart_heading("📋", "Detail Pendapatan Kategori")

        st.dataframe(
            category_summary,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 11. FOOTER
# =========================================================

st.sidebar.divider()

st.sidebar.markdown(
    """
    <div style="
        color: #B9C7E0;
        font-size: 0.82rem;
        line-height: 1.6;
    ">
        🗄️ <b>Dataset:</b><br>
        Brazilian E-Commerce Public Dataset by Olist
        <br><br>
        📑 <b>Analisis Akademik:</b><br>
        Dicoding Data Analysis Project
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="dashboard-footer">
        Olist E-Commerce Analytics Dashboard<br>
        Data Analysis Project
    </div>
    """,
    unsafe_allow_html=True
)
