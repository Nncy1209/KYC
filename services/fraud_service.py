class FraudService:

    def calculate_risk(
        self,
        quality,
        authenticity,
        face_verification,
        qr_verification,
        tampering
    ):

        risk_score = 0
        reasons = []

        # --------------------------------
        # IMAGE QUALITY
        # --------------------------------

        if quality.get("status") == "FAILED":
            risk_score += 30
            reasons.append("Poor image quality.")

        # --------------------------------
        # AUTHENTICITY
        # --------------------------------

        auth_status = authenticity.get("status")

        if auth_status == "Suspicious":
            risk_score += 30
            reasons.append(
                authenticity.get(
                    "reason",
                    "Document authenticity check failed."
                )
            )

        elif auth_status == "Unknown":
            risk_score += 15
            reasons.append(
                "Document authenticity could not be determined."
            )

        # --------------------------------
        # FACE VERIFICATION
        # --------------------------------

        if not face_verification.get("matched", False):

            risk_score += 30

            reasons.append(
                face_verification.get(
                    "reason",
                    "Face verification failed."
                )
            )

        # --------------------------------
        # QR VERIFICATION
        # --------------------------------

        qr_status = qr_verification.get("status")

        if qr_status == "FAILED":

            risk_score += 15

            reasons.append(
                "QR verification failed."
            )

        # SKIPPED QR should NOT automatically
        # be considered fraud because some
        # documents may not have a QR code.

        # --------------------------------
        # TAMPERING
        # --------------------------------

        tamper_status = tampering.get("status")

        if tamper_status == "HIGH_RISK":

            risk_score += 40

            reasons.append(
                "Strong document tampering indicators detected."
            )

        elif tamper_status == "MEDIUM_RISK":

            risk_score += 25

            reasons.append(
                "Possible document tampering detected."
            )

        elif tamper_status == "LOW_RISK":

            risk_score += 5

        # --------------------------------
        # LIMIT SCORE
        # --------------------------------

        risk_score = min(risk_score, 100)

        # --------------------------------
        # RISK LEVEL
        # --------------------------------

        if risk_score == 0:

            risk_level = "NO_RISK"

        elif risk_score < 30:

            risk_level = "LOW_RISK"

        elif risk_score < 70:

            risk_level = "MEDIUM_RISK"

        else:

            risk_level = "HIGH_RISK"

        # --------------------------------
        # FINAL DECISION
        # --------------------------------

        if risk_level == "NO_RISK":
            decision = "PASS"

        elif risk_level == "LOW_RISK":
            decision = "PASS"

        elif risk_level == "MEDIUM_RISK":
            decision = "REVIEW"

        else:
            decision = "REJECT"

        # --------------------------------
        # DEFAULT REASON
        # --------------------------------

        if not reasons:

            reasons.append(
                "No significant fraud indicators detected."
            )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "decision": decision,
            "reasons": reasons
        }