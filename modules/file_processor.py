"""
===========================================================
ENTERPRISE UNIVERSAL FILE PROCESSOR
Supports:
• PDF (digital)
• Scanned PDF (Poppler + OCR)
• Images (JPG, PNG, Checks, Salary Slips)
• Excel (XLSX)
• CSV
• TXT

Converts ANY file → TEXT → Phase-2 Extractor
===========================================================
"""

import os
import pandas as pd
import pytesseract
import pdfplumber

from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np


class UniversalFileLoader:

    def __init__(self, poppler_path=None, tesseract_path=None):

        self.poppler_path = poppler_path

        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        print("✅ Universal File Loader Ready")


    # =====================================================
    # MAIN ENTRY POINT
    # =====================================================

    def process(self, file_path):

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        print(f"📄 Processing file: {ext}")

        if ext == ".pdf":
            return self._process_pdf(file_path)

        elif ext in [".jpg", ".jpeg", ".png"]:
            return self._process_image(file_path)

        elif ext == ".xlsx":
            return self._process_excel(file_path)

        elif ext == ".csv":
            return self._process_csv(file_path)

        elif ext == ".txt":
            return self._process_txt(file_path)

        else:
            raise ValueError(f"Unsupported file type: {ext}")


    # =====================================================
    # PDF PROCESSING
    # =====================================================

    def _process_pdf(self, file_path):

        text = ""

        try:

            # Try digital PDF extraction first
            with pdfplumber.open(file_path) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

            # If digital text found → return
            if text.strip():
                print("✅ Digital PDF detected")
                return text

            # Otherwise use OCR
            print("🔍 Scanned PDF detected → Using OCR")
            return self._ocr_pdf(file_path)

        except Exception as e:

            print("⚠ PDF extraction failed → Using OCR fallback")
            return self._ocr_pdf(file_path)


    # =====================================================
    # IMAGE PROCESSING
    # =====================================================

    def _process_image(self, file_path):

        print("🖼 Processing Image with OCR")

        img = cv2.imread(file_path)

        processed = self._preprocess_image(img)

        text = pytesseract.image_to_string(processed)

        return text


    # =====================================================
    # OCR PDF USING POPPLER
    # =====================================================

    def _ocr_pdf(self, file_path):

        images = convert_from_path(
            file_path,
            poppler_path=self.poppler_path
        )

        full_text = ""

        for img in images:

            img_np = np.array(img)

            processed = self._preprocess_image(img_np)

            text = pytesseract.image_to_string(processed)

            full_text += text + "\n"

        return full_text


    # =====================================================
    # IMAGE PREPROCESSING (ENTERPRISE LEVEL)
    # Improves OCR accuracy dramatically
    # =====================================================

    def _preprocess_image(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Noise removal
        gray = cv2.medianBlur(gray, 3)

        # Thresholding
        thresh = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        return thresh


    # =====================================================
    # EXCEL PROCESSING
    # =====================================================

    def _process_excel(self, file_path):

        print("📊 Processing Excel")

        df = pd.read_excel(file_path)

        return df.to_string(index=False)


    # =====================================================
    # CSV PROCESSING
    # =====================================================

    def _process_csv(self, file_path):

        print("📊 Processing CSV")

        df = pd.read_csv(file_path)

        return df.to_string(index=False)


    # =====================================================
    # TXT PROCESSING
    # =====================================================

    def _process_txt(self, file_path):

        print("📄 Processing TXT")

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
