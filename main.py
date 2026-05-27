import streamlit as st
import numpy as np
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="PentaLogic - Prediksi Kelulusan",
    page_icon="🎓",
    layout="centered"
)

# --- CSS CUSTOM UNTUK TAMPILAN ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #005088; color: white; }
    .result-card { padding: 20px; border-radius: 15px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True) Harris=True)

st.title("🎓 PentaLogic Classifier")
st.subheader("Sistem Prediksi Kelulusan Berbasis 5 Konsep Matematika Diskrit")
st.write("Sistem ini mengevaluasi kelayakan lulus menggunakan alur logika matematika murni.")

# --- SIDEBAR INPUT DATA ---
st.sidebar.header("📊 Data Mahasiswa")
nama = st.sidebar.text_input("Nama Mahasiswa", "Budi Santoso")
kehadiran = st.sidebar.slider("Persentase Kehadiran (%)", 0, 100, 85)
sks_total = st.sidebar.number_input("Total SKS yang Ditempuh", 0, 150, 130)
ada_nilai_e = st.sidebar.radio("Apakah ada nilai E?", ("Tidak", "Ya"))

st.sidebar.divider()
ipk = st.sidebar.number_input("IPK Saat Ini", 0.0, 4.0, 3.4, step=0.1)
toefl = st.sidebar.number_input("Skor TOEFL", 0, 677, 480)

st.sidebar.divider()
st.sidebar.write("📝 **Nilai Mata Kuliah Inti (0-100):**")
n_algo = st.sidebar.number_input("Algoritma", 0, 100, 80)
n_db = st.sidebar.number_input("Basis Data", 0, 100, 75)
n_rpl = st.sidebar.number_input("RPL", 0, 100, 85)

# --- TOMBOL PREDIKSI ---
if st.button("Analisis Kelulusan Sekarang"):
    
    st.divider()
    
    # ==========================================
    # KONSEP 1: BOOLEAN (3 Variabel & Penyederhanaan)
    # ==========================================
    # A = Kehadiran cukup, B = SKS cukup, C = Tidak ada nilai E
    A = kehadiran >= 80
    B = sks_total >= 120
    C = ada_nilai_e == "Tidak"
    
    # Fungsi Boolean: F(A,B,C) = A ∧ B ∧ C
    lulus_boolean = A and B and C
    
    with st.expander("🔍 Detail Tahap 1: Evaluasi Boolean"):
        st.latex(r"F(A,B,C) = A \land B \land C")
        st.write(f"Kehadiran (A): {'✅' if A else '❌'}")
        st.write(f"Minimal SKS (B): {'✅' if B else '❌'}")
        st.write(f"Bebas Nilai E (C): {'✅' if C else '❌'}")

    if not lulus_boolean:
        st.error(f"**Hasil: TIDAK LULUS SYARAT DASAR**")
        st.warning("Mahasiswa gagal pada penyederhanaan fungsi Boolean syarat administratif.")
    else:
        # ==========================================
        # KONSEP 2: HIMPUNAN (Operasi Irisan / Intersection)
        # ==========================================
        mk_wajib = {"Algoritma", "Basis Data", "RPL"}
        # Asumsi mahasiswa menginput nilai maka dianggap sudah ambil
        mk_diambil = {"Algoritma", "Basis Data", "RPL"} 
        
        irisan = mk_wajib.intersection(mk_diambil)
        lulus_himpunan = irisan == mk_wajib
        
        with st.expander("🔍 Detail Tahap 2: Operasi Himpunan"):
            st.latex(r"MK_{Lulus} = MK_{Wajib} \cap MK_{Ambil}")
            st.write(f"Himpunan MK Wajib: `{mk_wajib}`")
            st.write(f"Mahasiswa memenuhi: `{irisan}`")

        # ==========================================
        # KONSEP 3: MATRIKS (Operasi Perkalian Bobot)
        # ==========================================
        # Matriks Nilai (1x3) dan Matriks Bobot SKS (3x1)
        m_nilai = np.array([n_algo, n_db, n_rpl])
        m_bobot = np.array([[3], [4], [3]]) # Bobot SKS
        
        # Perkalian Matriks
        total_poin = np.dot(m_nilai, m_bobot)[0]
        standar_poin = 700 # Batas poin lulus
        
        with st.expander("🔍 Detail Tahap 3: Operasi Matriks"):
            st.latex(r"\begin{bmatrix} n_1 & n_2 & n_3 \end{bmatrix} \cdot \begin{bmatrix} s_1 \\ s_2 \\ s_3 \end{bmatrix} = \text{Total Poin}")
            st.write(f"Hasil Kalkulasi Matriks: **{total_poin} Poin**")

        # ==========================================
        # KONSEP 4: LOGIKA (Aturan Keputusan Kompleks)
        # ==========================================
        if (ipk >= 3.5) and (toefl >= 500):
            kategori = "LULUS (CUMLAUDE)"
            warna = "success"
        elif (ipk >= 2.75) and (toefl >= 450):
            kategori = "LULUS (SANGAT MEMUASKAN)"
            warna = "info"
        else:
            kategori = "TIDAK LULUS (LOGIKA AKADEMIK)"
            warna = "error"

        # ==========================================
        # KONSEP 5: KOMBINATORIKA (Pemilihan Optimal)
        # ==========================================
        # Menghitung sisa cara mengambil MK Pilihan (Misal 5 tersedia, butuh 2)
        n_pilihan = 5
        r_butuh = 2
        kombinasi = math.comb(n_pilihan, r_butuh)

        # --- TAMPILAN AKHIR ---
        st.subheader("🏁 Kesimpulan Akhir")
        if warna == "success":
            st.balloons()
            st.success(f"**{nama} diprediksi: {kategori}**")
        elif warna == "info":
            st.info(f"**{nama} diprediksi: {kategori}**")
        else:
            st.error(f"**{nama} diprediksi: {kategori}**")
            
        st.write(f"**Analisis Kombinatorika:** Mahasiswa memiliki **{kombinasi} cara** untuk memilih mata kuliah pilihan sisa guna mengoptimalkan nilai.")

# --- FOOTER ---
st.divider()
st.caption("Aplikasi ini menggunakan konsep Matematika Diskrit: Boolean, Himpunan, Matriks, Logika Proposisional, dan Kombinatorika.")
