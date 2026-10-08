import hashlib
import streamlit as st
from PIL import Image


@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write("Add classroom photos to scan for attendance")

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if "processed_photo_hashes" not in st.session_state:
        st.session_state.processed_photo_hashes = set()

    t1, t2 = st.columns(2)

    with t1:

        type_camera = (
            "secondary"
            if st.session_state.photo_tab == "camera"
            else "primary"
        )

        if st.button(
            "Camera",
            type=type_camera,
            width="stretch"
        ):
            st.session_state.photo_tab = "camera"

    with t2:

        type_upload = (
            "secondary"
            if st.session_state.photo_tab == "upload"
            else "primary"
        )

        if st.button(
            "Upload photos",
            type=type_upload,
            width="stretch"
        ):
            st.session_state.photo_tab = "upload"

    if st.session_state.photo_tab == "camera":

        cam_photo = st.camera_input(
            "Take Snapshot",
            key="dialog_cam"
        )

        if cam_photo:

            photo_bytes = cam_photo.getvalue()
            photo_hash = hashlib.md5(photo_bytes).hexdigest()

            if photo_hash not in st.session_state.processed_photo_hashes:

                try:

                    image = Image.open(cam_photo)

                    st.session_state.attendance_images.append(
                        image.copy()
                    )

                    st.session_state.processed_photo_hashes.add(
                        photo_hash
                    )

                    st.success(
                        "Photo captured successfully!"
                    )

                except Exception:

                    st.error(
                        "Unable to read this photo. Please try again."
                    )

    elif st.session_state.photo_tab == "upload":

        uploaded_files = st.file_uploader(
            "Choose image files",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="dialog_upload"
        )

        if uploaded_files:

            new_photos = 0
            invalid_photos = 0

            for f in uploaded_files:

                try:

                    photo_bytes = f.getvalue()
                    photo_hash = hashlib.md5(photo_bytes).hexdigest()

                    if photo_hash in st.session_state.processed_photo_hashes:
                        continue

                    image = Image.open(f)
                    image.verify()

                    f.seek(0)

                    image = Image.open(f)

                    st.session_state.attendance_images.append(
                        image.copy()
                    )

                    st.session_state.processed_photo_hashes.add(
                        photo_hash
                    )

                    new_photos += 1

                except Exception:

                    invalid_photos += 1

                    st.error(
                        f"❌ {f.name} is not a valid image file."
                    )

            if new_photos > 0:

                st.success(
                    f"{new_photos} photo(s) uploaded successfully!"
                )

    st.divider()

    if st.session_state.attendance_images:

        st.write(
            f"**Photos added: {len(st.session_state.attendance_images)}**"
        )

    else:

        st.info(
            "No photos added yet."
        )

    if st.button(
        "Done",
        type="primary",
        width="stretch"
    ):
        st.rerun()