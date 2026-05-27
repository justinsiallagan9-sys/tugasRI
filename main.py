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
# Bobot: Tugas 20%, UTS 30%, UAS 50%
bobot = np.array([0.2, 0.3, 0.5])
nilai_input = np.array([tugas, uts, uas])
nilai_akhir = np.dot(nilai_input, bobot)

# 2. KONSEP BOOLEAN (3 Variabel + Penyederhanaan)
# A: Tugas >= 60, B: UTS >= 60, C: Kehadiran >= 75
A = 1 if tugas >= 60 else 0
B = 1 if uts >= 60 else 0
C = 1 if kehadiran >= 75 else 0
# Fungsi Boolean awal: (A*B*C) + (A*B*non C) + (non A*B*C) -> disederhanakan menjadi: B*(A + C)
status_boolean = B and (A or C)

# 3. KONSEP LOGIKA (Aturan Kompleks)
status_lulus = "GAGAL"
if kehadiran < 75:
status_lulus = "GAGAL (Kehadiran Kurang)"
elif nilai_akhir >= 60 and status_boolean:
status_lulus = "LULUS"
else:
status_lulus = "GAGAL (Kriteria Nilai Tidak Terpenuhi)"

# 4. KONSEP HIMPUNAN
set_akademik = set()
if tugas >= 60: set_akademik.add("Tugas Oke")
if uts >= 60: set_akademik.add("UTS Oke")
if uas >= 60: set_akademik.add("UAS Oke")

set_syarat = {"Tugas Oke", "UTS Oke", "UAS Oke"}
irisan = set_akademik.intersection(set_syarat)

# 5. KONSEP SPL (Target Nilai)
# Mencari UAS yang dibutuhkan jika ingin Nilai Akhir = 60
# Persamaan: 0.2*Tugas + 0.3*UTS + 0.5*UAS = 60
target_uas = (60 - (0.2 * tugas) - (0.3 * uts)) / 0.5

# --- TAMPILAN DASHBOARD ---
col1, col2 = st.columns(2)

with col1:
st.subheader("📊 Hasil Prediksi")
color = "green" if "LULUS" in status_lulus else "red"
st.markdown(f"### Status: :{color}[{status_lulus}]")
st.metric("Total Nilai Akhir", f"{nilai_akhir:.2f}/100")

st.subheader("🛠 Analisis Matematika")
with st.expander("Lihat Detail Konsep"):
st.write("**1. Matriks:** Nilai dihitung dengan perkalian dot antara vektor input dan matriks bobot.")
st.code(f"[{tugas}, {uts}, {uas}] . [0.2, 0.3, 0.5] = {nilai_akhir}")

st.write("**2. Boolean:** Fungsi disederhanakan dari f(A,B,C) menjadi `UTS & (Tugas | Kehadiran)`.")
st.write(f"Hasil Evaluasi: `{bool(B)} & ({bool(A)} | {bool(C)})` = **{bool(status_boolean)}**")

st.write("**3. Himpunan:** Irisan antara pencapaianmu dan syarat ideal.")
st.write(f"Komponen terpenuhi: {irisan}")

with col2:
st.subheader("💡 Fitur 'Target Saya' (SPL)")
if nilai_akhir < 60:
st.info(f"Untuk mencapai kelulusan (nilai 60), kamu minimal membutuhkan nilai UAS sebesar **{max(0, target_uas):.2f}**")
else:
st.success("Nilai kamu sudah mencapai ambang batas kelulusan!")

st.subheader("📈 Probabilitas")
prob = (nilai_akhir * 0.7) + (kehadiran * 0.3)
st.progress(int(prob))
st.write(f"Estimasi kemantapan posisi: {prob:.1f}%")
