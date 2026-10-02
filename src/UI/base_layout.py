import streamlit as st
import base64
from pathlib import Path

def image_base64(path: Path) -> str:
    """Convert a local image into a Base64 string for HTML display."""
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")
    
def style_background_home():
   st.html(
       f"""
       <style>
       .stApp {{
           background-image: url('data:image/png;base64,{image_base64(Path("assets/Background.png"))}');
              background-size: cover;
       }}
       </style>
       """
   )

def style_base_dashboard():
    st.markdown(
        """
        <style>
        .stApp {
            background: #E0E3FF  !important;
            min-height: 100vh;
        }
        </style>
        """,
        unsafe_allow_html=True  
    )    
def style_base_layout():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
        /*Hide top toolbar of streamlit */
              # #mainMenu,footer,header {
              # visibility: hidden;
              # }
              # .block-container{
              #     padding-top: 1.5rem !important;
              # }
              h1,h2{
                  font-family: 'Plus Jakarta Sans', sans-serif !important;
                  font-size:3.5rem !important;
                  line-height:1.1 !important;
                  margin-bottom:0rem !important;
                  font-weight:900 !important;
              }
              h3,h4,p{
                  font-family: 'Poppins', sans-serif !important;
                  font-weight:400 !important; 
              }
  
        </style>
        """,
        unsafe_allow_html=True  
    )   
    