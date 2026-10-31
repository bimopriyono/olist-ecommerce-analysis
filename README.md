# Olist E-Commerce Analytics Project

Proyek analisis data Brazilian E-Commerce Public Dataset by Olist.

## Struktur
- `notebook.ipynb`: Business Understanding, Data Wrangling, EDA, visualisasi, RFM, kesimpulan dan rekomendasi.
- `data/raw/`: sembilan dataset asli.
- `data/processed/`: hasil olahan yang diekspor dari notebook.
- `dashboard/dashboard.py`: aplikasi Streamlit empat halaman.
- `dashboard/main_data.csv`, `dashboard/category_items.csv`, `dashboard/rfm_data.csv`: data dashboard yang dihasilkan notebook.

## Menjalankan notebook
1. Buat environment Python atau buka Google Colab.
2. Pastikan sembilan file CSV tersedia di `data/raw/`.
3. Buka `notebook.ipynb` dan jalankan seluruh cell dari atas ke bawah.
4. Notebook akan menghasilkan file CSV pada folder `dashboard/` dan `data/processed/`.

Jika menggunakan Colab, unggah folder `data/raw` ke sesi Colab atau sesuaikan variabel `DATA_DIR` pada cell Gathering Data. Untuk menjalankan Streamlit secara lokal, unduh folder proyek lengkap setelah file hasil ekspor tersedia.

## Menjalankan dashboard secara lokal
Dari direktori utama proyek:

```bash
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

Pastikan file berikut sudah tersedia di folder `dashboard/`:
- `main_data.csv`
- `category_items.csv`
- `rfm_data.csv`

## Menjalankan dashboard dari folder dashboard
```bash
cd dashboard
pip install -r requirements.txt
streamlit run dashboard.py
```

## Catatan metodologi
- Revenue didefinisikan sebagai jumlah `price` pada item dari pesanan berstatus `delivered`; freight tidak dimasukkan ke revenue produk.
- Analisis RFM menggunakan `customer_unique_id` dan transaksi delivered.
- Recency dihitung terhadap tanggal pembelian terakhir dalam dataset ditambah satu hari.
- Delivery late didefinisikan sebagai tanggal diterima pelanggan lebih besar dari tanggal estimasi.
- Filter tanggal pada dashboard tidak menghitung ulang RFM; RFM menggunakan keseluruhan periode historis yang tersedia.
- Nilai pada dashboard harus dipahami sesuai definisi metrik tersebut.
