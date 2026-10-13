import cv2
import numpy as np


class ImageQualityService:

    @staticmethod
    def check_image_quality(image):

        result = {
            "blur_score": 0,
            "brightness": 0,
            "resolution": "",
            "status": "PASS",
            "warnings": []
        }

        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        height, width = img.shape[:2]

        result["resolution"] = f"{width} x {height}"

        # -----------------------
        # Blur Detection
        # -----------------------

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blur = cv2.Laplacian(gray, cv2.CV_64F).var()

        result["blur_score"] = round(blur, 2)

        if blur < 100:
            result["warnings"].append("Image is blurry.")

        # -----------------------
        # Brightness
        # -----------------------

        brightness = np.mean(gray)

        result["brightness"] = round(brightness, 2)

        if brightness < 60:
            result["warnings"].append("Image is too dark.")

        if brightness > 250:
            result["warnings"].append("Image is over exposed.")

        # -----------------------
        # Resolution
        # -----------------------

        if width < 800 or height < 500:
            result["warnings"].append("Low Resolution Image")

        if len(result["warnings"]) > 0:
            result["status"] = "WARNING"

        return result