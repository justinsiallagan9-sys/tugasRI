import streamlit as st

def build_ui():
    """Modul Antarmuka Pengguna Streamlit Berbasis Standar KKNI"""
    st.title("Sistem Prediksi Kelulusan & Evaluasi Akademik (Standar KKNI)")
    st.markdown("---")
    
    st.header("Parameter Input Nilai Mahasiswa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Kehadiran & Tugas KKNI")
        st.caption("Total Bobot Tugas: 50%")
        kehadiran = st.number_input("Kehadiran (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0)
        tugas_rutin = st.number_input("Tugas Rutin (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        cbr = st.number_input("Critical Book Report / CBR (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        cjr = st.number_input("Critical Journal Review / CJR (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        rekayasa_ide = st.number_input("Rekayasa Ide (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        mini_riset = st.number_input("Mini Riset (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        projek = st.number_input("Projek (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        
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
    if inputs[-1]: # Jika tombol ditekan
        st.warning("Menunggu integrasi modul komputasi matematika (Matriks & SPL)...")
