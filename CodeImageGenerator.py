import streamlit as st
from PIL import Image
from code_to_image import convert_code_to_image
import os
import tempfile
from io import BytesIO
import base64

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

st.title("Code to Image Converter")

# Input fields
code = st.text_area("Enter your code here:")
font_size = st.slider("Font size:", min_value=10, max_value=30, value=14, step=1)
padding = st.slider("Padding:", min_value=5, max_value=30, value=10, step=1)
border_width = st.slider("Border width:", min_value=1, max_value=10, value=5, step=1)
gradient_size = st.slider("Gradient size:", min_value=1, max_value=20, value=5, step=1)
corner_radius = st.slider("Corner radius:", min_value=0, max_value=20, value=10, step=1)
dpi_scale= st.slider("Scaling Factor:", min_value=1, max_value=20, value=1, step=1)

# Color pickers
col1, col2, col3 = st.columns(3)

with col1:
    text_color = st.color_picker("Text color:", value='#0AFA9E')
with col2:
    background_color = st.color_picker("Background color:", value='#1D1717')
with col3:
    border_color = st.color_picker("Gradient color:", value='#00AFEF')

# Font selection dropdown
fonts = ["Roboto","Custom"]# "Times New Roman", "Terminal", "Roboto", "custom"]

font_choice = st.selectbox("Font:", options=fonts)

if font_choice == "Custom":
    custom_font_file = st.file_uploader("Upload a font file (.ttf or .otf):")
    if custom_font_file:
        font_path = custom_font_file
    else:
        font_path = "Roboto.ttf"
else:
    font_path = f"{font_choice}.ttf"

if st.button("Generate Image"):
    # Call the convert_code_to_image function with user inputs
    img = convert_code_to_image(
        code,
        font_path=font_path,
        font_size=font_size,
        background_color=hex_to_rgb(background_color),
        text_color=hex_to_rgb(text_color),
        padding=padding,
        border_width=border_width,
        border_color=hex_to_rgb(border_color),
        gradient_size=gradient_size,
        corner_radius=corner_radius,
        dpi_scale=dpi_scale
    )

    # Display the generated image
    st.image(img, caption="Generated Image", use_column_width=True)

    # Save image button with styling and save functionality

    def get_image_download_link(img, file_name="code_image.png", text="Save Image"):
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:image/png;base64,{img_str}" download="{file_name}" style="text-decoration:none;color:white;">{text}</a>'
        return href

    file_name = st.text_input("Enter file name:", "code_image.png")
    st.markdown(get_image_download_link(img, file_name=file_name), unsafe_allow_html=True)
