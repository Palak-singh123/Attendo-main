import streamlit as st
import base64
from pathlib import Path


def image_base64(path: Path) -> str:
    """Convert a local image into a Base64 string."""
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


# =========================================================
# HOME BACKGROUND
# =========================================================

def style_background_home():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url(
                    'data:image/png;base64,{image_base64(Path("assets/Background.png"))}'
                );
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD BACKGROUND
# =========================================================

def style_background_dashboard():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url(
                    'data:image/png;base64,{image_base64(Path("assets/TeacherBackground.png"))}'
                );
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BASE LAYOUT
# =========================================================

def style_base_layout():
    st.markdown(
        """
        <style>

        /* =================================================
           GOOGLE FONTS
        ================================================= */

        @import url(
            'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@200;300;400;500;600;700;800&family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap'
        );


        /* =================================================
           HIDE STREAMLIT DEFAULT UI
        ================================================= */

        #MainMenu,
        footer,
        header {
            visibility: hidden;
        }


        /* =================================================
           MAIN CONTAINER
        ================================================= */

        .block-container {
            padding-top: 1.5rem !important;
        }


        /* =================================================
           HEADINGS
        ================================================= */

        h1,
        h2 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 3.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
            font-weight: 900 !important;
        }


        /* =================================================
           TEXT
        ================================================= */

        h3,
        h4,
        p {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 400 !important;
        }


        /* =================================================
           PRIMARY BUTTON — ORANGE
        ================================================= */

        div.stButton > button[kind="primary"] {
            background-color: #F07816 !important;
            color: white !important;
            border: none !important;
            border-radius: 1.5rem !important;
            padding: 10px 20px !important;
            transition: all 0.25s ease-in-out !important;
            cursor: pointer !important;
        }


        /* =================================================
           PRIMARY BUTTON — ORANGE HOVER
        ================================================= */

        div.stButton > button[kind="primary"]:hover {
            background-color: #E86608 !important;
            color: white !important;
            transform: scale(1.05) !important;
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.20) !important;
        }


        /* =================================================
           PRIMARY BUTTON — ORANGE CLICK
        ================================================= */

        div.stButton > button[kind="primary"]:active {
            transform: scale(0.98) !important;
        }


        /* =================================================
           SECONDARY BUTTON — PURPLE
        ================================================= */

        div.stButton > button[kind="secondary"] {
            background-color: #6C63FF !important;
            color: white !important;
            border: none !important;
            border-radius: 1.5rem !important;
            padding: 10px 20px !important;
            transition: all 0.25s ease-in-out !important;
            cursor: pointer !important;
        }


        /* =================================================
           SECONDARY BUTTON — PURPLE HOVER
        ================================================= */

        div.stButton > button[kind="secondary"]:hover {
            background-color: #574FE0 !important;
            color: white !important;
            transform: scale(1.05) !important;
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.20) !important;
        }


        /* =================================================
           SECONDARY BUTTON — PURPLE CLICK
        ================================================= */

        div.stButton > button[kind="secondary"]:active {
            transform: scale(0.98) !important;
        }
        /* TERTIARY BUTTON —*/

div.stButton > button[kind="tertiary"] {
    background-color: #EFC5DD  !important;
    color: white !important;
    border: none !important;
    border-radius: 1.5rem !important;
    padding: 10px 20px !important;
    transition: all 0.25s ease-in-out !important;
    cursor: pointer !important;
}

/* TERTIARY BUTTON — HOVER */

div.stButton > button[kind="tertiary"]:hover {
    background-color: #E5AFD0  !important;
    color: white !important;
    transform: scale(1.05) !important;
    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.20) !important;
}

/* TERTIARY BUTTON — CLICK */

div.stButton > button[kind="tertiary"]:active {
    transform: scale(0.98) !important;
}

        </style>
        """,
        unsafe_allow_html=True
    )