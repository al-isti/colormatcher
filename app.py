import streamlit as st
import pandas as pd
from colormath2.color_objects import sRGBColor
from colormath2.conversion import srgb_to_lab
from colormath2.difference import delta_e

# Convert HEX to RGB
def hex_to_rgb(hex_code):
    hex_code = hex_code.strip().lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

# Match input to closest color in CSV
def find_closest_color(input_hex, df):
    input_rgb = hex_to_rgb(input_hex)
    input_lab = srgb_to_lab(sRGBColor(*input_rgb, is_upscaled=True))

    min_delta = float('inf')
    closest_row = None

    for _, row in df.iterrows():
        lib_rgb = hex_to_rgb(row['Hex'])
        lib_lab = srgb_to_lab(sRGBColor(*lib_rgb, is_upscaled=True))
        delta = delta_e(input_lab, lib_lab, method='cie2000')

        if delta < min_delta:
            min_delta = delta
            closest_row = row

    return closest_row, min_delta

# Streamlit UI
st.title("🎨 HEX Color Matcher (Accurate Delta E)")
st.markdown("Upload your custom color library and match any HEX color using Delta E (CIE2000).")

uploaded_file = st.file_uploader("Upload your CSV file (Name,Hex)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if 'Name' not in df.columns or 'Hex' not in df.columns:
            st.error("CSV must contain 'Name' and 'Hex' columns.")
        else:
            input_hex = st.color_picker("Pick or enter a HEX color", "#aabbcc")

            if input_hex:
                closest, delta = find_closest_color(input_hex, df)

                st.subheader("🔍 Closest Match")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Input Color**")
                    st.color_picker(" ", input_hex, label_visibility="collapsed")

                with col2:
                    st.markdown(f"**Matched: {closest['Name']}**")
                    st.color_picker(" ", closest['Hex'], label_visibility="collapsed")

                st.write(f"**Delta E (CIE2000):** {delta:.2f} (lower is better match)")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Awaiting CSV upload...")
