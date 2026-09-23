import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import re
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.units import cm


# =========================================================
# KONFIGURASI
# =========================================================

st.set_page_config(
    page_title="Dashboard Produktivitas 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)




# =========================================================
# DESAIN DASHBOARD
# =========================================================

st.markdown("""
<style>
/* ========================= GLOBAL ========================= */
[data-testid="stAppViewContainer"] { background: #f5f7fb; }
[data-testid="stHeader"] { background: rgba(255,255,255,.96); border-bottom: 1px solid #e6ebf2; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1500px; }
h1,h2,h3 { color:#123b69 !important; letter-spacing:-.02em; }
p,li { color:#334e68; }
[data-testid="stCaptionContainer"] { color:#6b7c93 !important; }

/* ========================= SIDEBAR ========================= */
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#0b2f5b 0%,#104b82 55%,#0d4275 100%); }
section[data-testid="stSidebar"] > div { background:transparent; }
section[data-testid="stSidebar"] * { color:#f5f9ff; }
section[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.18); }
section[data-testid="stSidebar"] [data-testid="stRadio"] label { border-radius:10px; padding:8px 10px; margin:3px 0; transition:.2s ease; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:rgba(255,255,255,.10); }
section[data-testid="stSidebar"] label { color:#fff !important; font-weight:600 !important; }

/* ========================= SELECTBOX FIX ========================= */
section[data-testid="stSidebar"] div[data-baseweb="select"] { width:100% !important; }
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background:#fff !important; border:1px solid #c9d7e6 !important; border-radius:10px !important;
    min-height:42px !important; box-shadow:0 2px 6px rgba(0,0,0,.08) !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color:#173f6b !important; -webkit-text-fill-color:#173f6b !important; opacity:1 !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] [class*="singleValue"],
section[data-testid="stSidebar"] div[data-baseweb="select"] [class*="SingleValue"] {
    color:#173f6b !important; -webkit-text-fill-color:#173f6b !important; font-weight:600 !important; opacity:1 !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] input {
    color:#173f6b !important; -webkit-text-fill-color:#173f6b !important; opacity:1 !important; caret-color:#173f6b !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] input::placeholder {
    color:#7b8da3 !important; -webkit-text-fill-color:#7b8da3 !important; opacity:1 !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] svg { color:#315b83 !important; fill:#315b83 !important; }

div[data-baseweb="popover"] { background:#fff !important; border-radius:10px !important; box-shadow:0 8px 25px rgba(20,55,90,.18) !important; }
div[data-baseweb="popover"] * { color:#173f6b !important; -webkit-text-fill-color:#173f6b !important; }
div[data-baseweb="popover"] li { background:#fff !important; color:#173f6b !important; padding:9px 12px !important; }
div[data-baseweb="popover"] li:hover { background:#eaf3ff !important; color:#104d7b !important; }
div[data-baseweb="popover"] li[aria-selected="true"] { background:#dcecff !important; color:#0b4f8a !important; font-weight:600 !important; }

/* ========================= KPI ========================= */
div[data-testid="stMetric"] { background:#fff; border:1px solid #e1e9f2; border-radius:16px; padding:18px 20px; box-shadow:0 5px 18px rgba(25,61,96,.07); min-height:115px; transition:.2s ease; }
div[data-testid="stMetric"]:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(25,61,96,.11); }
div[data-testid="stMetric"] label { color:#60758b !important; font-weight:600 !important; font-size:14px !important; }
div[data-testid="stMetricValue"] { color:#123b69 !important; font-weight:750 !important; font-size:28px !important; }

/* ========================= CHART / TABLE ========================= */
div[data-testid="stPlotlyChart"] { background:#fff; border:1px solid #e1e9f2; border-radius:16px; padding:8px 8px 0; box-shadow:0 5px 18px rgba(25,61,96,.06); margin-bottom:15px; }
div[data-testid="stDataFrame"] { border:1px solid #e1e9f2; border-radius:14px; overflow:hidden; box-shadow:0 4px 14px rgba(25,61,96,.05); }

/* ========================= BUTTON / UPLOAD ========================= */
.stButton > button,.stDownloadButton > button { border-radius:10px; border:1px solid #cddceb; background:#fff; color:#173f6b; font-weight:600; min-height:42px; transition:.2s ease; }
.stButton > button:hover,.stDownloadButton > button:hover { border-color:#2c7fd3; color:#104d7b; box-shadow:0 4px 12px rgba(44,127,211,.15); }
[data-testid="stFileUploader"] { background:#fff; border:1.5px dashed #8db4d8; border-radius:16px; padding:10px; box-shadow:0 5px 18px rgba(25,61,96,.05); }
div[data-testid="stAlert"] { border-radius:12px; }
div[data-testid="stExpander"] { background:#fff; border:1px solid #e1e9f2; border-radius:14px; }
button[data-baseweb="tab"] { font-weight:600; color:#526b84 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color:#104d7b !important; }
hr { border-color:#e1e8f0; }

/* ========================= HEADER / FILTER ========================= */
.dashboard-header { background:linear-gradient(135deg,#0b3b68 0%,#145c91 100%); border-radius:20px; padding:28px 32px; margin-bottom:25px; box-shadow:0 8px 25px rgba(15,63,105,.15); }
.dashboard-header h1 { color:#fff !important; font-size:32px; margin-bottom:5px; }
.dashboard-header p { color:#dcecff !important; font-size:15px; margin-bottom:0; }
.filter-title { color:#fff; font-size:16px; font-weight:700; margin-top:10px; margin-bottom:12px; }
.filter-info { background:rgba(255,255,255,.10); border:1px solid rgba(255,255,255,.12); border-radius:10px; padding:10px 12px; margin-bottom:14px; font-size:13px; color:#eaf3ff !important; }
.section-title { color:#123b69; font-size:21px; font-weight:700; margin-top:20px; margin-bottom:12px; }
</style>
""", unsafe_allow_html=True)


# =========================================================
# NAMA SHEET
# =========================================================

TRAIN_SHEET = "Pelatihan Produktivitas"
BIM_SHEET = "Bimbingan Konsultasi"
REKAP_SHEET = "Rekap Pel Prod"
REKAP_BIM_SHEET = "Rekap Bimkon"

MONTHS = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember"
]


# =========================================================
# BACA EXCEL
# =========================================================

@st.cache_data(show_spinner=False)
def load_excel(file_bytes):

    xls = pd.ExcelFile(
        BytesIO(file_bytes),
        engine="openpyxl"
    )

    sheets = {}

    for sheet in xls.sheet_names:

        sheets[sheet] = pd.read_excel(
            xls,
            sheet_name=sheet,
            header=None
        )

    return sheets


@st.cache_data(show_spinner=False)
def process_uploaded_files(file_items):
    """Baca dan cleaning beberapa file Excel, lalu gabungkan per jenis data."""
    all_train, all_bim, all_rekap, all_rekap_bim = [], [], [], []

    for file_name, file_bytes in file_items:
        sheets = load_excel(file_bytes)

        if TRAIN_SHEET in sheets:
            df = clean_training(sheets[TRAIN_SHEET])
            if not df.empty:
                df["Sumber File"] = file_name
                all_train.append(df)

        if BIM_SHEET in sheets:
            df = clean_bim(sheets[BIM_SHEET])
            if not df.empty:
                df["Sumber File"] = file_name
                all_bim.append(df)

        if REKAP_SHEET in sheets:
            df = clean_rekap_realisasi(sheets[REKAP_SHEET])
            if not df.empty:
                df["Sumber File"] = file_name
                all_rekap.append(df)

        if REKAP_BIM_SHEET in sheets:
            df = clean_rekap_bimkon(sheets[REKAP_BIM_SHEET])
            if not df.empty:
                df["Sumber File"] = file_name
                all_rekap_bim.append(df)

    def combine(items):
        return pd.concat(items, ignore_index=True, sort=False) if items else pd.DataFrame()

    return combine(all_train), combine(all_bim), combine(all_rekap), combine(all_rekap_bim)


# =========================================================
# KOLOM UNIK
# =========================================================

def make_unique(cols):

    seen = {}
    output = []

    for col in cols:

        col = (
            str(col).strip()
            if pd.notna(col)
            else "Kolom"
        )

        seen[col] = (
            seen.get(col, 0) + 1
        )

        if seen[col] == 1:

            output.append(col)

        else:

            output.append(
                f"{col}_{seen[col]}"
            )

    return output


# =========================================================
# NORMALISASI TEKS
# =========================================================

def normalisasi_teks(value):

    if pd.isna(value):
        return pd.NA

    text = str(value).strip()

    if text == "":
        return pd.NA

    return text


# =========================================================
# STANDARDISASI PROVINSI
# =========================================================

