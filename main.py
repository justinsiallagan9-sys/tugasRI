import streamlit as st
import numpy as np

# Judul Aplikasi
st.set_page_config(page_title="Prediksi Kelulusan Mata Kuliah", layout="wide")
st.title("🎓 App Prediksi Kelulusan (Matematika Terapan)")
st.markdown("---")

# --- SIDEBAR: INPUT DATA ---
st.sidebar.header("📥 Input Data Mahasiswa")
nama = st.sidebar.text_input("Nama Mahasiswa", "Budi")
tugas = st.sidebar.slider("Nilai Tugas", 0, 100, 70)
uts = st.sidebar.slider("Nilai UTS", 0, 100, 65)
uas = st.sidebar.slider("Nilai UAS", 0, 100, 50)
kehadiran = st.sidebar.slider("Persentase Kehadiran (%)", 0, 100, 80)

# --- PROSES MATEMATIKA ---

# 1. KONSEP MATRIKS (Perhitungan Nilai Akhir)
# Menggunakan Vektor Nilai dan Vektor Bobot
bobot = np.array([0.2, 0.3, 0.5])
nilai_input = np.array([tugas, uts, uas])
nilai_akhir = np.dot(nilai_input, bobot)

# 2. KONSEP BOOLEAN (3 Variabel: A=Tugas, B=UTS, C=Presensi)
# Syarat: Tugas >= 60 (A), UTS >= 60 (B), Kehadiran >= 75 (C)
A = 1 if tugas >= 60 else 0
B = 1 if uts >= 60 else 0
C = 1 if kehadiran >= 75 else 0
# Fungsi Boolean: B AND (A OR C) -> Hasil penyederhanaan K-Map
status_boolean = bool(B and (A or C))

# 3. KONSEP LOGIKA (Aturan Keputusan Kompleks)
if kehadiran < 75:
status_lulus = "GAGAL (Kehadiran di bawah 75%)"
warna_status = "red"
elif nilai_akhir >= 60 and status_boolean:
status_lulus = "LULUS"
warna_status = "green"
else:
status_lulus = "GAGAL (Nilai atau Syarat Boolean tidak terpenuhi)"
warna_status = "red"

# 4. KONSEP HIMPUNAN
set_mahasiswa = set()
if tugas >= 60: set_mahasiswa.add("Lulus Tugas")
if uts >= 60: set_mahasiswa.add("Lulus UTS")
if uas >= 60: set_mahasiswa.add("Lulus UAS")
set_syarat_minimal = {"Lulus Tugas", "Lulus UTS"}
hasil_himpunan = set_mahasiswa.intersection(set_syarat_minimal)

# 5. KONSEP SPL (Sistem Persamaan Linear)
# Target Nilai Akhir = 60. Persamaan: 0.2*Tugas + 0.3*UTS + 0.5*UAS_diperlukan = 60
uas_diperlukan = (60 - (0.2 * tugas) - (0.3 * uts)) / 0.5

# --- TAMPILAN DASHBOARD ---
col1, col2 = st.columns([2, 1])

with col1:
st.subheader(f"📊 Analisis untuk: {nama}")
st.markdown(f"### Status: :{warna_status}[{status_lulus}]")

st.write("#### 🛠 Transparansi Konsep Matematika")
exp1 = st.expander("Klik untuk melihat detail 5 Konsep Matematika")
with exp1:
st.write(f"**1. Matriks:** `[Tugas, UTS, UAS] . Bobot` = `{nilai_input} . {bobot} = {nilai_akhir:.2f}`")
st.write(f"**2. Boolean:** `B ∧ (A ∨ C)` = `{bool(B)} ∧ ({bool(A)} ∨ {bool(C)})` = **{status_boolean}**")
st.write(f"**3. Logika:** Menggunakan aturan Bertingkat (Nested If) untuk Kehadiran dan Nilai Akhir.")
st.write(f"**4. Himpunan:** Kamu memenuhi {len(hasil_himpunan)} dari {len(set_syarat_minimal)} syarat wajib awal.")
st.write(f"**5. SPL:** Menghitung variabel UAS yang belum diketahui untuk mencapai target 60.")

with col2:
st.subheader("💡 Info Target")
if nilai_akhir < 60:
st.warning(f"Butuh UAS: **{max(0, uas_diperlukan):.2f}**")
else:
st.success("Target nilai 60 sudah tercapai!")

st.subheader("📉 Kemantapan")
probabilitas = min(100, int((nilai_akhir * 0.7) + (kehadiran * 0.3)))
st.progress(probabilitas)
st.write(f"Tingkat Keyakinan: {probabilitas}%")
