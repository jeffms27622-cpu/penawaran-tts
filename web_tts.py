import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Sistem Penawaran TTS", layout="wide")

# --- FUNGSI LOGIN ---
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Login Staf TTS")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            # Username dan Password bisa kamu ganti di sini
            if user == "admin" and pwd == "tts123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Username atau Password salah!")
        return False
    return True

# --- FUNGSI PDF (Sesuai Format Dokumen Asli) ---
class PDF_TTS(FPDF):
    def header(self):
        # Menambahkan Logo (logo.png, posisi x=10, y=8, lebar=33)
        # Pastikan file logo.png sudah diupload ke GitHub
        if os.path.exists("logo.png"):
            self.image("logo.png", 10, 8, 33)
            self.set_x(45) # Geser teks ke kanan agar tidak tertabrak logo
        
        # Nama Perusahaan
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 0, 128)
        self.cell(0, 5, 'PT. THEA THEO STATIONARY', 0, 1, 'L')
        
        # Detail Alamat & Kontak sesuai dokumen
        self.set_x(45) # Tetap di posisi kanan logo
        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        self.cell(0, 5, 'Supplier Alat Tulis Kantor & Sekolah', 0, 1, 'L')
        
        self.set_x(45)
        self.cell(0, 5, 'Komp. Ruko Modernland Cipondoh Blok. AR No. 27, Tangerang', 0, 1, 'L')
        
        self.set_x(45)
        self.cell(0, 5, 'Ph: 021-55780659, Fax: 021 - 22292650', 0, 1, 'L')
        
        self.set_x(45)
        self.cell(0, 5, 'Email: alattulis.tts@gmail.com', 0, 1, 'L')
        
        self.ln(5)
        self.line(10, 38, 200, 38) # Garis pembatas header
        self.ln(5)

