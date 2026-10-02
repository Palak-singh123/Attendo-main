import streamlit as st
from pathlib import Path
import base64
def image_base64(path: Path) -> str:
    """Convert a local image into Base64."""
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")
def teacher_page():    
    teacherBG_img = image_base64(
        Path("assets/TeacherBackground.png")
    )

    st.html(f"""
        <div class="teacher-bg">
            <img src="data:image/png;base64,{teacherBG_img}" alt="Teacher">
        </div>
""")

teacher_page()