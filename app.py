import streamlit as st
import pandas as pd
from basic_colormath import hex_to_lab, get_delta_e_hex

# Match input to closest color
def find_closest_color(input_hex, df):
    best_row = None
    best_delta = float('inf')

    for _, row in df.iterrows():
        delta = get_delta_e_hex(input_hex, row['Hex'])
        if delta < best_delta:
            best_delta = delta
            best_row = row

    return best_row, best_delta

st.title("🎨 HEX Color Matcher")
st.markdown("Upload your `Name,Hex` CSV and find the closest match (Delta E CIE2000).")

uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
    if 'Name' not in df.columns or 'Hex' not in df.columns:
        st.error("CSV must have 'Name' and 'Hex' columns")
    else:
        input_hex = st.color_picker("Pick or enter HEX", "#aabbcc")
        if input_hex:
            match, delta = find_closest_color(input_hex, df)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Input Color**")
                st.color_picker("", input_hex, label_visibility="collapsed")
            with col2:
                st.markdown(f"**Matched: {match['Name']}**")
                st.color_picker("", match['Hex'], label_visibility="collapsed")
            st.write(f"**ΔE (CIE2000):** {delta:.2f}")
else:
    st.info("Awaiting CSV upload...")