def generate_pdf(cust_data, items, totals):
    pdf = PDF_TTS()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    
    # Header Info
    pdf.cell(0, 5, f'Tangerang, {cust_data["tanggal"]}', 0, 1, 'R')
    pdf.cell(0, 5, f'No: {cust_data["no_surat"]}', 0, 1, 'L')
    pdf.cell(0, 5, 'Hal: Surat Penawaran Harga', 0, 1, 'L')
    pdf.ln(5)
    
    pdf.cell(0, 5, 'Kepada Yth,', 0, 1, 'L')
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, cust_data["nama_pt"], 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, f'Up. {cust_data["up_nama"]}', 0, 1, 'L')
    pdf.ln(5)

    # Tabel
    pdf.set_font('Arial', 'B', 9)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(10, 8, 'No', 1, 0, 'C', True)
    pdf.cell(75, 8, 'Nama Barang', 1, 0, 'C', True)
    pdf.cell(20, 8, 'Satuan', 1, 0, 'C', True)
    pdf.cell(15, 8, 'Qty', 1, 0, 'C', True)
    pdf.cell(35, 8, 'Harga Satuan', 1, 0, 'C', True)
    pdf.cell(35, 8, 'Jumlah', 1, 1, 'C', True)

    pdf.set_font('Arial', '', 9)
    for idx, item in enumerate(items, 1):
        pdf.cell(10, 7, str(idx), 1, 0, 'C')
        pdf.cell(75, 7, f" {item['nama']}", 1)
        pdf.cell(20, 7, item['satuan'], 1, 0, 'C')
        pdf.cell(15, 7, str(item['qty']), 1, 0, 'C')
        pdf.cell(35, 7, f"{item['harga']:,.0f}", 1, 0, 'R')
        pdf.cell(35, 7, f"{item['total']:,.0f}", 1, 1, 'R')

    # Perhitungan Akhir sesuai dokumen
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(120, 7, '', 0, 0)
    pdf.cell(35, 7, 'Sub Total', 1, 0, 'L')
    pdf.cell(35, 7, f"{totals['subtotal']:,.0f}", 1, 1, 'R')
    pdf.cell(120, 7, '', 0, 0)
    pdf.cell(35, 7, 'PPN 11%', 1, 0, 'L')
    pdf.cell(35, 7, f"{totals['ppn']:,.0f}", 1, 1, 'R')
    pdf.cell(120, 7, '', 0, 0)
    pdf.cell(35, 7, 'TOTAL', 1, 0, 'L')
    pdf.cell(35, 7, f"{totals['grand_total']:,.0f}", 1, 1, 'R')

    # Tanda Tangan
    pdf.ln(10)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, 'Atas perhatian dan kerja samanya kami ucapkan terima kasih.', 0, 1, 'L')
    pdf.ln(10)
    pdf.cell(145)
    pdf.cell(40, 5, 'Hormat Kami,', 0, 1, 'C')
    pdf.ln(20)
    pdf.cell(145)
    pdf.set_font('Arial', 'BU', 10)
    pdf.cell(40, 5, 'A.Sin', 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(145)
    pdf.cell(40, 5, 'Marketing', 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

# --- JALANKAN PROGRAM ---
if login():
    # SEMUA KODE GENERATOR DI DALAM BLOK LOGIN INI
    st.sidebar.success("✅ Terhubung sebagai Staf TTS")
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🖨️ Generator Penawaran Harga - TTS")
    
    # Load Data dari Excel
    if os.path.exists("database_barang.xlsx"):
        df_db = pd.read_excel("database_barang.xlsx")
        DB_BARANG = {"Pilih Barang...": {"satuan": "-", "harga": 0}}
        for _, row in df_db.iterrows():
            DB_BARANG[row['Nama']] = {"satuan": row['Satuan'], "harga": row['Harga']}
    else:
        st.error("File 'database_barang.xlsx' tidak ditemukan!")
        DB_BARANG = {"Pilih Barang...": {"satuan": "-", "harga": 0}}

    # Data Customer
    col1, col2 = st.columns(2)
    with col1:
        no_surat = st.text_input("Nomor Surat", value="107/S-TTS/II/2026")
        nama_pt = st.text_input("Nama PT Customer", placeholder="Contoh: PT. Hutama Solusi Indonesia")
    with col2:
        up_nama = st.text_input("Up. (Nama Penerima)", placeholder="Contoh: Ibu Ayu")
        tanggal = st.date_input("Tanggal", datetime.date.today()).strftime("%d %B %Y")

    # Input Barang
    st.markdown("### 🛒 Tambah Barang")
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        pilihan = st.selectbox("Cari Barang:", list(DB_BARANG.keys()))
    with c2:
        qty = st.number_input("Qty", min_value=1, value=1)
    with c3:
        st.write("")
        st.write("")
        if st.button("Tambah ke Tabel"):
            if pilihan != "Pilih Barang...":
                if 'keranjang' not in st.session_state:
                    st.session_state.keranjang = []
                data = DB_BARANG[pilihan]
                st.session_state.keranjang.append({
                    "nama": pilihan, "satuan": data['satuan'], 
                    "harga": data['harga'], "qty": qty, "total": data['harga'] * qty
                })
            else:
                st.warning("Pilih barang dari daftar!")

    # Tabel Penawaran
    if 'keranjang' in st.session_state and st.session_state.keranjang:
        st.markdown("---")
        df_cart = pd.DataFrame(st.session_state.keranjang)
        st.table(df_cart.style.format({"harga": "{:,.0f}", "total": "{:,.0f}"}))

        subtotal = sum(i['total'] for i in st.session_state.keranjang)
        ppn = subtotal * 0.11
        grand_total = subtotal + ppn

        st.write(f"**Subtotal:** Rp {subtotal:,.0f}")
        st.write(f"**PPN (11%):** Rp {ppn:,.0f}")
        st.write(f"### **Total: Rp {grand_total:,.0f}**")

        # Cetak PDF
        cust_info = {"no_surat": no_surat, "nama_pt": nama_pt, "up_nama": up_nama, "tanggal": tanggal}
        total_info = {"subtotal": subtotal, "ppn": ppn, "grand_total": grand_total}
        
        pdf_out = generate_pdf(cust_info, st.session_state.keranjang, total_info)
        
        st.download_button(
            label="📄 Unduh PDF Penawaran",
            data=pdf_out,
            file_name=f"Penawaran_{nama_pt}.pdf",
            mime="application/pdf",
            type="primary"
        )
        
        if st.button("Kosongkan Semua"):
            st.session_state.keranjang = []
            st.rerun()
