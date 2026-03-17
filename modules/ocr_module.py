import pytesseract
from PIL import Image
import pdfplumber
import pandas as pd
from pdf2image import convert_from_bytes
import cv2
import numpy as np
import re
import io

# ==========================================================
# SET TESSERACT PATH (IMPORTANT)
# ==========================================================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ==========================================================
# AUTO ROTATION USING TESSERACT OSD
# ==========================================================

def correct_rotation(image):

    try:
        osd = pytesseract.image_to_osd(image)
        angle = int(re.search(r"Rotate: (\d+)", osd).group(1))

        if angle == 90:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

        elif angle == 180:
            image = cv2.rotate(image, cv2.ROTATE_180)

        elif angle == 270:
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    except:
        pass

    return image


# ==========================================================
# DESKEW IMAGE
# ==========================================================

def deskew(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    coords = np.column_stack(np.where(gray > 0))

    if len(coords) == 0:
        return image

    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]

    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    rotated = cv2.warpAffine(
        image,
        M,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    return rotated


# ==========================================================
# IMAGE PREPROCESSING
# ==========================================================

def preprocess_image(pil_image):

    img = np.array(pil_image)

    img = correct_rotation(img)

    if len(img.shape) == 2:

        gray = img

    elif len(img.shape) == 3 and img.shape[2] == 3:

        img = deskew(img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif len(img.shape) == 3 and img.shape[2] == 4:

        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    else:
        raise ValueError("Unsupported image format")

    # Contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Noise removal
    gray = cv2.medianBlur(gray, 3)

    # Upscale
    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        5
    )

    return thresh


# ==========================================================
# TEXT CLEANING
# ==========================================================

def clean_text(text):

    lines = text.split("\n")

    cleaned = []

    for line in lines:

        line = line.strip()

        if len(line) < 2:
            continue

        # Remove common header noise
        if re.search(
            r'page|account|statement|customer|branch|ifsc|micr|bank|balance|opening',
            line.lower()
        ):
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


# ==========================================================
# OCR FROM IMAGE (IMPROVED FOR TABLE DATA)
# ==========================================================

def ocr_image(pil_image):

    processed = preprocess_image(pil_image)

    config = r'--oem 3 --psm 6 -l eng'

    # Extract structured OCR data
    data = pytesseract.image_to_data(
        processed,
        config=config,
        output_type=pytesseract.Output.DATAFRAME
    )

    data = data.dropna()

    words = data["text"].tolist()

    text = " ".join(words)

    text = clean_text(text)

    return text


# ==========================================================
# OCR / TEXT EXTRACTION
# ==========================================================

def extract_text_from_file(file):

    filename = file.filename.lower()

    file.stream.seek(0)

    # Detect file type

    if filename.endswith(".pdf"):
        file_type = "pdf"

    elif filename.endswith((".png", ".jpg", ".jpeg")):
        file_type = "image"

    elif filename.endswith(".csv"):
        file_type = "csv"

    elif filename.endswith((".xls", ".xlsx")):
        file_type = "excel"

    else:
        file_type = "unknown"


    # ======================================================
    # PDF FILES
    # ======================================================

    if file_type == "pdf":

        text = ""

        try:

            with pdfplumber.open(file) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

        except:
            pass


        # If PDF already contains text
        if len(text.strip()) > 50:

            return clean_text(text), file_type


        # OCR fallback

        file.stream.seek(0)

        pdf_bytes = file.read()

        images = convert_from_bytes(pdf_bytes, dpi=400)

        full_text = ""

        for img in images:

            page_text = ocr_image(img)

            full_text += page_text + "\n"

        return full_text, file_type


    # ======================================================
    # IMAGE FILES
    # ======================================================

    elif file_type == "image":

        try:
            image = Image.open(file.stream)
        except:
            return "", file_type

        text = ocr_image(image)

        return text, file_type


    # ======================================================
    # CSV FILES
    # ======================================================

    elif file_type == "csv":

        try:

            file.stream.seek(0)

            df = pd.read_csv(file)

            df = df.astype(str)

            text = df.apply(lambda x: ' '.join(x), axis=1)

            return "\n".join(text), file_type

        except:
            return "", file_type


    # ======================================================
    # EXCEL FILES
    # ======================================================

    elif file_type == "excel":

        try:

            file.stream.seek(0)

            xls = pd.ExcelFile(file)

            full_text = ""

            for sheet in xls.sheet_names:

                df = pd.read_excel(xls, sheet_name=sheet)

                df = df.astype(str)

                sheet_text = df.apply(lambda x: ' '.join(x), axis=1)

                full_text += "\n".join(sheet_text) + "\n"

            return full_text, file_type

        except:
            return "", file_type


    # ======================================================
    # UNKNOWN FILE TYPE
    # ======================================================

    return "", file_type