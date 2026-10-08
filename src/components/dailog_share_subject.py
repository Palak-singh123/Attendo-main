
import streamlit as st
import segno
import io


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):

    app_domain = "attendo-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    # =========================================================
    # CSS
    # =========================================================

    st.markdown("""
    <style>

    /* =====================================================
       GOOGLE FONTS
    ===================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Poppins:wght@400;500;600;700&display=swap'
    );


    /* =====================================================
       DIALOG BOX
    ===================================================== */

    [data-testid="stDialog"] [role="dialog"] {
        background: #ffffff !important;
        border-radius: 20px !important;
    }


    /* =====================================================
       SHARE CLASS LINK
       Only the dialog title
    ===================================================== */

    [data-testid="stDialog"] [role="dialog"] > div:first-child h2 {
        font-family: 'Climate Crisis', sans-serif !important;
        font-size: 38px !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        line-height: 1.05 !important;

        margin-top: 0 !important;
        margin-bottom: 8px !important;
    }


    /* =====================================================
       SCAN TO JOIN
       Custom class — so it doesn't affect Share Class Link
    ===================================================== */

    [data-testid="stDialog"] .scan-title {
        font-family: 'Climate Crisis', sans-serif !important;
        font-size: 45px !important;
        font-weight: 400 !important;
        color: #1e293b !important;
        line-height: 1.1 !important;

        margin-top: 10px !important;
        margin-bottom: 20px !important;
    }


    /* =====================================================
       COPY LINK + SCAN TO JOIN LABELS
    ===================================================== */

    [data-testid="stDialog"] .stMarkdown h3 {
        font-family: 'Poppins', sans-serif !important;
        font-size: 19px !important;
        font-weight: 600 !important;
        color: #1e293b !important;

        margin-bottom: 10px !important;
    }


    /* =====================================================
       NORMAL TEXT
    ===================================================== */

    [data-testid="stDialog"] [role="dialog"] p {
        font-family: 'Poppins', sans-serif !important;
        font-size: 15px !important;
        font-weight: 400 !important;
        color: #334155 !important;
    }


    /* =====================================================
       CODE BOX
    ===================================================== */

    [data-testid="stDialog"] [role="dialog"] pre {
        background: #f8f9ff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px !important;
    }


    [data-testid="stDialog"] [role="dialog"] pre code {
        font-family: monospace !important;
        font-size: 15px !important;
        color: #334155 !important;
    }


    /* =====================================================
       INFO BOX
    ===================================================== */

    [data-testid="stDialog"] [role="dialog"]
    [data-testid="stAlert"] {
        background: #eaf4ff !important;
        border: none !important;
        border-radius: 10px !important;
    }


    [data-testid="stDialog"] [role="dialog"]
    [data-testid="stAlert"] p {
        font-family: 'Poppins', sans-serif !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #334155 !important;
    }


    /* =====================================================
       CLOSE BUTTON
    ===================================================== */

    [data-testid="stDialog"] [role="dialog"]
    button[aria-label="Close"] {
        color: #9370DB !important;
        font-size: 24px !important;
    }


    /* =====================================================
       QR CAPTION
    ===================================================== */

    [data-testid="stDialog"] [role="dialog"]
    [data-testid="stImage"] p {
        font-family: 'Poppins', sans-serif !important;
        font-size: 13px !important;
        color: #64748b !important;
    }

    </style>
    """, unsafe_allow_html=True)


    # =========================================================
    # SCAN TO JOIN
    # =========================================================

    st.markdown(
        '<div class="scan-title">Scan to Join</div>',
        unsafe_allow_html=True
    )


    # =========================================================
    # QR CODE
    # =========================================================

    qr = segno.make(join_url)

    out = io.BytesIO()

    qr.save(
        out,
        kind="png",
        scale=10,
        border=1
    )


    # =========================================================
    # TWO COLUMNS
    # =========================================================

    col1, col2 = st.columns(2)


    # =========================================================
    # LEFT — COPY LINK
    # =========================================================

    with col1:

        st.markdown("### Copy Link")

        st.code(
            join_url,
            language="text"
        )

        st.code(
            subject_code,
            language="text"
        )

        st.info(
            "Copy this link to share on Whatsapp or Email"
        )


    # =========================================================
    # RIGHT — QR CODE
    # =========================================================

    with col2:

        st.markdown("### Scan to Join")

        st.image(
            out.getvalue(),
            caption="QRCODE for class joining"
        )