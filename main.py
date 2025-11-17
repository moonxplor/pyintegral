import streamlit as st
from PIL import Image
import pytesseract
import sympy as sp
import re
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def clean_math_expression(text):
    text = text.replace("−", "-")
    text = text.replace("—", "-")
    text = text.replace("^", "**")
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.replace("∫", "")
    text = text.replace("dx", "")
    text = re.sub(r"^\d+[\.\)]", "", text)

    text = re.sub(r"[^0-9xX\+\-\*\/\^\(\)]", "", text)
    text = text.replace("xX", "x")
    text = text.replace("xx", "x")

    return text

def safe_parse(expr):
    try:
        return sp.sympify(expr)
    except:
        expr = re.sub(r"[^0-9a-zA-Z\+\-\*\/\^\(\)\.]","", expr)
        return sp.sympify(expr)

st.title("📷 Math OCR Integral Solver")
st.write("Upload an image containing an integral expression.")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    # OCR
    raw_text = pytesseract.image_to_string(image, config='--psm 6')
    st.write("🔹 Raw OCR Output:")
    st.code(raw_text)

    cleaned = clean_math_expression(raw_text)

    st.write("🔹 Cleaned Expression:")
    st.code(cleaned)

    try:
        x = sp.symbols("x")
        expr = safe_parse(cleaned)
        result = sp.integrate(expr, x)
        st.success(f"✅ Solution:\n\n{result} + C")

    except Exception as e:
        st.error(f"❌ Failed to solve expression.\nError: {e}")