import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def load_data(file_name):
    return pd.read_csv(file_name)

def create_bar_chart(data, x, y, title, labels, color):
    return px.bar(data, x=x, y=y, title=title, labels=labels, color=color)

def create_pie_chart(data, names, values, title):
    return px.pie(data, names=names, values=values, title=title)

def create_word_cloud(data, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(data)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    st.pyplot(plt)

def create_line_chart(data, x, y, title, labels, color=None, line_group=None):
    return px.line(data, x=x, y=y, title=title, labels=labels, color=color, line_group=line_group)

def group_and_sort_data(df, group_by_cols, sort_by_cols, ascending):
    grouped_data = df.groupby(group_by_cols).size().reset_index(name='Count')
    sorted_data = grouped_data.sort_values(sort_by_cols, ascending=ascending)
    return sorted_data.drop_duplicates(subset=group_by_cols[0], keep='first')

df = load_data('group8.csv')
members = ['Bianca', 'Genevieve', 'John']

# Create a combined graph for all members
combined_data = df.groupby('Activity Type')['Duration'].sum().reset_index()
combined_sorted_data = combined_data.sort_values(by='Duration', ascending=False)
combined_fig = create_bar_chart(combined_sorted_data, 'Activity Type', 'Duration', 'Total Duration of Activity Types Across All Members (in hours)', {'Duration': 'Total Duration (hours)'}, 'Activity Type')

# Create a pie chart to show the distribution of time spent in different locations
location_data = df.groupby('Location')['Duration'].sum().reset_index()
location_fig = create_pie_chart(location_data, 'Location', 'Duration', 'Distribution of Time Spent in Different Locations (in hours)')

# Create a word cloud for the "How I feel" column
create_word_cloud(' '.join(df['How I feel'].dropna()), 'Word Cloud for "How I feel"')

# Filter data for sleep activities
df_sleep = df[(df['Member'].isin(members)) & (df['Activity'].isin(['Sleep']))]
df_sleep['DateTime'] = pd.to_datetime(df_sleep['Date'] + ' ' + df_sleep['Time'])

# Group by date and calculate average sleep duration per day among members
average_sleep_data = df_sleep.groupby(['Date', 'Member'])['Duration'].sum().reset_index()
average_sleep_duration = average_sleep_data.groupby('Date')['Duration'].mean().reset_index()
average_line_chart = create_line_chart(average_sleep_duration, 'Date', 'Duration', 'Average Sleep Duration per Day Across Members (in hours)', {'Duration': 'Average Sleep Duration (hours)'})

# Create a line chart using plotly for the sleep duration per day for each member
grouped_sleep_data = df_sleep.groupby(['Date', 'Member'])['Duration'].sum().reset_index()
line_chart = create_line_chart(grouped_sleep_data, 'Date', 'Duration', 'Sleep Duration per Day for Each Member (in hours)', {'Duration': 'Sleep Duration (hours)'}, 'Member', 'Member')

# Create pie charts for the top 5 feelings during School, Leisure, and Travel
for activity in ['School', 'Leisure', 'Travel']:
    top_feelings = df[df['Activity Type'] == activity]['How I feel'].value_counts().head(5).reset_index()
    top_feelings.columns = ['Feeling', 'Count']
    feelings_pie = create_pie_chart(top_feelings, 'Feeling', 'Count', f'Top 5 Feelings During {activity}')
    st.plotly_chart(feelings_pie, key=f'Feelings During {activity}')

# Group the data by 'Activity Type' and 'How I feel' columns, sorted in descending order by 'Count'
feelings_data = group_and_sort_data(df, ['Activity Type', 'How I feel'], ['Count'], [False])
feelings_fig = create_bar_chart(feelings_data, 'Activity Type', 'Count', 'Highest Feeling/Emotion Felt During Each Activity Type', {'Count': 'Count of Feelings'}, 'How I feel')

# Display the charts in Streamlit
for chart in [average_line_chart, line_chart, combined_fig, location_fig, feelings_fig]:
    st.plotly_chart(chart)
    
# Count the occurrences of each activity
activity_counts = df['Activity'].value_counts()

# Select the top 15 activities
top_15_activities = activity_counts.head(15)

# Filter the DataFrame to include only the top 15 activities
df_top_15 = df[df['Activity'].isin(top_15_activities.index)]

# Create a tree map with both Activity and Location
fig = px.treemap(df_top_15, path=['Location', 'Activity'], 
                 title='Top Activities with Highest Occurrences by Location',
                 width=800, height=600)

fig.update_layout(
    title=dict(text='Top Activities with Highest Occurrences by Location', x=0.5, y=0.95, font=dict(color='black')),
    paper_bgcolor='rgba(0,0,0,0)'  # Set the paper background color to transparent
)

st.plotly_chart(fig)
