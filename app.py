import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# Konfigurasi halaman Streamlit agar terlihat menarik
st.set_page_config(
    page_title="Ekstraktor Palet Warna",
    page_icon="🎨",
    layout="centered"
)

# Fungsi untuk mengubah nilai RGB menjadi Hex Code
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# Fungsi utama untuk mengekstrak warna dominan menggunakan K-Means
def extract_dominant_colors(image, num_colors=5):
    # Ubah ukuran gambar agar proses clustering berjalan lebih cepat
    img = image.copy()
    img.thumbnail((150, 150))
    
    # Pastikan gambar dalam mode RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    # Konversi gambar menjadi array numpy dan ubah bentuknya (flatten)
    img_array = np.array(img)
    pixels = img_array.reshape(-1, 3)
    
    # Gunakan K-Means untuk mengelompokkan warna
    kmeans = KMeans(n_clusters=num_colors, init='k-means++', random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Ambil titik tengah (centroid) sebagai warna dominan
    colors = kmeans.cluster_centers_.astype(int)
    return colors

# --- Tampilan Antarmuka (UI) ---

st.title("🎨 Image Color Palette Generator")
st.write("Unggah gambar Anda dan temukan **5 warna paling dominan** yang membentuk estetika gambar tersebut secara instan!")

st.write("---")

# Komponen Upload Gambar
uploaded_file = st.file_uploader("Pilih file gambar (PNG, JPG, JPEG)...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Buka dan tampilkan gambar yang diunggah
    image = Image.open(uploaded_file)
    
    # Membuat dua kolom untuk estetika layout (Gambar di kiri/tengah)
    st.image(image, caption="Gambar yang Anda Unggah", use_container_width=True)
    
    st.write("---")
    st.subheader("✨ 5 Warna Paling Dominan:")
    
    # Animasi loading saat memproses gambar
    with st.spinner("Sedang menganalisis warna gambar..."):
        dominant_colors = extract_dominant_colors(image, num_colors=5)
    
    # Menampilkan palet warna dalam bentuk grid 5 kolom
    cols = st.columns(5)
    
    for i, color in enumerate(dominant_colors):
        hex_code = rgb_to_hex(color)
        
        with cols[i]:
            # Membuat kotak warna menggunakan HTML & CSS custom agar menarik
            st.markdown(
                f"""
                <div style="
                    background-color: {hex_code}; 
                    height: 120px; 
                    border-radius: 12px; 
                    margin-bottom: 8px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                    transition: transform 0.2s;
                "></div>
                """, 
                unsafe_allow_html=True
            )
            # Menampilkan hex code yang bisa langsung disalin (copyable)
            st.code(hex_code, language="")
            st.caption(f"RGB: {color[0]}, {color[1]}, {color[2]}")

else:
    # Tampilan placeholder saat belum ada gambar yang diunggah
    st.info("💡 Silakan unggah gambar terlebih dahulu pada tombol di atas untuk melihat palet warna.")