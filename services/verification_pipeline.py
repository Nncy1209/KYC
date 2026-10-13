from PIL import Image

from services.image_quality_service import ImageQualityService
from services.ocr_service import OCRService
from services.authenticity_service import AuthenticityService
from services.document_parser import DocumentParser
from services.document_validator import DocumentValidator
from services.face_service import FaceService
from services.qr_service import QRService
from services.tampering_service import TamperingService
from services.fraud_service import FraudService

class VerificationPipeline:

    def __init__(self):
        self.fraud_service = FraudService()
        self.tampering_service = TamperingService()
        self.qr_service = QRService()
        self.face_service = FaceService()
        self.validator = DocumentValidator()
        self.auth_service = AuthenticityService()
        self.quality_service = ImageQualityService()
        self.ocr_service = OCRService()
        self.document_parser = DocumentParser()

    def verify(self, front_file, document_type, back_file=None, selfie_file=None):

        # --------------------------------
        # FRONT IMAGE
        # --------------------------------

        front_image = Image.open(front_file)

        quality = self.quality_service.check_image_quality(
            front_image
        )

        if quality["status"] == "FAILED":

            return {
                "status": "FAILED",
                "quality": quality
            }

        # --------------------------------
        # OCR - FRONT
        # --------------------------------

        front_text = self.ocr_service.extract_text(
            front_image
        )

        # --------------------------------
        # OCR - BACK
        # --------------------------------

        back_text = ""

        if back_file is not None:

            back_image = Image.open(back_file)

            back_text = self.ocr_service.extract_text(
                back_image
            )

        # --------------------------------
        # QR VERIFICATION
        # --------------------------------

        qr_result = {
            "status": "SKIPPED",
            "detected": False,
            "data": "",
            "reason": "QR verification not required."
        }

        if document_type == "PAN Card":

            # PAN QR → FRONT
            qr_result = self.qr_service.verify(front_image)


        elif document_type == "Aadhaar Card":

            # Aadhaar QR → BACK
            if back_file is not None:

                qr_result = self.qr_service.verify(
                    back_image
                )

            else:

                qr_result = {
                    "status": "SKIPPED",
                    "detected": False,
                    "data": "",
                    "reason": "Back image required for Aadhaar QR verification."
                }


        elif document_type == "Driving License":

            # Try FRONT
            qr_result = self.qr_service.verify(
                front_image
            )

            # If QR not found → try BACK
            if not qr_result["detected"] and back_file is not None:

                qr_result = self.qr_service.verify(
                    back_image
                )

        elif document_type == "Voter ID":

            # Voter ID QR/barcode can be on either side
            qr_result = self.qr_service.verify(front_image)

            # If not found on front, try back
            if not qr_result["detected"] and back_file is not None:
                qr_result = self.qr_service.verify(back_image)

        # ---------------------------------
        # TAMPERING DETECTION
        # ---------------------------------

        tampering_result = self.tampering_service.analyze(
            front_image
        )

        # --------------------------------
        # COMBINE OCR
        # --------------------------------

        combined_text = front_text

        if back_text:

            combined_text += "\n" + back_text

        # --------------------------------
        # DOCUMENT VALIDATION
        # --------------------------------

        validation = self.validator.validate(
            document_type,
            combined_text
        )

        if not validation["valid"]:

            return {
                "status": "FAILED",
                "reason": validation["message"]
            }

        # --------------------------------
        # FIELD EXTRACTION
        # --------------------------------

        parsed = self.document_parser.parse(
            combined_text,
            document_type
        )

        fields = parsed.get("fields", {})

        # --------------------------------
        # AUTHENTICITY
        # --------------------------------

        auth = self.auth_service.verify(
            document_type,
            fields
        )

        # ---------------------------------
        # Face Verification
        # ---------------------------------
        if selfie_file is None:
            return {
                "status": "FAILED",
                "reason": "Selfie is required for face verification."
            }
        selfie_image = Image.open(selfie_file)

        face_result = self.face_service.verify(
            document_image=front_image,
            selfie_image=selfie_image
        )

        # --------------------------------
        # FRAUD / RISK SCORING
        # --------------------------------

        fraud_result = self.fraud_service.calculate_risk(
            quality=quality,
            authenticity=auth,
            face_verification=face_result,
            qr_verification=qr_result,
            tampering=tampering_result
        )


        # --------------------------------
        # FINAL RESULT
        # --------------------------------

        return {
            "status": "SUCCESS",
            "quality": quality,
            "document_type": document_type,
            "fields": fields,
            "authenticity": auth,
            "face_verification": face_result,
            "qr_verification": qr_result,
            "tampering": tampering_result,
            "fraud_risk": fraud_result
        }