
import streamlit as st
import trimesh
import tempfile
import os

st.set_page_config(page_title="3D Baskı Fiyat Hesaplayıcı", page_icon="🧾")

st.title("🧾 3D Baskı Fiyat Hesaplayıcı")
st.write("Lütfen STL dosyanızı yükleyin. Birazdan size fiyat bilgisi vereceğim...")

uploaded_file = st.file_uploader("STL Dosyası Yükle (.stl)", type=["stl"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        mesh = trimesh.load_mesh(tmp_path)
        volume_cm3 = mesh.volume
        density_pla = 1.24  # g/cm³
        price_per_gram = 4.0  # TL

        mass_grams = volume_cm3 * density_pla
        total_price = mass_grams * price_per_gram

        st.success("✅ Dosya başarıyla işlendi!")
        st.write(f"**Tahmini Hacim:** {volume_cm3:.2f} cm³")
        st.write(f"**Tahmini Ağırlık (PLA):** {mass_grams:.2f} gram")
        st.write(f"**Tahmini Fiyat:** {total_price:.2f} TL")

        st.markdown("---")
        st.header("📦 Sipariş Bilgileri")
        name = st.text_input("Ad Soyad")
        email = st.text_input("E-posta")
        address = st.text_area("Adres")

        if name and email and address:
            st.success("Sipariş bilgileri alındı. En kısa sürede sizinle iletişime geçeceğiz.")
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")
    finally:
        os.remove(tmp_path)