def standardisasi_provinsi(value):

    if pd.isna(value):
        return "Tidak Diisi"

    text = str(value).strip().upper()

    mapping = {

        "DKI JAKARTA": "DKI Jakarta",

        "JAWA BARAT": "Jawa Barat",
        "JAWA TENGAH": "Jawa Tengah",
        "JAWA TIMUR": "Jawa Timur",

        "BANTEN": "Banten",

        "SUMATERA BARAT": "Sumatera Barat",
        "SUMATERA UTARA": "Sumatera Utara",
        "SUMATERA SELATAN": "Sumatera Selatan",

        "KALIMANTAN TIMUR": "Kalimantan Timur",
        "KALIMANTAN BARAT": "Kalimantan Barat",
        "KALIMANTAN SELATAN": "Kalimantan Selatan",
        "KALIMANTAN TENGAH": "Kalimantan Tengah",
        "KALIMANTAN UTARA": "Kalimantan Utara",

        "ACEH": "Aceh",

        "SULAWESI SELATAN": "Sulawesi Selatan",
        "SULSEL": "Sulawesi Selatan",

        "SULAWESI TENGGARA": "Sulawesi Tenggara",
        "SULAWESI UTARA": "Sulawesi Utara",
        "SULAWESI TENGAH": "Sulawesi Tengah",

        "PAPUA BARAT DAYA": "Papua Barat Daya",
        "PAPUA": "Papua"
    }

    return mapping.get(
        text,
        str(value).strip().title()
    )


# =========================================================
# STANDARDISASI METODE
# =========================================================

def standardisasi_metode(value):

    if pd.isna(value):
        return "Tidak Diisi"

    text = str(value).strip().lower()

    if text == "online":
        return "Online"

    if text == "offline":
        return "Offline"

    if text == "hybrid":
        return "Hybrid"

    return str(value).strip().title()


# =========================================================
# JENIS PELATIHAN
# =========================================================

def standardisasi_jenis_pelatihan(value):

    if pd.isna(value):
        return "Tidak Diisi"

    text = str(value).strip().upper()

    if text == "NON BOARDING":
        return "Non Boarding"

    if text == "BOARDING":
        return "Boarding"

    return str(value).strip().title()


# =========================================================
# STATUS LULUS
# =========================================================

def standardisasi_status_lulus(value):

    if pd.isna(value):
        return "Tidak Diisi"

    text = str(value).strip().lower()

    if text in [
        "lulus",
        "100"
    ]:
        return "Lulus"

    if text in [
        "tidak lulus",
        "0"
    ]:
        return "Tidak Lulus"

    return str(value).strip().title()


# =========================================================
# STATUS SELESAI
# =========================================================

def standardisasi_status_selesai(value):

    if pd.isna(value):
        return "Tidak Diisi"

    text = str(value).strip().lower()

    if text in [
        "selesai",
        "ya",
        "1"
    ]:
        return "Selesai"

    if text in [
        "belum selesai",
        "tidak",
        "0"
    ]:
        return "Belum Selesai"

    return str(value).strip().title()


# =========================================================
# KEJURUAN
# =========================================================

def standardisasi_kejuruan(value):

    if pd.isna(value):
        return "Tidak Diisi"

    text = str(value).strip().lower()

    if text == "produktivitas":
        return "Produktivitas"

    return str(value).strip().title()


# =========================================================
# KATEGORI BIDANG USAHA
# =========================================================

def kategori_bidang_usaha(value):

    if pd.isna(value):
        return "Tidak Diisi"

    text = str(value).strip().lower()

    if text == "":
        return "Tidak Diisi"


    # MAKANAN & MINUMAN

    if any(
        k in text
        for k in [

            "kuliner",
            "bakery",
            "keripik",
            "snack",
            "dimsum",
            "kue",
            "catering",
            "bawang goreng",
            "jus",
            "bubur",
            "jamu",
            "peyek",
            "tape",
            "bandeng presto",
            "sambal",
            "seblak",
            "warung makan",
            "minuman",
            "ayam gepuk",
            "donat",
            "abon",
            "crispy",
            "tepung",
            "makanan"
        ]
    ):

        return "Makanan & Minuman"


    # TEKSTIL

    if any(
        k in text
        for k in [

            "menjahit",
            "jahit",
            "fashion",
            "konveksi",
            "pakaian",
            "tekstil",
            "bordir"
        ]
    ):

        return "Tekstil & Fashion"


    # OTOMOTIF

    if any(
        k in text
        for k in [

            "bengkel",
            "otomotif",
            "motor",
            "mobil",
            "kendaraan"
        ]
    ):

        return "Otomotif"


    # PERTANIAN & PERIKANAN

    if any(
        k in text
        for k in [

            "budidaya",
            "pertanian",
            "peternakan",
            "perikanan",
            "ikan",
            "perkebunan"
        ]
    ):

        return "Pertanian & Perikanan"


    # PERDAGANGAN

    if any(
        k in text
        for k in [

            "dagang",
            "toko",
            "agen",
            "perdagangan",
            "distributor"
        ]
    ):

        return "Perdagangan"


    # JASA

    if any(
        k in text
        for k in [

            "jasa",
            "expedisi",
            "ekspedisi",
            "service"
        ]
    ):

        return "Jasa"


    return "Lainnya"


# =========================================================
# CLEANING REKAP REALISASI LEMBAGA
# =========================================================

def clean_rekap_realisasi(raw):
    df = raw.copy()
    header = None

    for i, row in df.iterrows():
        values = [
            str(v).strip().upper()
            for v in row.tolist()
            if pd.notna(v)
        ]
        joined = " | ".join(values)
        if "LEMBAGA/INSTANSI" in joined and "TARGET PESERTA PELATIHAN P3" in joined:
            header = i
            break

    if header is None:
        return pd.DataFrame()

    df.columns = make_unique(df.iloc[header])
    df = df.iloc[header + 1:].copy().dropna(how="all")

    rename_map = {}
    realisasi_found = False
    for col in df.columns:
        text = str(col).strip().upper()
        if "LEMBAGA/INSTANSI" in text:
            rename_map[col] = "Lembaga/Instansi"
        elif "TARGET PESERTA PELATIHAN P3" in text and "PEKERJAAN HIJAU" not in text:
            rename_map[col] = "Target Pelatihan P3"
        elif text == "REALISASI" and not realisasi_found:
            rename_map[col] = "Realisasi Pelatihan P3"
            realisasi_found = True

    df = df.rename(columns=rename_map)
    if "Lembaga/Instansi" not in df.columns or "Realisasi Pelatihan P3" not in df.columns:
        return pd.DataFrame()

    df["Lembaga/Instansi"] = df["Lembaga/Instansi"].apply(normalisasi_teks)
    df = df[df["Lembaga/Instansi"].notna()].copy()
    df = df[~df["Lembaga/Instansi"].astype(str).str.upper().isin([
        "PELATIHAN PRODUKTIVITAS", "BIMBINGAN KONSULTANSI", "JUMLAH TOTAL", "TOTAL"
    ])]

    for col in ["Target Pelatihan P3", "Realisasi Pelatihan P3"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Status Realisasi"] = df["Realisasi Pelatihan P3"].apply(
        lambda x: "Sudah Terealisasi" if x > 0 else "Belum Terealisasi"
    )

    if "Target Pelatihan P3" in df.columns:
        df["Persentase Realisasi"] = df.apply(
            lambda r: (r["Realisasi Pelatihan P3"] / r["Target Pelatihan P3"] * 100)
            if r["Target Pelatihan P3"] > 0 else 0,
            axis=1
        ).round(1)

    return df.reset_index(drop=True)


# =========================================================
# CLEANING REKAP REALISASI BIMBINGAN KONSULTASI
# =========================================================

def clean_rekap_bimkon(raw):
    df = raw.copy()
    header = None

    # Cari baris header yang berisi kolom lembaga, target, dan realisasi.
    for i, row in df.iterrows():
        values = [
            str(v).strip().upper()
            for v in row.tolist()
            if pd.notna(v)
        ]
        joined = " | ".join(values)

        if (
            "LEMBAGA/INSTANSI" in joined
            and "TARGET PERUSAHAAN" in joined
            and "REALISASI" in joined
        ):
            header = i
            break

    if header is None:
        return pd.DataFrame()

    header_values = [
        str(v).strip() if pd.notna(v) else "Kolom"
        for v in raw.iloc[header].tolist()
    ]
    df = raw.iloc[header + 1:].copy()
    df.columns = make_unique(header_values)
    df = df.dropna(how="all")

    rename_map = {}
    for col in df.columns:
        text = str(col).strip().upper()
        if text == "LEMBAGA/INSTANSI":
            rename_map[col] = "Lembaga/Instansi"
        elif text == "TARGET PERUSAHAAN":
            rename_map[col] = "Target Perusahaan"
        elif text == "REALISASI":
            rename_map[col] = "Realisasi Bimbingan"

    df = df.rename(columns=rename_map)

    required = [
        "Lembaga/Instansi",
        "Target Perusahaan",
        "Realisasi Bimbingan"
    ]
    if not all(col in df.columns for col in required):
        return pd.DataFrame()

    df["Lembaga/Instansi"] = df["Lembaga/Instansi"].apply(normalisasi_teks)
    df = df[df["Lembaga/Instansi"].notna()].copy()

    exclude = [
        "BIMBINGAN KONSULTANSI",
        "JUMLAH TOTAL",
        "TOTAL",
        "PELATIHAN PRODUKTIVITAS"
    ]
    df = df[
        ~df["Lembaga/Instansi"].astype(str).str.strip().str.upper().isin(exclude)
    ].copy()

    for col in ["Target Perusahaan", "Realisasi Bimbingan"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Status Realisasi"] = df["Realisasi Bimbingan"].apply(
        lambda x: "Sudah Terealisasi" if x > 0 else "Belum Terealisasi"
    )

    df["Persentase Realisasi"] = df.apply(
        lambda r: (
            r["Realisasi Bimbingan"] / r["Target Perusahaan"] * 100
        ) if r["Target Perusahaan"] > 0 else 0,
        axis=1
    ).round(1)

    return df.reset_index(drop=True)


