import streamlit as st
import pandas as pd
from datetime import datetime

from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase


@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):

    st.write(
        "Record audio of students saying I am present. Then AI will recognize the students."
    )

    audio_data = st.audio_input(
        "Record classroom audio"
    )

    if st.button(
        "Analyze Audio",
        width="stretch",
        type="primary"
    ):

        if audio_data is None:
            st.warning(
                "Please record classroom audio first."
            )
            return

        with st.spinner("Processing audio data..."):

            enrolled_res = (
                supabase
                .table("subject_students")
                .select("*, students(*)")
                .eq(
                    "subject_id",
                    selected_subject_id
                )
                .execute()
            )

            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning(
                    "No students enrolled in this course."
                )
                return

            candidates_dict = {
                student["students"]["student_id"]:
                student["students"]["voice_embedding"]
                for student in enrolled_students
                if student["students"].get("voice_embedding")
            }

            if not candidates_dict:
                st.error(
                    "No enrolled students have voice profiles registered."
                )
                return

            audio_bytes = audio_data.read()

            if not audio_bytes:
                st.warning(
                    "The recorded audio is empty. Please record again."
                )
                return

            detected_scores = process_bulk_audio(
                audio_bytes,
                candidates_dict
            )

            results = []
            attendance_to_log = []

            current_timestamp = datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S"
            )

            for node in enrolled_students:

                student = node["students"]

                score = float(
                    detected_scores.get(
                        student["student_id"],
                        0.0
                    )
                )

                is_present = score > 0

                results.append({
                    "Name": student["name"],
                    "ID": student["student_id"],
                    "Source": (
                        round(score, 4)
                        if is_present
                        else "-"
                    ),
                    "Status": (
                        "✅ Present"
                        if is_present
                        else "❌ Absent"
                    )
                })

                attendance_to_log.append({
                    "student_id": student["student_id"],
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": is_present
                })

            st.session_state.voice_attendance_results = (
                pd.DataFrame(results),
                attendance_to_log
            )

    if st.session_state.get(
        "voice_attendance_results"
    ):

        st.divider()

        st.markdown(
            "### Please review attendance before confirming."
        )

        df_results, logs = (
            st.session_state.voice_attendance_results
        )

        st.dataframe(
            df_results,
            width="stretch",
            hide_index=True
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Discard",
                width="stretch",
                type="secondary",
                key="discard_voice_attendance"
            ):

                st.session_state.pop(
                    "voice_attendance_results",
                    None
                )

                st.rerun()

        with col2:

            if st.button(
                "Confirm & Save",
                width="stretch",
                type="primary",
                key="confirm_voice_attendance"
            ):

                try:

                    supabase.table(
                        "attendance_logs"
                    ).insert(
                        logs
                    ).execute()

                    st.success(
                        "Attendance saved successfully!"
                    )

                    st.session_state.pop(
                        "voice_attendance_results",
                        None
                    )

                except Exception as e:

                    st.error(
                        f"Unable to save attendance: {e}"
                    )