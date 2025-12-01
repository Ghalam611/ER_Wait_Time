## ER Wait Time Dashboard

The ER Wait Time Dashboard is an analytical Streamlit application designed to explore and visualize factors affecting emergency room wait times. It provides hospitals, analysts, and healthcare administrators with data-driven insights to improve patient flow, reduce congestion, and enhance overall patient satisfaction.

⸻

## Overview

This dashboard analyzes synthetic ER visit data across multiple dimensions such as time of day, day of week, urgency level, seasonal patterns, nurse-to-patient ratios, and patient satisfaction scores.
Through interactive filters and dynamic visualizations, users can identify operational bottlenecks and evaluate performance trends that influence ER efficiency.

⸻

## Key Features
	•	Interactive visual dashboards built using Plotly
	•	Filters for day of week, season, urgency level, and hospital
	•	Heatmaps, bar charts, line charts, and scatter plots
	•	Advanced analysis of staffing patterns and congestion peaks
	•	Automatic operational recommendations under each visualization
	•	Insights page summarizing findings and improvement opportunities
	•	Clean and intuitive Streamlit user interface
	•	Data preview and descriptive statistics

⸻

## Dataset Description

The dataset includes the following fields:
	•	Visit ID and Patient ID
	•	Hospital Name and Region
	•	Season, Day of Week, Time of Day
	•	Urgency Level (Critical, High, Medium, Low)
	•	Nurse-to-Patient Ratio
	•	Total Wait Time (minutes/hours)
	•	Time to see the medical professional
	•	Patient Satisfaction Score (1–5)

The dataset was cleaned and preprocessed to remove missing values and ensure numeric consistency across time-related columns.

⸻

## Dashboard Pages

1. Dashboard Overview

Displays overall statistics including:
	•	Average total wait time
	•	Average time to see a medical doctor
	•	Average patient satisfaction

⸻

2. Data Preview

Shows the first portion of the dataset with descriptive statistics for a clear understanding of the data.

⸻

3. Visualizations

A. Average ER Wait Time by Day of Week and Time of Day

A heatmap that highlights congestion peaks during late morning and evening.
Recommendation: Align staffing levels with peak periods and activate fast-track lanes for simple cases.

B. Average ER Wait Time by Urgency Level

A bar chart showing that low-urgency patients experience the longest delays.
Recommendation: Implement a dedicated fast-track area for low-to-moderate urgency cases.

C. Wait Time vs Nurse-to-Patient Ratio

A line plot showing longer delays when nurse-to-patient ratios increase.
Recommendation: Maintain safe nurse staffing and use flexible scheduling during peak times.

D. Average ER Wait Time Across Seasons

A seasonal trend line that shows winter and summer have the highest wait times.
Recommendation: Prepare seasonal staffing plans and promote preventive health programs.

E. Patient Satisfaction vs Time to Medical Professional

A scatter plot demonstrating a strong negative correlation between waiting time and satisfaction.
Recommendation: Prioritize reducing physician waiting time and strengthen triage performance.

⸻

## Insights Summary
	•	Wait times consistently peak during late morning and evening hours.
	•	Low-urgency patients face the longest delays and benefit the most from fast-track systems.
	•	Higher nurse-to-patient ratios are linked to significantly longer wait times.
	•	Seasonal illnesses increase pressure on ERs, especially in winter and summer.
	•	Patient satisfaction decreases rapidly when the time to see a medical professional increases.

⸻

## Future Improvements
	•	Predictive modeling for estimating wait times
	•	Simulation tools for staff allocation and resource optimization
	•	Multi-hospital benchmark comparison
	•	Bilingual dashboard (Arabic/English)
	•	Automated PDF reporting with embedded charts

⸻

## Technologies Used:

	•	Python
  
	•	Streamlit
  
	•	Pandas
  
	•	NumPy
  
	•	Plotly Express
  
⸻

## Done by:

Ghala Almutairi
  
