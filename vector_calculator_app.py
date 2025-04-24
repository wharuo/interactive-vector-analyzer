import streamlit as st
import math

st.set_page_config(page_title="Vector Calculator", layout="centered")
st.title("🧮 Vector Calculator - All in One")

# Utility functions
def to_radians(deg):
    return deg * math.pi / 180

def calculate_components(magnitude, angle_deg):
    angle_rad = to_radians(angle_deg)
    x = magnitude * math.cos(angle_rad)
    y = magnitude * math.sin(angle_rad)
    return round(x, 4), round(y, 4)

def calculate_resultant(vectors):
    x_total = sum(v[0] for v in vectors)
    y_total = sum(v[1] for v in vectors)
    magnitude = math.sqrt(x_total**2 + y_total**2)
    angle = math.degrees(math.atan2(y_total, x_total))
    if angle < 0:
        angle += 360
    return round(x_total, 4), round(y_total, 4), round(magnitude, 2), round(angle, 1), round(magnitude, 1), round(angle)


# Interface Tabs
tabs = st.tabs(["Vector Components", "Operations: v1, v2, v3", "Angle Converter", "Final Summary"])

# TAB 1 - Vector Components
with tabs[0]:
    st.header("📌 Calculate Vector Components")
    magn = st.number_input("Vector Magnitude:", value=0.0, step=0.1)
    angle = st.number_input("Standard Position Angle (degrees):", value=0.0, step=0.1)
    if st.button("Calculate Components"):
        x, y = calculate_components(magn, angle)
        st.success(f"Component X = {x:.4f}, Component Y = {y:.4f}")

# TAB 2 - Vector Operations
with tabs[1]:
    st.header("➕➖ Vector Operations with v1, v2, v3")
    op_type = st.selectbox("Operation Type", [
        "vR = v1 + v2 + v3",
        "vR = v1 + v2 - v3",
        "vR = v1 - v2 + v3",
        "vR = v1 - v2 - v3"
    ])
    def input_vector(label):
        mag = st.number_input(f"{label} - Magnitude", key=f"mag_{label}", value=0.0)
        ang = st.number_input(f"{label} - Angle (degrees)", key=f"ang_{label}", value=0.0)
        return calculate_components(mag, ang)

    v1 = input_vector("v1")
    v2 = input_vector("v2")
    v3 = input_vector("v3")

    if st.button("Calculate Resultant Vector"):
        if op_type == "vR = v1 + v2 + v3":
            total = [v1, v2, v3]
        elif op_type == "vR = v1 + v2 - v3":
            total = [v1, v2, (-v3[0], -v3[1])]
        elif op_type == "vR = v1 - v2 + v3":
            total = [v1, (-v2[0], -v2[1]), v3]
        elif op_type == "vR = v1 - v2 - v3":
            total = [v1, (-v2[0], -v2[1]), (-v3[0], -v3[1])]

        xR, yR, magR, angleR, mag1, ang1 = calculate_resultant(total)
        st.success(f"vR → X: {xR}, Y: {yR}\nMagnitude: {magR} | Standard Angle: {angleR}°")

# TAB 3 - Angle Converter
with tabs[2]:
    st.header("🔄 Convert Y-Axis Angle to Standard Position")
    ang_rel = st.number_input("Angle with Y-axis:", value=0.0)
    eixo = st.selectbox("Vector Position", [
        "Above +X axis", "Above -X axis", "Below -X axis", "Below +X axis"])
    if st.button("Convert to Standard Angle"):
        angX = 90 - ang_rel
        if eixo == "Above +X axis":
            ang_std = angX
        elif eixo == "Above -X axis":
            ang_std = 180 - angX
        elif eixo == "Below -X axis":
            ang_std = 180 + angX
        elif eixo == "Below +X axis":
            ang_std = 360 - angX
        st.info(f"Standard Position Angle: {ang_std:.1f}°")

# TAB 4 - Final Summary
with tabs[3]:
    st.header("📊 Final Results and Legends")
    st.markdown("""
    - All components rounded to **4 decimal places**
    - Magnitude to **2 decimals**, and then **1 decimal** (Pearson style)
    - Reference and standard angles are automatically calculated
    - Uses formula: √(X² + Y²) for magnitude, atan2 for angle
    """)
    st.markdown("Use the previous tabs to generate input and validate your solution step by step.")
