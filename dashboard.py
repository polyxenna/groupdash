import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load the dataset
data = pd.read_csv('group.csv')

# Convert the 'Date' column to a datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Filter the data for rows where 'Activity' is 'Sleep' or 'Sleeping'
sleep_data = data[data['Activity'].isin(['Sleep', 'Sleeping'])]

# Extract and parse the 'Time' column as a string in the format '%I:%M:%S %p'
sleep_data['Time'] = pd.to_datetime(sleep_data['Time'], format='%I:%M:%S %p').dt.strftime('%I:%M %p')

# Group the data by 'Date' and calculate the average 'Time' for each day
average_sleep_start = sleep_data.groupby('Date')['Time'].min()

# Reset the index to make 'Date' a column
average_sleep_start = average_sleep_start.reset_index()

# Calculate the average sleep duration
average_sleep_duration = sleep_data.groupby('Date')['Duration'].mean() / 60  # Convert minutes to hours

# Reset the index to make 'Date' a column
average_sleep_duration = average_sleep_duration.reset_index()

# Create a line plot for average sleep duration using Plotly
fig_duration = px.line(average_sleep_duration, x='Date', y='Duration', labels={'x': 'Date', 'y': 'Average Duration (hours)'})
fig_duration.update_xaxes(
    tickvals=average_sleep_duration['Date'],
    ticktext=average_sleep_duration['Date'].dt.strftime('%m/%d/%Y'),
    title_text='Date'
)

# Create a line plot for average sleep start time using Plotly
fig_start_time = px.line(average_sleep_start, x='Date', y='Time', labels={'x': 'Date', 'y': 'Average Sleep Start Time'})
fig_start_time.update_xaxes(
    tickvals=average_sleep_start['Date'],
    ticktext=average_sleep_start['Date'].dt.strftime('%m/%d/%Y'),
    title_text='Date'
)
fig_start_time.update_yaxes(
    tickvals=average_sleep_start['Time'].unique(),
    ticktext=average_sleep_start['Time'],
    title_text='Average Sleep Start Time'
)

# Streamlit app
st.title('Sleep Dashboard')

st.write("### Average Sleep Duration per Day")
st.plotly_chart(fig_duration)

st.write("### Average Sleep Start Time per Day")
st.plotly_chart(fig_start_time)
