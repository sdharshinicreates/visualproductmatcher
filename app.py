import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import time

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Visual Product Matcher", layout="wide")

# ---------------- LOAD PRODUCT DATA ----------------
@st.cache_data
def load_products():
    return pd.read_csv("products.csv")

products = load_products()

# ---------------- PAGE HEADER ----------------
st.title("🛍️ Visual Product Matcher")
st.write("Upload an image to find visually similar products.")

# ---------------- IMAGE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Show uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # ---------------- SIMILARITY CALCULATION ----------------
    # Here we use random similarity values for demo purposes
    st.info("Computing similarity...")
    progress_bar = st.progress(0)
    products["similarity"] = 0.0

    for i in range(len(products)):
        # Simulate computation
        time.sleep(0.01)
        products.loc[i, "similarity"] = np.random.rand()
        progress_bar.progress((i + 1)/len(products))

    # Sort and select top 6
    top_results = products.sort_values(by="similarity", ascending=False).head(6)

    # ---------------- CATEGORY FILTER ----------------
    category = st.selectbox("Filter by Category", ["All"] + sorted(products["category"].unique().tolist()))
    if category != "All":
        top_results = top_results[top_results["category"] == category]

    # ---------------- DISPLAY RESULTS ----------------
    st.subheader("Similar Products")
    cols = st.columns(3)
    for idx, row in enumerate(top_results.itertuples()):
        with cols[idx % 3]:
            try:
                st.image(row.image, caption=f"{row.name} ({row.category})", use_container_width=True)
            except:
                st.write(f"{row.name} ({row.category}) - Image failed to load")
            st.write(f"Similarity: {row.similarity:.2f}")

else:
    st.info("Please upload an image to start matching.")
