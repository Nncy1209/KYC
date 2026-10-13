import cv2
import numpy as np
from PIL import Image
import io


class TamperingService:

    def __init__(self):
        # Thresholds
        self.ela_threshold = 25
        self.high_error_ratio = 0.15

    # ---------------------------------
    # Convert image to PIL
    # ---------------------------------

    def _to_pil(self, image):

        if isinstance(image, Image.Image):
            return image.convert("RGB")

        if isinstance(image, np.ndarray):

            # BGR -> RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            return Image.fromarray(image)

        raise TypeError("Unsupported image type.")

    # ---------------------------------
    # ELA - Error Level Analysis
    # ---------------------------------

    def _ela_analysis(self, image):

        image = self._to_pil(image)

        # Save image again with controlled JPEG quality
        buffer = io.BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=90
        )

        buffer.seek(0)

        recompressed = Image.open(buffer).convert("RGB")

        original = np.array(image).astype(np.int16)
        compressed = np.array(recompressed).astype(np.int16)

        # Pixel difference
        diff = np.abs(original - compressed)

        # Average RGB difference
        ela = np.mean(diff, axis=2)

        # Calculate percentage of high-error pixels
        high_error_pixels = np.sum(
            ela > self.ela_threshold
        )

        total_pixels = ela.size

        high_error_ratio = (
            high_error_pixels / total_pixels
        )

        return {
            "high_error_ratio": float(high_error_ratio),
            "mean_error": float(np.mean(ela)),
            "max_error": float(np.max(ela))
        }

    # ---------------------------------
    # Image Consistency
    # ---------------------------------

    def _consistency_analysis(self, image):

        image = self._to_pil(image)

        img = np.array(image)

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_RGB2GRAY
        )

        # Blur image slightly
        blurred = cv2.GaussianBlur(
            gray,
            (5, 5),
            0
        )

        # Difference between original and blurred
        difference = cv2.absdiff(
            gray,
            blurred
        )

        mean_difference = float(
            np.mean(difference)
        )

        return {
            "mean_difference": mean_difference
        }

    # ---------------------------------
    # Metadata Analysis
    # ---------------------------------

    def _metadata_analysis(self, image):

        image = self._to_pil(image)

        metadata = image.getexif()

        suspicious_software = []

        software = metadata.get(305)

        if software:

            software = str(software)

            suspicious_keywords = [
                "photoshop",
                "gimp",
                "paint.net",
                "illustrator",
                "canva"
            ]

            for keyword in suspicious_keywords:

                if keyword.lower() in software.lower():

                    suspicious_software.append(
                        software
                    )

        return {
            "metadata_present": len(metadata) > 0,
            "software": str(software) if software else "",
            "suspicious_software": suspicious_software
        }

    # ---------------------------------
    # Main Verification
    # ---------------------------------

    def analyze(self, image):

        ela = self._ela_analysis(image)

        consistency = self._consistency_analysis(
            image
        )

        metadata = self._metadata_analysis(
            image
        )

        # ---------------------------------
        # Risk calculation
        # ---------------------------------

        risk_score = 0

        reasons = []

        # ELA
        if ela["high_error_ratio"] > self.high_error_ratio:

            risk_score += 40

            reasons.append(
                "High ELA error region detected."
            )

        elif ela["high_error_ratio"] > 0.08:

            risk_score += 20

            reasons.append(
                "Moderate ELA inconsistency detected."
            )

        # Metadata
        if metadata["suspicious_software"]:

            risk_score += 30

            reasons.append(
                "Image metadata indicates possible editing software."
            )

        # Consistency
        if consistency["mean_difference"] > 15:

            risk_score += 20

            reasons.append(
                "Unusual image consistency detected."
            )

        # Limit score
        risk_score = min(
            risk_score,
            100
        )

        # ---------------------------------
        # Final status
        # ---------------------------------

        if risk_score == 0:
            status = "NO_RISK"

        elif risk_score < 30:
            status = "LOW_RISK"

        elif risk_score < 70:
            status = "MEDIUM_RISK"

        else:
            status = "HIGH_RISK"

        if not reasons:

            reasons.append(
                "No strong tampering indicators detected."
            )

        return {

            "status": status,

            "risk_score": risk_score,

            "ela": ela,

            "consistency": consistency,

            "metadata": metadata,

            "reasons": reasons
        }