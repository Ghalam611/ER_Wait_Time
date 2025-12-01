import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------ PAGE SETUP ------------------
st.set_page_config(
    page_title="ER Wait Time Dashboard",
    page_icon="⏱️",
    layout="wide"
)

st.title("⏱️ ER Wait Time – Interactive Dashboard")
st.write(
    "This dashboard analyzes **Emergency Room (ER)** wait times and provides "
    "operational recommendations to improve patient flow and satisfaction."
)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clean_data.csv")
    # Make sure numeric columns are numeric
    for col in [
        "Total Wait Time (min)",
        "Total_Wait_Hours",
        "Time_to_MD_Hours",
        "Patient Satisfaction",
        "Nurse-to-Patient Ratio",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

df = load_data()

# Small helper for missing column warning
def require_columns(cols):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        st.warning(f"Missing column(s): {', '.join(missing)}")
        return False
    return True

# ------------------ SIDEBAR ------------------
st.sidebar.header("Dataset & Filters")

st.sidebar.markdown(
    """
**Dataset description**

- Synthetic ER visits dataset  
- Includes visit date, hospital, urgency level, season, time of day  
- Time to registration, triage, and medical professional  
- Total wait time and patient satisfaction
"""
)

# Filters
if "Day of Week" in df.columns:
    day_filter = st.sidebar.multiselect(
        "Filter by Day of Week",
        options=sorted(df["Day of Week"].dropna().unique()),
        default=sorted(df["Day of Week"].dropna().unique())
    )
else:
    day_filter = None

if "Season" in df.columns:
    season_filter = st.sidebar.multiselect(
        "Filter by Season",
        options=sorted(df["Season"].dropna().unique()),
        default=sorted(df["Season"].dropna().unique())
    )
else:
    season_filter = None

if "Urgency Level" in df.columns:
    urgency_filter = st.sidebar.multiselect(
        "Filter by Urgency Level",
        options=sorted(df["Urgency Level"].dropna().unique()),
        default=sorted(df["Urgency Level"].dropna().unique())
    )
else:
    urgency_filter = None

if "Hospital Name" in df.columns:
    hospital_filter = st.sidebar.multiselect(
        "Filter by Hospital",
        options=sorted(df["Hospital Name"].dropna().unique()),
        default=sorted(df["Hospital Name"].dropna().unique())
    )
else:
    hospital_filter = None

# Apply filters
df_filtered = df.copy()

if day_filter is not None:
    df_filtered = df_filtered[df_filtered["Day of Week"].isin(day_filter)]
if season_filter is not None:
    df_filtered = df_filtered[df_filtered["Season"].isin(season_filter)]
if urgency_filter is not None:
    df_filtered = df_filtered[df_filtered["Urgency Level"].isin(urgency_filter)]
if hospital_filter is not None:
    df_filtered = df_filtered[df_filtered["Hospital Name"].isin(hospital_filter)]

st.sidebar.markdown("---")
st.sidebar.write(f"**Filtered rows:** {len(df_filtered):,}")

# ------------------ NAVIGATION MENU ------------------
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Dashboard", "📄 Data Preview", "📊 Visualizations", "💡 Insights"]
)

