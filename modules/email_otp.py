# ==========================================================
# FININTEL EMAIL OTP MODULE (ENTERPRISE VERSION)
# Production-ready Email Verification System
# Supports:
# - Gmail SMTP
# - OTP generation
# - OTP expiry (5 minutes)
# - OTP validation
# - OTP attempt protection
# - OTP resend protection
# - Device authentication support
# - Rate limiting
# - Secure structure
# ==========================================================

import smtplib
import random
import time
import hashlib

from email.mime.text import MIMEText


# ==========================================================
# YOUR GMAIL CONFIGURATION
# ==========================================================

EMAIL_ADDRESS = "finintel.security@gmail.com"

EMAIL_APP_PASSWORD = "hzhe huga qeyr mekz"


# ==========================================================
# OTP STORAGE STRUCTURE
# ==========================================================

EMAIL_OTP_STORE = {}

# Structure example:
# EMAIL_OTP_STORE[email] = {
#     "otp": "123456",
#     "timestamp": 1710000000,
#     "attempts": 0,
#     "resend_count": 1,
#     "device_id": "abc123"
# }


OTP_EXPIRY_SECONDS = 300        # 5 minutes
MAX_OTP_ATTEMPTS = 5
MAX_RESEND_LIMIT = 3
RESEND_COOLDOWN = 30            # seconds


# ==========================================================
# GENERATE DEVICE HASH (OPTIONAL SUPPORT)
# ==========================================================

def generate_device_hash(email, user_agent="unknown"):

    raw = f"{email}_{user_agent}_{time.time()}"

    return hashlib.sha256(raw.encode()).hexdigest()


# ==========================================================
# GENERATE OTP
# ==========================================================

def generate_email_otp(email, device_id=None):

    otp = str(random.randint(100000, 999999))

    current_time = time.time()

    existing = EMAIL_OTP_STORE.get(email)

    resend_count = 1

    if existing:
        resend_count = existing.get("resend_count", 0) + 1

    EMAIL_OTP_STORE[email] = {

        "otp": otp,

        "timestamp": current_time,

        "attempts": 0,

        "resend_count": resend_count,

        "device_id": device_id

    }

    return otp


# ==========================================================
# CHECK RESEND LIMIT
# ==========================================================

def can_resend_otp(email):

    record = EMAIL_OTP_STORE.get(email)

    if not record:
        return True

    resend_count = record.get("resend_count", 0)

    timestamp = record.get("timestamp", 0)

    if resend_count >= MAX_RESEND_LIMIT:

        print(f"[FinIntel] OTP resend limit reached for {email}")

        return False

    if time.time() - timestamp < RESEND_COOLDOWN:

        print(f"[FinIntel] OTP resend cooldown active for {email}")

        return False

    return True


# ==========================================================
# SEND EMAIL OTP
# ==========================================================

def send_email_otp(receiver_email, device_id=None):

    # Check resend protection
    if not can_resend_otp(receiver_email):

        return False

    otp = generate_email_otp(receiver_email, device_id)

    subject = "FinIntel Email Verification Code"

    body = f"""
Dear User,

Your FinIntel verification code is:

{otp}

This code is valid for 5 minutes.

If you did not request this login, please secure your account immediately.

Device Security Enabled.

Regards,
FinIntel Security Team
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email


    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)

        server.sendmail(
            EMAIL_ADDRESS,
            receiver_email,
            msg.as_string()
        )

        server.quit()

        print(f"[FinIntel] Email OTP sent to {receiver_email}")

        return True


    except Exception as e:

        print("[FinIntel] Email OTP Error:", e)

        return False


# ==========================================================
# VERIFY EMAIL OTP
# ==========================================================

def verify_email_otp(email, entered_otp):

    record = EMAIL_OTP_STORE.get(email)

    if not record:

        print(f"[FinIntel] OTP verify failed: no record for {email}")

        return False, "No OTP found. Request again."


    stored_otp = record["otp"]

    timestamp = record["timestamp"]

    attempts = record.get("attempts", 0)


    # Check expiry
    if time.time() - timestamp > OTP_EXPIRY_SECONDS:

        del EMAIL_OTP_STORE[email]

        print(f"[FinIntel] OTP expired for {email}")

        return False, "OTP expired. Request new one."


    # Check attempt limit
    if attempts >= MAX_OTP_ATTEMPTS:

        del EMAIL_OTP_STORE[email]

        print(f"[FinIntel] OTP attempts exceeded for {email}")

        return False, "Too many failed attempts."


    # Check match
    if entered_otp != stored_otp:

        record["attempts"] += 1

        print(f"[FinIntel] Invalid OTP attempt {record['attempts']} for {email}")

        return False, "Invalid OTP."


    # Success
    del EMAIL_OTP_STORE[email]

    print(f"[FinIntel] OTP verified successfully for {email}")

    return True, "Verification successful."


# ==========================================================
# CLEANUP EXPIRED OTPS
# ==========================================================

def cleanup_expired_otps():

    current_time = time.time()

    expired = []

    for email, data in EMAIL_OTP_STORE.items():

        if current_time - data["timestamp"] > OTP_EXPIRY_SECONDS:

            expired.append(email)


    for email in expired:

        del EMAIL_OTP_STORE[email]

        print(f"[FinIntel] Cleaned expired OTP for {email}")


# ==========================================================
# GET OTP STATUS (DEBUG / OPTIONAL)
# ==========================================================

def get_otp_status(email):

    record = EMAIL_OTP_STORE.get(email)

    if not record:
        return None

    remaining_time = OTP_EXPIRY_SECONDS - (time.time() - record["timestamp"])

    return {

        "email": email,

        "expires_in_seconds": max(0, int(remaining_time)),

        "attempts": record.get("attempts", 0),

        "resend_count": record.get("resend_count", 0)

    }
