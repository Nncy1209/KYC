import json
from services.groq_service import GroqService


class DocumentParser:

    def __init__(self):
        self.groq = GroqService()

    def parse(self, ocr_text, document_type):

        # --------------------------------
        # Document-specific schema
        # --------------------------------

        if document_type == "Aadhaar Card":

            schema = """
{
    "fields": {
        "name": "",
        "father_name": "",
        "dob": "",
        "gender": "",
        "address": "",
        "aadhaar_number": ""
    }
}
"""

        elif document_type == "PAN Card":

            schema = """
{
    "fields": {
        "name": "",
        "father_name": "",
        "dob": "",
        "pan_number": ""
    }
}
"""

        elif document_type == "Passport":

            schema = """
{
    "fields": {
        "name": "",
        "passport_number": "",
        "dob": "",
        "nationality": "",
        "expiry_date": ""
    }
}
"""

        elif document_type == "Driving License":

            schema = """
{
    "fields": {
        "name": "",
        "license_number": "",
        "dob": "",
        "address": "",
        "issue_date": "",
        "valid_upto": ""
    }
}
"""

        elif document_type == "Voter ID":

            schema = """
{
    "fields": {
        "name": "",
        "father_name": "",
        "gender": "",
        "address": "",
        "voter_id": ""
    }
}
"""

        else:

            schema = """
{
    "fields": {}
}
"""

        # --------------------------------
        # Prompt
        # --------------------------------

        prompt = f"""
You are an AI KYC Document Parser.

The uploaded document has ALREADY been validated as:

{document_type}

Do NOT identify the document type again.

The OCR text may contain information from BOTH the
FRONT and BACK sides of the document.

Extract information from the COMPLETE OCR text.

Important rules:

1. Return ONLY valid JSON.
2. Do NOT return markdown.
3. Do NOT invent values.
4. Missing values must be "".
5. Return EXACTLY the schema provided below.
6. Extract ONLY fields relevant to the selected document.
7. Use information from BOTH front and back sides when available.
8. For Aadhaar Card, the address may be present on the BACK side.
9. If an address exists anywhere in the OCR text, extract it completely.
10. Do not confuse Aadhaar number, VID, PAN number, license number,
    or voter ID with each other.

Return EXACTLY this JSON schema:

{schema}

COMPLETE OCR TEXT:

{ocr_text}
"""

        # --------------------------------
        # Groq
        # --------------------------------

        response = self.groq.generate(prompt)

        response = response.strip()

        # --------------------------------
        # Remove markdown code fences
        # --------------------------------

        if response.startswith("```json"):

            response = response.replace(
                "```json", ""
            ).replace(
                "```", ""
            )

        elif response.startswith("```"):

            response = response.replace(
                "```", ""
            )

        # --------------------------------
        # Parse JSON
        # --------------------------------

        try:

            return json.loads(response)

        except Exception:

            return {
                "fields": {},
                "raw_response": response
            }