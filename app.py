import streamlit as st

from ui.upload_ui import upload_screen
from services.verification_pipeline import VerificationPipeline

st.set_page_config(
    page_title="AI KYC Verification",
    page_icon="🛡",
    layout="wide"
)

# -----------------------------
# Upload UI
# -----------------------------
document_type, front, back, selfie, verify = upload_screen()

# -----------------------------
# Verify Button
# -----------------------------
if verify:

    # Validate uploads
    if front is None:
        st.error("Please upload the front image.")
        st.stop()

    if selfie is None:
        st.error("Please upload a selfie.")
        st.stop()

    # Run complete verification pipeline
    pipeline = VerificationPipeline()

    result = pipeline.verify(
        front,
        document_type,
        back,
        selfie
    )

    # -----------------------------
    # Image Quality Failed
    # -----------------------------
    if result["status"] == "FAILED":

        st.error("❌ Image Quality Failed")

        st.write("## Image Quality Report")
        st.json(result["quality"])

        st.stop()

    # -----------------------------
    # Verification Successful
    # -----------------------------
    st.success("✅ Verification Completed")

    st.write("## Image Quality Report")
    st.json(result["quality"])


    st.write("## Detected Document Type")
    st.success(result["document_type"])

    st.write("## Extracted Fields")
    st.json(result["fields"])

    st.write("## Authenticity Check")
    st.json(result["authenticity"])

    st.subheader("Face Verification")
    st.json(result["face_verification"])

    st.subheader("QR Verification")
    st.json(result["qr_verification"])

    st.subheader("Tampering Detection")
    st.json(result["tampering"])

    st.subheader("Fraud / Risk Scoring")
    st.json(result["fraud_risk"])

    # -----------------------------
    # Final KYC Decision
    # -----------------------------

    st.write("## Final KYC Decision")

    fraud_result = result["fraud_risk"]

    decision = fraud_result.get("decision")
    risk_level = fraud_result.get("risk_level")
    risk_score = fraud_result.get("risk_score")

    st.write(f"**Risk Score:** {risk_score}")
    st.write(f"**Risk Level:** {risk_level}")

    if decision == "PASS":

        st.success("✅ KYC PASSED")

    elif decision == "REVIEW":

        st.warning("⚠️ KYC REQUIRES MANUAL REVIEW")

    else:

        st.error("❌ KYC REJECTED")

    st.write("### Reasons")

    for reason in fraud_result.get("reasons", []):
        st.write(f"- {reason}")

    st.write("## Uploaded Images")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Front")
        st.image(front)

    with col2:
        if back:
            st.write("Back")
            st.image(back)

    with col3:
        st.write("Selfie")
        st.image(selfie)