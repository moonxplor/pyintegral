import streamlit as st
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
from sympy import symbols, integrate, diff, sympify, pretty
import matplotlib.pyplot as plt
import numpy as np
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

st.title("🧮 Photo Calculus Solver")
st.write("Upload an image of a math expression (e.g., ∫x² dx or d/dx(sin(x)))")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

x = symbols('x')

if uploaded_file is not None:
   
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

   
    text = pytesseract.image_to_string(img)
    st.write("📜 Extracted Text:", text)

    expr_text = text.replace("∫", "").replace("dx", "").replace("d/dx", "").strip()

    try:
        expr = sympify(expr_text)
        if "∫" in text or "integrate" in text.lower():
            result = integrate(expr, x)
            st.success("✅ Integral Result:")
            st.latex(pretty(result))
        elif "d/dx" in text or "derivative" in text.lower():
            result = diff(expr, x)
            st.success("✅ Derivative Result:")
            st.latex(pretty(result))
        else:
            st.warning("Couldn't detect if it's an integral or derivative.")
            st.write("Parsed expression:", expr)

        st.write("📈 Function Plot:")
        f = lambda t: eval(str(expr), {"x": t, "sin": np.sin, "cos": np.cos, "exp": np.exp})
        X = np.linspace(-10, 10, 400)
        Y = [f(t) for t in X]

        fig, ax = plt.subplots()
        ax.plot(X, Y)
        ax.grid(True)
        st.pyplot(fig)
       
    except Exception as e:
            st.error(f"Error: {e}")