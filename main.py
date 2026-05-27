import streamlit as st

def build_ui():
    """Modul Antarmuka Pengguna Streamlit"""
    st.title("Sistem Prediksi Kelulusan & Evaluasi Akademik")
    st.markdown("---")
    
    st.header("Parameter Input Mahasiswa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Kinerja Harian")
        kehadiran = st.number_input("Kehadiran (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0)
        tugas_selesai = st.number_input("Tugas Dikerjakan (Jumlah)", min_value=0, value=0, step=1)
        tugas_kosong = st.number_input("Tugas Tidak Dikerjakan (Jumlah)", min_value=0, value=0, step=1)
        
    with col2:
        st.subheader("Evaluasi Ujian")
        nilai_uts = st.number_input("Nilai UTS (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        nilai_uas = st.number_input("Nilai UAS (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        
    st.markdown("---")
    submitted = st.button("Proses Prediksi dan Evaluasi", type="primary")
    
    return kehadiran, tugas_selesai, tugas_kosong, nilai_uts, nilai_uas, submitted

# Blok eksekusi sementara untuk pengujian UI (Akan diubah pada langkah integrasi)
if __name__ == "__main__":
    kehadiran, tugas_selesai, tugas_kosong, nilai_uts, nilai_uas, submitted = build_ui()
    
    if submitted:
        st.warning("Menunggu integrasi modul komputasi matematika...")
