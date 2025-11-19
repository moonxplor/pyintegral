import streamlit as st
from PIL import Image
import pytesseract
import re
import sympy as sp
import numpy as np
import cv2
import base64

st.set_page_config(page_title="Photo Calculus AI", layout="centered")

st.markdown("<h1 style='text-align:center;'>📸 Calculus Scanner</h1>", unsafe_allow_html=True)
st.write("Upload or capture a math problem, and I'll solve the integral automatically!")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg","jpeg","png"])

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV,11,2)
    return thresh

def clean_expression(expr):
    if not expr:
        return ""

    replacements = {
        '∫': 'integrate ',
        '÷': '/',
        '×': '*',
        'x ': 'x',
        '–': '-',
        '−': '-',
        '¹':'^1','²':'^2','³':'^3','⁴':'^4','⁵':'^5','⁶':'^6','⁷':'^7','⁸':'^8','⁹':'^9','⁰':'0',
        '|':'','£':'','t':'x','I':'1'
    }

    for old, new in replacements.items():
        expr = expr.replace(old, new)

    # Force close parentheses if OCR misses them
    if expr.count("(") > expr.count(")"):
        expr += ")" * (expr.count("(") - expr.count(")"))

    # Remove trailing operators like +, -, /, *, ^
    expr = expr.rstrip("+-/*^")

    return expr.strip()

    # Remove extra spaces and new lines
    text = text.replace(" ", "").replace("\n", "")

    # Remove ∫ sign and dx (only leave expression)
    text = text.replace("∫", "").replace("dx", "")

    return text

if uploaded_file:
    img = Image.open(uploaded_file)
    img_np = np.array(img)

    st.image(img, caption="📷 Uploaded Image", use_column_width=True)

    processed = preprocess_image(img_np)

    text = pytesseract.image_to_string(processed)
    st.write("### 🔍 OCR Output:")
    st.code(text)

    expr = clean_math(text)
    st.write("### 🧹 Cleaned Expression:")
    st.code(expr)

    try:
        x = sp.symbols("x")
        parsed = sp.sympify(expr)
        result = sp.integrate(parsed, x)

        st.success("✔ Integral Solved!")
        st.latex(f"\\int {expr} \\, dx = {sp.latex(result)} + C")

    except Exception as e:
        st.error(f"❌ Failed to interpret math: {e}")
        st.info("Tip: Try cropping your image better or writing clearer.")