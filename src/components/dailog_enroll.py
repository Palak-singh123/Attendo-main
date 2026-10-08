import time
import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Enroll in Subject")
def enroll_dialog():

    st.write("Enter the subject code provided by your teacher to enroll")

    join_code = st.text_input(
        "Subject Code",
        placeholder="Eg. CS101"
    )

    if st.button(
        "Enroll now",
        type="primary",
        width="stretch"
    ):

        if not join_code.strip():
            st.warning("Please enter a subject code")
            return

        code = join_code.strip().upper()

        student_data = st.session_state.get("student_data")

        if not student_data:
            st.error("Student information not found.")
            return

        student_id = student_data["student_id"]

        res = (
            supabase
            .table("subjects")
            .select("subject_id,name,subject_code")
            .eq("subject_code", code)
            .execute()
        )

        if not res.data:
            st.error(f"Subject code '{code}' not found.")
            return

        subject = res.data[0]

        subject_id = subject["subject_id"]

        check = (
            supabase
            .table("subject_students")
            .select("*")
            .eq("student_id", student_id)
            .eq("subject_id", subject_id)
            .execute()
        )

        if check.data:
            st.warning(
                f"You are already enrolled in {subject['name']}."
            )
            return

        try:
            enroll_student_to_subject(
                student_id,
                subject_id
            )

            st.success(
                f"Successfully enrolled in {subject['name']}!"
            )

            time.sleep(1)
            st.rerun()

        except Exception as e:
            st.error(f"Unable to enroll: {str(e)}")