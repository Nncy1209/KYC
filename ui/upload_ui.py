import streamlit as st
from config.constants import SUPPORTED_DOCUMENTS


def upload_screen():
    st.title("🛡 AI Powered KYC Verification")

    st.write("---")

    document_type = st.selectbox(
        "Select Document",
        SUPPORTED_DOCUMENTS
    )

    front_image = st.file_uploader(
        "Upload Front Image",
        type=["jpg", "jpeg", "png"]
    )

    back_image = st.file_uploader(
        "Upload Back Image (Optional)",
        type=["jpg", "jpeg", "png"]
    )

    selfie = st.file_uploader(
        "Upload Selfie",
        type=["jpg", "jpeg", "png"]
    )

    verify = st.button(
        "✅ Verify Document",
        use_container_width=True
    )

    return (
        document_type,
        front_image,
        back_image,
        selfie,
        verify
    )