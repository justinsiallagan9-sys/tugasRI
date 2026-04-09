import streamlit as st
import math

# Konfigurasi Halaman sesuai Judul Rekayasa Ide [cite: 1, 4]
st.set_page_config(page_title="Smart Password Analyzer", page_icon="🔐", layout="wide")

st.title("Aplikasi Smart Password Analyzer")
st.caption("Implementasi Rekayasa Ide Kelompok 3 PTIK-B - Universitas Negeri Medan [cite: 11, 15]")

# Sidebar untuk Navigasi sesuai rencana penelitian [cite: 199]
menu = st.sidebar.selectbox("Pilih Modul:", ["Kalkulator Kombinatorik", "Analisis Keamanan Password"])

# --- MODUL 1: KALKULATOR KOMBINATORIK (Media Pembelajaran) [cite: 163, 200] ---
if menu == "Kalkulator Kombinatorik":
    st.header("1. Kalkulator Kombinatorik")
    st.write("Modul ini membantu mahasiswa memahami perhitungan dasar faktorial, permutasi, dan kombinasi[cite: 171, 201].")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Faktorial (n!)")
        n_fact = st.number_input("Masukkan n:", min_value=0, step=1, key="fact")
        if st.button("Hitung Faktorial"):
            st.success(f"{n_fact}! = {math.factorial(n_fact)}")

    with col2:
        st.subheader("Permutasi (P)")
        n_p = st.number_input("Masukkan n:", min_value=0, step=1, key="np")
        r_p = st.number_input("Masukkan r:", min_value=0, step=1, key="rp")
        if st.button("Hitung Permutasi"):
            if n_p >= r_p:
                hasil_p = math.perm(n_p, r_p)
                st.success(f"P({n_p}, {r_p}) = {hasil_p}")
            else:
                st.error("n harus ≥ r")

    with col3:
        st.subheader("Kombinasi (C)")
        n_c = st.number_input("Masukkan n:", min_value=0, step=1, key="nc")
        r_c = st.number_input("Masukkan r:", min_value=0, step=1, key="rc")
        if st.button("Hitung Kombinasi"):
            if n_c >= r_c:
                hasil_c = math.comb(n_c, r_c)
                st.success(f"C({n_c}, {r_c}) = {hasil_c}")
            else:
                st.error("n harus ≥ r")

# --- MODUL 2: ANALISIS KEAMANAN PASSWORD (Penerapan Kontekstual) [cite: 66, 202] ---
else:
    st.header("2. Analisis Keamanan Password")
    st.write("Menganalisis tingkat kerumitan berdasarkan teori kombinatorik[cite: 137, 202].")

    # Input password dari responden penelitian [cite: 203]
    user_password = st.text_input("Masukkan kata sandi untuk dianalisis:", type="password")

    if user_password:
        # LOGIKA PENGECEKAN KARAKTER (Menentukan n) [cite: 147, 215]
        n = 0
        k = len(user_password) # Panjang password (k) [cite: 148, 215]
        
        # Pengecekan isi password satu per satu
        has_lower = any(c.islower() for c in user_password)
        has_upper = any(c.isupper() for c in user_password)
        has_digit = any(c.isdigit() for c in user_password)
        has_special = any(not c.isalnum() for c in user_password)

        # Menentukan variasi karakter (n) [cite: 147, 215]
        if has_lower: n += 26
        if has_upper: n += 26
        if has_digit: n += 10
        if has_special: n += 32

        # MODEL MATEMATIKA REKAYASA IDE [cite: 209]
        # 1. Total Kombinasi C = n^k [cite: 144, 213]
        total_kombinasi = n ** k
        
        # 2. Faktor Prediktabilitas (P) [cite: 218, 220]
        p_factor = 1.0
        kata_umum = ["password", "12345678", "admin123", "unimed2026", "ptikunimed"]
        if user_password.lower() in kata_umum:
            p_factor = 1000.0 # Password umum meningkatkan prediktabilitas 
        
        # 3. Estimasi Waktu T = C / (R * alpha) [cite: 150, 223]
        R = 10**9 # Kecepatan tebakan per detik (R) [cite: 221]
        alpha = 1.0 # Koefisien efisiensi (alpha) [cite: 222]
        waktu_detik = total_kombinasi / (R * alpha * p_factor)

        # OUTPUT VISUALISASI [cite: 207, 246]
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Variasi Karakter (n)", n)
        c2.metric("Panjang (k)", k)
        c3.metric("Prediktabilitas (P)", p_factor)

        st.subheader("Total Kombinasi Matematis ($C = n^k$):")
        st.code(f"{total_kombinasi:,}")

        # Konversi Waktu [cite: 205]
        if waktu_detik > 31536000:
            hasil_waktu = f"{waktu_detik/31536000:,.2f} Tahun"
        elif waktu_detik > 86400:
            hasil_waktu = f"{waktu_detik/86400:,.2f} Hari"
        else:
            hasil_waktu = f"{waktu_detik:,.2f} Detik"

        st.subheader("Estimasi Waktu Serangan Brute Force[cite: 204]:")
        st.info(f"Dibutuhkan sekitar **{hasil_waktu}** untuk meretas password ini.")

        # Kesimpulan & Rekomendasi [cite: 207, 241]
        if k < 12:
            st.warning("Password terlalu pendek. Gunakan minimal 12 karakter[cite: 161].")
        elif n < 60:
            st.warning("Kurang variasi. Gunakan campuran huruf besar, angka, dan simbol[cite: 49].")
        else:
            st.success("Password ini memiliki tingkat keamanan yang tinggi secara matematis[cite: 157].")

st.sidebar.divider()
st.sidebar.caption("Modul ini digunakan untuk penelitian Mixed Method Kelompok 3[cite: 229, 230].")