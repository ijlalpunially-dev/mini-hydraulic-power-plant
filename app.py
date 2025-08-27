import streamlit as st
import math

# ---------------- Helper Functions ---------------- #
def cusec_to_m3s(Q_cusec):
    """Convert discharge from cusec (ft³/s) to m³/s."""
    return Q_cusec * 0.0283168  # 1 ft³ = 0.0283168 m³

def fps_to_mps(v_fps):
    """Convert velocity from ft/s to m/s."""
    return v_fps * 0.3048

def hydraulic_power(rho, g, Q_m3s, H_m):
    """Theoretical hydraulic power (W)."""
    return rho * g * Q_m3s * H_m

def actual_power(P_hydraulic_W, eta_turbine, eta_generator):
    """Actual electrical output power (W)."""
    return P_hydraulic_W * eta_turbine * eta_generator

def penstock_diameter(Q_m3s, v_mps):
    """Penstock diameter (m)."""
    if v_mps <= 0:
        return None
    D = math.sqrt((4 * Q_m3s) / (math.pi * v_mps))
    return D

def suggest_turbine(H):
    """Suggest turbine type based on net head."""
    if H > 300:
        return "Pelton Turbine (High Head)"
    elif 50 <= H <= 300:
        return "Francis Turbine (Medium Head)"
    else:
        return "Kaplan / Propeller Turbine (Low Head)"

# ---------------- Streamlit UI ---------------- #
st.set_page_config(page_title="Mini Hydraulic Power Plant", page_icon="💡", layout="centered")

st.title("💡 Mini Hydraulic Power Plant Calculator")
st.caption("Civil • Mechanical • Electrical Engineering | Hugging Face Spaces")

with st.sidebar:
    st.header("Inputs")

    Q_cusec = st.number_input("Discharge Q (cusec)", value=100.0, min_value=0.0, step=1.0)
    v_fps = st.number_input("Velocity v (ft/s)", value=6.0, min_value=0.1, step=0.1)
    H_m = st.number_input("Net Head H (m)", value=20.0, min_value=0.0, step=0.1)

    st.markdown("---")
    eta_turbine = st.slider("Turbine Efficiency ηₜ (%)", min_value=1, max_value=100, value=85) / 100
    eta_generator = st.slider("Generator Efficiency ηg (%)", min_value=1, max_value=100, value=90) / 100

# Convert units
Q_m3s = cusec_to_m3s(Q_cusec)
v_mps = fps_to_mps(v_fps)

# Compute powers
rho, g = 1000, 9.81  # default for water
P_hydraulic_W = hydraulic_power(rho, g, Q_m3s, H_m)
P_actual_W = actual_power(P_hydraulic_W, eta_turbine, eta_generator)

# Compute penstock diameter
D_penstock = penstock_diameter(Q_m3s, v_mps)

# ---------------- Results ---------------- #
st.subheader("Results")

col1, col2 = st.columns(2)
with col1:
    st.metric("Hydraulic Power (theoretical)", f"{P_hydraulic_W/1000:.3f} kW")
    st.caption("P = ρ g Q H")

with col2:
    st.metric("Electrical Output Power", f"{P_actual_W/1000:.3f} kW")
    st.caption("P_out = P × ηₜ × ηg")

st.markdown("### ⚡ Electrical Power in MW")
st.write(f"- {P_actual_W/1e6:.6f} MW")

# Penstock Diameter
st.markdown("### 🚰 Penstock Pipe Diameter")
if D_penstock:
    st.success(f"Recommended Diameter ≈ {D_penstock:.3f} m (for velocity {v_mps:.2f} m/s)")
else:
    st.error("Invalid velocity selected.")

# Turbine Suggestion
st.markdown("### 🌀 Suggested Turbine Type")
st.info(suggest_turbine(H_m))

st.markdown("---")
with st.expander("📘 Equations & Notes"):
    st.markdown(
        r"""
        **Equations**

        - Hydraulic Power:  
          \( P = \rho g Q H \) (Watts)

        - Electrical Output Power:  
          \( P_{out} = P \times \eta_t \times \eta_g \)

        - Penstock Diameter:  
          \( D = \sqrt{\dfrac{4Q}{\pi v}} \)

        **Conversions**
        - 1 cusec = 1 ft³/s = 0.0283168 m³/s  
        - 1 ft/s = 0.3048 m/s  

        **Turbine Selection by Head**
        - High Head (> 300 m) → Pelton Turbine  
        - Medium Head (50 – 300 m) → Francis Turbine  
        - Low Head (< 50 m) → Kaplan / Propeller Turbine  
        """
    )

st.caption("Made with Streamlit • Mini Hydro Plant Calculator • Input: Q (cusec), v (ft/s), H (m)")

