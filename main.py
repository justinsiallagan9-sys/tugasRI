import streamlit as st

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
