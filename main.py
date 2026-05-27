import streamlit as st
import numpy as np

def build_ui():
    """Modul Antarmuka Pengguna Streamlit Berbasis Status Pengerjaan Tugas KKNI"""
    st.title("Sistem Prediksi Kelulusan & Evaluasi Akademik (Standar KKNI)")
    st.markdown("---")
    
    st.header("Parameter Input Nilai & Status Mahasiswa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Kehadiran & Status Tugas KKNI")
        st.caption("Centang jika tugas dikerjakan (Bobot Total Tugas: 50%)")
        kehadiran = st.number_input("Kehadiran (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0)
        
        # Input Biner menggunakan Checkbox
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
    submitted = st.button("Proses Prediksi dan Evaluasi", type="primary")
    
    return kehadiran, tugas_rutin, cbr, cjr, rekayasa_ide, mini_riset, projek, nilai_uts, nilai_uas, submitted

# Blok eksekusi sementara
if __name__ == "__main__":
    inputs = build_ui()
    if inputs[-1]: 
        st.warning("Menunggu integrasi modul komputasi matematika (Matriks & SPL)...")
        
def hitung_matriks_dan_spl(tugas_rutin, cbr, cjr, rekayasa_ide, mini_riset, projek, nilai_uts, nilai_uas):
    """
    Modul Komputasi 1: Matriks (Agregasi Nilai) & SPL (Target Rekomendasi)
    """
    # 1. KONVERSI BINER & OPERASI MATRIKS
    # Konversi boolean ke float (100.0 atau 0.0)
    tugas_array = [float(tugas_rutin)*100, float(cbr)*100, float(cjr)*100, 
                   float(rekayasa_ide)*100, float(mini_riset)*100, float(projek)*100]
    
    # Matriks Input (1x8)
    M = np.array([*tugas_array, nilai_uts, nilai_uas])
    
    # Matriks Bobot (8x1)
    # 6 tugas @ 8.333% (0.08333), UTS 25% (0.25), UAS 25% (0.25)
    bobot_tugas = (0.50 / 6)
    W = np.array([bobot_tugas, bobot_tugas, bobot_tugas, bobot_tugas, bobot_tugas, bobot_tugas, 0.25, 0.25])
    
    # Perkalian Matriks (Dot Product)
    nilai_agregat = np.dot(M, W)
    
    # 2. SISTEM PERSAMAAN LINEAR (SPL)
    # Mencari nilai ideal x (Tugas), y (UTS), z (UAS) untuk mencapai nilai 70
    A = np.array([
        [0.5, 0.25, 0.25], 
        [1.0, -1.0, 0.0],   
        [0.0, 1.0, -1.0]    
    ])
    B = np.array([70.0, 10.0, -5.0])
    
    # Penyelesaian SPL dengan numpy.linalg.solve
    try:
        solusi_spl = np.linalg.solve(A, B)
        target_tugas, target_uts, target_uas = solusi_spl[0], solusi_spl[1], solusi_spl[2]
    except np.linalg.LinAlgError:
        target_tugas, target_uts, target_uas = 70.0, 70.0, 70.0 # Fallback jika matriks singular
        
    return nilai_agregat, (target_tugas, target_uts, target_uas)

# Parameter ini akan dipanggil oleh modul utama nanti

def komputasi_lanjutan(kehadiran, tugas_array, nilai_uts, nilai_uas, nilai_agregat):
    """
    Modul Komputasi 2: Boolean, Himpunan, dan Logika Keputusan
    """
    # 3. BOOLEAN (Fungsi 3 Variabel)
    # A: Kehadiran >= 75
    # B: Minimal 3 tugas dikerjakan (Total nilai biner >= 300)
    # C: UAS >= 50
    A = kehadiran >= 75.0
    B = sum(tugas_array) >= 300.0
    C = nilai_uas >= 50.0
    
    kelayakan_dasar = (A and B) or C
    
    # 4. HIMPUNAN (Operasi Selisih)
    himpunan_standar = {"Kehadiran", "Tugas", "UTS", "UAS"}
    himpunan_mahasiswa = set()
    
    if kehadiran >= 75.0: 
        himpunan_mahasiswa.add("Kehadiran")
    if sum(tugas_array) >= 300.0: 
        himpunan_mahasiswa.add("Tugas")
    if nilai_uts >= 70.0: 
        himpunan_mahasiswa.add("UTS")
    if nilai_uas >= 70.0: 
        himpunan_mahasiswa.add("UAS")
        
    komponen_evaluasi = himpunan_standar.difference(himpunan_mahasiswa)
    
    # 5. LOGIKA (Aturan Keputusan Kompleks)
    # Kalkulasi probabilitas dasar berbasis nilai agregat (Batas ideal = 70.0)
    probabilitas = (nilai_agregat / 70.0) * 100.0
    if probabilitas > 100.0: 
        probabilitas = 100.0
        
    status = ""
    rekomendasi = ""
    
    # Percabangan bersarang
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
        probabilitas = probabilitas * 0.5 # Penalti fatal
        rekomendasi = f"Tidak memenuhi standar minimal kelulusan. Wajib mengulang kelas. Titik lemah utama: {', '.join(komponen_evaluasi)}."
        
    return status, probabilitas, rekomendasi, komponen_evaluasi
