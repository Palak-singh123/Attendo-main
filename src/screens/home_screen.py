# 
import base64
from pathlib import Path
import streamlit as st

from src.components.footer import footer_home
from src.components.header import header_home
from src.UI.base_layout import style_base_layout, style_background_home


# =========================================================
# IMAGE → BASE64
# =========================================================

def image_base64(path: Path) -> str:
    """Convert a local image into Base64."""
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


# =========================================================
# HOME SCREEN
# =========================================================

def home_screen():

    style_background_home()
    style_base_layout()
    header_home()

    # =====================================================
    # PAGE CSS
    # =====================================================

    st.markdown(
        """
        <style>

        /* Remove Streamlit vertical gaps */
        div[data-testid="stVerticalBlock"] {
            gap: 0rem;
        }

        /* ================================================
           ROLE CARD
        ================================================ */

        .role-card {
            position: relative;

            width: min(820px, calc(100vw - 80px));
            height: 200px;

            margin: 0 auto;

            display: flex;
            align-items: center;

            background: rgba(255, 255, 255, 0.90);

            border: 1px solid rgba(110, 80, 180, 0.16);
            border-radius: 32px;

            padding: 15px 110px 15px 28px;

            box-sizing: border-box;

            box-shadow:
                0 10px 30px rgba(85, 55, 150, 0.06);

            overflow: hidden;
        }


        /* ================================================
           CHARACTER
        ================================================ */

        .role-img {
            width: 200px;
            height: 185px;

            flex: 0 0 200px;

            object-fit: contain;
        }


        /* ================================================
           TEXT
        ================================================ */

        .role-content {
            flex: 1;
            min-width: 0;

            margin-left: 20px;
        }


        .role-title {
            margin: 0;

            color: #18245c;

            font-family: 'Plus Jakarta Sans', sans-serif;

            font-size: 36px;
            font-weight: 750;

            line-height: 1.2;

            white-space: nowrap;
        }


        .student-title {
            color: #673de6;
        }


        .teacher-title {
            color: #f07816;
        }


        .role-description {
            margin: 13px 0 0 0;

            color: #64708a;

            font-family: 'Poppins', sans-serif;

            font-size: 17px;
            line-height: 1.55;

            font-weight: 400;
        }


        /* ================================================
           ARROW
        ================================================ */

        .role-arrow {
            position: absolute;

            right: 25px;
            top: 50%;

            transform: translateY(-50%);

            width: 70px;
            height: 70px;

            display: flex;
            align-items: center;
            justify-content: center;

            border: none;
            border-radius: 50%;

            text-decoration: none;

            font-family: Arial, sans-serif;
            font-size: 35px;
            font-weight: 500;

            cursor: pointer;

            transition:
                background 0.2s ease,
                color 0.2s ease,
                transform 0.2s ease;
        }


        /* ================================================
           STUDENT ARROW
        ================================================ */

        .student-arrow {
            background: #EEE7FF;
            color: #6438E5;
        }


        .student-arrow:hover {
            background: #DFD1FF;
            color: #4E1EC4;

            transform: translateY(-50%) scale(1.08);
        }


        /* ================================================
           TEACHER ARROW
        ================================================ */

        .teacher-arrow {
            background: #FFF0E5;
            color: #F07816;
        }


        .teacher-arrow:hover {
            background: #FFE0CC;
            color: #E86608;

            transform: translateY(-50%) scale(1.08);
        }


        /* ================================================
           GAP BETWEEN CARDS
        ================================================ */

        .role-gap {
            height: 30px;
        }


        /* ================================================
           MOBILE
        ================================================ */

        @media (max-width: 700px) {

            .role-card {
                width: calc(100vw - 30px);
                height: 180px;

                padding:
                    12px
                    85px
                    12px
                    15px;

                border-radius: 24px;
            }


            .role-img {
                width: 110px;
                height: 155px;

                flex: 0 0 110px;
            }


            .role-content {
                margin-left: 10px;
            }


            .role-title {
                font-size: 23px;
            }


            .role-description {
                margin-top: 8px;
                font-size: 12px;
            }


            .role-arrow {
                right: 15px;

                width: 55px;
                height: 55px;

                font-size: 28px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


    # =====================================================
    # IMAGE DATA
    # =====================================================

    student_img = image_base64(
        Path("assets/Studentimg.png")
    )

    teacher_img = image_base64(
        Path("assets/Teacherimg.png")
    )


    # =====================================================
    # STUDENT CARD
    # =====================================================

    st.html(
        f"""
        <div class="role-card">

            <img
                src="data:image/png;base64,{student_img}"
                class="role-img"
                alt="Student"
            >

            <div class="role-content">

                <h2 class="role-title">
                    I'm a
                    <span class="student-title">
                        Student
                    </span>
                </h2>

                <p class="role-description">
                    Access your classes, assignments,<br>
                    and learning resources.
                </p>

            </div>

            <a
                href="/student"
                class="role-arrow student-arrow"
                aria-label="Go to Student page"
            >
                →
            </a>

        </div>
        """
    )


    # =====================================================
    # GAP
    # =====================================================

    st.html(
        """
        <div class="role-gap"></div>
        """
    )


    # =====================================================
    # TEACHER CARD
    # =====================================================

    st.html(
        f"""
        <div class="role-card">

            <img
                src="data:image/png;base64,{teacher_img}"
                class="role-img"
                alt="Teacher"
            >

            <div class="role-content">

                <h2 class="role-title">
                    I'm a
                    <span class="teacher-title">
                        Teacher
                    </span>
                </h2>

                <p class="role-description">
                    Create classes, manage students<br>
                    and share resources.
                </p>

            </div>

            <a
                href="/teacher"
                class="role-arrow teacher-arrow"
                aria-label="Go to Teacher page"
            >
                →
            </a>

        </div>
        """
    )
    footer_home()    


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    home_screen()