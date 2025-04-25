
import streamlit as st
import trimesh
import tempfile
import os

# Malzeme fiyat bilgileri
MATERIAL_PRICES = {
    "PLA": 4000  # TL / kg
}

DENSITY = {
    "PLA": 1.24  # g/cm³
}

st.set_page_config(page_title="3D Baskı Fiyat Hesaplayıcı", page_icon="🧮")

st.title("📦 STL Dosyası ile 3D Baskı Fiyat Hesaplayıcı")
st.write("Lütfen STL dosyanızı yükleyin, ardından tahmini fiyat bilgisini öğrenin.")

with st.form("upload_form"):
    uploaded_file = st.file_uploader("STL Dosyasını Yükle (.stl formatı)", type=["stl"])
    material = st.selectbox("Malzeme Türü", list(MATERIAL_PRICES.keys()))
    name = st.text_input("İsim Soyisim")
    email = st.text_input("E-posta")
    address = st.text_area("Adres")

    submitted = st.form_submit_button("Fiyatı Hesapla")

if submitted:
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        mesh = trimesh.load(tmp_path)
        os.remove(tmp_path)

        # STL dosyaları genelde mm³ birimindedir. cm³'e çevirmek için 1000'e böl.
        volume_mm3 = mesh.volume
        volume_cm3 = volume_mm3 / 1000

        density = DENSITY[material]
        weight_g = volume_cm3 * density
        weight_kg = weight_g / 1000

        price_per_kg = MATERIAL_PRICES[material]
        estimated_price = weight_kg * price_per_kg

        st.success("🎉 Fiyatlandırma Tamamlandı!")
        st.markdown(f"**Tahmini Hacim:** {volume_cm3:.2f} cm³")
        st.markdown(f"**Tahmini Ağırlık ({material}):** {weight_g:.2f} gram")
        st.markdown(f"**Tahmini Fiyat:** {estimated_price:.2f} TL")

        st.markdown("---")
        st.markdown("📝 Sipariş Bilgileri:")
        st.markdown(f"**İsim:** {name}")
        st.markdown(f"**E-posta:** {email}")
        st.markdown(f"**Adres:** {address}")
    else:
        st.warning("Lütfen geçerli bir STL dosyası yükleyin.")

