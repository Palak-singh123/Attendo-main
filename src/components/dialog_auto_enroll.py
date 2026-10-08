import time
import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):

    # =====================================================
    # GET STUDENT
    # =====================================================

    student_id = st.session_state.student_data["student_id"]

    # =====================================================
    # FIND SUBJECT
    # =====================================================

    res = (
        supabase
        .table("subjects")
        .select("subject_id, name")
        .eq("subject_code", subject_code)
        .execute()
    )

    # =====================================================
    # SUBJECT NOT FOUND
    # =====================================================

    if not res.data:

        st.error("Subject Code not found!")

        if st.button("Close"):
            st.query_params.clear()
            st.rerun()

        return

    subject = res.data[0]

    # =====================================================
    # CHECK ALREADY ENROLLED
    # =====================================================

    check = (
        supabase
        .table("subject_students")
        .select("*")
        .eq("subject_id", subject["subject_id"])
        .eq("student_id", student_id)
        .execute()
    )

    if check.data:

        st.info("You are already enrolled")

        if st.button("Close"):
            st.query_params.clear()
            st.rerun()

        return

    # =====================================================
    # ENROLLMENT QUESTION
    # =====================================================

    st.markdown(
        f"Would you like to enroll in **{subject['name']}**?"
    )

    # =====================================================
    # TWO BUTTONS
    # =====================================================

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # NO THANKS
    # -----------------------------------------------------

    with col1:

        if st.button(
            "No thanks",
            key="auto_enroll_no",
            width="stretch"
        ):

            st.query_params.clear()
            st.session_state["pending_join_code"] = None
            st.rerun()

    # -----------------------------------------------------
    # YES ENROLL NOW
    # -----------------------------------------------------

    with col2:

        if st.button(
            "Yes enroll now!",
            key="auto_enroll_yes",
            type="primary",
            width="stretch"
        ):

            enroll_student_to_subject(
                student_id,
                subject["subject_id"]
            )

            st.success("Joined successfully!")

            st.query_params.clear()
            st.session_state["pending_join_code"] = None

            time.sleep(2)

            st.rerun()