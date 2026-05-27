import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

st.set_page_config(
    layout="centered"
)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def extractColors(image, num_colors=5):
    img = image.copy()
    img.thumbnail((150, 150))
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    img_array = np.array(img)
    pixels = img_array.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=num_colors, init='k-means++', random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    colors = kmeans.cluster_centers_.astype(int)
    return colors

#UI

st.title("Image Color Palette Generator")
st.write("Unggah gambar dan temukan 5 warna paling dominan")

st.write("---")

uploadedFile = st.file_uploader("Upload file gambar (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploadedFile is not None:
    image = Image.open(uploadedFile)
    
    st.image(image, caption="Gambar yang Anda Unggah", use_container_width=True)
    
    st.write("---")
    st.subheader("5 Warna Paling Dominan:")
    
    with st.spinner("Sedang menganalisis warna gambar..."):
        dominant_colors = extractColors(image, num_colors=5)
    
    cols = st.columns(5)
    
    for i, color in enumerate(dominant_colors):
        hex_code = rgb_to_hex(color)
        
        with cols[i]:
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
            st.code(hex_code, language="")
            st.caption(f"RGB: {color[0]}, {color[1]}, {color[2]}")

else:
    st.info("Silakan unggah gambar terlebih dahulu pada tombol di atas untuk melihat palet warna.")