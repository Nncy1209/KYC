import re


class DocumentValidator:

    @staticmethod
    def validate(document_type, ocr_text):

        text = ocr_text.lower()

        if document_type == "Aadhaar Card":

            keywords = [
                "aadhaar",
                "uidai",
                "unique identification authority",
                "government of india",
                "vid"
            ]

            aadhaar = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", ocr_text)

            found = any(word in text for word in keywords)

            if found or aadhaar:
                return {
                    "valid": True,
                    "message": "Valid Aadhaar Card"
                }

            return {
                "valid": False,
                "message": "Uploaded document is not an Aadhaar Card."
            }

        elif document_type == "PAN Card":

            keywords = [
                "income tax department",
                "permanent account number"
            ]

            pan = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", ocr_text)

            if any(k in text for k in keywords) or pan:
                return {
                    "valid": True,
                    "message": "Valid PAN Card"
                }

            return {
                "valid": False,
                "message": "Uploaded document is not a PAN Card."
            }

        elif document_type == "Passport":

            keywords = [
                "passport",
                "republic of india"
            ]

            passport = re.search(r"[A-Z][0-9]{7}", ocr_text)

            if any(k in text for k in keywords) or passport:
                return {
                    "valid": True,
                    "message": "Valid Passport"
                }

            return {
                "valid": False,
                "message": "Uploaded document is not a Passport."
            }

        elif document_type == "Driving License":

            keywords = [
                "driving licence",
                "driving license",
                "transport department"
            ]

            if any(k in text for k in keywords):
                return {
                    "valid": True,
                    "message": "Valid Driving License"
                }

            return {
                "valid": False,
                "message": "Uploaded document is not a Driving License."
            }

        elif document_type == "Voter ID":

            keywords = [
                "election commission",
                "elector",
                "epic"
            ]

            if any(k in text for k in keywords):
                return {
                    "valid": True,
                    "message": "Valid Voter ID"
                }

            return {
                "valid": False,
                "message": "Uploaded document is not a Voter ID."
            }

        return {
            "valid": False,
            "message": "Unknown document type."
        }