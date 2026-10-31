
from pathlib import Path

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
        main["is_late"] = (
            main["is_late"].fillna(False).astype(bool)
        )

    return main, category, rfm


try:
    main_df, category_df, rfm_df = load_data()

except FileNotFoundError:
    st.error(
        "File data dashboard tidak ditemukan. "
        "Pastikan main_data.csv, category_items.csv, dan "
        "rfm_data.csv berada di folder dashboard."
    )
    st.stop()


# =========================================================
# 3. CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ================= BACKGROUND ================= */

.stApp {
    background-color: #F4F6FB;
    color: #1E293B;
}

[data-testid="stAppViewContainer"] {
    background-color: #F4F6FB;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

section[data-testid="stSidebar"] h1 {
    color: #312E81 !important;
    font-size: 1.55rem;
    font-weight: 800;
}

section[data-testid="stSidebar"] p {
    color: #64748B;
}

section[data-testid="stSidebar"] label {
    color: #334155 !important;
    font-weight: 600;
}

/* Navigasi */
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 8px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: #F8FAFC;
    border-radius: 9px;
    padding: 10px 12px;
    border: 1px solid #E2E8F0;
    transition: 0.2s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: #EEF2FF;
    border-color: #C7D2FE;
}

/* ================= TEXT ================= */

h1, h2, h3 {
    color: #172554 !important;
    font-weight: 750 !important;
}

p {
    color: #475569;
}

[data-testid="stCaptionContainer"] {
    color: #64748B;
}

/* ================= HEADER ================= */

.main-header {
    background: linear-gradient(120deg, #312E81, #5145CD);
    padding: 28px 32px;
    border-radius: 16px;
    margin-bottom: 25px;
    box-shadow: 0 5px 18px rgba(49, 46, 129, 0.12);
}

.main-header h1 {
    color: #FFFFFF !important;
    font-size: 2rem;
    margin: 0;
    font-weight: 800;
}

.main-header p {
    color: #E0E7FF !important;
    margin-top: 9px;
    margin-bottom: 0;
    font-size: 0.95rem;
}

/* ================= KPI CARDS ================= */

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 20px 18px;
    min-height: 125px;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
    transition: 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #A5B4FC;
    box-shadow: 0 5px 15px rgba(49, 46, 129, 0.08);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-size: 0.88rem;
    font-weight: 650;
}

[data-testid="stMetricLabel"] p {
    color: #64748B !important;
}

[data-testid="stMetricValue"] {
    color: #312E81 !important;
    font-size: 1.65rem;
    font-weight: 800;
}

[data-testid="stMetricDelta"] {
    color: #475569 !important;
}

/* ================= CHARTS ================= */

[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 13px;
    padding: 10px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

/* ================= TABLES ================= */

[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    overflow: hidden;
}

/* ================= INPUTS ================= */

.stDateInput input {
    background-color: #FFFFFF;
    border-radius: 8px;
}

.stMultiSelect div[data-baseweb="select"] {
    background-color: #FFFFFF;
    border-radius: 8px;
}

/* ================= BUTTONS ================= */

.stButton button {
    border-radius: 9px;
    font-weight: 600;
}

/* ================= DIVIDER ================= */

hr {
    border-color: #E2E8F0;
}

/* ================= ALERT ================= */

[data-testid="stAlert"] {
    border-radius: 10px;
}

/* ================= RESPONSIVE ================= */

@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .main-header {
        padding: 22px;
    }

    .main-header h1 {
        font-size: 1.45rem;
    }

    [data-testid="stMetric"] {
        padding: 14px;
        min-height: 105px;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.3rem;
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
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def style_chart(fig, height=400):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            color="#334155",
            size=12
        ),
        title_font=dict(
            color="#172554",
            size=17
        ),
        margin=dict(
            l=20,
            r=20,
            t=35,
            b=25
        ),
        height=height,
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_color="#1E293B"
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0)"
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#EDF0F5",
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EDF0F5",
        zeroline=False
    )

    return fig


def add_overview_metrics(data):
    revenue = data["revenue"].fillna(0).sum()
    order_count = data["order_id"].nunique()
    customer_count = data["customer_unique_id"].nunique()

    aov = revenue / order_count if order_count else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Revenue",
        format_brl(revenue)
    )

    c2.metric(
        "Total Orders",
        f"{order_count:,}"
    )

    c3.metric(
        "Unique Customers",
        f"{customer_count:,}"
    )

    c4.metric(
        "Average Order Value",
        format_brl(aov)
    )


# =========================================================
# 5. SIDEBAR DAN FILTER
# =========================================================

