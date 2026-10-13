import cv2
import numpy as np
from PIL import Image


class QRService:

    def verify(self, image):

        print("QR verification started")
        print("Image size:", image.size if hasattr(image, "size") else "unknown")

        if image is None:
            return {
                "status": "FAILED",
                "detected": False,
                "data": "",
                "reason": "No image provided."
            }

        # -----------------------------
        # Convert PIL -> OpenCV
        # -----------------------------

        if isinstance(image, Image.Image):
            image = np.array(image)

            if image.ndim == 3:
                image = cv2.cvtColor(
                    image,
                    cv2.COLOR_RGB2BGR
                )

            print("OpenCV image shape:", image.shape)

        # -----------------------------
        # Create QR detector
        # -----------------------------

        detector = cv2.QRCodeDetector()

        # -----------------------------
        # Try original image
        # -----------------------------

        data, points, _ = detector.detectAndDecode(image)

        if data:
            return {
                "status": "SUCCESS",
                "detected": True,
                "data": data,
                "reason": "QR decoded from original image."
            }

        # -----------------------------
        # Try enlarged image
        # -----------------------------

        enlarged = cv2.resize(
            image,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        data, points, _ = detector.detectAndDecode(enlarged)

        if data:
            return {
                "status": "SUCCESS",
                "detected": True,
                "data": data,
                "reason": "QR decoded after enlargement."
            }

        # -----------------------------
        # Try grayscale
        # -----------------------------

        gray = cv2.cvtColor(
            enlarged,
            cv2.COLOR_BGR2GRAY
        )

        data, points, _ = detector.detectAndDecode(gray)

        if data:
            return {
                "status": "SUCCESS",
                "detected": True,
                "data": data,
                "reason": "QR decoded from grayscale image."
            }

        # -----------------------------
        # Try thresholding
        # -----------------------------

        _, binary = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        data, points, _ = detector.detectAndDecode(binary)

        if data:
            return {
                "status": "SUCCESS",
                "detected": True,
                "data": data,
                "reason": "QR decoded after thresholding."
            }

        # -----------------------------
        # Try multi QR detector
        # -----------------------------

        try:

            retval, decoded_info, points, _ = (
                detector.detectAndDecodeMulti(image)
            )

            if retval and decoded_info:

                for value in decoded_info:

                    if value:

                        return {
                            "status": "SUCCESS",
                            "detected": True,
                            "data": value,
                            "reason": "QR decoded using multi-QR detection."
                        }

        except Exception:
            pass

        # -----------------------------
        # Failed
        # -----------------------------

        return {
            "status": "FAILED",
            "detected": False,
            "data": "",
            "reason": "QR was not decoded by the available decoder."
        }