import time
import streamlit as st
import numpy as np
import pandas as pd

from datetime import datetime

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dailog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.UI.base_layout import (
    style_background_dashboard,
    style_base_layout
)
from src.components.dialog_add_photo import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.database.config import supabase
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher
)
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from datetime import datetime
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

        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Poppins:wght@400;500;600;700&display=swap');

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
            background-color: #fff4d6 !important;
            border: 1px solid #f2c96d !important;
            border-radius: 12px !important;
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
        }

        div[data-testid="stAlert"] * {
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
        }

        div[data-testid="stSelectbox"] label {
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] {
            background: #ffffff !important;
            color: #18245c !important;
            border-radius: 12px !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background: #ffffff !important;
            color: #18245c !important;
            border: 2px solid #ddd9ff !important;
            border-radius: 12px !important;
            min-height: 48px !important;
            box-shadow: none !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] * {
            background-color: transparent !important;
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
            fill: #18245c !important;
            color: #18245c !important;
        }

        div[data-testid="stSelectbox"] [data-baseweb="select"]:focus-within > div {
            border: 2px solid #6C63FF !important;
            box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.12) !important;
        }

        div[role="listbox"] {
            background-color: #ffffff !important;
            border: 1px solid #ddd9ff !important;
            border-radius: 12px !important;
        }

        div[role="option"] {
            background-color: #ffffff !important;
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
        }

        div[role="option"] * {
            color: #18245c !important;
        }

        div[role="option"]:hover {
            background-color: #eee7ff !important;
            color: #18245c !important;
        }

        .st-key-clear_photos button,
        .st-key-run_face_analysis button,
        .st-key-voice_attendance button {
            border-radius: 14px !important;
            height: 48px !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        .st-key-clear_photos button {
            background-color: #ffffff !important;
            color: #18245c !important;
            border: 2px solid #ddd9ff !important;
        }

        .st-key-clear_photos button:hover {
            background-color: #f4f0ff !important;
            border-color: #6C63FF !important;
            color: #18245c !important;
        }

        .st-key-run_face_analysis button {
            background-color: #f078b0 !important;
            color: white !important;
            border: 2px solid #f078b0 !important;
        }

        .st-key-run_face_analysis button:hover {
            background-color: #e65b9a !important;
            border-color: #e65b9a !important;
            color: white !important;
        }

        .st-key-voice_attendance button {
            background-color: #6C63FF !important;
            color: white !important;
            border: 2px solid #6C63FF !important;
        }

        .st-key-voice_attendance button:hover {
            background-color: #574FE8 !important;
            border-color: #574FE8 !important;
            color: white !important;
        }

        [class*="st-key-photo_container_"] {
            position: relative !important;
        }

        [class*="st-key-photo_container_"] [class*="st-key-remove_photo_"] {
            position: absolute !important;
            top: 8px !important;
            right: 8px !important;
            z-index: 100 !important;
        }

        [class*="st-key-remove_photo_"] button {
            width: 30px !important;
            height: 30px !important;
            min-height: 30px !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 50% !important;
            background: #ffffff !important;
            color: #18245c !important;
            border: 2px solid #ffffff !important;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.18) !important;
            font-family: Arial, sans-serif !important;
            font-size: 19px !important;
            font-weight: 700 !important;
            line-height: 26px !important;
        }

        [class*="st-key-remove_photo_"] button:hover {
            background: #f078b0 !important;
            color: #ffffff !important;
            border-color: #f078b0 !important;
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

        teacher_id = st.session_state.teacher_data["teacher_id"]

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
                <h3>Take AI Attendance</h3>
                <p>Face recognition attendance panel will appear here.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if "attendance_images" not in st.session_state:
            st.session_state.attendance_images = []

        subjects = get_teacher_subjects(teacher_id)

        if not subjects:

            st.warning(
                "You haven't created any subjects yet! Please create one to begin!"
            )

            footer_dashboard()
            return

        subject_options = {
            f"{s['name']} - {s['subject_code']}": s['subject_id']
            for s in subjects
        }

        col1, col2 = st.columns(
            [3, 1],
            vertical_alignment="bottom"
        )

        with col1:

            selected_subject_label = st.selectbox(
                "Select Subject",
                options=list(subject_options.keys()),
                key="attendance_subject"
            )

        with col2:

            if st.button(
                "Add Photos",
                type="primary",
                icon=":material/photo_prints:",
                width="stretch",
                key="add_photos"
            ):
                add_photos_dialog()

        selected_subject_id = subject_options[
            selected_subject_label
        ]

        st.html("<hr>")

        if st.session_state.attendance_images:

            st.markdown(
                """
                <h3 style="
                    color:#18245c;
                    font-family:Poppins,sans-serif;
                    margin-top:20px;
                ">
                    Added Photos
                </h3>
                """,
                unsafe_allow_html=True
            )

            gallery_cols = st.columns(4)

            for idx, img in enumerate(
                st.session_state.attendance_images
            ):

                with gallery_cols[idx % 4]:

                    with st.container(
                        key=f"photo_container_{idx}",
                        border=False
                    ):

                        if st.button(
                            "×",
                            key=f"remove_photo_{idx}",
                            help="Remove this photo"
                        ):

                            st.session_state.attendance_images.pop(
                                idx
                            )

                            if "processed_photo_hashes" in st.session_state:
                                st.session_state.processed_photo_hashes = set()

                            st.rerun()

                        st.image(
                            img,
                            width="stretch",
                            caption=f"Photo {idx + 1}"
                        )

        has_photos = bool(
            st.session_state.attendance_images
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            if st.button(
                "Clear all photos",
                width="stretch",
                type="secondary",
                icon=":material/delete:",
                key="clear_photos"
            ):

                if not has_photos:

                    st.warning(
                        "You have no photos to delete."
                    )

                else:

                    st.session_state.attendance_images = []

                    if "processed_photo_hashes" in st.session_state:
                        st.session_state.processed_photo_hashes = set()

                    st.rerun()

        with c2:

            if st.button(
                "Run Face Analysis",
                width="stretch",
                type="primary",
                icon=":material/analytics:",
                key="run_face_analysis",
                disabled=not has_photos
            ):

                with st.spinner(
                    "Scanning classroom photos..."
                ):

                    all_detected_ids = {}

                    for idx, img in enumerate(
                        st.session_state.attendance_images
                    ):

                        img_np = np.array(
                            img.convert("RGB")
                        )

                        detected, _, _ = predict_attendance(
                            img_np
                        )

                        if detected:

                            for sid in detected.keys():

                                student_id = int(sid)

                                all_detected_ids.setdefault(
                                    student_id,
                                    []
                                ).append(
                                    f"Photo {idx + 1}"
                                )

                    enrolled_res = (
                        supabase
                        .table("subject_students")
                        .select("*,students(*)")
                        .eq(
                            "subject_id",
                            selected_subject_id
                        )
                        .execute()
                    )

                    enrolled_students = enrolled_res.data

                    if not enrolled_students:

                        st.warning(
                            "No students in this course."
                        )

                    else:

                        results = []
                        attendance_to_log = []

                        current_timestamp = (
                            datetime.now()
                            .strftime(
                                "%Y-%m-%dT%H:%M:%S"
                            )
                        )

                        for node in enrolled_students:

                            student = node["students"]

                            sources = all_detected_ids.get(
                                int(student["student_id"]),
                                []
                            )

                            is_present = len(sources) > 0

                            results.append(
                                {
                                    "Name": student["name"],
                                    "ID": student["student_id"],
                                    "Sources": (
                                        ",".join(sources)
                                        if is_present
                                        else "-"
                                    ),
                                    "Status": (
                                        "✅ Present"
                                        if is_present
                                        else "❌ Absent"
                                    )
                                }
                            )

                            attendance_to_log.append(
                                {
                                    "student_id": student["student_id"],
                                    "subject_id": selected_subject_id,
                                    "timestamp": current_timestamp,
                                    "is_present": bool(is_present)
                                }
                            )

                        attendance_result_dialog(
                            pd.DataFrame(results),
                            attendance_to_log
                        )

        with c3:

            if st.button(
                "Use Voice Attendance",
                type="secondary",
                width="stretch",
                icon=":material/mic:",
                key="voice_attendance"
            ):
                voice_attendance_dialog(selected_subject_id)
               

    elif st.session_state.current_teacher_tab == "manage_subjects":

        teacher_id = st.session_state.teacher_data["teacher_id"]

        col1, col2 = st.columns(2)

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
                        margin-top: 2rem !important;
                    }

                    .subj_divider {
                        border: none;
                        height: 1px;
                        background-color: #6C63FF;
                        margin-top: 10px;
                        margin-bottom: 20px;
                        width: 700px;
                    }

                </style>

                <hr class="subj_divider">
                <p class="manage_subj">Manage Subjects</p>
                """
            )

        with col2:

            st.markdown(
                """
                <style>

                    .st-key-create_subject button {
                        background-color: #6C63FF !important;
                        color: white !important;
                        border: 2px solid #6C63FF !important;
                        border-radius: 10px !important;
                        margin-top: 1.5rem;
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
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Create New Subject",
                width="stretch",
                type="primary",
                key="create_subject"
            ):
                create_subject_dialog(teacher_id)

        subjects = get_teacher_subjects(teacher_id)

        if subjects:

            for sub in subjects:

                stats = [
                    (
                        "👥",
                        "Students",
                        sub["total_students"]
                    ),
                    (
                        "🕰️",
                        "Classes",
                        sub["total_classes"]
                    )
                ]

                def share_btn(
                    name=sub["name"],
                    code=sub["subject_code"]
                ):

                    if st.button(
                        f"Share Code: {name}",
                        type="primary",
                        key=f"share_{code}",
                        icon=":material/share:"
                    ):

                        share_subject_dialog(
                            name,
                            code
                        )

                subject_card(
                    name=sub["name"],
                    code=sub["subject_code"],
                    section=sub["section"],
                    stats=stats,
                    footer_callback=share_btn
                )

                st.space()

        else:

            st.info(
                "NO SUBJECTS FOUND, CREATE ONE ABOVE"
            )

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
        teacher_id = st.session_state.teacher_data['teacher_id']

        records = get_attendance_for_teacher(teacher_id)

        if not records:
            return
        
        data = []

        for r in records:
            ts = r.get('timestamp')

            data.append({
                "ts_group": ts.split(".") [0] if ts else None,
                'Time': datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
                "Subject":r['subjects']['name'],
                "Subject Code":r['subjects']['subject_code'],
                "is_present":bool(r.get('is_present',False))
            })
        df = pd.DataFrame(data)

        summary = (
            df.groupby(['ts_group','Time','Subject','Subject Code']).agg(
                Present_Count = ('is_present','sum'),
                Total_Count = ('is_present','count')
            ).reset_index()
        )
        summary['Attendance Stats'] = (
            "✅" + summary['Present_Count'].astype(str) + 
            "/" + summary['Total_Count'].astype(str) + 'Students'
        )

        display_df = (summary.sort_values(by='ts_group',ascending=False)
                      [['Time','Subject','Subject Code','Attendance Stats']]
                      )
        st.dataframe(display_df,width="stretch",hide_index=True)
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


teacher_screen()