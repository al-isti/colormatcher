import streamlit as st
import pandas as pd
from basic_colormath import get_delta_e_hex

def find_closest_color(input_hex, df):
    best_row = None
    best_delta = float('inf')
    for _, row in df.iterrows():
        try:
            delta = get_delta_e_hex(input_hex, row['Hex'])
        except Exception:
            continue
        if delta < best_delta:
            best_delta = delta
            best_row = row
    return best_row, best_delta

st.title("🎨 HEX Color Matcher (ΔE CIE2000)")
st.markdown("Upload a CSV with columns `Name,Hex` and find closest match using perceptual ΔE distance.")

uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
    if 'Name' not in df.columns or 'Hex' not in df.columns:
        st.error("CSV must have 'Name' and 'Hex' columns.")
    else:
        input_hex = st.color_picker("Pick or enter a HEX color", "#aabbcc")
        if input_hex:
            match, delta = find_closest_color(input_hex, df)
            if match is None:
                st.error("No valid HEX values found in CSV.")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Input Color**")
                    st.color_picker("", input_hex, label_visibility="collapsed")
                with col2:
                    st.markdown(f"**Matched: {match['Name']}**")
                    st.color_picker("", match['Hex'], label_visibility="collapsed")
                st.write(f"**ΔE (CIE2000)**: {delta:.2f}")
else:
    st.info("Awaiting CSV upload...")
