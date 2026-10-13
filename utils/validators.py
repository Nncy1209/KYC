import re


class Validators:

    @staticmethod
    def clean(value):
        """Normalize OCR-extracted document numbers."""
        if not value:
            return ""

        return re.sub(r"[\s-]", "", value.upper())

    @staticmethod
    def validate_aadhaar(number):

        number = Validators.clean(number)

        if not number:
            return False

        return bool(
            re.fullmatch(r"\d{12}", number)
        )

    @staticmethod
    def validate_pan(number):

        if not number:
            return False

        # Normalize OCR output
        number = str(number).upper().strip()
        number = re.sub(r"[^A-Z0-9]", "", number)

        # PAN format: XXXXX9999X
        # Correct common OCR mistakes only in numeric positions
        if len(number) == 10:

            chars = list(number)

            ocr_corrections = {
                "O": "0",
                "I": "1",
                "L": "1",
                "S": "5",
                "B": "8"
            }

            for i in range(5, 9):
                if chars[i] in ocr_corrections:
                    chars[i] = ocr_corrections[chars[i]]

            number = "".join(chars)

        # Final PAN format validation
        return bool(
            re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", number)
        )

    @staticmethod
    def validate_passport(number):

        number = Validators.clean(number)

        if not number:
            return False

        # Current test format: 2 letters + 6 digits
        return bool(
            re.fullmatch(r"[A-Z]{2}[0-9]{6}", number)
        )

    @staticmethod
    def validate_voter(number):

        number = Validators.clean(number)

        if not number:
            return False

        return bool(
            re.fullmatch(r"[A-Z]{3}[0-9]{7}", number)
        )

    @staticmethod
    def validate_dl(number):

        if not number:
            return False

        # Normalize OCR output
        number = Validators.clean(number)

        # -----------------------------------------
        # OCR correction for Driving License
        # -----------------------------------------
        # DL format:
        # 2 letters + 13 digits
        #
        # Example:
        # BR21 20250009312
        #
        # OCR may read:
        # BR2I 20250009312
        #     ↑
        #     I instead of 1
        # -----------------------------------------

        if len(number) == 15:

            # First two characters are state letters.
            # Remaining 13 characters should be digits.

            prefix = number[:2]
            remaining = number[2:]

            # Common OCR mistakes in numeric portion
            remaining = remaining.replace("I", "1")
            remaining = remaining.replace("L", "1")
            remaining = remaining.replace("O", "0")

            number = prefix + remaining

        # Final validation
        return bool(
            re.fullmatch(r"[A-Z]{2}[0-9]{13}", number)
        )