# =========================================================
# CLEANING PELATIHAN
# =========================================================

def clean_training(raw):

    df = raw.copy()

    df.columns = make_unique(
        df.iloc[0]
    )

    df = df.iloc[1:].copy()

    df = df.dropna(
        how="all"
    )


    # Hanya peserta

    if "Nama Peserta" in df.columns:

        df = df[
            df["Nama Peserta"].notna()
        ].copy()


    # Tanggal

    for col in [

        "Tanggal Mulai Pelatihan",
        "Tanggal Selesai Pelatihan",
        "Tanggal Lahir"

    ]:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce",
                dayfirst=True
            )


    # Numeric

    for col in [

        "Durasi (JP)",
        "Absensi"

    ]:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )


    # Bulan & Tahun

    if "Tanggal Mulai Pelatihan" in df.columns:

        bulan = {

            1: "Januari",
            2: "Februari",
            3: "Maret",
            4: "April",
            5: "Mei",
            6: "Juni",
            7: "Juli",
            8: "Agustus",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Desember"
        }

        df["Bulan Pelatihan"] = (
            df["Tanggal Mulai Pelatihan"]
            .dt.month
            .map(bulan)
        )

        df["Tahun Pelatihan"] = (
            df["Tanggal Mulai Pelatihan"]
            .dt.year
        )


    # Standardisasi

    if "Provinsi" in df.columns:

        df["Provinsi"] = (
            df["Provinsi"]
            .apply(standardisasi_provinsi)
        )


    if "Metode Pelatihan" in df.columns:

        df["Metode Pelatihan"] = (
            df["Metode Pelatihan"]
            .apply(standardisasi_metode)
        )


    if "Jenis Pelatihan" in df.columns:

        df["Jenis Pelatihan"] = (
            df["Jenis Pelatihan"]
            .apply(standardisasi_jenis_pelatihan)
        )


    if "Status KeLulusan" in df.columns:

        df["Status KeLulusan"] = (
            df["Status KeLulusan"]
            .apply(standardisasi_status_lulus)
        )


    if "Status Selesai Pelatihan" in df.columns:

        df["Status Selesai Pelatihan"] = (
            df["Status Selesai Pelatihan"]
            .apply(standardisasi_status_selesai)
        )


    if "Kejuruan" in df.columns:

        df["Kejuruan"] = (
            df["Kejuruan"]
            .apply(standardisasi_kejuruan)
        )


    # Normalisasi teks

    for col in [

        "Kab./Kota",
        "Nama Lembaga",
        "Judul Program Pelatihan",
        "Jenis Kelamin",
        "Pendidikan Terakhir (setara dengan)"

    ]:

        if col in df.columns:

            df[col] = (
                df[col]
                .apply(normalisasi_teks)
            )


    return df.reset_index(
        drop=True
    )


# =========================================================
# CLEANING BIMBINGAN
# =========================================================

def clean_bim(raw):

    df = raw.copy()

    header = 0


    # Cari header

    for i, row in df.iterrows():

        values = (
            row.astype(str)
            .str.upper()
            .tolist()
        )

        if "NAMA PERUSAHAAN" in values:

            header = i

            break


    df.columns = make_unique(
        df.iloc[header]
    )

    df = df.iloc[
        header + 1:
    ].copy()

    df = df.dropna(
        how="all"
    )


    # Hanya perusahaan

    if "NAMA PERUSAHAAN" in df.columns:

        df = df[
            df["NAMA PERUSAHAAN"].notna()
        ].copy()

        df = df[
            df["NAMA PERUSAHAAN"]
            .astype(str)
            .str.upper()
            != "CONTOH PENGISIAN"
        ]


    # Tanggal pelaksanaan

    if "WAKTU PELAKSANAAN" in df.columns:

        df["Tanggal Pelaksanaan"] = pd.to_datetime(
            df["WAKTU PELAKSANAAN"],
            errors="coerce",
            dayfirst=True
        )


        # Contoh:
        # 20/7/2026 s/d 12/08/2026

        mask = (
            df["Tanggal Pelaksanaan"]
            .isna()
        )

        if mask.any():

            extracted = (
                df.loc[
                    mask,
                    "WAKTU PELAKSANAAN"
                ]
                .astype(str)
                .str.extract(
                    r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
                )[0]
            )

            df.loc[
                mask,
                "Tanggal Pelaksanaan"
            ] = pd.to_datetime(
                extracted,
                errors="coerce",
                dayfirst=True
            )


    # Tanggal data

    if (
        "DATA PER TANGGAL (tanggal/bulan/tahun)"
        in df.columns
    ):

        df["Tanggal Data"] = pd.to_datetime(
            df[
                "DATA PER TANGGAL (tanggal/bulan/tahun)"
            ],
            errors="coerce",
            dayfirst=True
        )


    # Bulan & tahun

    if "Tanggal Pelaksanaan" in df.columns:

        bulan = {

            1: "Januari",
            2: "Februari",
            3: "Maret",
            4: "April",
            5: "Mei",
            6: "Juni",
            7: "Juli",
            8: "Agustus",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Desember"
        }

        df["Bulan Bimbingan"] = (
            df["Tanggal Pelaksanaan"]
            .dt.month
            .map(bulan)
        )

        df["Tahun Bimbingan"] = (
            df["Tanggal Pelaksanaan"]
            .dt.year
        )


    # Normalisasi teks

    for col in [

        "NAMA KABUPATEN/KOTA",
        "BIDANG USAHA",
        "PELAKSANA",
        "AKTIVITAS PENINGKATAN PRODUKTIVITAS",
        "HASIL PENINGKATAN PRODUKTIVITAS"

    ]:

        if col in df.columns:

            df[col] = (
                df[col]
                .apply(normalisasi_teks)
            )


    # Bidang usaha

    if "BIDANG USAHA" in df.columns:

        df["BIDANG USAHA ASLI"] = (
            df["BIDANG USAHA"]
        )

        df["Bidang Usaha Kategori"] = (
            df["BIDANG USAHA"]
            .apply(kategori_bidang_usaha)
        )


    return df.reset_index(
        drop=True
    )


# =========================================================
# FILTER
# =========================================================

def selectbox_filter(
    df,
    col,
    label,
    key=None
):

    if col not in df.columns:
        return df

    values = (
        df[col]
        .dropna()
        .astype(str)
        .str.strip()
    )
    values = sorted(values[values != ""].unique().tolist())

    selected = st.sidebar.selectbox(
        label,
        ["Semua"] + values,
        index=0,
        key=key
    )

    if selected == "Semua":
        return df

    return df[
        df[col].astype(str).str.strip() == selected
    ].copy()


# =========================================================
# FORMAT ANGKA
# =========================================================

def format_number(value):

    try:

        return f"{int(value):,}".replace(
            ",",
            "."
        )

    except:

        return "0"


# =========================================================
# PERSENTASE
# =========================================================

def percentage(part, total):

    if total == 0:
        return 0

    return (
        part / total
    ) * 100


# =========================================================
# DATA BULANAN
# =========================================================

def monthly_data(
    df,
    month_column,
    value_name
):

    if month_column not in df.columns:

        return pd.DataFrame({
            "Bulan": MONTHS,
            value_name: [0] * 12
        })


    x = (
        df[month_column]
        .value_counts()
        .reindex(MONTHS)
        .fillna(0)
        .reset_index()
    )

    x.columns = [
        "Bulan",
        value_name
    ]

    return x


# =========================================================
# STYLE PLOTLY
# =========================================================

def style_chart(
    fig,
    height=370
):

    fig.update_layout(

        height=height,

        margin=dict(
            l=25,
            r=25,
            t=60,
            b=35
        ),

        paper_bgcolor="white",

        plot_bgcolor="white",

        font=dict(
            family="Arial",
            color="#17324d"
        ),

        title_font=dict(
            size=18,
            color="#104d7b"
        ),

        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        )
    )


    fig.update_xaxes(
        showgrid=True,
        gridcolor="#e6eef5",
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#e6eef5",
        zeroline=False
    )

    return fig


# =========================================================
# INSIGHT PELATIHAN
# =========================================================

