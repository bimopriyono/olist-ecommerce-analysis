from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# Konfigurasi halaman
# ---------------------------------------------------------
st.set_page_config(
    page_title="Olist | E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    main = pd.read_csv(BASE_DIR / "main_data.csv")
    category = pd.read_csv(BASE_DIR / "category_items.csv")
    rfm = pd.read_csv(BASE_DIR / "rfm_data.csv")

    for col in [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]:
        if col in main.columns:
            main[col] = pd.to_datetime(main[col], errors="coerce")

    if "order_purchase_timestamp" in category.columns:
        category["order_purchase_timestamp"] = pd.to_datetime(
            category["order_purchase_timestamp"], errors="coerce"
        )
    if "last_purchase" in rfm.columns:
        rfm["last_purchase"] = pd.to_datetime(rfm["last_purchase"], errors="coerce")

    if "is_late" in main.columns:
        main["is_late"] = main["is_late"].fillna(False).astype(bool)

    return main, category, rfm

try:
    main_df, category_df, rfm_df = load_data()
except FileNotFoundError as error:
    st.error(
        "File data dashboard belum ditemukan. Jalankan notebook.ipynb terlebih dahulu "
        "untuk menghasilkan main_data.csv, category_items.csv, dan rfm_data.csv, "
        "kemudian letakkan ketiganya di folder dashboard."
    )
    st.stop()

# ---------------------------------------------------------
# Style dan sidebar
# ---------------------------------------------------------
st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {
        background: #F4F7FB;
        border: 1px solid #E5EAF1;
        padding: 15px 18px;
        border-radius: 12px;
    }
    [data-testid="stSidebar"] {background: #F7F9FC;}
    h1, h2, h3 {color: #172B4D;}
    .small-note {color: #64748B; font-size: 0.85rem;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🛍️ Olist Analytics")
st.sidebar.caption("E-Commerce Business Intelligence")
page = st.sidebar.radio(
    "Navigasi",
    ["Overview", "Customer Analytics", "Delivery Analytics", "Product Analytics"]
)
st.sidebar.divider()
st.sidebar.subheader("Filter Data")

valid_dates = main_df["order_purchase_timestamp"].dropna()
if valid_dates.empty:
    st.error("Tidak ada tanggal transaksi yang valid pada data dashboard.")
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()
date_range = st.sidebar.date_input(
    "Periode transaksi",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

states = sorted(main_df["customer_state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "State pelanggan",
    options=states,
    default=states
)

# Filter utama berdasarkan waktu dan wilayah
filtered_main = main_df[
    main_df["order_purchase_timestamp"].dt.date.between(start_date, end_date)
    & main_df["customer_state"].isin(selected_states)
].copy()

filtered_category = category_df[
    category_df["order_purchase_timestamp"].dt.date.between(start_date, end_date)
    & category_df["customer_state"].isin(selected_states)
].copy()

filtered_rfm = rfm_df[rfm_df["customer_state"].isin(selected_states)].copy()

# Analisis penjualan dan AOV menggunakan delivered orders
delivered = filtered_main[filtered_main["order_status"].eq("delivered")].copy()

def format_brl(value):
    return f"R$ {value:,.2f}"

def page_header(title, subtitle):
    st.title(title)
    st.caption(subtitle)

def add_overview_metrics(data):
    revenue = data["revenue"].fillna(0).sum()
    order_count = data["order_id"].nunique()
    customer_count = data["customer_unique_id"].nunique()
    aov = revenue / order_count if order_count else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", format_brl(revenue))
    c2.metric("Total Orders", f"{order_count:,}")
    c3.metric("Unique Customers", f"{customer_count:,}")
    c4.metric("Average Order Value", format_brl(aov))

# ---------------------------------------------------------
# 1. Overview
# ---------------------------------------------------------
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
    left, right = st.columns(2)

    monthly = (
        delivered.assign(
            month=delivered["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("month", as_index=False)
        .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
    )
    with left:
        st.subheader("Tren Pendapatan Bulanan")
        fig = px.line(
            monthly, x="month", y="revenue", markers=True,
            labels={"month": "Bulan", "revenue": "Pendapatan (BRL)"},
            template="plotly_white"
        )
        fig.update_layout(margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Jumlah Pesanan Bulanan")
        fig = px.bar(
            monthly, x="month", y="orders",
            labels={"month": "Bulan", "orders": "Jumlah Pesanan"},
            template="plotly_white"
        )
        fig.update_layout(margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Status Pesanan")
    status = filtered_main["order_status"].value_counts().rename_axis("status").reset_index(name="orders")
    fig = px.bar(
        status, x="status", y="orders", color="status",
        labels={"status": "Status Pesanan", "orders": "Jumlah Pesanan"},
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Revenue dihitung dari penjumlahan harga produk (price) pada order berstatus "
        "delivered. Biaya pengiriman (freight_value) tidak dimasukkan ke revenue produk."
    )

# ---------------------------------------------------------
# 2. Customer Analytics
# ---------------------------------------------------------
elif page == "Customer Analytics":
    page_header(
        "Customer Analytics",
        "Segmentasi pelanggan menggunakan Recency, Frequency, dan Monetary (RFM)."
    )
    st.caption(
        "RFM dihitung dari seluruh periode transaksi delivered yang tersedia. "
        "Filter wilayah diterapkan pada pelanggan; filter tanggal tidak mengubah skor RFM."
    )

    if filtered_rfm.empty:
        st.warning("Tidak ada pelanggan pada wilayah yang dipilih.")
        st.stop()

    total_customers = filtered_rfm["customer_unique_id"].nunique()
    total_monetary = filtered_rfm["monetary"].sum()
    avg_frequency = filtered_rfm["frequency"].mean()
    avg_recency = filtered_rfm["recency"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pelanggan", f"{total_customers:,}")
    c2.metric("Total Monetary", format_brl(total_monetary))
    c3.metric("Rata-rata Frequency", f"{avg_frequency:.2f}")
    c4.metric("Rata-rata Recency", f"{avg_recency:.1f} hari")

    segment_order = [
        "Champions", "Loyal Customers", "Potential Loyalists",
        "Needs Attention", "At Risk", "Hibernating"
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
            summary, x="segment", y="customers",
            category_orders={"segment": segment_order},
            labels={"segment": "Segmen", "customers": "Jumlah Pelanggan"},
            template="plotly_white"
        )
        fig.update_layout(xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Kontribusi Monetary per Segmen")
        fig = px.bar(
            summary, x="segment", y="monetary",
            category_orders={"segment": segment_order},
            labels={"segment": "Segmen", "monetary": "Monetary (BRL)"},
            template="plotly_white"
        )
        fig.update_layout(xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Ringkasan Segmen RFM")
    st.dataframe(
        summary.sort_values("monetary", ascending=False),
        use_container_width=True, hide_index=True
    )

    st.subheader("Daftar Pelanggan")
    st.dataframe(
        filtered_rfm[
            ["customer_unique_id", "customer_state", "recency", "frequency",
             "monetary", "R_score", "F_score", "M_score", "segment"]
        ].sort_values("monetary", ascending=False).head(100),
        use_container_width=True, hide_index=True
    )

    st.markdown("""
    **Arahan strategi:** pertahankan Champions dan Loyal Customers melalui program loyalitas.
    Prioritaskan kampanye reaktivasi untuk At Risk dan Hibernating, lalu evaluasi responsnya.
    """)

# ---------------------------------------------------------
# 3. Delivery Analytics
# ---------------------------------------------------------
elif page == "Delivery Analytics":
    page_header(
        "Delivery Performance",
        "Evaluasi ketepatan waktu pengiriman berdasarkan tanggal aktual dan estimasi."
    )
    delivery = delivered.dropna(
        subset=["order_delivered_customer_date", "order_estimated_delivery_date"]
    ).copy()

    if delivery.empty:
        st.warning("Tidak ada data pengiriman lengkap pada filter yang dipilih.")
        st.stop()

    total_delivery = delivery["order_id"].nunique()
    late_orders = int(delivery["is_late"].sum())
    late_rate = late_orders / total_delivery * 100 if total_delivery else 0
    on_time_rate = 100 - late_rate
    avg_days = delivery["delivery_days"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pesanan Dianalisis", f"{total_delivery:,}")
    c2.metric("Late Delivery Rate", f"{late_rate:.2f}%")
    c3.metric("On-Time Rate", f"{on_time_rate:.2f}%")
    c4.metric("Rata-rata Durasi", f"{avg_days:.1f} hari")

    state_delivery = (
        delivery.groupby("customer_state", as_index=False)
        .agg(
            total_orders=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
            avg_delivery_days=("delivery_days", "mean")
        )
    )
    state_delivery["late_rate"] = (
        state_delivery["late_orders"] / state_delivery["total_orders"] * 100
    )
    state_delivery = state_delivery[state_delivery["total_orders"] >= 100]
    state_delivery = state_delivery.sort_values("late_rate", ascending=False)

    st.subheader("Tingkat Keterlambatan per State")
    fig = px.bar(
        state_delivery, x="late_rate", y="customer_state", orientation="h",
        hover_data=["total_orders", "late_orders", "avg_delivery_days"],
        labels={
            "late_rate": "Keterlambatan (%)",
            "customer_state": "State",
            "total_orders": "Total Pesanan",
            "late_orders": "Pesanan Terlambat",
            "avg_delivery_days": "Rata-rata Durasi (hari)"
        },
        template="plotly_white"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Distribusi Status Ketepatan Waktu")
    delivery["delivery_status"] = delivery["is_late"].map(
        {True: "Terlambat", False: "Tepat waktu"}
    )
    status = delivery["delivery_status"].value_counts().rename_axis("status").reset_index(name="orders")
    fig = px.pie(
        status, names="status", values="orders", hole=0.55,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(state_delivery, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# 4. Product Analytics
# ---------------------------------------------------------
elif page == "Product Analytics":
    page_header(
        "Product Analytics",
        "Analisis kategori produk berdasarkan pendapatan dan jumlah item terjual."
    )

    if filtered_category.empty:
        st.warning("Tidak ada item delivered pada filter yang dipilih.")
        st.stop()

    category_summary = (
        filtered_category.groupby("category", as_index=False)
        .agg(
            revenue=("price", "sum"),
            items_sold=("order_item_id", "count")
        )
        .sort_values("revenue", ascending=False)
    )
    total_revenue = category_summary["revenue"].sum()
    total_items = category_summary["items_sold"].sum()
    top_category = category_summary.iloc[0]["category"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Kategori Produk", f"{category_summary['category'].nunique():,}")
    c2.metric("Item Terjual", f"{total_items:,}")
    c3.metric("Kategori Pendapatan Tertinggi", top_category)

    st.subheader("Top 10 Kategori berdasarkan Pendapatan")
    top10 = category_summary.head(10)
    fig = px.bar(
        top10.sort_values("revenue"), x="revenue", y="category",
        orientation="h",
        labels={"revenue": "Pendapatan Produk (BRL)", "category": "Kategori"},
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Perbandingan Pendapatan dan Item Terjual")
    fig = px.scatter(
        category_summary, x="items_sold", y="revenue",
        hover_name="category", size="revenue",
        labels={
            "items_sold": "Jumlah Item Terjual",
            "revenue": "Pendapatan Produk (BRL)"
        },
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detail Kategori")
    st.dataframe(category_summary, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.sidebar.divider()
st.sidebar.caption("Dataset: Brazilian E-Commerce Public Dataset by Olist")
st.sidebar.caption("Analisis akademik • Dicoding Data Analysis Project")