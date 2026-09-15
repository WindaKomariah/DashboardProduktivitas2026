# Dashboard Streamlit Pelatihan Produktivitas & Bimbingan Konsultasi

## Menjalankan
1. Install Python 3.10+.
2. Buka terminal pada folder ini.
3. Jalankan `pip install -r requirements.txt`.
4. Jalankan `streamlit run app.py`.
5. Browser akan membuka dashboard.
6. Upload file `.xlsx`.

## Struktur Excel yang didukung
- `Pelatihan Produktivitas`
- `Bimbingan Konsultasi`

Sheet rekap tetap ada di file dan tidak mengganggu dashboard. Data detail dibaca langsung dari dua sheet tersebut.

## Fitur
- Upload Excel tanpa mengubah kode.
- Cleaning otomatis.
- Filter tahun, provinsi, metode, jenis pelatihan, status kelulusan, bidang usaha, wilayah, dan pelaksana.
- KPI otomatis.
- Grafik interaktif.
- Insight otomatis berbasis data.
- Tabel data detail.
- Download hasil cleaning.