def insights_training(df):

    insights = []

    if df.empty:

        return [
            "Tidak ada data sesuai filter."
        ]


    total = len(df)


    # Provinsi

    if "Provinsi" in df.columns:

        x = (
            df["Provinsi"]
            .fillna("Tidak Diisi")
            .value_counts()
        )

        if not x.empty:

            nama = x.index[0]
            jumlah = int(x.iloc[0])
            persen = percentage(
                jumlah,
                total
            )

            insights.append(
                (
                    "🏆 Provinsi Dominan — "
                    f"{nama} memiliki peserta terbanyak, "
                    f"yaitu {format_number(jumlah)} peserta "
                    f"({persen:.1f}%)."
                )
            )


    # Bulan

    if "Bulan Pelatihan" in df.columns:

        x = (
            df["Bulan Pelatihan"]
            .value_counts()
            .reindex(MONTHS)
            .fillna(0)
        )

        if x.max() > 0:

            bulan = x.idxmax()
            jumlah = int(x.max())

            insights.append(
                (
                    "📈 Bulan Tertinggi — "
                    f"Jumlah peserta tertinggi terjadi pada "
                    f"{bulan}, sebanyak "
                    f"{format_number(jumlah)} peserta."
                )
            )


    # Kelulusan

    if "Status KeLulusan" in df.columns:

        lulus = (
            df["Status KeLulusan"]
            .astype(str)
            .str.lower()
            == "lulus"
        ).sum()

        persen = percentage(
            lulus,
            total
        )

        insights.append(
            (
                "🎓 Kelulusan — "
                f"Sebanyak {format_number(lulus)} peserta "
                f"berstatus lulus dengan tingkat kelulusan "
                f"{persen:.1f}%."
            )
        )


    # Metode

    if "Metode Pelatihan" in df.columns:

        x = (
            df["Metode Pelatihan"]
            .fillna("Tidak Diisi")
            .value_counts()
        )

        if not x.empty:

            metode = x.index[0]
            jumlah = int(x.iloc[0])
            persen = percentage(
                jumlah,
                total
            )

            insights.append(
                (
                    "⚙️ Metode Dominan — "
                    f"Metode {metode} digunakan oleh "
                    f"{format_number(jumlah)} peserta "
                    f"({persen:.1f}%)."
                )
            )


    return insights


# =========================================================
# INSIGHT BIMBINGAN
# =========================================================

def insights_bim(df):

    insights = []

    if df.empty:

        return [
            "Tidak ada data sesuai filter."
        ]


    total = len(df)


    # Bidang usaha

    if "Bidang Usaha Kategori" in df.columns:

        x = (
            df["Bidang Usaha Kategori"]
            .fillna("Tidak Diisi")
            .value_counts()
        )

        if not x.empty:

            bidang = x.index[0]
            jumlah = int(x.iloc[0])
            persen = percentage(
                jumlah,
                total
            )

            insights.append(
                (
                    "🏭 Bidang Usaha Dominan — "
                    f"{bidang} menjadi kategori dengan "
                    f"bimbingan terbanyak, yaitu "
                    f"{format_number(jumlah)} kegiatan "
                    f"({persen:.1f}%)."
                )
            )


    # Wilayah

    if "NAMA KABUPATEN/KOTA" in df.columns:

        x = (
            df["NAMA KABUPATEN/KOTA"]
            .fillna("Tidak Diisi")
            .value_counts()
        )

        if not x.empty:

            wilayah = x.index[0]
            jumlah = int(x.iloc[0])

            insights.append(
                (
                    "📍 Wilayah Dominan — "
                    f"{wilayah} menjadi wilayah dengan "
                    f"kegiatan bimbingan terbanyak, "
                    f"yaitu {format_number(jumlah)} kegiatan."
                )
            )


    # Bulan

    if "Bulan Bimbingan" in df.columns:

        x = (
            df["Bulan Bimbingan"]
            .value_counts()
            .reindex(MONTHS)
            .fillna(0)
        )

        if x.max() > 0:

            bulan = x.idxmax()
            jumlah = int(x.max())

            insights.append(
                (
                    "📅 Bulan Tertinggi — "
                    f"Aktivitas bimbingan tertinggi terjadi "
                    f"pada {bulan}, sebanyak "
                    f"{format_number(jumlah)} kegiatan."
                )
            )


    return insights


# =========================================================
# EXPORT PDF HASIL DASHBOARD
# =========================================================

