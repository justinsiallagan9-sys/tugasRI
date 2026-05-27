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
