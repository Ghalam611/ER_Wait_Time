import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# إعداد الصفحة
st.set_page_config(
    page_title="ER Wait Time Dashboard",
    layout="wide"
)

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv("clean_data.csv")

df = load_data()

# أسماء الأعمدة في ملفك
WAIT_COL = "Total Wait Time (min)"
TIME_OF_DAY_COL = "Time of Day"
URGENCY_COL = "Urgency Level"
NURSE_RATIO_COL = "Nurse-to-Patient Ratio"
SEASON_COL = "Season"
SATISFACTION_COL = "Patient Satisfaction"

# ===========================
# العنوان والمعاينة
# ===========================
st.title("ER Wait Time – Interactive Dashboard")

st.markdown(
    """
    This dashboard analyzes *Emergency Room (ER) wait times*  
    and provides operational recommendations to improve patient flow  
    and satisfaction.
    """
)

st.subheader("Data Preview")
st.dataframe(df.head(20))

st.markdown("---")

# ===========================
# 1) Average Wait Time by Time of Day
# ===========================
st.subheader("1. Average Wait Time by Time of Day")

if TIME_OF_DAY_COL in df.columns and WAIT_COL in df.columns:
    fig1_data = (
        df.groupby(TIME_OF_DAY_COL)[WAIT_COL]
        .mean()
        .reset_index()
        .sort_values(WAIT_COL, ascending=False)
    )

    fig1 = px.bar(
        fig1_data,
        x=TIME_OF_DAY_COL,
        y=WAIT_COL,
        title="Average ER Wait Time by Time of Day",
        labels={WAIT_COL: "Average Wait Time (minutes)"}
    )

    st.plotly_chart(fig1, use_container_width=True, height=420)

    st.markdown(
        """
        *Recommendations:*  
        - Adjust staffing levels per shift based on patient volume.  
        - Increase triage team speed and size during *late morning (~11:00)* to reduce crowding.  
        - Implement a *fast track* system for mild to moderate cases.  
        """
    )
else:
    st.info("Columns for time of day or wait time are missing.")

st.markdown("---")

# ===========================
# 2) Wait Time by Urgency Level
# ===========================
st.subheader("2. Wait Time by Urgency Level")

if URGENCY_COL in df.columns and WAIT_COL in df.columns:
    fig2 = px.box(
        df,
        x=URGENCY_COL,
        y=WAIT_COL,
        title="Wait Time Distribution by Urgency Level"
    )

    st.plotly_chart(fig2, use_container_width=True, height=420)

    st.markdown(
        """
        *Recommendation:*  
        - To reduce wait time for *Low* urgency patients, create a dedicated *fast track*  
          pathway for simple and moderate cases.  
        """
    )
else:
    st.info("Column for urgency level is missing.")

st.markdown("---")

# ===========================
# 3) Nurse-to-Patient Ratio
# ===========================
st.subheader("3. Nurse-to-Patient Ratio and Peak Hours")

if NURSE_RATIO_COL in df.columns and WAIT_COL in df.columns:
    # بدون trendline عشان ما نحتاج statsmodels
    fig3 = px.scatter(
        df,
        x=NURSE_RATIO_COL,
        y=WAIT_COL,
        opacity=0.6,
        title="Wait Time vs Nurse-to-Patient Ratio"
    )

    st.plotly_chart(fig3, use_container_width=True, height=420)

    st.markdown(
        """
        *Recommendations:*  
        - Increase the number of nurses during *peak hours*.  
        - Use *flexible scheduling* based on expected patient volume.  
        - Increase triage staff to reduce initial waiting time.  
        """
    )
else:
    st.info("Column for nurse-to-patient ratio is missing.")

st.markdown("---")

# ===========================
# 4) Seasonal Patterns
# ===========================
st.subheader("4. Seasonal Patterns and Wait Times")

if SEASON_COL in df.columns and WAIT_COL in df.columns:
    fig4_data = (
        df.groupby(SEASON_COL)[WAIT_COL]
        .mean()
        .reset_index()
    )

    fig4 = px.bar(
        fig4_data,
        x=SEASON_COL,
        y=WAIT_COL,
        title="Average Wait Time by Season"
    )

    st.plotly_chart(fig4, use_container_width=True, height=420)

    st.markdown(
        """
        *Recommendation:*  
        - Enhance *seasonal health awareness* campaigns during  
          winter & summer, including vaccines and preventive medications.  
        """
    )
else:
    st.info("Column for season is missing.")

st.markdown("---")

# ===========================
# 5) Patient Satisfaction vs Wait Time
# ===========================
st.subheader("5. Patient Satisfaction vs Total Wait Time")

if SATISFACTION_COL in df.columns and WAIT_COL in df.columns:
    fig5 = px.scatter(
        df,
        x=WAIT_COL,
        y=SATISFACTION_COL,
        opacity=0.6,
        title="Wait Time vs Patient Satisfaction"
    )

    st.plotly_chart(fig5, use_container_width=True, height=420)

    corr = df[[WAIT_COL, SATISFACTION_COL]].corr().iloc[0, 1]

    st.markdown(
        f"""
        *Insights:*  
        - There is a clear *negative relationship* between wait time and patient satisfaction  
          (correlation ≈ {corr:.2f}).  
        - Waiting before seeing the physician is a *critical factor* in patient experience.  

        *Recommendation:*  
        - Improve the *speed of access* to medical professionals after triage and registration.  
        """
    )
else:
    st.info("Column for patient satisfaction is missing.")

st.markdown("---")
st.markdown("Dashboard generated for ER Wait Time Project.")