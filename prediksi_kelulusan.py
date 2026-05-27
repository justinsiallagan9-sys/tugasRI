import streamlit as st
import numpy as np

# --- MODUL 1: ANTARMUKA PENGGUNA ---
def build_ui():
    st.set_page_config(page_title="Prediksi Kelulusan", layout="wide")
    st.title("Sistem Prediksi Kelulusan & Evaluasi Akademik (Standar KKNI)")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Kehadiran & Status Tugas KKNI")
        st.caption("Centang jika tugas dikerjakan (Bobot Total Tugas: 50%)")
        kehadiran = st.number_input("Kehadiran (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0)
        
        tugas_rutin = st.checkbox("Tugas Rutin (Dikerjakan)", value=False)
        cbr = st.checkbox("Critical Book Report / CBR (Dikerjakan)", value=False)
        cjr = st.checkbox("Critical Journal Review / CJR (Dikerjakan)", value=False)
        rekayasa_ide = st.checkbox("Rekayasa Ide (Dikerjakan)", value=False)
        mini_riset = st.checkbox("Mini Riset (Dikerjakan)", value=False)
        projek = st.checkbox("Projek (Dikerjakan)", value=False)
        
    with col2:
        st.subheader("Evaluasi Ujian")
        st.caption("Total Bobot Ujian: 50%")
        nilai_uts = st.number_input("Nilai UTS (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        nilai_uas = st.number_input("Nilai UAS (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        
    st.markdown("---")
    submitted = st.button("Proses Prediksi dan Evaluasi", type="primary", use_container_width=True)
    
    return kehadiran, tugas_rutin, cbr, cjr, rekayasa_ide, mini_riset, projek, nilai_uts, nilai_uas, submitted

# --- MODUL 2: MATRIKS & SPL ---
def hitung_matriks_dan_spl(tugas_rutin, cbr, cjr, rekayasa_ide, mini_riset, projek, nilai_uts, nilai_uas):
    tugas_array = [float(tugas_rutin)*100, float(cbr)*100, float(cjr)*100, 
                   float(rekayasa_ide)*100, float(mini_riset)*100, float(projek)*100]
    
    M = np.array([*tugas_array, nilai_uts, nilai_uas])
    bobot_tugas = (0.50 / 6)
    W = np.array([bobot_tugas, bobot_tugas, bobot_tugas, bobot_tugas, bobot_tugas, bobot_tugas, 0.25, 0.25])
    
    nilai_agregat = np.dot(M, W)
    
    A = np.array([[0.5, 0.25, 0.25], [1.0, -1.0, 0.0], [0.0, 1.0, -1.0]])
    B = np.array([70.0, 10.0, -5.0])
    
    try:
        solusi_spl = np.linalg.solve(A, B)
        target_tugas, target_uts, target_uas = solusi_spl[0], solusi_spl[1], solusi_spl[2]
    except np.linalg.LinAlgError:
        target_tugas, target_uts, target_uas = 70.0, 70.0, 70.0
        
    return nilai_agregat, (target_tugas, target_uts, target_uas), tugas_array

# --- MODUL 3: BOOLEAN, HIMPUNAN & LOGIKA ---
def komputasi_lanjutan(kehadiran, tugas_array, nilai_uts, nilai_uas, nilai_agregat):
    A = kehadiran >= 75.0
    B = sum(tugas_array) >= 300.0
    C = nilai_uas >= 50.0
    kelayakan_dasar = (A and B) or C
    
    himpunan_standar = {"Kehadiran", "Tugas", "UTS", "UAS"}
    himpunan_mahasiswa = set()
    
    if kehadiran >= 75.0: himpunan_mahasiswa.add("Kehadiran")
    if sum(tugas_array) >= 300.0: himpunan_mahasiswa.add("Tugas")
    if nilai_uts >= 70.0: himpunan_mahasiswa.add("UTS")
    if nilai_uas >= 70.0: himpunan_mahasiswa.add("UAS")
        
    komponen_evaluasi = himpunan_standar.difference(himpunan_mahasiswa)
    
    probabilitas = (nilai_agregat / 70.0) * 100.0
    if probabilitas > 100.0: probabilitas = 100.0
        
    if nilai_agregat >= 70.0 and kelayakan_dasar:
        status = "LULUS"
        if len(komponen_evaluasi) == 0:
            rekomendasi = "Kinerja sangat baik dan memenuhi standar di semua komponen. Pertahankan."
        else:
            rekomendasi = f"Lulus bersyarat. Meskipun agregat cukup, perbaiki komponen berikut: {', '.join(komponen_evaluasi)}."
    elif nilai_agregat >= 50.0 and kelayakan_dasar:
        status = "TIDAK LULUS (DAPAT MENGULANG UJIAN)"
        rekomendasi = f"Nilai marginal. Wajib evaluasi pada komponen: {', '.join(komponen_evaluasi)}."
    else:
        status = "TIDAK LULUS"
        probabilitas = probabilitas * 0.5
        rekomendasi = f"Tidak memenuhi standar minimal kelulusan. Wajib mengulang kelas. Titik lemah utama: {', '.join(komponen_evaluasi)}."
        
    return status, probabilitas, rekomendasi

# --- MODUL UTAMA ---
if __name__ == "__main__":
    inputs = build_ui()
    kehadiran = inputs[0]
    tugas_inputs = inputs[1:7]
    nilai_uts = inputs[7]
    nilai_uas = inputs[8]
    submitted = inputs[9]
    
    if submitted:
        st.header("Hasil Analisis")
        
        nilai_agregat, target_spl, tugas_array = hitung_matriks_dan_spl(*tugas_inputs, nilai_uts, nilai_uas)
        status, probabilitas, rekomendasi = komputasi_lanjutan(kehadiran, tugas_array, nilai_uts, nilai_uas, nilai_agregat)
        
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("Nilai Agregat (Matriks)", f"{nilai_agregat:.2f}")
        col_res2.metric("Probabilitas Lulus", f"{probabilitas:.1f}%")
        col_res3.metric("Status Akhir", status)
        
        if "TIDAK LULUS" in status:
            st.error(f"**Rekomendasi Evaluasi:** {rekomendasi}")
            st.info(f"**Analisis SPL (Target Ideal agar Lulus):** Rata-rata Tugas: {target_spl[0]:.1f}, UTS: {target_spl[1]:.1f}, UAS: {target_spl[2]:.1f}")
        else:
            st.success(f"**Rekomendasi Evaluasi:** {rekomendasi}")
