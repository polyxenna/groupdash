import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

def load_data(file_name):
    return pd.read_csv(file_name)

def create_bar_chart(data, x, y, labels, color):
    return px.bar(data, x=x, y=y, labels=labels, color=color)

def create_pie_chart(data, names, values, title='', explode_index=None):
    fig = px.pie(data, names=names, values=values, title=title)
    fig.update_layout(width=500)

    if explode_index is not None:
        # Calculate the pull values
        pull_values = [0.1 if i == explode_index else 0 for i in range(len(data))]
        fig.update_traces(pull=pull_values)

    return fig



def create_word_cloud(data, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(data)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

import plotly.express as px

def create_line_chart(data, x, y, labels, color=None, line_group=None):
    data_copy = data.copy()
    data_copy[y] = data_copy[y] / 60  # Convert duration from minutes to hours
    return px.line(data_copy, x=x, y=y, labels=labels, color=color, line_group=line_group, template='plotly', hover_name=line_group, custom_data=[data_copy[y]])

def group_and_sort_data(df, group_by_cols, sort_by_cols, ascending):
    grouped_data = df.groupby(group_by_cols).size().reset_index(name='Count')
    sorted_data = grouped_data.sort_values(sort_by_cols, ascending=ascending)
    return sorted_data.drop_duplicates(subset=group_by_cols[0], keep='first')

df = load_data('group8.csv')
members = ['Bianca', 'Genevieve', 'John']

# Create a combined graph for all members
combined_data = df.groupby('Activity Type')['Duration'].sum().reset_index()
combined_sorted_data = combined_data.sort_values(by='Duration', ascending=False)
combined_sorted_data['Duration'] /= 60  # Convert duration from minutes to hours
combined_fig = create_bar_chart(combined_sorted_data, 'Activity Type', 'Duration', {'Duration': 'Total Duration (hours)'}, 'Activity Type')


# Create a pie chart to show the distribution of time spent in different locations
location_data = df.groupby('Location')['Duration'].sum().reset_index()

location_fig = create_pie_chart(location_data, 'Location', 'Duration', explode_index=0)

# Group the data by 'Activity Type' and 'How I feel' columns, sorted in descending order by 'Count'
feelings_data = group_and_sort_data(df, ['Activity Type', 'How I feel'], ['Count'], [False])
feelings_fig = create_bar_chart(feelings_data, 'Activity Type', 'Count', {'Count': 'Count of Feelings'}, 'How I feel')

# Filter data for sleep activities
df_sleep = df[(df['Member'].isin(members)) & (df['Activity'].isin(['Sleep']))]
df_sleep['DateTime'] = pd.to_datetime(df_sleep['Date'] + ' ' + df_sleep['Time'])

# Group by date and calculate average sleep duration per day among members
average_sleep_data = df_sleep.groupby(['Date', 'Member'])['Duration'].sum().reset_index()
average_sleep_duration = average_sleep_data.groupby('Date')['Duration'].mean().reset_index()
average_line_chart = create_line_chart(average_sleep_duration, 'Date', 'Duration', {'Duration': 'Average Sleep Duration (hours)'})

# Create a line chart using plotly for the sleep duration per day for each member
grouped_sleep_data = df_sleep.groupby(['Date', 'Member'])['Duration'].sum().reset_index()
line_chart = create_line_chart(grouped_sleep_data, 'Date', 'Duration', {'Duration': 'Sleep Duration (hours)'}, 'Member', 'Member')

# Count the occurrences of each activity
activity_counts = df['Activity'].value_counts()

# Select the top 15 activities
top_15_activities = activity_counts.head(15)

# Filter the DataFrame to include only the top 15 activities
df_top_15 = df[df['Activity'].isin(top_15_activities.index)]

# Create a tree map with both Activity and Location
fig = px.treemap(df_top_15, path=['Location', 'Activity'],
                 width=550, height=500)

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)'  # Set the paper background color to transparent
)

# Add a header text in a round-edged rectangle using st.markdown with inline HTML/CSS styles
header_html = """
    <div style='
        text-align: center;
        color: #004080;
        background-color: #CE93D8;
        padding: 5px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        '>
        <h1>
            Group 8 - 2 Week Activity Analysis
        </h1>
        <p>
        Bianca Jessa A. Carabio | Genevieve N. Miao | John Oscar D. Roble
        </p>
    </div>
"""

# Use st.markdown to display the HTML content
st.markdown(header_html, unsafe_allow_html=True)

# Create a container for the charts
chart_container = st.container()

