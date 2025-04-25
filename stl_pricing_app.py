import streamlit as st
import trimesh
import tempfile
import os

# Malzeme yoğunlukları (g/cm³)
DENSITY = {
    "PLA": 1.24,
    "PETG": 1.27,
    "ABS": 1.04,
}

# Kullanıcı arayüzü
st.title("3D Baskı Fiyat Tahmini")

uploaded_file = st.file_uploader("STL Dosyanızı Yükleyin", type=["stl"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        mesh = trimesh.load_mesh(tmp_file_path)
        volume_cm3 = mesh.volume / 1000  # mm³ to cm³
        st.success(f"Model Hacmi: {volume_cm3:.2f} cm³")

        # Kullanıcıdan ek bilgiler al
        infill_percent = st.slider("Infill (%)", 1, 100, 20)
        needs_support = st.selectbox("Destek Gerekli mi?", ["Hayır", "Evet"])
        layer_height = st.selectbox("Katman Yüksekliği (mm)", ["0.1", "0.2", "0.3"])
        nozzle = st.selectbox("Nozzle Çapı", ["0.4", "0.6", "0.8"])
        material = st.selectbox("Malzeme", list(DENSITY.keys()))

        # Etkin yoğunluk ve destek çarpanı
        effective_density = DENSITY[material] * (infill_percent / 100)
        support_multiplier = 1.2 if needs_support == "Evet" else 1.0

        # Hesaplamalar
        weight_g = volume_cm3 * effective_density * support_multiplier
        price_per_kg = 4000  # TL
        cost = weight_g * (price_per_kg / 1000)

        st.write(f"Tahmini Ağırlık: {weight_g:.2f} gram")
        st.write(f"Tahmini Fiyat: {cost:.2f} TL")

        # Sipariş formu
        st.markdown("---")
        st.subheader("Sipariş Bilgileri")
        name = st.text_input("İsim")
        email = st.text_input("E-posta")
        address = st.text_area("Adres")

        if st.button("Siparişi Gönder"):
            st.success("Siparişiniz başarıyla alındı! Size en kısa sürede dönüş yapılacaktır.")

    except Exception as e:
        st.error("Dosya okunurken bir hata oluştu. Lütfen geçerli bir STL dosyası yükleyin.")
    finally:
        os.remove(tmp_file_path)
else:
    st.info("Lütfen bir STL dosyası yükleyin.")