# ------------------ DASHBOARD ------------------
if menu == "🏠 Dashboard":
    st.header("🏠 Dashboard Overview")

    if df_filtered.empty:
        st.warning("No data after applying filters.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            if "Total_Wait_Hours" in df_filtered.columns:
                avg_wait = df_filtered["Total_Wait_Hours"].mean()
                st.metric("Avg Total Wait Time (hours)", f"{avg_wait:.2f}")
            else:
                st.metric("Avg Total Wait Time (hours)", "N/A")

        with col2:
            if "Time_to_MD_Hours" in df_filtered.columns:
                avg_md = df_filtered["Time_to_MD_Hours"].mean()
                st.metric("Avg Time to See MD (hours)", f"{avg_md:.2f}")
            else:
                st.metric("Avg Time to See MD (hours)", "N/A")

        with col3:
            if "Patient Satisfaction" in df_filtered.columns:
                avg_sat = df_filtered["Patient Satisfaction"].mean()
                st.metric("Avg Patient Satisfaction", f"{avg_sat:.2f} / 5")
            else:
                st.metric("Avg Patient Satisfaction", "N/A")

        st.markdown("---")
        st.subheader("📌 Quick Notes")
        st.write(
            "- Use the **left sidebar filters** to focus on specific days, seasons, "
            "urgency levels, or hospitals.\n"
            "- Navigate to **Visualizations** for detailed charts.\n"
            "- Go to **Insights** to read summarized recommendations."
        )

# ------------------ DATA PREVIEW ------------------
elif menu == "📄 Data Preview":
    st.header("📄 Data Preview")
    st.write("Below is a sample of the filtered dataset:")
    st.dataframe(df_filtered.head(50), use_container_width=True)

    st.markdown("### Summary statistics")
    st.write(df_filtered.describe(include="all"))

# ------------------ VISUALIZATIONS ------------------
elif menu == "📊 Visualizations":
    st.header("📊 Visualizations")

    # 1) Heatmap: Average wait by Day & Time of Day
    st.subheader("1. Average ER Wait Time by Day of Week and Time of Day")
    if require_columns(["Day of Week", "Time of Day", "Total_Wait_Hours"]):
        pivot = (
            df_filtered
            .groupby(["Day of Week", "Time of Day"])["Total_Wait_Hours"]
            .mean()
            .reset_index()
        )

        if not pivot.empty:
            heat_data = pivot.pivot(
                index="Day of Week",
                columns="Time of Day",
                values="Total_Wait_Hours"
            )
            fig1 = px.imshow(
                heat_data,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="Blues",
                labels=dict(color="Avg Wait (h)"),
            )
            fig1.update_layout(margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig1, use_container_width=True)

            st.markdown(
                """
**Recommendation:**  
- Adjust medical staff numbers per shift to match peak demand.  
- Increase triage speed and staffing during **late morning** and **evening peaks**.  
- Use **fast-track pathways** for simple and moderate cases to relieve congestion.
"""
            )
        else:
            st.info("No data available for this chart with current filters.")

    st.markdown("---")

    # 2) Bar: Wait time by Urgency Level
    st.subheader("2. Average ER Wait Time by Urgency Level")
    if require_columns(["Urgency Level", "Total_Wait_Hours"]):
        urg = (
            df_filtered
            .groupby("Urgency Level")["Total_Wait_Hours"]
            .mean()
            .reset_index()
            .sort_values("Total_Wait_Hours")
        )
        if not urg.empty:
            fig2 = px.bar(
                urg,
                x="Urgency Level",
                y="Total_Wait_Hours",
                labels={"Total_Wait_Hours": "Avg Wait (hours)"},
            )
            st.plotly_chart(fig2, use_container_width=True)

            st.markdown(
                """
**Recommendation:**  
- Low-urgency patients experience the longest delays.  
- Implement a **dedicated fast-track system** to handle low and moderate cases quickly.
"""
            )

    st.markdown("---")

    # 3) Line: Wait vs Nurse-to-Patient Ratio
    st.subheader("3. Average ER Wait Time by Nurse-to-Patient Ratio")
    if require_columns(["Nurse-to-Patient Ratio", "Total_Wait_Hours"]):
        n2p = (
            df_filtered
            .groupby("Nurse-to-Patient Ratio")["Total_Wait_Hours"]
            .mean()
            .reset_index()
            .sort_values("Nurse-to-Patient Ratio")
        )
        if not n2p.empty:
            fig3 = px.line(
                n2p,
                x="Nurse-to-Patient Ratio",
                y="Total_Wait_Hours",
                markers=True,
                labels={"Total_Wait_Hours": "Avg Wait (hours)"},
            )
            st.plotly_chart(fig3, use_container_width=True)

            st.markdown(
                """
**Recommendation:**  
- Increase the number of nurses during **peak hours**.  
- Apply **flexible staffing schedules** based on expected patient volume.  
- Reinforce **triage nurses** to reduce initial waiting time.
"""
            )

    st.markdown("---")

    # 4) Line: Wait across Seasons
    st.subheader("4. Average ER Wait Time Across Seasons")
    if require_columns(["Season", "Total_Wait_Hours"]):
        seas = (
            df_filtered
            .groupby("Season")["Total_Wait_Hours"]
            .mean()
            .reset_index()
        )
        if not seas.empty:
            # To keep season order nice if possible
            season_order = ["Winter", "Spring", "Summer", "Fall"]
            seas["Season"] = pd.Categorical(
                seas["Season"], categories=season_order, ordered=True
            )
            seas = seas.sort_values("Season")

            fig4 = px.line(
                seas,
                x="Season",
                y="Total_Wait_Hours",
                markers=True,
                labels={"Total_Wait_Hours": "Avg Wait (hours)"},
            )
            st.plotly_chart(fig4, use_container_width=True)

            st.markdown(
                """
**Recommendation:**  
- **Winter** and sometimes **Summer** show higher wait times.  
- Enhance **seasonal health awareness** (vaccines, respiratory illness prevention)  
  and plan additional staffing during peak seasons.
"""
            )

    st.markdown("---")

    # 5) Scatter: Satisfaction vs Time to MD
    st.subheader("5. Patient Satisfaction vs Time to See Medical Professional")
    if require_columns(["Time_to_MD_Hours", "Patient Satisfaction"]):
        scat = df_filtered.dropna(
            subset=["Time_to_MD_Hours", "Patient Satisfaction"]
        )
        if not scat.empty:
            fig5 = px.scatter(
                scat,
                x="Time_to_MD_Hours",
                y="Patient Satisfaction",
                opacity=0.4,
                labels={
                    "Time_to_MD_Hours": "Time to MD (hours)",
                    "Patient Satisfaction": "Satisfaction Score",
                },
            )
            st.plotly_chart(fig5, use_container_width=True)

            st.markdown(
                """
**Recommendation:**  
- There is a clear **negative relationship** between wait time and satisfaction.  
- Reducing the time to see a medical professional should be a top priority.  
- Fast-track simple cases and optimize triage flow to protect patient experience.
"""
            )

# ------------------ INSIGHTS PAGE ------------------
elif menu == "💡 Insights":
    st.header("💡 Key Insights & Recommendations")

    st.subheader("1. Peak Times & Staffing")
    st.write(
        "- Evening and late-morning periods show the **highest congestion**.\n"
        "- Staff levels should be aligned with these peak patterns, especially in triage."
    )

    st.subheader("2. Urgency Level Management")
    st.write(
        "- **Low-urgency patients** wait the longest and are most affected by delays.\n"
        "- A dedicated **fast-track area** for simple and moderate cases can significantly "
        "reduce overall ER crowding."
    )

    st.subheader("3. Nurse-to-Patient Ratio")
    st.write(
        "- As the **nurse-to-patient ratio** increases, wait time rises sharply.\n"
        "- Hospitals should maintain safe ratios during busy hours and consider "
        "**dynamic staffing models**."
    )

    st.subheader("4. Seasonal Patterns")
    st.write(
        "- **Winter** and sometimes **Summer** have longer wait times due to seasonal illnesses.\n"
        "- Preventive campaigns and pre-planned staffing can reduce seasonal pressure on ERs."
    )

    st.subheader("5. Patient Satisfaction")
    st.write(
        "- There is a strong **negative correlation** between wait time and satisfaction.\n"
        "- Reducing time to see a doctor is critical to improving patient experience.\n"
        "- Quick triage, effective routing, and fast-track services are key strategies."
    )

    st.markdown("---")
    st.write("✅ Use this dashboard together with hospital operations teams to design data-driven improvements.")

# ------------------ FOOTER ------------------
st.markdown("---")
st.write("👩‍⚕️ **ER Wait Time Dashboard – built with Streamlit.**")
