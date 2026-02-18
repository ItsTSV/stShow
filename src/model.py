import streamlit as st
from rembg import remove
from PIL import Image
import io


# Caching
@st.cache_data
def process_image(img_bytes):
    """Process the uploaded image and remove the background. Needs to accept bytes, as img cant be hashed."""
    img = Image.open(io.BytesIO(img_bytes))
    return remove(img)


# Random text go
st.title("Background Remover")
st.markdown("""
This page shows how to use pretrained models and caching in Streamlit. This model uses the 'rembg' library, which
is a wrapper around the U2Net architecture. Caching is used to prevent the model from repeatedly processing
the same image, which can be time consuming. For caching, bytes need to be used, as Streamlit cannot hash images
directly.
""")

# File uploader
uploaded_file = st.file_uploader(
    "Upload a photo (person, object, pet...)", type=["jpg", "jpeg", "png"]
)
if uploaded_file:
    file_bytes = uploaded_file.getvalue()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(Image.open(io.BytesIO(file_bytes)), width="content")
        with st.spinner("Removing background...", show_time=True):
            result = process_image(file_bytes)
    with col2:
        st.subheader("Result")
        st.image(result, width="content")
    st.divider()

    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    byte_image = buffer.getvalue()

    st.download_button(
        label="Download clear PNG",
        data=byte_image,
        file_name="removed_bg.png",
        mime="image/png",
        width="content",
    )
