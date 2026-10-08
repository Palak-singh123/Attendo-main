import streamlit as st

from src.screens.home_screen import home_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog
from pathlib import Path


def main():
    st.set_page_config(
        page_title = 'Attendo - Making Attendance faster using AI',
        page_icon=str(Path("assets/Favicon.png")),
        layout="wide"
    )
    if "pending_join_code" not in st.session_state:
        st.session_state.pending_join_code = None

    join_code = st.query_params.get("join-code")

    if join_code:
        st.session_state.pending_join_code = join_code

    if st.session_state.pending_join_code:

        # Student already logged in
        if "student_data" in st.session_state:

            code = st.session_state.pending_join_code

            # Clear it first so dialog doesn't repeatedly open
            st.session_state.pending_join_code = None

            auto_enroll_dialog(code)

            return

        # Student is NOT logged in
        else:

            st.info("Please login as a student to enroll in this subject.")

            if st.button(
                "Go to Student Login",
                type="primary",
                width="stretch"
            ):
                st.switch_page("pages/student.py")

            return

    # -----------------------------------------------------
    # NORMAL HOME PAGE
    # -----------------------------------------------------

    home_screen()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()