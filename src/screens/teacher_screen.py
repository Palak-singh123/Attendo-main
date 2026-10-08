import time

import streamlit as st

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dailog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.UI.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    create_subject,
    teacher_login,
    get_teacher_subjects
)

from src.components.dialog_add_photo import add_photos_dialog

def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return

    if "teacher_login_type" not in st.session_state:
        st.session_state.teacher_login_type = "login"

    if st.session_state.teacher_login_type == "login":
        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_common_style():

    st.markdown(
        """
        <style>
f
        @import url(
            'https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Poppins:wght@400;500;600;700&display=swap'
        );

        .LoginTitle p,
        .RegisterTitle p {
            color: #18245c !important;
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 40px !important;
            font-weight: 400 !important;
            margin-left: 15px !important;
            margin-top: 1rem !important;
            margin-bottom: 0 !important;
        }

        .RegisterTitle p {
            margin-top: 0.3rem !important;
            margin-bottom: 0 !important;
        }

        div[data-testid="stTextInput"] label {
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 15px !important;
            font-weight: 500 !important;
        }

        .st-key-styledinput1 input,
        .st-key-styledinput2 input,
        .st-key-register_username input,
        .st-key-register_name input,
        .st-key-register_password input,
        .st-key-register_confirm_password input {
            border-radius: 10px !important;
            background-color: #ffffff !important;
            color: #18245c !important;
            border: 2px solid #ddd9ff !important;
            outline: none !important;
            box-shadow: none !important;
            height: 42px !important;
            min-height: 42px !important;
            padding: 0 14px !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 14px !important;
        }

        .st-key-styledinput1 input:hover,
        .st-key-styledinput2 input:hover,
        .st-key-register_username input:hover,
        .st-key-register_name input:hover,
        .st-key-register_password input:hover,
        .st-key-register_confirm_password input:hover {
            border-color: #9b95ff !important;
        }

        .st-key-styledinput1 input:focus,
        .st-key-styledinput2 input:focus,
        .st-key-register_username input:focus,
        .st-key-register_name input:focus,
        .st-key-register_password input:focus,
        .st-key-register_confirm_password input:focus {
            border-color: #6C63FF !important;
            box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.12) !important;
            outline: none !important;
        }

        .st-key-styledinput1 input::placeholder,
        .st-key-styledinput2 input::placeholder,
        .st-key-register_username input::placeholder,
        .st-key-register_name input::placeholder,
        .st-key-register_password input::placeholder,
        .st-key-register_confirm_password input::placeholder {
            color: #777889 !important;
            opacity: 0.7 !important;
        }

        hr.login-divider,
        hr.register-divider {
            border: none !important;
            height: 2px !important;
            background-color: #6C63FF !important;
        }

        hr.login-divider {
            margin: 40px 0 !important;
        }

        hr.register-divider {
            margin: 18px 0 !important;
        }

        .register-page {
            margin-top: -5px !important;
        }

        .register-page div[data-testid="stVerticalBlock"] {
            gap: 0.25rem !important;
        }

        .TeacherWelcome {
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 34px !important;
            font-weight: 700 !important;
            text-align: center !important;
            margin-bottom: 15px !important;
        }

        div[data-testid="stButton"] button {
            font-family: 'Poppins', sans-serif !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px !important;
            font-family: 'Poppins', sans-serif !important;
        }

        div[data-testid="stAlert"] p {
            font-family: 'Poppins', sans-serif !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def teacher_dashboard():

    teacher_common_style()

    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(
        2,
        vertical_alignment="bottom",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:

        st.markdown(
            f"""
            <div class="TeacherWelcome">
                Welcome, {teacher_data['name']}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Logout",
            type="primary",
            key="teacher_logout",
            shortcut="control+backspace"
        ):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("teacher_data", None)
            st.session_state.pop("current_teacher_tab", None)
            st.switch_page("app.py")

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    st.markdown(
        '<div class="DashboardTabs">',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.columns(
        3,
        gap="medium"
    )

    with tab1:
        if st.button(
            "Take Attendance",
            type=(
                "primary"
                if st.session_state.current_teacher_tab == "take_attendance"
                else "secondary"
            ),
            width="stretch",
            icon=":material/face_retouching_natural:",
            key="teacher_take_attendance"
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:

        if st.button(
            "Manage Subjects",
            type=(
                "primary"
                if st.session_state.current_teacher_tab == "manage_subjects"
                else "secondary"
            ),
            width="stretch",
            icon=":material/menu_book:",
            key="teacher_manage_subjects"
        ):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
 
        if st.button(
            "Attendance Records",
            type=(
                "primary"
                if st.session_state.current_teacher_tab == "attendance_records"
                else "secondary"
            ),
            width="stretch",
            icon=":material/assignment:",
            key="teacher_attendance_records"
        ):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()


    if st.session_state.current_teacher_tab == "take_attendance":

        st.markdown(
            """
            <div style="
                margin-top:25px;
                padding:25px;
                border-radius:20px;
                background:rgba(255,255,255,0.65);
                text-align:center;
                font-family:Poppins,sans-serif;
                color:#18245c;
            ">
                <h3>Take Attendance</h3>
                <p>Face recognition attendance panel will appear here.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_id = st.session_state.teacher_data['teacher_id']
        col1,col2 = st.columns(2)
        with col1:
          st.html(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Poppins:wght@400;500;600;700&display=swap');

            .manage_subj {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 35px !important;
                font-weight: 400 !important;
                color: #000000 !important;
                line-height: 1.2 !important;
                margin: 0 !important;
                padding: 0 !important;
                margin-top:2rem !important;
            }
            .subj_divider {
                border: none;
                height: 1px;
                background-color: #6C63FF;
                margin-top: 10px;
                margin-bottom: 20px;
                width:700px;
            }
            
        </style>
        <hr class="subj_divider">
        <p class="manage_subj">Manage Subjects</p>
        """,
    )

        with col2:
             st.markdown("""
               <style>
                    .st-key-create_subject button {
                       background-color: #6C63FF !important;
                       color: white !important;
                       border: 2px solid #6C63FF !important;
                       border-radius: 10px !important;
                       margin-top:1.5rem;
                       font-family: 'Poppins', sans-serif !important;
                       font-size: 15px !important;
                       font-weight: 600 !important;

                       height: 45px !important;
                   }

                   .st-key-create_subject button:hover {
                       background-color: #574FE8 !important;
                       border-color: #574FE8 !important;
                       color: white !important;
                   }
               </style>
""",unsafe_allow_html=True)
             if st.button("Create New Subject", width="stretch",type="primary",key="create_subject"):
                 create_subject_dialog(teacher_id)


 #   list all subjects
        subjects = get_teacher_subjects(teacher_id)
        if subjects:
            for sub in subjects:
                stats = [
                    ("👥","Students",sub['total_students']),
                    ("🕰️","Classes",sub['total_classes']),
                ]
            def share_btn():
                if st.button(f"Share Code: {sub['name']}",type="primary",key=f"share_{sub['subject_code']}",icon=":material/share:"):
                    share_subject_dialog(sub['name'],sub['subject_code'])
                st.space()

            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = stats,
                footer_callback = share_btn
            )
        else:
            st.info("NO SUBJECTS FOUND,CREATE ONE ABOVE")       


    elif st.session_state.current_teacher_tab == "attendance_records":

        st.markdown(
            """
            <div style="
                margin-top:25px;
                padding:25px;
                border-radius:20px;
                background:rgba(255,255,255,0.65);
                text-align:center;
                font-family:Poppins,sans-serif;
                color:#18245c;
            ">
                <h3>Attendance Records</h3>
                <p>Attendance records will appear here.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    footer_dashboard()


def login_teacher(username, password):

    if not username or not password:
        return False

    teacher = teacher_login(
        username,
        password
    )

    if teacher:

        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True

        return True

    return False


def teacher_screen_login():

    teacher_common_style()

    c1, c2 = st.columns(
        2,
        vertical_alignment="bottom",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:

        if st.button(
            "Go back to home",
            type="primary",
            key="loginbackbtn",
            shortcut="control+backspace"
        ):
            st.session_state["login_state"] = None
            st.switch_page("app.py")

    st.markdown(
        """
        <div class="LoginTitle">
            <p>Login using password</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy",
        key="styledinput1"
    )

    teacher_password = st.text_input(
        "Enter password",
        type="password",
        key="styledinput2",
        placeholder="Enter your password"
    )

    st.markdown(
        """
        <hr class="login-divider">
        """,
        unsafe_allow_html=True
    )

    btnc1, btnc2 = st.columns(2)

    with btnc1:

        if st.button(
            "Login",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
            type="primary"
        ):

            if login_teacher(
                teacher_username,
                teacher_password
            ):

                st.toast(
                    "Welcome back!",
                    icon="👋🏻"
                )

                time.sleep(1)
                st.rerun()

            else:

                st.error(
                    "Invalid username and password"
                )

    with btnc2:

        if st.button(
            "Register Instead",
            icon=":material/passkey:",
            width="stretch",
            type="secondary"
        ):

            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


def register_teacher(
    teacher_username,
    teacher_name,
    teacher_password,
    teacher_confirm_password
):

    if (
        not teacher_username
        or not teacher_name
        or not teacher_password
        or not teacher_confirm_password
    ):
        return False, "All Fields are required!"

    if check_teacher_exists(teacher_username):
        return False, "Username already taken"

    if teacher_password != teacher_confirm_password:
        return False, "Password doesn't match"

    try:

        create_teacher(
            teacher_username,
            teacher_password,
            teacher_name
        )

        return True, "Successfully Created! Login Now"

    except Exception as e:

        return False, str(e)


def teacher_screen_register():

    teacher_common_style()

    st.markdown(
        """
        <div class="register-page">
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(
        2,
        vertical_alignment="bottom",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:

        if st.button(
            "Go back to home",
            type="secondary",
            key="registerbackbtn",
            shortcut="control+backspace"
        ):
            st.session_state["login_state"] = None
            st.switch_page("app.py")

    st.markdown(
        """
        <div class="RegisterTitle">
            <p>Register your teacher profile</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.space(size="small")

    teacher_username = st.text_input(
        "Enter username",
        placeholder="Ananya Roy",
        key="register_username"
    )

    teacher_name = st.text_input(
        "Enter name",
        placeholder="Ananya Roy",
        key="register_name"
    )

    teacher_password = st.text_input(
        "Enter password",
        type="password",
        key="register_password",
        placeholder="Enter your password"
    )

    teacher_confirm_password = st.text_input(
        "Confirm your password",
        type="password",
        key="register_confirm_password",
        placeholder="Confirm your password"
    )

    st.markdown(
        """
        <hr class="register-divider">
        """,
        unsafe_allow_html=True
    )

    btnc1, btnc2 = st.columns(2)

    with btnc1:

        if st.button(
            "Register",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
            type="primary"
        ):

            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_password,
                teacher_confirm_password
            )

            if success:

                st.success(message)

                time.sleep(2)

                st.session_state.teacher_login_type = "login"
                st.rerun()

            else:

                st.error(message)

    with btnc2:

        if st.button(
            "Login Instead",
            icon=":material/passkey:",
            width="stretch",
            type="secondary"
        ):

            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )

