import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Aplikasi Penawaran TTS", layout="wide")

# --- DATABASE BARANG ---
import pandas as pd

# Membaca data dari Excel
df_db = pd.read_excel("database_barang.xlsx")

# Mengubahnya menjadi format yang dipahami program
DB_BARANG = {"Pilih Barang...": {"satuan": "-", "harga": 0}}
for index, row in df_db.iterrows():
    DB_BARANG[row['Nama']] = {"satuan": row['Satuan'], "harga": row['Harga']}

# --- FUNGSI PDF ---
class PDF_TTS(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 0, 128)
        self.cell(0, 5, 'PT. THEA THEO STATIONARY', 0, 1, 'L')
        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, 'Supplier Alat Tulis Kantor & Sekolah', 0, 1, 'L')
        self.cell(0, 5, 'Komp. Ruko Modernland Cipondoh Blok. AR No. 27, Tangerang', 0, 1, 'L')
        self.cell(0, 5, 'Ph: 021-55780659, Fax: 021 - 22292650', 0, 1, 'L')
        self.cell(0, 5, 'Email: alattulis.tts@gmail.com', 0, 1, 'L')
        self.ln(2)
        self.line(10, 38, 200, 38)
        self.ln(8)

def generate_pdf(cust_data, items, total_data):
    pdf = PDF_TTS()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    
    # Info Surat
    pdf.cell(0, 5, f'Tangerang, {cust_data["tanggal"]}', 0, 1, 'R')
    pdf.cell(0, 5, f'No: {cust_data["no_surat"]}', 0, 1, 'L')
    pdf.cell(0, 5, 'Hal: Surat Penawaran Harga', 0, 1, 'L')
    pdf.ln(5)
    
    # Penerima
    pdf.cell(0, 5, 'Kepada Yth,', 0, 1, 'L')
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, cust_data["nama_pt"], 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, f'Up. {cust_data["up_nama"]}', 0, 1, 'L')
    pdf.ln(5)

    # Header Tabel
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(10, 8, 'No', 1, 0, 'C', True)
    pdf.cell(75, 8, 'Nama Barang', 1, 0, 'C', True)
    pdf.cell(20, 8, 'Satuan', 1, 0, 'C', True)
    pdf.cell(15, 8, 'Qty', 1, 0, 'C', True)
    pdf.cell(35, 8, 'Harga Satuan', 1, 0, 'C', True)
    pdf.cell(35, 8, 'Jumlah', 1, 1, 'C', True)

    # Isi Tabel
    pdf.set_font('Arial', '', 9)
    for idx, item in enumerate(items, 1):
        pdf.cell(10, 7, str(idx), 1, 0, 'C')
        pdf.cell(75, 7, f" {item['nama']}", 1)
        pdf.cell(20, 7, item['satuan'], 1, 0, 'C')
        pdf.cell(15, 7, str(item['qty']), 1, 0, 'C')
        pdf.cell(35, 7, f"{item['harga']:,.0f}", 1, 0, 'R')
        pdf.cell(35, 7, f"{item['total']:,.0f}", 1, 1, 'R')

    # Total
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(120, 7, '', 0, 0)
    pdf.cell(35, 7, 'Sub Total', 1, 0, 'L')
    pdf.cell(35, 7, f"{total_data['subtotal']:,.0f}", 1, 1, 'R')
    pdf.cell(120, 7, '', 0, 0)
    pdf.cell(35, 7, 'PPN 11%', 1, 0, 'L')
    pdf.cell(35, 7, f"{total_data['ppn']:,.0f}", 1, 1, 'R')
    pdf.cell(120, 7, '', 0, 0)
    pdf.cell(35, 7, 'TOTAL', 1, 0, 'L')
    pdf.cell(35, 7, f"{total_data['grand_total']:,.0f}", 1, 1, 'R')

    # Footer
    pdf.ln(10)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, 'Atas perhatian dan kerja samanya kami ucapkan terima kasih.', 0, 1, 'L')
    pdf.ln(10)
    pdf.cell(140)
    pdf.cell(40, 5, 'Hormat Kami,', 0, 1, 'C')
    pdf.ln(20)
    pdf.cell(140)
    pdf.set_font('Arial', 'BU', 10)
    pdf.cell(40, 5, 'A.Sin', 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(140)
    pdf.cell(40, 5, 'Marketing', 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE WEB ---
st.title("🖨️ Generator Penawaran Harga - TTS")
st.markdown("---")

# Session State (Keranjang Belanja)
if 'keranjang' not in st.session_state:
    st.session_state.keranjang = []

# Input Data Customer
col1, col2 = st.columns(2)
with col1:
    no_surat = st.text_input("Nomor Surat", value="107/S-TTS/II/2026")
    nama_pt = st.text_input("Nama PT Customer")
with col2:
    up_nama = st.text_input("Up. (Nama Penerima)")
    tanggal = st.date_input("Tanggal", datetime.date.today()).strftime("%d %B %Y")

st.markdown("### 🛒 Input Barang")

# Form Input Barang
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    pilihan = st.selectbox("Pilih Barang:", list(DB_BARANG.keys()))
with c2:
    qty = st.number_input("Qty", min_value=1, value=1)
with c3:
    st.write("")
    st.write("")
    if st.button("➕ Tambah"):
        if pilihan != "Pilih Barang...":
            data = DB_BARANG[pilihan]
            st.session_state.keranjang.append({
                "nama": pilihan, "satuan": data['satuan'], "harga": data['harga'],
                "qty": qty, "total": data['harga'] * qty
            })
            st.success(f"Masuk keranjang: {pilihan}")
        else:
            st.error("Pilih barang dulu!")

# Tampilkan Tabel
if st.session_state.keranjang:
    st.markdown("---")
    df = pd.DataFrame(st.session_state.keranjang)
    st.table(df.style.format({"harga": "{:,.0f}", "total": "{:,.0f}"}))

    # Hitung Total
    subtotal = sum(item['total'] for item in st.session_state.keranjang)
    ppn = subtotal * 0.11
    grand_total = subtotal + ppn

    # Tampilkan Total di Layar
    c_tot1, c_tot2 = st.columns([3, 1])
    with c_tot2:
        st.metric("Total Akhir", f"Rp {grand_total:,.0f}")

    # Tombol Download PDF
    cust_data = {"no_surat": no_surat, "nama_pt": nama_pt, "up_nama": up_nama, "tanggal": tanggal}
    total_data = {"subtotal": subtotal, "ppn": ppn, "grand_total": grand_total}
    
    pdf_bytes = generate_pdf(cust_data, st.session_state.keranjang, total_data)
    
    st.download_button(
        label="📄 DOWNLOAD PDF",
        data=pdf_bytes,
        file_name=f"Penawaran_{nama_pt}.pdf",
        mime="application/pdf",
        type="primary"
    )

    if st.button("Hapus Semua Data"):
        st.session_state.keranjang = []
        st.rerun()