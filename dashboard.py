import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('group8.csv')

# Filter the dataset for the specified members (Bianca, Genevieve, John)
members = ['Bianca', 'Genevieve', 'John']

# Create a list to store the individual graphs
individual_graphs = []

# Create separate graphs for each member
for member in members:
    # Filter data for the current member
    df_member = df[df['Member'] == member]

    # Group by Activity Type and calculate the total duration in hours
    grouped_data = df_member.groupby('Activity Type')['Duration'].sum() / 60.0  # Convert minutes to hours
    grouped_data = grouped_data.reset_index()

    # Sort the data by the total duration in descending order
    sorted_data = grouped_data.sort_values(by='Duration', ascending=False)

    # Create a bar graph using plotly for the current member
    fig = px.bar(sorted_data, x='Activity Type', y='Duration',
                 title=f'Total Duration of Activity Types for {member} (in hours)',
                 labels={'Duration': 'Total Duration (hours)'}, color='Activity Type')

    # Add the current graph to the list
    individual_graphs.append(fig)

# Create a combined graph for all members
combined_data = df.groupby('Activity Type')['Duration'].sum() / 60.0  # Convert minutes to hours
combined_data = combined_data.reset_index()
combined_sorted_data = combined_data.sort_values(by='Duration', ascending=False)

# Create a bar graph using plotly for the combined data
combined_fig = px.bar(combined_sorted_data, x='Activity Type', y='Duration',
                      title='Total Duration of Activity Types Across All Members (in hours)',
                      labels={'Duration': 'Total Duration (hours)'}, color='Activity Type')

# Create a pie chart to show the distribution of time spent in different locations
location_data = df.groupby('Location')['Duration'].sum() / 60.0  # Convert minutes to hours
location_data = location_data.reset_index()
location_fig = px.pie(location_data, names='Location', values='Duration',
                      title='Distribution of Time Spent in Different Locations (in hours)')

# Create a word cloud for the "How I feel" column
wordcloud_data = ' '.join(df['How I feel'].dropna())  # Join all "How I feel" entries
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wordcloud_data)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud for "How I feel"')
st.pyplot(plt)

# Filter data for sleep activities
sleep_activities = ['Sleep', 'Sleeping']
df_sleep = df[(df['Member'].isin(members)) & (df['Activity'].isin(sleep_activities))]

# Convert 'Date' and 'Time' columns to datetime
df_sleep['DateTime'] = pd.to_datetime(df_sleep['Date'] + ' ' + df_sleep['Time'])

# Group by date and calculate average sleep duration per day among members
average_sleep_data = df_sleep.groupby(['Date', 'Member'])['Duration'].sum() / 60.0  # Convert minutes to hours
average_sleep_data = average_sleep_data.reset_index()
average_sleep_duration = average_sleep_data.groupby('Date')['Duration'].mean()  # Average among members
average_sleep_duration = average_sleep_duration.reset_index()

# Create a line chart using plotly for the average sleep duration
average_line_chart = px.line(average_sleep_duration, x='Date', y='Duration',
                             title='Average Sleep Duration per Day Across Members (in hours)',
                             labels={'Duration': 'Average Sleep Duration (hours)'})

# Create a line chart using plotly for the sleep duration per day for each member
grouped_sleep_data = df_sleep.groupby(['Date', 'Member'])['Duration'].sum() / 60.0  # Convert minutes to hours
grouped_sleep_data = grouped_sleep_data.reset_index()
line_chart = px.line(grouped_sleep_data, x='Date', y='Duration', color='Member',
                     title='Sleep Duration per Day for Each Member (in hours)',
                     labels={'Duration': 'Sleep Duration (hours)'}, line_group='Member')

# Display the line charts, individual graphs, combined graph, pie chart, and word cloud in Streamlit
st.plotly_chart(average_line_chart, key='Average Sleep Duration Line Chart')
st.plotly_chart(line_chart, key='Sleep Duration Line Chart')

for i, graph in enumerate(individual_graphs):
    st.plotly_chart(graph, key=f'Graph {i+1}')

st.plotly_chart(combined_fig, key='Combined Graph')
st.plotly_chart(location_fig, key='Location Pie Chart')