def _pdf_text(text):
    """Bersihkan markdown sederhana dari insight sebelum dimasukkan ke PDF."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", str(text))
    return text.replace("—", "-").replace("📌", "").strip()


def _save_chart_png(fig):
    """Simpan matplotlib figure ke memory agar bisa dimasukkan ke PDF."""
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


def _matplotlib_training_charts(df):
    charts = []
    # Tren peserta
    x = monthly_data(df, "Bulan Pelatihan", "Peserta")
    if not x.empty:
        fig, ax = plt.subplots(figsize=(8.0, 3.8))
        ax.plot(x["Bulan"], x["Peserta"], marker="o")
        ax.set_title("Peserta per Bulan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Peserta")
        ax.tick_params(axis="x", rotation=45)
        charts.append(_save_chart_png(fig))

    # Top provinsi
    if "Provinsi" in df.columns:
        x = df["Provinsi"].fillna("Tidak Diisi").value_counts().head(10).sort_values()
        if not x.empty:
            fig, ax = plt.subplots(figsize=(8.0, 4.2))
            ax.barh(x.index.astype(str), x.values)
            ax.set_title("Top 10 Provinsi")
            ax.set_xlabel("Peserta")
            charts.append(_save_chart_png(fig))

    # Kelulusan
    if "Status KeLulusan" in df.columns:
        x = df["Status KeLulusan"].fillna("Tidak Diisi").value_counts()
        if not x.empty:
            fig, ax = plt.subplots(figsize=(6.5, 4.0))
            ax.pie(x.values, labels=x.index.astype(str), autopct="%1.1f%%")
            ax.set_title("Status Kelulusan")
            charts.append(_save_chart_png(fig))

    # Metode
    if "Metode Pelatihan" in df.columns:
        x = df["Metode Pelatihan"].fillna("Tidak Diisi").value_counts()
        if not x.empty:
            fig, ax = plt.subplots(figsize=(7.0, 4.0))
            ax.bar(x.index.astype(str), x.values)
            ax.set_title("Metode Pelatihan")
            ax.set_ylabel("Peserta")
            ax.tick_params(axis="x", rotation=25)
            charts.append(_save_chart_png(fig))
    return charts


def _matplotlib_bim_charts(df):
    charts = []
    # Tren bimbingan
    x = monthly_data(df, "Bulan Bimbingan", "Kegiatan")
    if not x.empty:
        fig, ax = plt.subplots(figsize=(8.0, 3.8))
        ax.plot(x["Bulan"], x["Kegiatan"], marker="o")
        ax.set_title("Tren Bimbingan Konsultasi")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Kegiatan")
        ax.tick_params(axis="x", rotation=45)
        charts.append(_save_chart_png(fig))

    # Bidang usaha
    if "Bidang Usaha Kategori" in df.columns:
        x = df["Bidang Usaha Kategori"].fillna("Tidak Diisi").value_counts().sort_values()
        if not x.empty:
            fig, ax = plt.subplots(figsize=(8.0, 4.2))
            ax.barh(x.index.astype(str), x.values)
            ax.set_title("Kegiatan Berdasarkan Bidang Usaha")
            ax.set_xlabel("Kegiatan")
            charts.append(_save_chart_png(fig))

    # Wilayah
    for col in ["NAMA KABUPATEN/KOTA", "Kabupaten/Kota", "NAMA KABUPATEN / KOTA"]:
        if col in df.columns:
            x = df[col].fillna("Tidak Diisi").value_counts().head(10).sort_values()
            if not x.empty:
                fig, ax = plt.subplots(figsize=(8.0, 4.2))
                ax.barh(x.index.astype(str), x.values)
                ax.set_title("Top 10 Wilayah")
                ax.set_xlabel("Kegiatan")
                charts.append(_save_chart_png(fig))
            break
    return charts


def create_dashboard_pdf(training_df=None, bim_df=None, rekap_df=None, rekap_bim_df=None, title="Hasil Analisis Dashboard Produktivitas 2026"):
    """Membuat PDF visual dari hasil dashboard sesuai filter aktif."""
    output = BytesIO()
    doc = SimpleDocTemplate(
        output, pagesize=A4,
        rightMargin=1.4*cm, leftMargin=1.4*cm,
        topMargin=1.3*cm, bottomMargin=1.3*cm
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="PdfTitle", parent=styles["Title"], alignment=TA_CENTER, fontSize=17, leading=21, spaceAfter=8))
    styles.add(ParagraphStyle(name="PdfSub", parent=styles["Normal"], alignment=TA_CENTER, fontSize=9, textColor=colors.grey, spaceAfter=12))
    styles.add(ParagraphStyle(name="PdfHead", parent=styles["Heading2"], fontSize=13, leading=16, spaceBefore=8, spaceAfter=7))
    styles.add(ParagraphStyle(name="PdfBody", parent=styles["BodyText"], fontSize=9, leading=13, spaceAfter=5))
    styles.add(ParagraphStyle(name="PdfSmall", parent=styles["BodyText"], fontSize=8, leading=11, spaceAfter=4))

    story = [Paragraph(title, styles["PdfTitle"]),
             Paragraph("Laporan visual berdasarkan data dan filter yang sedang aktif pada dashboard.", styles["PdfSub"])]

    def add_kpis(items):
        data = [[Paragraph(f"<b>{k}</b><br/>{v}", styles["PdfSmall"]) for k, v in items]]
        table = Table(data, colWidths=[(A4[0]-2.8*cm)/len(items)]*len(items))
        table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ]))
        story.extend([table, Spacer(1, 8)])

    if training_df is not None and not training_df.empty:
        df = training_df
        story.append(Paragraph("🎓 Pelatihan Produktivitas", styles["PdfHead"]))
        add_kpis([
            ("Total Peserta", format_number(len(df))),
            ("Total Program", format_number(df["Judul Program Pelatihan"].nunique() if "Judul Program Pelatihan" in df.columns else 0)),
            ("Total Provinsi", format_number(df["Provinsi"].nunique() if "Provinsi" in df.columns else 0)),
            ("Total Lembaga", format_number(df["Nama Lembaga"].nunique() if "Nama Lembaga" in df.columns else 0)),
        ])
        story.append(Paragraph("Analisis Grafik", styles["PdfHead"]))
        charts = _matplotlib_training_charts(df)
        for i, chart in enumerate(charts):
            story.append(Image(chart, width=16.5*cm, height=8.0*cm))
            if i < len(charts)-1: story.append(Spacer(1, 5))
        story.append(Paragraph("Insight Otomatis", styles["PdfHead"]))
        for text in insights_training(df):
            story.append(Paragraph("• " + _pdf_text(text), styles["PdfBody"]))
        story.append(Paragraph("Kesimpulan", styles["PdfHead"]))
        story.append(Paragraph("Analisis pelatihan menggambarkan jumlah peserta, program, pemerataan provinsi dan lembaga, serta pola kelulusan dan metode pelatihan berdasarkan filter yang dipilih.", styles["PdfBody"]))

    if rekap_df is not None and not rekap_df.empty:
        story.append(PageBreak())
        story.append(Paragraph("🏢 Status Realisasi Lembaga", styles["PdfHead"]))
        sudah = rekap_df[rekap_df["Status Realisasi"] == "Sudah Terealisasi"]
        belum = rekap_df[rekap_df["Status Realisasi"] == "Belum Terealisasi"]
        pct_sudah = (len(sudah) / len(rekap_df) * 100) if len(rekap_df) else 0
        add_kpis([
            ("Sudah Terealisasi", format_number(len(sudah))),
            ("Belum Terealisasi", format_number(len(belum))),
            ("Persentase Terealisasi", f"{pct_sudah:.1f}%")
        ])
        table_data = [["Lembaga/Instansi", "Target", "Realisasi", "Status"]]
        for _, row in rekap_df.sort_values(["Status Realisasi", "Lembaga/Instansi"]).iterrows():
            table_data.append([
                _pdf_text(row.get("Lembaga/Instansi", "")),
                format_number(row.get("Target Pelatihan P3", 0)),
                format_number(row.get("Realisasi Pelatihan P3", 0)),
                _pdf_text(row.get("Status Realisasi", ""))
            ])
        table = Table(table_data, colWidths=[8.0*cm, 2.0*cm, 2.0*cm, 4.0*cm], repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#EAF2F8")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#17365D")),
            ("GRID", (0,0), (-1,-1), 0.4, colors.lightgrey),
            ("FONTSIZE", (0,0), (-1,-1), 7.5),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        story.append(table)

    if rekap_bim_df is not None and not rekap_bim_df.empty:
        story.append(PageBreak())
        story.append(Paragraph("🏢 Status Realisasi Bimbingan Konsultasi", styles["PdfHead"]))
        sudah = rekap_bim_df[rekap_bim_df["Status Realisasi"] == "Sudah Terealisasi"]
        belum = rekap_bim_df[rekap_bim_df["Status Realisasi"] == "Belum Terealisasi"]
        pct_sudah = (len(sudah) / len(rekap_bim_df) * 100) if len(rekap_bim_df) else 0
        add_kpis([
            ("Sudah Terealisasi", format_number(len(sudah))),
            ("Belum Terealisasi", format_number(len(belum))),
            ("Persentase Terealisasi", f"{pct_sudah:.1f}%")
        ])
        table_data = [["Lembaga/Instansi", "Target Perusahaan", "Realisasi", "Status"]]
        for _, row in rekap_bim_df.sort_values(["Status Realisasi", "Lembaga/Instansi"]).iterrows():
            table_data.append([
                _pdf_text(row.get("Lembaga/Instansi", "")),
                format_number(row.get("Target Perusahaan", 0)),
                format_number(row.get("Realisasi Bimbingan", 0)),
                _pdf_text(row.get("Status Realisasi", ""))
            ])
        table = Table(table_data, colWidths=[7.0*cm, 3.0*cm, 2.0*cm, 4.0*cm], repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#EAF2F8")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#17365D")),
            ("GRID", (0,0), (-1,-1), 0.4, colors.lightgrey),
            ("FONTSIZE", (0,0), (-1,-1), 7.5),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        story.append(table)

    if bim_df is not None and not bim_df.empty:
        if training_df is not None and not training_df.empty:
            story.append(PageBreak())
        df = bim_df
        story.append(Paragraph("🤝 Bimbingan Konsultasi", styles["PdfHead"]))
        add_kpis([
            ("Total Kegiatan", format_number(len(df))),
            ("Total Perusahaan", format_number(df["NAMA PERUSAHAAN"].nunique() if "NAMA PERUSAHAAN" in df.columns else 0)),
            ("Total Wilayah", format_number(df["NAMA KABUPATEN/KOTA"].nunique() if "NAMA KABUPATEN/KOTA" in df.columns else 0)),
            ("Bidang Usaha", format_number(df["Bidang Usaha Kategori"].nunique() if "Bidang Usaha Kategori" in df.columns else 0)),
        ])
        story.append(Paragraph("Analisis Grafik", styles["PdfHead"]))
        charts = _matplotlib_bim_charts(df)
        for i, chart in enumerate(charts):
            story.append(Image(chart, width=16.5*cm, height=8.0*cm))
            if i < len(charts)-1: story.append(Spacer(1, 5))
        story.append(Paragraph("Insight Otomatis", styles["PdfHead"]))
        for text in insights_bim(df):
            story.append(Paragraph("• " + _pdf_text(text), styles["PdfBody"]))
        story.append(Paragraph("Kesimpulan", styles["PdfHead"]))
        story.append(Paragraph("Analisis bimbingan memberikan gambaran mengenai konsentrasi kegiatan berdasarkan bidang usaha, wilayah, dan waktu pelaksanaan untuk mendukung monitoring dan evaluasi pendampingan.", styles["PdfBody"]))

    if not story:
        story.append(Paragraph("Tidak ada data sesuai filter.", styles["PdfBody"]))
    doc.build(story)
    output.seek(0)
    return output.getvalue()


# =========================================================
# EXPORT HASIL ANALISIS
# =========================================================

def create_analysis_excel(
    training_df=None,
    bim_df=None
):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:


        # =================================================
        # PELATIHAN
        # =================================================

        if (
            training_df is not None
            and not training_df.empty
        ):

            # Data filter

            training_df.to_excel(
                writer,
                sheet_name="Data Pelatihan",
                index=False
            )


            # KPI

            total_peserta = len(
                training_df
            )

            total_program = (
                training_df[
                    "Judul Program Pelatihan"
                ].nunique()
                if "Judul Program Pelatihan"
                in training_df.columns
                else 0
            )

            total_provinsi = (
                training_df[
                    "Provinsi"
                ].nunique()
                if "Provinsi"
                in training_df.columns
                else 0
            )

            total_lembaga = (
                training_df[
                    "Nama Lembaga"
                ].nunique()
                if "Nama Lembaga"
                in training_df.columns
                else 0
            )


            kpi = pd.DataFrame({

                "Indikator": [

                    "Total Peserta",
                    "Total Program",
                    "Total Provinsi",
                    "Total Lembaga"

                ],

                "Nilai": [

                    total_peserta,
                    total_program,
                    total_provinsi,
                    total_lembaga

                ]

            })


            kpi.to_excel(
                writer,
                sheet_name="KPI Pelatihan",
                index=False
            )


            # Peserta per bulan

            bulanan = monthly_data(
                training_df,
                "Bulan Pelatihan",
                "Jumlah Peserta"
            )

            bulanan.to_excel(
                writer,
                sheet_name="Peserta per Bulan",
                index=False
            )


            # Provinsi

            if "Provinsi" in training_df.columns:

                provinsi = (
                    training_df["Provinsi"]
                    .fillna("Tidak Diisi")
                    .value_counts()
                    .reset_index()
                )

                provinsi.columns = [
                    "Provinsi",
                    "Jumlah Peserta"
                ]

                provinsi.to_excel(
                    writer,
                    sheet_name="Peserta per Provinsi",
                    index=False
                )


            # Kelulusan

            if "Status KeLulusan" in training_df.columns:

                status = (
                    training_df["Status KeLulusan"]
                    .fillna("Tidak Diisi")
                    .value_counts()
                    .reset_index()
                )

                status.columns = [
                    "Status Kelulusan",
                    "Jumlah"
                ]

                status.to_excel(
                    writer,
                    sheet_name="Status Kelulusan",
                    index=False
                )


            # Metode

            if "Metode Pelatihan" in training_df.columns:

                metode = (
                    training_df["Metode Pelatihan"]
                    .fillna("Tidak Diisi")
                    .value_counts()
                    .reset_index()
                )

                metode.columns = [
                    "Metode Pelatihan",
                    "Jumlah"
                ]

                metode.to_excel(
                    writer,
                    sheet_name="Metode Pelatihan",
                    index=False
                )


            # Insight

            insight_text = insights_training(
                training_df
            )

            insight_df = pd.DataFrame({

                "Insight": [
                    x.replace("**", "")
                    for x in insight_text
                ]

            })

            insight_df.to_excel(
                writer,
                sheet_name="Insight Analisis",
                index=False
            )


        # =================================================
        # BIMBINGAN
        # =================================================

        if (
            bim_df is not None
            and not bim_df.empty
        ):

            bim_df.to_excel(
                writer,
                sheet_name="Data Bimbingan",
                index=False
            )


            total_kegiatan = len(
                bim_df
            )

            total_perusahaan = (
                bim_df[
                    "NAMA PERUSAHAAN"
                ].nunique()
                if "NAMA PERUSAHAAN"
                in bim_df.columns
                else 0
            )

            total_wilayah = (
                bim_df[
                    "NAMA KABUPATEN/KOTA"
                ].nunique()
                if "NAMA KABUPATEN/KOTA"
                in bim_df.columns
                else 0
            )

            total_bidang = (
                bim_df[
                    "Bidang Usaha Kategori"
                ].nunique()
                if "Bidang Usaha Kategori"
                in bim_df.columns
                else 0
            )


            kpi = pd.DataFrame({

                "Indikator": [

                    "Total Kegiatan",
                    "Total Perusahaan",
                    "Total Wilayah",
                    "Kategori Bidang Usaha"

                ],

                "Nilai": [

                    total_kegiatan,
                    total_perusahaan,
                    total_wilayah,
                    total_bidang

                ]

            })


            kpi.to_excel(
                writer,
                sheet_name="KPI Bimbingan",
                index=False
            )


            # Bulanan

            bulanan = monthly_data(
                bim_df,
                "Bulan Bimbingan",
                "Jumlah Kegiatan"
            )

            bulanan.to_excel(
                writer,
                sheet_name="Bimbingan per Bulan",
                index=False
            )


            # Bidang usaha

            if "Bidang Usaha Kategori" in bim_df.columns:

                bidang = (
                    bim_df[
                        "Bidang Usaha Kategori"
                    ]
                    .fillna("Tidak Diisi")
                    .value_counts()
                    .reset_index()
                )

                bidang.columns = [
                    "Bidang Usaha",
                    "Jumlah Kegiatan"
                ]

                bidang.to_excel(
                    writer,
                    sheet_name="Bidang Usaha",
                    index=False
                )


            # Wilayah

            if "NAMA KABUPATEN/KOTA" in bim_df.columns:

                wilayah = (
                    bim_df[
                        "NAMA KABUPATEN/KOTA"
                    ]
                    .fillna("Tidak Diisi")
                    .value_counts()
                    .reset_index()
                )

                wilayah.columns = [
                    "Wilayah",
                    "Jumlah Kegiatan"
                ]

                wilayah.to_excel(
                    writer,
                    sheet_name="Wilayah",
                    index=False
                )


            # Insight

            insight_text = insights_bim(
                bim_df
            )

            insight_df = pd.DataFrame({

                "Insight": [
                    x.replace("**", "")
                    for x in insight_text
                ]

            })

            insight_df.to_excel(
                writer,
                sheet_name="Insight Analisis",
                index=False
            )


    return output.getvalue()


# =========================================================
# HALAMAN AWAL / PEMILIHAN FILE
# =========================================================
# Halaman pembuka hanya ditampilkan sebelum file Excel dipilih.
# Setelah file dipilih, aplikasi langsung masuk ke menu dashboard.

if "excel_files" not in st.session_state:
    st.session_state.excel_files = []

if not st.session_state.excel_files:
    st.markdown("### MONITORING PROGRAM • 2026")

    hero_left, hero_right = st.columns([1.35, 0.65], gap="large", vertical_alignment="center")

    with hero_left:
        st.markdown("# Dashboard Produktivitas 2026")
        st.markdown("### Pelatihan Produktivitas & Bimbingan Konsultasi")
        st.write(
            "Platform monitoring dan analisis untuk melihat capaian program, "
            "sebaran kegiatan, realisasi lembaga, serta temuan utama sebagai "
            "bahan evaluasi dan pengambilan keputusan."
        )

    with hero_right:
        with st.container(border=True):
            st.markdown("#### 📊 Monitoring & Evaluasi")
            st.markdown("**Pelatihan**  •  **Bimbingan**")
            st.markdown("**Realisasi**  •  **Insight**")
            st.caption("Data dianalisis langsung dari file Excel yang Anda unggah.")

    st.divider()

    st.markdown("### Fokus Dashboard")
    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        with st.container(border=True):
            st.markdown("#### 🎓 Pelatihan")
            st.caption("Peserta, program, provinsi, metode dan kelulusan.")

    with c2:
        with st.container(border=True):
            st.markdown("#### 🤝 Bimbingan")
            st.caption("Perusahaan, wilayah, bidang usaha dan kegiatan.")

    with c3:
        with st.container(border=True):
            st.markdown("#### 🏢 Realisasi")
            st.caption("Lembaga yang sudah dan belum terealisasi.")

    with c4:
        with st.container(border=True):
            st.markdown("#### 💡 Insight")
            st.caption("Temuan utama, tren dan ringkasan analisis.")

    st.divider()

    st.markdown("### Mulai Analisis Data")
    st.caption(
        "Upload satu atau beberapa file Excel. Data dari file-file yang dipilih "
        "akan dibersihkan dan digabungkan secara otomatis."
    )

    upload_box = st.container(border=True)
    with upload_box:
        uploaded = st.file_uploader(
            "Upload File Excel (bisa beberapa file)",
            type=["xlsx"],
            accept_multiple_files=True,
            help="Pilih satu atau beberapa file Excel data produktivitas.",
            key="excel_uploader"
        )

    if not uploaded:
        st.info("Pilih satu atau beberapa file Excel untuk melanjutkan ke dashboard analisis.")
        st.stop()

    st.session_state.excel_files = [
        (file.name, file.getvalue())
        for file in uploaded
    ]
    st.session_state.excel_names = [file.name for file in uploaded]
    st.rerun()


# File yang sudah dipilih disimpan di session agar halaman pembuka tidak
# muncul lagi ketika pengguna berpindah menu.
file_items = st.session_state.excel_files

# =========================================================
# PROSES DATA
# =========================================================

with st.spinner(
    "⏳ Membaca dan membersihkan data dari semua file..."
):
    train, bim, rekap, rekap_bim = process_uploaded_files(file_items)


st.success(
    f"✅ {format_number(len(file_items))} file berhasil diproses — "
    f"{format_number(len(train))} data pelatihan dan "
    f"{format_number(len(bim))} data bimbingan."
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "## 📊 Dashboard"
)

st.sidebar.caption(
    "Analisis Produktivitas 2026"
)

st.sidebar.divider()


page = st.sidebar.radio(
    "Menu",
    [
        "🏠 Overview",
        "🎓 Pelatihan Produktivitas",
        "🤝 Bimbingan Konsultasi",
        "📋 Data Detail"
    ]
)


st.sidebar.divider()

# File Excel hanya dipilih pada halaman awal agar sidebar tetap bersih.
# Tidak ada uploader tambahan di atas filter.


# =========================================================
# OVERVIEW
# =========================================================

if page == "🏠 Overview":

    st.header("🏠 Overview Produktivitas 2026")
    st.caption("Ringkasan pelaksanaan Pelatihan Produktivitas dan Bimbingan Konsultasi")
    st.divider()


    total_program = (

        train[
            "Judul Program Pelatihan"
        ].nunique()

        if "Judul Program Pelatihan"
        in train.columns

        else 0
    )


    total_perusahaan = (

        bim[
            "NAMA PERUSAHAAN"
        ].nunique()

        if "NAMA PERUSAHAAN"
        in bim.columns

        else 0
    )


    a, b, c, d = st.columns(4)


    with a:

        st.metric(
            "👥 Total Peserta",
            format_number(
                len(train)
            )
        )


    with b:

        st.metric(
            "📚 Total Program",
            format_number(
                total_program
            )
        )


    with c:

        st.metric(
            "🤝 Total Bimbingan",
            format_number(
                len(bim)
            )
        )


    with d:

        st.metric(
            "🏢 Total Perusahaan",
            format_number(
                total_perusahaan
            )
        )


    st.markdown(
        "### 📈 Gambaran Aktivitas"
    )


    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # PESERTA
    # -----------------------------------------------------

    with col1:

        x = monthly_data(
            train,
            "Bulan Pelatihan",
            "Peserta"
        )

        fig = px.line(
            x,
            x="Bulan",
            y="Peserta",
            markers=True,
            text="Peserta",
            title="🎓 Tren Peserta Pelatihan"
        )

        fig.update_traces(
            line_width=4,
            textposition="top center"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


    # -----------------------------------------------------
    # BIMBINGAN
    # -----------------------------------------------------

    with col2:

        x = monthly_data(
            bim,
            "Bulan Bimbingan",
            "Kegiatan"
        )

        fig = px.bar(
            x,
            x="Bulan",
            y="Kegiatan",
            text="Kegiatan",
            title="🤝 Tren Bimbingan Konsultasi"
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


    # -----------------------------------------------------
    # INSIGHT
    # -----------------------------------------------------

    st.markdown(
        "### 💡 Temuan Utama"
    )


    ta = insights_training(
        train
    )

    ba = insights_bim(
        bim
    )


    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            "#### 🎓 Pelatihan"
        )

        for text in ta:
            with st.container(border=True):
                st.markdown(text.replace("**", ""))


    with col2:

        st.markdown(
            "#### 🤝 Bimbingan"
        )

        for text in ba:
            with st.container(border=True):
                st.markdown(text.replace("**", ""))


    # -----------------------------------------------------
    # KESIMPULAN
    # -----------------------------------------------------

    st.subheader("🎯 Kesimpulan Analisis")
    st.info(
        "Dashboard memberikan gambaran mengenai jumlah peserta, program pelatihan, "
        "wilayah, kegiatan bimbingan, perusahaan, bidang usaha, serta perkembangan "
        "aktivitas sepanjang periode data yang tersedia.\n\n"
        "Informasi tersebut dapat digunakan sebagai dasar monitoring, evaluasi, "
        "dan penyusunan laporan pelaksanaan program produktivitas."
    )


# =========================================================
# PELATIHAN
# =========================================================

elif page == "🎓 Pelatihan Produktivitas":

    st.header("🎓 Pelatihan Produktivitas")
    st.caption("Analisis peserta, program, provinsi, kelulusan, dan metode pelatihan")
    st.divider()


    st.sidebar.markdown(
        "### 🔎 Filter Pelatihan"
    )


    f = train.copy()


    # Filter

    for col, label, key in [

        (
            "Tahun Pelatihan",
            "Tahun",
            "train_year"
        ),

        (
            "Provinsi",
            "Provinsi",
            "train_province"
        ),

        (
            "Metode Pelatihan",
            "Metode",
            "train_method"
        ),

        (
            "Jenis Pelatihan",
            "Jenis Pelatihan",
            "train_type"
        ),

        (
            "Status KeLulusan",
            "Status Kelulusan",
            "train_status"
        )

    ]:

        f = selectbox_filter(
            f,
            col,
            label,
            key
        )


    st.caption(
        f"📌 Menampilkan **{format_number(len(f))} peserta** "
        "sesuai filter."
    )


    # -----------------------------------------------------
    # KPI
    # -----------------------------------------------------

    a, b, c, d = st.columns(4)


    with a:

        st.metric(
            "👥 Total Peserta",
            format_number(
                len(f)
            )
        )


    with b:

        total_program = (

            f[
                "Judul Program Pelatihan"
            ].nunique()

            if "Judul Program Pelatihan"
            in f.columns

            else 0
        )

        st.metric(
            "📚 Total Program",
            format_number(
                total_program
            )
        )


    with c:

        total_provinsi = (

            f[
                "Provinsi"
            ].nunique()

            if "Provinsi"
            in f.columns

            else 0
        )

        st.metric(
            "📍 Total Provinsi",
            format_number(
                total_provinsi
            )
        )


    with d:

        total_lembaga = (

            f[
                "Nama Lembaga"
            ].nunique()

            if "Nama Lembaga"
            in f.columns

            else 0
        )

        st.metric(
            "🏢 Total Lembaga",
            format_number(
                total_lembaga
            )
        )


    # -----------------------------------------------------
    # STATUS REALISASI LEMBAGA
    # -----------------------------------------------------

    st.markdown("### 🏢 Status Realisasi Lembaga")
    st.caption(
        "Menunjukkan lembaga/instansi yang sudah memiliki realisasi pelatihan P3 dan yang belum terealisasi."
    )

    if not rekap.empty:
        sudah = rekap[rekap["Status Realisasi"] == "Sudah Terealisasi"].copy()
        belum = rekap[rekap["Status Realisasi"] == "Belum Terealisasi"].copy()
        total_lembaga_rekap = len(rekap)
        pct_sudah = (len(sudah) / total_lembaga_rekap * 100) if total_lembaga_rekap else 0

        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("Sudah Terealisasi", format_number(len(sudah)))
        with r2:
            st.metric("Belum Terealisasi", format_number(len(belum)))
        with r3:
            st.metric("Persentase Lembaga Terealisasi", f"{pct_sudah:.1f}%")

        status_chart = pd.DataFrame({
            "Status": ["Sudah Terealisasi", "Belum Terealisasi"],
            "Jumlah Lembaga": [len(sudah), len(belum)]
        })
        fig_status = px.bar(
            status_chart, x="Status", y="Jumlah Lembaga",
            text="Jumlah Lembaga", title="Status Realisasi Lembaga/Instansi"
        )
        fig_status.update_traces(textposition="outside")
        st.plotly_chart(style_chart(fig_status, 350), use_container_width=True)

        t1, t2 = st.columns(2)
        with t1:
            st.markdown("#### ✅ Sudah Terealisasi")
            cols = [c for c in ["Lembaga/Instansi", "Target Pelatihan P3", "Realisasi Pelatihan P3", "Persentase Realisasi"] if c in sudah.columns]
            st.dataframe(sudah[cols].sort_values("Realisasi Pelatihan P3", ascending=False), use_container_width=True, hide_index=True)

        with t2:
            st.markdown("#### ⏳ Belum Terealisasi")
            cols = [c for c in ["Lembaga/Instansi", "Target Pelatihan P3", "Realisasi Pelatihan P3", "Persentase Realisasi"] if c in belum.columns]
            st.dataframe(belum[cols].sort_values("Lembaga/Instansi"), use_container_width=True, hide_index=True)
    else:
        st.info(
            "Data rekap realisasi lembaga belum tersedia pada file Excel. Pastikan terdapat sheet **Rekap Pel Prod** dengan kolom Lembaga/Instansi, Target, dan Realisasi."
        )


    # -----------------------------------------------------
    # ANALISIS
    # -----------------------------------------------------

    st.markdown(
        "### 📊 Analisis Pelatihan"
    )


    col1, col2 = st.columns(2)


    # Tren peserta

    with col1:

        x = monthly_data(
            f,
            "Bulan Pelatihan",
            "Peserta"
        )

        fig = px.line(
            x,
            x="Bulan",
            y="Peserta",
            markers=True,
            text="Peserta",
            title="📈 Peserta per Bulan"
        )

        fig.update_traces(
            line_width=4,
            textposition="top center"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


    # Top provinsi

    with col2:

        if "Provinsi" in f.columns:

            x = (
                f["Provinsi"]
                .fillna("Tidak Diisi")
                .value_counts()
                .head(10)
                .sort_values()
                .reset_index()
            )

            x.columns = [
                "Provinsi",
                "Peserta"
            ]

            fig = px.bar(
                x,
                x="Peserta",
                y="Provinsi",
                orientation="h",
                text="Peserta",
                title="🏆 Top 10 Provinsi"
            )

            fig.update_traces(
                textposition="outside"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


    # -----------------------------------------------------
    # STATUS + METODE
    # -----------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        if "Status KeLulusan" in f.columns:

            x = (
                f[
                    "Status KeLulusan"
                ]
                .fillna("Tidak Diisi")
                .value_counts()
                .reset_index()
            )

            x.columns = [
                "Status",
                "Jumlah"
            ]

            fig = px.pie(
                x,
                names="Status",
                values="Jumlah",
                hole=0.55,
                title="🎓 Status Kelulusan"
            )

            fig.update_traces(
                textinfo="percent+label"
            )

            st.plotly_chart(
                style_chart(fig, 350),
                use_container_width=True
            )


    with col2:

        if "Metode Pelatihan" in f.columns:

            x = (
                f[
                    "Metode Pelatihan"
                ]
                .fillna("Tidak Diisi")
                .value_counts()
                .reset_index()
            )

            x.columns = [
                "Metode",
                "Jumlah"
            ]

            fig = px.bar(
                x,
                x="Metode",
                y="Jumlah",
                text="Jumlah",
                title="⚙️ Metode Pelatihan"
            )

            fig.update_traces(
                textposition="outside"
            )

            st.plotly_chart(
                style_chart(fig, 350),
                use_container_width=True
            )


    # -----------------------------------------------------
    # INSIGHT
    # -----------------------------------------------------

    st.markdown(
        "### 💡 Insight Otomatis"
    )


    if f.empty:

        st.warning(
            "Tidak ada data sesuai filter."
        )

    else:

        for text in insights_training(f):

            st.info(text.replace("**", ""))


    # -----------------------------------------------------
    # DOWNLOAD HASIL ANALISIS
    # -----------------------------------------------------

    st.subheader("📥 Download Hasil Analisis")
    st.caption(
        "Download PDF berisi hasil akhir dashboard sesuai filter aktif: KPI, grafik, "
        "insight, dan kesimpulan analisis."
    )

    if not f.empty:
        pdf_training = create_dashboard_pdf(training_df=f, rekap_df=rekap)
        st.download_button(
            label="📄 Download Hasil Dashboard Pelatihan (PDF)",
            data=pdf_training,
            file_name="Hasil_Dashboard_Pelatihan_Produktivitas_2026.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# =========================================================
# BIMBINGAN
# =========================================================

elif page == "🤝 Bimbingan Konsultasi":

    st.header("🤝 Bimbingan Konsultasi")
    st.caption("Analisis kegiatan, perusahaan, wilayah, bidang usaha, dan pelaksana")
    st.divider()


    st.sidebar.markdown(
        "### 🔎 Filter Bimbingan"
    )


    f = bim.copy()


    for col, label, key in [

        (
            "Bidang Usaha Kategori",
            "Bidang Usaha",
            "bim_business"
        ),

        (
            "NAMA KABUPATEN/KOTA",
            "Kabupaten/Kota",
            "bim_region"
        ),

        (
            "PELAKSANA",
            "Pelaksana",
            "bim_executor"
        ),

        (
            "Tahun Bimbingan",
            "Tahun",
            "bim_year"
        )

    ]:

        f = selectbox_filter(
            f,
            col,
            label,
            key
        )


    st.caption(
        f"📌 Menampilkan **{format_number(len(f))} kegiatan** "
        "sesuai filter."
    )


    # -----------------------------------------------------
    # KPI
    # -----------------------------------------------------

    a, b, c, d = st.columns(4)


    with a:

        st.metric(
            "📋 Total Kegiatan",
            format_number(
                len(f)
            )
        )


    with b:

        total_perusahaan = (

            f[
                "NAMA PERUSAHAAN"
            ].nunique()

            if "NAMA PERUSAHAAN"
            in f.columns

            else 0
        )

        st.metric(
            "🏢 Total Perusahaan",
            format_number(
                total_perusahaan
            )
        )


    with c:

        total_wilayah = (

            f[
                "NAMA KABUPATEN/KOTA"
            ].nunique()

            if "NAMA KABUPATEN/KOTA"
            in f.columns

            else 0
        )

        st.metric(
            "📍 Total Wilayah",
            format_number(
                total_wilayah
            )
        )


    with d:

        total_bidang = (

            f[
                "Bidang Usaha Kategori"
            ].nunique()

            if "Bidang Usaha Kategori"
            in f.columns

            else 0
        )

        st.metric(
            "🏭 Bidang Usaha",
            format_number(
                total_bidang
            )
        )


    # -----------------------------------------------------
    # STATUS REALISASI LEMBAGA / INSTANSI
    # -----------------------------------------------------

    st.markdown("### 🏢 Status Realisasi Bimbingan Konsultasi")
    st.caption(
        "Menunjukkan lembaga/instansi yang sudah memiliki realisasi bimbingan konsultasi dan yang belum terealisasi."
    )

    if not rekap_bim.empty:
        sudah_bim = rekap_bim[
            rekap_bim["Status Realisasi"] == "Sudah Terealisasi"
        ].copy()
        belum_bim = rekap_bim[
            rekap_bim["Status Realisasi"] == "Belum Terealisasi"
        ].copy()
        total_rekap_bim = len(rekap_bim)
        pct_sudah_bim = (
            len(sudah_bim) / total_rekap_bim * 100
            if total_rekap_bim else 0
        )

        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("Sudah Terealisasi", format_number(len(sudah_bim)))
        with r2:
            st.metric("Belum Terealisasi", format_number(len(belum_bim)))
        with r3:
            st.metric(
                "Persentase Lembaga Terealisasi",
                f"{pct_sudah_bim:.1f}%"
            )

        status_bim_chart = pd.DataFrame({
            "Status": ["Sudah Terealisasi", "Belum Terealisasi"],
            "Jumlah Lembaga": [len(sudah_bim), len(belum_bim)]
        })
        fig_status_bim = px.bar(
            status_bim_chart,
            x="Status",
            y="Jumlah Lembaga",
            text="Jumlah Lembaga",
            title="Status Realisasi Bimbingan Konsultasi"
        )
        fig_status_bim.update_traces(textposition="outside")
        st.plotly_chart(
            style_chart(fig_status_bim, 350),
            use_container_width=True
        )

        t1, t2 = st.columns(2)
        with t1:
            st.markdown("#### ✅ Sudah Terealisasi")
            cols_bim = [
                c for c in [
                    "Lembaga/Instansi",
                    "Target Perusahaan",
                    "Realisasi Bimbingan",
                    "Persentase Realisasi"
                ] if c in sudah_bim.columns
            ]
            st.dataframe(
                sudah_bim[cols_bim].sort_values(
                    "Realisasi Bimbingan", ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

        with t2:
            st.markdown("#### ⏳ Belum Terealisasi")
            cols_bim = [
                c for c in [
                    "Lembaga/Instansi",
                    "Target Perusahaan",
                    "Realisasi Bimbingan",
                    "Persentase Realisasi"
                ] if c in belum_bim.columns
            ]
            st.dataframe(
                belum_bim[cols_bim].sort_values(
                    "Lembaga/Instansi"
                ),
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info(
            "Data rekap realisasi bimbingan belum tersedia. Pastikan terdapat sheet "
            "**Rekap Bimkon** dengan kolom Lembaga/Instansi, Target Perusahaan, dan Realisasi."
        )


    # -----------------------------------------------------
    # GRAFIK
    # -----------------------------------------------------

    st.markdown(
        "### 📊 Analisis Bimbingan"
    )


    col1, col2 = st.columns(2)


    # Bidang usaha

    with col1:

        if "Bidang Usaha Kategori" in f.columns:

            x = (
                f[
                    "Bidang Usaha Kategori"
                ]
                .fillna("Tidak Diisi")
                .value_counts()
                .sort_values()
                .reset_index()
            )

            x.columns = [
                "Bidang Usaha",
                "Jumlah"
            ]

            fig = px.bar(
                x,
                x="Jumlah",
                y="Bidang Usaha",
                orientation="h",
                text="Jumlah",
                title="🏭 Bimbingan per Bidang Usaha"
            )

            fig.update_traces(
                textposition="outside"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


    # Wilayah

    with col2:

        if "NAMA KABUPATEN/KOTA" in f.columns:

            x = (
                f[
                    "NAMA KABUPATEN/KOTA"
                ]
                .fillna("Tidak Diisi")
                .value_counts()
                .head(10)
                .sort_values()
                .reset_index()
            )

            x.columns = [
                "Wilayah",
                "Jumlah"
            ]

            fig = px.bar(
                x,
                x="Jumlah",
                y="Wilayah",
                orientation="h",
                text="Jumlah",
                title="📍 Top 10 Wilayah"
            )

            fig.update_traces(
                textposition="outside"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


    # -----------------------------------------------------
    # BULAN
    # -----------------------------------------------------

    x = monthly_data(
        f,
        "Bulan Bimbingan",
        "Kegiatan"
    )

    fig = px.line(
        x,
        x="Bulan",
        y="Kegiatan",
        markers=True,
        text="Kegiatan",
        title="📅 Jumlah Bimbingan per Bulan"
    )

    fig.update_traces(
        line_width=4,
        textposition="top center"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )


    # -----------------------------------------------------
    # INSIGHT
    # -----------------------------------------------------

    st.markdown(
        "### 💡 Insight Otomatis"
    )


    if f.empty:

        st.warning(
            "Tidak ada data sesuai filter."
        )

    else:

        for text in insights_bim(f):

            st.info(text.replace("**", ""))


    # -----------------------------------------------------
    # KESIMPULAN
    # -----------------------------------------------------

    st.subheader("🎯 Kesimpulan Analisis Bimbingan")
    st.info(
        "Analisis bimbingan memberikan gambaran mengenai konsentrasi kegiatan "
        "berdasarkan bidang usaha, wilayah, dan waktu pelaksanaan.\n\n"
        "Data tersebut dapat digunakan untuk monitoring pemerataan pendampingan "
        "serta identifikasi wilayah atau bidang usaha yang masih membutuhkan "
        "perhatian lebih lanjut."
    )


    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    st.subheader("📥 Download Hasil Analisis")
    st.caption(
        "Download PDF berisi hasil akhir dashboard sesuai filter aktif: KPI, grafik, "
        "insight, dan kesimpulan analisis."
    )

    if not f.empty:
        pdf_bim = create_dashboard_pdf(bim_df=f, rekap_bim_df=rekap_bim)
        st.download_button(
            label="📄 Download Hasil Dashboard Bimbingan (PDF)",
            data=pdf_bim,
            file_name="Hasil_Dashboard_Bimbingan_Konsultasi_2026.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# =========================================================
# DATA DETAIL
# =========================================================

else:

    st.header("📋 Data Detail & Hasil Cleaning")
    st.caption("Data setelah proses cleaning dan standardisasi")
    st.divider()


    tipe = st.radio(
        "Pilih data",
        [
            "Pelatihan",
            "Bimbingan"
        ],
        horizontal=True
    )


    df = (
        train
        if tipe == "Pelatihan"
        else bim
    )


    a, b = st.columns(2)


    with a:

        st.metric(
            "📊 Jumlah Baris",
            format_number(
                len(df)
            )
        )


    with b:

        st.metric(
            "🧹 Jumlah Kolom",
            format_number(
                len(df.columns)
            )
        )


    st.dataframe(
        df,
        use_container_width=True,
        height=550
    )


    # =====================================================
    # DOWNLOAD DATA CLEANING
    # =====================================================

    output = BytesIO()


    df.to_excel(
        output,
        index=False,
        engine="openpyxl"
    )


    st.download_button(

        label="⬇️ Download Data Hasil Cleaning",

        data=output.getvalue(),

        file_name=(
            f"data_{tipe.lower()}_clean.xlsx"
        ),

        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),

        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "📊 Dashboard Analisis Produktivitas 2026 • Data mengikuti file Excel yang diunggah "
    "• Cleaning dan standardisasi dilakukan otomatis"
)
