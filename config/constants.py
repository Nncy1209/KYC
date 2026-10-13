# ===============================
# Supported Documents
# ===============================

AADHAAR = "Aadhaar Card"
PAN = "PAN Card"
PASSPORT = "Passport"
DL = "Driving License"
VOTER = "Voter ID"

SUPPORTED_DOCUMENTS = [
    AADHAAR,
    PAN,
    PASSPORT,
    DL,
    VOTER
]

# ===============================
# Verification Status
# ===============================

UPLOADED = "UPLOADED"
PROCESSING = "PROCESSING"
VERIFIED = "VERIFIED"
FAILED = "FAILED"
SUSPICIOUS = "SUSPICIOUS"

# ===============================
# Verification Result
# ===============================

AUTHENTIC = "Authentic"
FAKE = "Fake"
UNKNOWN = "Unknown"