# Display the first graph in the first column
with chart_container:
    # Create two columns
    col1, col2, col10 = st.columns(3)

    # Display the first graph in the first column
    with col1:
        # Add a text inside a round-edged rectangle
        st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h3>
                    Activity Types Ranking based on Total Duration
                </h3>
            </div>
        """, unsafe_allow_html=True)
        # Display the first graph
        st.plotly_chart(combined_fig)

    # Display the second graph in the second column
    with col2:
        # Add a text inside a round-edged rectangle
        st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h3>
                    Distribution of Time Spent in Different Locations
                </h3>
            </div>
        """, unsafe_allow_html=True)
        # Display the second graph
        st.plotly_chart(location_fig)

    with col10:
        # Add a text inside a round-edged rectangle
        st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h3>
                    Top Activities with Highest Occurrences by Location
                </h3>
            </div>
        """, unsafe_allow_html=True)
        # Display the second graph
        st.plotly_chart(fig)

# Create another container for additional charts
additional_chart_container = st.container()

# Display the Word Cloud and Highest Feeling/Emotion graphs in the second container
with additional_chart_container:
    # Create two columns
    col3, col4 = st.columns(2)

    # Display the Word Cloud in the first column
    with col3:
        # Add a text inside a round-edged rectangle
        st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h3>
                    Word Cloud for "How I feel"
                </h3>
            </div>
        """, unsafe_allow_html=True)
        # Display the Word Cloud
        create_word_cloud(' '.join(df['How I feel'].dropna()), '')

    # Display the Highest Feeling/Emotion graph in the second column
    with col4:
        # Add a text inside a round-edged rectangle
        st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h3>
                    Highest Feeling/Emotion Felt During Each Activity Type
                </h3>
            </div>
        """, unsafe_allow_html=True)
        # Display the Highest Feeling/Emotion graph
        st.plotly_chart(feelings_fig)

st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h3>
                    Top 5 Feelings for Each Activity Type
                </h3>
            </div>
        """, unsafe_allow_html=True)

# Create another container for top 5 feelings during School, Travel, and Leisure
top_feelings_container = st.container()

# Display the top 5 feelings during School, Travel, and Leisure in the third container
with top_feelings_container:
    # Create three columns
    col5, col6, col7 = st.columns(3)

    # Create and display the graph for top 5 feelings during School in the first column
    # Create and display the graph for top 5 feelings during School in the first column
    with col5:
        st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding-top:15px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h5>
                    School
                </h5>
            </div>
        """, unsafe_allow_html=True)
        top_school_feelings = df[df['Activity Type'] == 'School']['How I feel'].value_counts().head(5).reset_index()
        top_school_feelings.columns = ['Feeling', 'Count']
        # Get the index of the row with the highest count
        explode_index_school = top_school_feelings['Count'].idxmax()
        feelings_school_pie = create_pie_chart(top_school_feelings, 'Feeling', 'Count', explode_index=explode_index_school)
        st.plotly_chart(feelings_school_pie, key='Feelings During School')

    # Create and display the graph for top 5 feelings during Travel in the second column
    with col6:
        st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding-top:15px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h5>
                    Travel
                </h5>
            </div>
        """, unsafe_allow_html=True)
        top_travel_feelings = df[df['Activity Type'] == 'Travel']['How I feel'].value_counts().head(5).reset_index()
        top_travel_feelings.columns = ['Feeling', 'Count']
        # Get the index of the row with the highest count
        explode_index_travel = top_travel_feelings['Count'].idxmax()
        feelings_travel_pie = create_pie_chart(top_travel_feelings, 'Feeling', 'Count', explode_index=explode_index_travel)
        st.plotly_chart(feelings_travel_pie, key='Feelings During Travel')

    # Create and display the graph for top 5 feelings during Leisure in the third column
    with col7:
        st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding-top:15px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h5>
                    Leisure
                </h5>
            </div>
        """, unsafe_allow_html=True)
        top_leisure_feelings = df[df['Activity Type'] == 'Leisure']['How I feel'].value_counts().head(5).reset_index()
        top_leisure_feelings.columns = ['Feeling', 'Count']
        # Get the index of the row with the highest count
        explode_index_leisure = top_leisure_feelings['Count'].idxmax()
        feelings_leisure_pie = create_pie_chart(top_leisure_feelings, 'Feeling', 'Count', explode_index=explode_index_leisure)
        st.plotly_chart(feelings_leisure_pie, key='Feelings During Leisure')

# Create another container for sleep duration charts
sleep_duration_container = st.container()

# Display the sleep duration charts in the fourth container
with sleep_duration_container:
    # Create two columns
    col8, col9 = st.columns(2)

    # Display the graph for sleep duration per day for each member in the first column
    with col8:
        # Add a text inside a round-edged rectangle
        st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h3>
                    Sleep Duration per Day for Each Member
                </h3>
            </div>
        """, unsafe_allow_html=True)
        # Display the graph for sleep duration per day for each member
        st.plotly_chart(line_chart)

    with col9:
         # Add a text inside a round-edged rectangle
        st.markdown("""
            <div style='
                text-align: center;
                color: #004080;
                background-color: #CE93D8;
                padding: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                '>
                <h3>
                    Average Sleep Duration per Day Across Members
                </h3>
            </div>
        """, unsafe_allow_html=True)
        # Display the graph for average sleep duration
        st.plotly_chart(average_line_chart)

