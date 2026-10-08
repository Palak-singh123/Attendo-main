import time

import streamlit as st
from PIL import Image
import numpy as np

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from src.UI.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.subject_card import subject_card
from src.components.dailog_enroll import enroll_dialog

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embediings,
    train_classifier,
    check_duplicate_face
)

from src.pipelines.voice_pipeline import get_voice_embedding

from src.database.db import (
    get_all_students,
    create_student,
    get_student_subject,
    get_student_attendance,
    unenroll_student_to_subject
)


# STUDENT DASHBOARD

def student_dashboard():

    style_background_dashboard()
    style_base_layout()
    student_common_style()

    student_data = st.session_state.get("student_data")

    if not student_data:
        st.switch_page("app.py")
        return

    student_id = student_data["student_id"]

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
            <div class="StudentWelcome">
                Welcome, {student_data['name']}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Logout",
            type="primary",
            key="student_logout",
            shortcut="control+backspace"
        ):
            st.session_state["is_logged_in"] = False
            st.session_state["user_role"] = None
            st.session_state.pop("student_data", None)
            st.session_state.pop("current_student_tab", None)
            st.session_state.pop("pending_join_code", None)

            st.switch_page("app.py")

    st.space()

    st.markdown(
        """
        <div class="LoginTitle">
            <p>Student Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # SUBJECT SECTION

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="EnrolledTitle">
                Your Enrolled Subjects
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        if st.button(
            "Enroll in Subject",
            type="primary",
            width="stretch",
            key="enroll_subject_button"
        ):
            enroll_dialog()

    st.markdown(
        """
        <div class="CompactDivider"></div>
        """,
        unsafe_allow_html=True
    )

    st.space()

    # LOAD SUBJECTS

    with st.spinner("Loading your enrolled subjects..."):

        subjects = get_student_subject(student_id)
        logs = get_student_attendance(student_id)

    # ATTENDANCE STATS

    stats_map = {}

    for log in logs:

        sid = log["subject_id"]

        if sid not in stats_map:
            stats_map[sid] = {
                "total": 0,
                "attended": 0
            }

        stats_map[sid]["total"] += 1

        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    # SUBJECT CARDS

    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):

        sub = sub_node.get("subjects")

        if not sub:
            continue

        sid = sub["subject_id"]

        stats = stats_map.get(
            sid,
            {
                "total": 0,
                "attended": 0
            }
        )

        def unenroll_button(subject_id=sid):

            if st.button(
                "Unenroll from this course",
                width="stretch",
                key=f"unenroll_{subject_id}",
                icon=":material/delete_forever:"
            ):

                try:

                    unenroll_student_to_subject(
                        student_id,
                        subject_id
                    )

                    st.toast(
                        f"Successfully unenrolled from {sub['name']} course."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Unable to unenroll: {str(e)}"
                    )

        with cols[i % 2]:

            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=[
                    ("📆", "Classes", stats["total"]),
                    ("✅", "Attended", stats["attended"])
                ],
                footer_callback=unenroll_button
            )

    footer_dashboard()


# STUDENT LOGIN / REGISTRATION

def student_screen():

    if "student_data" not in st.session_state:
        st.session_state.student_data = None

    if st.session_state.student_data is not None:
        student_dashboard()
        return

    style_background_dashboard()
    style_base_layout()
    student_common_style()

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
            key="studentbackbtn",
            shortcut="control+backspace"
        ):
            st.session_state["login_state"] = None
            st.session_state["pending_join_code"] = None
            st.switch_page("app.py")

    st.markdown(
        """
        <div class="LoginTitle">
            <p>Login with FaceID</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.space()
    st.space()

    show_registration = False

    # CAMERA

    photo_source = st.camera_input(
        "Position your face in the center",
        key="student_camera"
    )

    if photo_source:

        img = np.array(
            Image.open(photo_source)
        )

        with st.spinner("AI is scanning..."):

            detected, all_ids, num_faces = predict_attendance(img)

        if num_faces == 0:

            show_registration = False

            st.warning(
                "No face detected. Please position your face properly."
            )

        elif num_faces > 1:

            show_registration = False

            st.warning(
                "Multiple faces detected. Please make sure only one person is visible."
            )

        else:

            if detected:

                student_id = list(
                    detected.keys()
                )[0]

                all_students = get_all_students()

                student = next(
                    (
                        s
                        for s in all_students
                        if s["student_id"] == student_id
                    ),
                    None
                )

                if student:

                    st.session_state["is_logged_in"] = True
                    st.session_state["user_role"] = "student"
                    st.session_state["student_data"] = student

                    st.toast(
                        f"Welcome Back {student['name']}"
                    )

                    time.sleep(1)

                    st.rerun()

            else:

                show_registration = True

    # REGISTRATION

    if show_registration:

        with st.container(border=True):

            st.markdown(
                """
                <div class="RegistrationTitle">
                    Register New Profile
                </div>
                """,
                unsafe_allow_html=True
            )

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Palak Singh",
                key="student_name"
            )

            st.markdown(
                """
                <div class="VoiceTitle">
                    Optional: Voice Enrollment
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="VoiceDescription">
                    Enroll yourself for voice-only attendance.
                    Record a short phrase like:
                    <b>"I am present, my name is Palak."</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            audio_data = None

            try:

                audio_data = st.audio_input(
                    "Record your voice",
                    key="student_voice"
                )

            except Exception:

                audio_data = None

            if st.button(
                "Create Account",
                type="primary",
                key="create_student_account"
            ):

                if not new_name.strip():

                    st.warning(
                        "Please enter your name."
                    )

                else:

                    with st.spinner("Creating profile..."):

                        img = np.array(
                            Image.open(photo_source)
                        )

                        encodings = get_face_embediings(img)

                        if not encodings:

                            st.error(
                                "No face detected. Please take another photo."
                            )

                        else:

                            face_emb = encodings[0]

                            # DUPLICATE FACE CHECK

                            duplicate_student = check_duplicate_face(
                                face_emb
                            )

                            if duplicate_student:

                                st.error(
                                    f"This face is already registered as "
                                    f"'{duplicate_student['name']}'. "
                                    f"You cannot create another account with the same face."
                                )

                            else:

                                face_emb = face_emb.tolist()

                                voice_emb = None

                                if audio_data:

                                    voice_emb = get_voice_embedding(
                                        audio_data.read()
                                    )

                                response_data = create_student(
                                    new_name.strip(),
                                    face_embedding=face_emb,
                                    voice_embedding=voice_emb
                                )

                                if response_data:

                                    train_classifier()

                                    st.session_state["is_logged_in"] = True
                                    st.session_state["user_role"] = "student"
                                    st.session_state["student_data"] = response_data[0]

                                    st.toast(
                                        f"Profile Created! Hi {new_name.strip()}"
                                    )

                                    time.sleep(1)

                                    st.rerun()


# STUDENT PAGE STYLING

def student_common_style():

    st.markdown(
        """
        <style>

        @import url(
            'https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Poppins:wght@400;500;600;700&display=swap'
        );

        /* MAIN TITLE */

        .LoginTitle {
            width: 100%;
            text-align: center;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }

        .LoginTitle p {
            color: #18245c !important;
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 40px !important;
            font-weight: 400 !important;
            margin: 0 !important;
            text-align: center !important;
        }

        /* WELCOME */

        .StudentWelcome {
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 22px !important;
            font-weight: 600 !important;
            text-align: right !important;
            margin-bottom: 8px !important;
        }

        /* ENROLLED SUBJECT TITLE */

        .EnrolledTitle {
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 24px !important;
            font-weight: 700 !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.2 !important;
        }

        /* COMPACT DIVIDER */

        .CompactDivider {
            height: 1px;
            background: rgba(24, 36, 92, 0.15);
            width: 100%;
            margin-top: 8px;
            margin-bottom: 10px;
        }

        /* REGISTRATION CARD */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 1.5px solid rgba(108, 99, 255, 0.25) !important;
            border-radius: 20px !important;
            background: rgba(255, 255, 255, 0.72) !important;
            padding: 24px !important;
            box-shadow: 0 10px 30px rgba(24, 36, 92, 0.08) !important;
        }

        .RegistrationTitle {
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 30px !important;
            font-weight: 700 !important;
            margin-bottom: 18px !important;
        }

        /* TEXT INPUT */

        div[data-testid="stTextInput"] label {
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 15px !important;
            font-weight: 600 !important;
        }

        div[data-testid="stTextInput"] input {
            background-color: #ffffff !important;
            color: #18245c !important;
            border: 2px solid #d8d5ff !important;
            border-radius: 12px !important;
            height: 48px !important;
            padding: 0 16px !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 15px !important;
            font-weight: 500 !important;
        }

        div[data-testid="stTextInput"] input:hover {
            border-color: #9b95ff !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #6C63FF !important;
            box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.15) !important;
            outline: none !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #8c8da3 !important;
            opacity: 1 !important;
        }

        /* VOICE */

        .VoiceTitle {
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 20px !important;
            font-weight: 700 !important;
            margin-top: 24px !important;
            margin-bottom: 10px !important;
        }

        .VoiceDescription {
            color: #5f6175 !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 14px !important;
            margin-top: 8px !important;
            margin-bottom: 8px !important;
        }

        .VoiceDescription b {
            color: #18245c !important;
        }

        /* CAMERA */

        div[data-testid="stCameraInput"] label {
            display: block !important;
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 16px !important;
            font-weight: 600 !important;
        }

        div[data-testid="stCameraInput"] button {
            background-color: #6C63FF !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
        }

        div[data-testid="stCameraInput"] button:hover {
            background-color: #554CFF !important;
        }

        /* AUDIO */

        div[data-testid="stAudioInput"] label {
            color: #18245c !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 15px !important;
            font-weight: 600 !important;
        }

        /* PRIMARY BUTTONS */

        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #ff7a00 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 10px 24px !important;
            font-family: 'Poppins', sans-serif !important;
            font-size: 15px !important;
            font-weight: 600 !important;
        }

        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: #e96d00 !important;
            color: #ffffff !important;
        }

        /* GENERAL MARKDOWN */

        .stMarkdown p {
            font-family: 'Poppins', sans-serif;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
