from utils.validators import Validators


class AuthenticityService:

    def verify(self, document_type, fields):

        result = {
            "status": "Authentic",
            "reason": "Valid"
        }

        try:

            if document_type == "PAN Card":

                if not Validators.validate_pan(
                    fields.get("pan_number")
                ):
                    result["status"] = "Suspicious"
                    result["reason"] = "Invalid PAN Number"

            elif document_type == "Aadhaar Card":

                if not Validators.validate_aadhaar(
                    fields.get("aadhaar_number")
                ):
                    result["status"] = "Suspicious"
                    result["reason"] = "Invalid Aadhaar Number"

            elif document_type == "Passport":

                if not Validators.validate_passport(
                    fields.get("passport_number")
                ):
                    result["status"] = "Suspicious"
                    result["reason"] = "Invalid Passport Number"

            elif document_type == "Driving License":

                if not Validators.validate_dl(
                    fields.get("license_number")
                ):
                    result["status"] = "Suspicious"
                    result["reason"] = "Invalid Driving License"

            elif document_type == "Voter ID":

                if not Validators.validate_voter(
                    fields.get("voter_id")
                ):
                    result["status"] = "Suspicious"
                    result["reason"] = "Invalid Voter ID"

        except Exception:

            result["status"] = "Unknown"

        return result