st.sidebar.title("🛍️ Olist Analytics")
st.sidebar.caption("E-Commerce Business Intelligence")

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGASI",
    [
        "Overview",
        "Customer Analytics",
        "Delivery Analytics",
        "Product Analytics"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("Filter Data")

valid_dates = main_df["order_purchase_timestamp"].dropna()

if valid_dates.empty:
    st.error("Tidak ada tanggal transaksi yang valid.")
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

date_range = st.sidebar.date_input(
    "Periode Transaksi",
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
    "Wilayah Pelanggan",
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


# Analisis penjualan menggunakan pesanan delivered
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

    st.divider()

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

    left, right = st.columns(2)

    with left:
        st.subheader("Tren Pendapatan Bulanan")

        fig = px.line(
            monthly,
            x="month",
            y="revenue",
            markers=True,
            labels={
                "month": "Bulan",
                "revenue": "Pendapatan (BRL)"
            },
            color_discrete_sequence=["#635BDB"]
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Jumlah Pesanan Bulanan")

        fig = px.bar(
            monthly,
            x="month",
            y="orders",
            labels={
                "month": "Bulan",
                "orders": "Jumlah Pesanan"
            },
            color_discrete_sequence=["#818CF8"]
        )

        fig.update_traces(
            marker_line_width=0,
            opacity=0.9
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Distribusi Status Pesanan")

    status = (
        filtered_main["order_status"]
        .value_counts()
        .rename_axis("status")
        .reset_index(name="orders")
    )

    fig = px.bar(
        status,
        x="status",
        y="orders",
        color="status",
        labels={
            "status": "Status Pesanan",
            "orders": "Jumlah Pesanan"
        },
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    style_chart(fig)
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

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Pelanggan",
        f"{total_customers:,}"
    )

    c2.metric(
        "Total Monetary",
        format_brl(total_monetary)
    )

    c3.metric(
        "Rata-rata Frequency",
        f"{avg_frequency:.2f}"
    )

    c4.metric(
        "Rata-rata Recency",
        f"{avg_recency:.1f} hari"
    )

    st.divider()

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

    left, right = st.columns(2)

    with left:
        st.subheader("Jumlah Pelanggan per Segmen")

        fig = px.bar(
            summary,
            x="segment",
            y="customers",
            category_orders={
                "segment": segment_order
            },
            labels={
                "segment": "Segmen",
                "customers": "Jumlah Pelanggan"
            },
            color_discrete_sequence=["#635BDB"]
        )

        fig.update_layout(
            xaxis_tickangle=-25
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Kontribusi Monetary per Segmen")

        fig = px.bar(
            summary,
            x="segment",
            y="monetary",
            category_orders={
                "segment": segment_order
            },
            labels={
                "segment": "Segmen",
                "monetary": "Monetary (BRL)"
            },
            color_discrete_sequence=["#818CF8"]
        )

        fig.update_layout(
            xaxis_tickangle=-25
        )

        style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Ringkasan Segmen RFM")

    st.dataframe(
        summary.sort_values(
            "monetary",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Daftar Pelanggan")

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

    st.divider()

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

    late_orders = int(
        delivery["is_late"].sum()
    )

    late_rate = (
        late_orders / total_delivery * 100
        if total_delivery else 0
    )

    on_time_rate = 100 - late_rate

    avg_days = delivery["delivery_days"].mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Pesanan Dianalisis",
        f"{total_delivery:,}"
    )

    c2.metric(
        "Late Delivery Rate",
        f"{late_rate:.2f}%"
    )

    c3.metric(
        "On-Time Rate",
        f"{on_time_rate:.2f}%"
    )

    c4.metric(
        "Rata-rata Durasi",
        f"{avg_days:.1f} hari"
    )

    st.divider()

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
    ]

    state_delivery = state_delivery.sort_values(
        "late_rate",
        ascending=False
    )

    st.subheader("Tingkat Keterlambatan per State")

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

    style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Distribusi Ketepatan Waktu Pengiriman")

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
            "Terlambat": "#F87171",
            "Tepat Waktu": "#34D399"
        }
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detail Pengiriman per State")

    st.dataframe(
        state_delivery.sort_values(
            "late_rate",
            ascending=False
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

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Kategori Produk",
        f"{category_summary['category'].nunique():,}"
    )

    c2.metric(
        "Item Terjual",
        f"{total_items:,}"
    )

    c3.metric(
        "Kategori Pendapatan Tertinggi",
        top_category
    )

    st.divider()

    st.subheader("Top 10 Kategori berdasarkan Pendapatan")

    top10 = category_summary.head(10).sort_values(
        "revenue",
        ascending=True
    )

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

    style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Perbandingan Pendapatan dan Item Terjual")

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

    style_chart(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detail Pendapatan Kategori")

    st.dataframe(
        category_summary,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# 11. FOOTER
# =========================================================

st.sidebar.divider()

st.sidebar.caption(
    "Dataset: Brazilian E-Commerce Public Dataset by Olist"
)

st.sidebar.caption(
    "Analisis Akademik | Dicoding Data Analysis Project"
)

st.markdown("""
<div style="
    text-align:center;
    padding:25px 10px 5px 10px;
    color:#94A3B8;
    font-size:12px;
">
    Olist E-Commerce Analytics Dashboard
    <br>
    Data Analysis Project
</div>
""", unsafe_allow_html=True)
