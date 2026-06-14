import streamlit as st
import base64

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

def set_style(show_sidebar):
    bg_base64 = get_base64_image("gambar.jpeg")
    bg_css = f"background-image: url('data:image/jpeg;base64,{bg_base64}');" if bg_base64 else "background: #eef2f7;"
    
    sidebar_display = "block" if show_sidebar else "none"

    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ {bg_css} background-size: cover; background-attachment: fixed; }}
    [data-testid="stSidebar"] {{ display: {sidebar_display} !important; background: white !important; }}
    header {{ visibility: hidden; }}
    .glass {{ background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); border-radius: 20px; padding: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
    </style>
    """, unsafe_allow_html=True)