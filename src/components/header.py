import streamlit as st
from pathlib import Path
import base64
def image_base64(path: Path) -> str:
    """Convert a local image into a Base64 string for HTML display."""
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")
def header_home():
   st.markdown(
       """
       <style>
           .AttendoLogo {
               text-align: center;
               margin: 20px 0;
           }
       </style>
       """
   ,unsafe_allow_html=True)
   st.html(
       f"""
       <div class="AttendoLogo">
          <img  
              src="data:image/png;base64,{image_base64(Path("assets/AttendoLogo.png"))}" 
              width="500">
       </div>
       """,
   )
    
   st.markdown("""
                
   """, unsafe_allow_html=True)
def header_dashboard():
    st.markdown(
        """
        <style>
            .AttendoLogoDashboard {
                text-align: center;
            }

            .AttendoLogoDashboard img {
                position: relative;
                left: -80px !important;
                top: 20px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.html(
        f"""
        <div class="AttendoLogoDashboard">
            <img
                src="data:image/png;base64,{image_base64(Path("assets/AttendoLogo.png"))}"
                width="250"
            >
        </div>
        """
    )
