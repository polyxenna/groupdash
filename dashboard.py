import pandas as pd
import plotly.express as px
import streamlit as st

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

# Display the individual graphs, the combined graph, and the pie chart in Streamlit
for i, graph in enumerate(individual_graphs):
    st.plotly_chart(graph, key=f'Graph {i+1}')

st.plotly_chart(combined_fig, key='Combined Graph')
st.plotly_chart(location_fig, key='Location Pie Chart')
