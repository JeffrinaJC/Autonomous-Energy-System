import streamlit as st
import plotly.graph_objects as go

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="CORE-AI | Autonomous Energy Controller",
    page_icon="⚡",
    layout="wide"
)

# -------------------------------------------------
# UI STYLING
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono&display=swap');

.stApp {
    background: radial-gradient(circle at top, #050b18 0%, #010203 75%);
    color: #e5e7eb;
    font-family: 'Inter', sans-serif;
}

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.5);
}

.label {
    font-size: 0.7rem;
    letter-spacing: 1px;
    color: #94a3b8;
}

.value {
    font-size: 1.5rem;
    font-weight: 800;
}

.intent {
    background: rgba(0,242,254,0.05);
    border-left: 3px solid #00f2fe;
    padding: 16px;
    margin-top: 14px;
    font-style: italic;
    color: #cbd5f5;
}

.footer {
    text-align: center;
    font-size: 0.75rem;
    opacity: 0.35;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR INPUTS (SIMULATION)
# -------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ SYSTEM CONDITIONS")
    solar_power = st.slider("🌞 Solar Power (kW)", 0.0, 10.0, 5.0)
    load_demand = st.slider("🏠 Load Demand (kW)", 0.0, 10.0, 4.0)
    battery_level = st.slider("🔋 Battery State of Charge (%)", 0, 100, 50)
    time_of_day = st.selectbox(
        "⏰ Time of Day",
        ["Morning", "Afternoon", "Evening", "Night"],
        index=2
    )

# -------------------------------------------------
# AGENT AI – RE15 CORRECT LOGIC
# -------------------------------------------------

# ENERGY SOURCE PRIORITY: SOLAR → BATTERY → GRID
if solar_power >= load_demand:
    energy_source = "USING SOLAR POWER"
    battery_action = "Charging" if battery_level < 100 else "Idle"
    net_flow = solar_power - load_demand

elif battery_level > 20:
    energy_source = "USING BATTERY POWER"
    battery_action = "Discharging"
    net_flow = load_demand - solar_power

else:
    energy_source = "USING GRID POWER"
    battery_action = "Battery Protected"
    net_flow = 0.0

# BATTERY HEALTH ZONE
if battery_level <= 20:
    zone_status = "CRITICAL"
    zone_color = "#f43f5e"
elif battery_level >= 85:
    zone_status = "OPTIMAL"
    zone_color = "#10b981"
else:
    zone_status = "SAFE"
    zone_color = "#22d3ee"

# AI INTENT (EXPLAINABLE)
if energy_source == "USING SOLAR POWER":
    intent_msg = "Solar generation meets demand. AI powers the load using renewable energy and stores excess safely."
elif energy_source == "USING BATTERY POWER":
    intent_msg = "Solar is insufficient. AI supplies load using stored battery energy to avoid grid dependency."
else:
    intent_msg = "Battery is below safe threshold. AI switches to grid power to protect battery health."

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(
    "<h1 style='font-weight:800;'>⚡ AUTONOMOUS ENERGY CONTROLLER</h1>",
    unsafe_allow_html=True
)
st.caption("Agent AI • Renewable-First • Real-Time Decision System")

# -------------------------------------------------
# STATUS CARDS
# -------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="label">ACTIVE ENERGY SOURCE</div>
        <div class="value" style="color:#22d3ee;">{energy_source}</div>
        <div style="opacity:0.6;">Battery: {battery_action}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="label">BATTERY STATUS</div>
        <div class="value" style="color:{zone_color};">{battery_level}%</div>
        <div style="opacity:0.6;">Zone: {zone_status}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="label">SYSTEM LOAD</div>
        <div class="value">{load_demand:.1f} kW</div>
        <div style="opacity:0.6;">Time: {time_of_day}</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# AI INTENT PANEL
# -------------------------------------------------
st.markdown(f"""
<div class="intent">
    <div class="label" style="color:#22d3ee;">AGENT AI DECISION LOGIC</div>
    "{intent_msg}"
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# NEW GRAPH – DIFFERENT STYLE & COLORS
# -------------------------------------------------
st.markdown("#### ⚖️ Energy Flow Snapshot")

fig = go.Figure()

fig.add_bar(
    y=["Solar Generation"],
    x=[solar_power],
    orientation="h",
    marker=dict(color="#22d3ee"),
    name="Solar"
)

fig.add_bar(
    y=["Load Consumption"],
    x=[load_demand],
    orientation="h",
    marker=dict(color="#fbbf24"),
    name="Load"
)

fig.update_layout(
    barmode="overlay",
    height=120,
    margin=dict(l=40, r=20, t=10, b=10),
    xaxis=dict(
        title="Power (kW)",
        showgrid=False,
        zeroline=False,
        color="#94a3b8"
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        color="#94a3b8"
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#94a3b8",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    "<div class='footer'>Autonomous Mode Active • Renewable Energy First • RE15 Prototype</div>",
    unsafe_allow_html=True
)
