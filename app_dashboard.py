import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objs as go
import math

st.set_page_config(layout="centered", initial_sidebar_state="expanded")

# Load the dataset
df = pd.read_csv('group.csv')


# Import custom CSS file
st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)

#SIDEBAR

st.sidebar.header("Activity Log")

# Create sidebar with buttons to show specific plots
option = st.sidebar.selectbox('Select a plot', ('Introduction','Amount of Sleep Per Day', 'Location of Time Spent', 'Time Spent per Activity Type', 'Average Time Spent on Commute per Day', 'Number of Times That I Eat per Day', 'Number of Times That I Eat Each Type of Meal', 'Trend of High Productivity Instances Over Time (School Related Work)', 'Distribution of my Feelings over the Past 2 Weeks'))

st.sidebar.markdown('''
---
Created by Bianca Jessa A. Carabio BSIT - G1
''')

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Convert 'Duration' column to timedelta format
df['Duration'] = pd.to_timedelta(df['Duration'])

if option == 'Introduction':
    # Add markdown to explain the dashboard
    # Add markdown to explain the dashboard
    st.markdown('# About the Dashboard\nHello! I am Bianca Jessa A. Carabio. This is a dashboard powered by Streamlit and Plotly showing graphs created from my 2 week activity log. Here is a peek into my dataset.')

    # Create a table trace
    table_trace = go.Table(
        header=dict(values=list(df.columns),
                fill_color='#004D40',  # Change to a darker shade of paleturquoise
                align='left'),
        cells=dict(values=[df[col] for col in df.columns],
               fill_color='#009688',  # Change to a darker shade of lavender
               align='left'))

    # Create a Plotly figure and add the table trace
    fig = go.Figure(data=[table_trace])

    # Show the Plotly figure
    st.plotly_chart(fig)

else:
    if option == 'Amount of Sleep Per Day':
        # Filter out rows where 'Activity' is not 'Sleep'
        sleep_df = df[df['Activity'] == 'Sleep']

        # Group by 'Date' and sum 'Duration'
        sleep_per_day = sleep_df.groupby('Date')['Duration'].sum()

        # Reset index to make 'Date' a column again
        sleep_per_day = sleep_per_day.reset_index()

        # Convert 'Duration' to hours for easier interpretation
        sleep_per_day['Duration'] = sleep_per_day['Duration'].dt.total_seconds() / 3600

        # Calculate average amount of sleep
        average_sleep = sleep_per_day['Duration'].mean()

        # Add markdown to explain the plot
        st.markdown(f"### Amount of Sleep Per Day for 2 Weeks\n\nThis plot shows the amount of sleep I had per day for the past 2 weeks.\n\n")

        # Plot line chart
        fig2 = px.line(sleep_per_day, x='Date', y='Duration', title='Amount of Sleep Per Day for 2 Weeks')
        fig2.update_layout(xaxis_title='Date', yaxis_title='Sleep in Hours', xaxis=dict(dtick='D1', tickformat='%b %d'))
        st.plotly_chart(fig2)

        # Add markdown to explain the plot
        st.markdown(f"### Sleep Start Times\n\nThis plot shows the time I went to sleep every day for the past 2 weeks.\n\n")

        # Filter out rows where 'Activity' is not 'Sleep'
        sleep_start_df = sleep_df[['Date', 'Time']]

        # Add dummy date to 'Time' column
        sleep_start_df['Time'] = '2022-01-01 ' + sleep_start_df['Time']

        # Convert 'Time' to datetime format
        sleep_start_df['Time'] = pd.to_datetime(sleep_start_df['Time'])

        # Extract hour and minute from 'Time'
        sleep_start_df['Hour'] = sleep_start_df['Time'].dt.hour
        sleep_start_df['Minute'] = sleep_start_df['Time'].dt.minute

        # Combine 'Hour' and 'Minute' into 'Time' column
        sleep_start_df['Time'] = sleep_start_df['Time'].dt.strftime('%I:%M %p')

        # Plot line chart
        fig14 = px.line(sleep_start_df, x='Date', y='Time', title='Sleep Start Times')
        fig14.update_layout(xaxis_title='Date', yaxis_title='Time', xaxis=dict(dtick='D1', tickformat='%b %d'))
        st.plotly_chart(fig14)

                # Calculate average sleep start time
        average_sleep_start = sleep_start_df['Time'].mode()[0]

        # Add metric to show the average amount of sleep and average sleep start time
        st.markdown(f'<div class="metric-container"><div class="metric"><div class="metric-item">Average Sleep: {average_sleep:.2f} hours</div><div class="metric-item">Average Sleep Start Time: {average_sleep_start}</div></div></div>', unsafe_allow_html=True)

    elif option == 'Location of Time Spent':
        # Group by 'Location' and sum 'Duration'
        time_spent = df.groupby('Location')['Duration'].sum()

        # Reset index to make 'Location' a column again
        time_spent = time_spent.reset_index()

        # Convert 'Duration' to hours for easier interpretation
        time_spent['Duration'] = time_spent['Duration'].dt.total_seconds() / 3600

        # Add markdown to explain the plot
        st.markdown(f"### Where I spent my time\n\nThis plot shows where I spent my time from the past 2 weeks.\n\n")

        # Plot pie chart
        fig3 = px.pie(time_spent, values='Duration', names='Location', title='Location of Time Spent')
        st.plotly_chart(fig3)

        # Add metrics for total duration by location
        st.markdown('### Total Duration by Location')
        st.write('---')
        col1, col2, col3 = st.columns(3)
        col1.markdown(f'<div class="metric">Home<br>{time_spent.loc[time_spent["Location"] == "Home", "Duration"].iloc[0]:.2f} hours</div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="metric">School<br>{time_spent.loc[time_spent["Location"] == "School", "Duration"].iloc[0]:.2f} hours</div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="metric">Others<br>{time_spent.loc[time_spent["Location"] == "Others", "Duration"].iloc[0]:.2f} hours</div>', unsafe_allow_html=True)

        
    elif option == 'Time Spent per Activity Type':
        # Group by 'Activity Type' and sum 'Duration'
        activity_type_df = df.groupby('Activity Type')['Duration'].sum()

        # Reset index to make 'Activity Type' a column again
        activity_type_df = activity_type_df.reset_index()

        # Convert 'Duration' to hours for easier interpretation
        activity_type_df['Duration'] = activity_type_df['Duration'].dt.total_seconds() / 3600

        # Add markdown to explain the plot
        st.markdown(f"### Distribution of my time based on my Activities\n\nThis plot shows the time i spent on my activities for the past 2 weeks.\n\n")

        # Plot pie chart
        fig4 = px.pie(activity_type_df, values='Duration', names='Activity Type', title='Time Spent per Activity Type')
        st.plotly_chart(fig4)
 
        # Add metrics for total duration by activity type
        st.markdown('### Top 3 Activities')
        st.write('---')
        top_activities = ['Sleep', 'School', 'Self-Care']
        col1, col2, col3 = st.columns(3)
        for i, activity in enumerate(top_activities):
            duration = activity_type_df.loc[activity_type_df['Activity Type'] == activity, 'Duration'].iloc[0]
            col = col1 if i == 0 else col2 if i == 1 else col3
            col.markdown(f'<div class="metric">{activity}<br>{duration:.2f} hours</div>', unsafe_allow_html=True)

    elif option == 'Average Time Spent on Commute per Day':
        # Filter out rows where 'Activity' is not 'Commute'
        commute_df = df[df['Activity'] == 'Commute']

        # Group by 'Date' and sum 'Duration'
        commute_per_day = commute_df.groupby('Date')['Duration'].sum()

        # Reset index to make 'Date' a column again
        commute_per_day = commute_per_day.reset_index()

        # Convert 'Duration' to hours for easier interpretation
        commute_per_day['Duration'] = commute_per_day['Duration'].dt.total_seconds() / 3600

        # Calculate average commute time
        average_commute = commute_per_day['Duration'].mean()

        # Add markdown to explain the plot
        st.markdown(f"### How much time I spend commuting per day\n\nThis plot shows the amount of time I spend on my daily commutes.\n\n")

        # Plot bar chart
        fig5 = px.bar(commute_per_day, x='Date', y='Duration', title='Time Spent on Commute per Day')
        fig5.update_layout(xaxis_title='Date', yaxis_title='Time in Hours', xaxis=dict(dtick='D1', tickformat='%b %d'))
        st.plotly_chart(fig5)

        # Add metric for average commute time
        st.markdown(f'<div class="metric">Average Commute Time Per Day<br>{average_commute:.2f} hours</div>', unsafe_allow_html=True)

    elif option == 'Number of Times That I Eat per Day':
        # Filter out rows where 'Activity' does not contain 'Eat'
        if df["Activity"].isna().any():
            eat_df = df.dropna(subset=["Activity"])
        else:
            eat_df = df.copy()

        eat_df = eat_df[eat_df["Activity"].str.contains("Eat")]

        # Count the number of times you eat each day
        eat_per_day = eat_df.groupby('Date').size()

        # Reset index to make 'Date' a column again
        eat_per_day = eat_per_day.reset_index()

        # Rename the count column to 'Times'
        eat_per_day.columns = ['Date', 'Times']

        # Add markdown to explain the plot
        st.markdown(f"### How many times I eat in a day\n\nThis plot shows the amount of times that I eat in a day. The reason I included this plot is because I have noticed that for this semester, I have been eating less than normal and I wanted to check if it was actually true.\n\n")

        # Plot bar chart
        fig6 = px.bar(eat_per_day, x='Date', y='Times', title='Number of Times That I Eat per Day')
        fig6.update_layout(xaxis_title='Date', yaxis_title='Count', xaxis=dict(dtick='D1', tickformat='%b %d'))
        st.plotly_chart(fig6)

        # Add metric for average number of times you eat in a day
        st.markdown(f'<div class="metric">Average Time that I Eat per Day: {eat_per_day["Times"].mean():.2f}</div>', unsafe_allow_html=True)

        # Add markdown to explain the plot
        st.markdown(f"After seeing the results of this plot, I can definitely say to myself that I need to eat more frequently. Preferably actually 3 times a day\n\n")

    elif option == 'Number of Times That I Eat Each Type of Meal':
        # Filter out rows where 'Activity' does not contain 'Eat'
        eat_df = df.dropna(subset=["Activity"])
        eat_df = eat_df[eat_df["Activity"].str.contains("Eat")]

        # Count the number of times you eat each type of meal each day
        meal_counts = eat_df['Activity'].value_counts()

        # Reset index to make 'Activity' a column again
        meal_counts = meal_counts.reset_index()

        # Rename the columns to 'Meal' and 'Count'
        meal_counts.columns = ['Meal', 'Count']

        # Add markdown to explain the plot
        st.markdown(f"### Distribution of Meals that I eat in a day\n\nBased on the previous plot which showed how much I ate in a day, I created this plot to show which type of meal do i eat most.\n\n")
        # Plot pie chart
        fig7 = px.pie(meal_counts, values='Count', names=meal_counts['Meal'].str.replace('Eat ', ''), title='Number of Times That I Eat Each Type of Meal')
        st.plotly_chart(fig7)

        # Add metric for meal that you eat the most
        most_eaten_meal = meal_counts['Meal'].iloc[0].replace('Eat ', '')
        st.markdown(f'<div class="metric">Most Eaten Meal: {most_eaten_meal}</div>', unsafe_allow_html=True)

    elif option == 'Trend of High Productivity Instances Over Time (School Related Work)':
        # Filter out rows where 'Value' is not 'High' and 'Activity Type' is not 'School'
        productive_df = df[(df['Value'] == 'High') & (df['Activity Type'] == 'School')]

        # Count the number of high productivity instances each day
        productive_per_day = productive_df.groupby('Date').size()

        # Reset index to make 'Date' a column again
        productive_per_day = productive_per_day.reset_index()

        # Rename the count column to 'Count'
        productive_per_day.columns = ['Date', 'Count']

        # Add markdown to explain the plot
        st.markdown(f"### Trend of Highly Productive School Related Activities\n\nThis plot shows the trend of school related work I have done daily over the course of the past 2 weeks.\n\n")

        # Plot line chart
        fig11 = px.line(productive_per_day, x='Date', y='Count', title='Trend of High Productivity Instances Over Time (School Related Work)')
        fig11.update_layout(xaxis_title='Date', yaxis_title='Count', xaxis=dict(dtick='D1', tickformat='%b %d'))
        st.plotly_chart(fig11)

        # Add plot for distribution of highly productive school related work activities by time of day
        productive_df['Time'] = pd.to_datetime(productive_df['Time'])
        productive_df['Hour'] = productive_df['Time'].dt.strftime('%I:%M %p')
        productive_by_hour = productive_df.groupby('Hour').size().reset_index(name='Count')
        fig13 = px.line(productive_by_hour, x='Hour', y='Count', title='Distribution of Highly Productive School Related Work Activities by Time of Day')
        fig13.update_layout(xaxis_title='Hour of Day', yaxis_title='Count')
        st.plotly_chart(fig13)

        # Add metric for top 3 times of day spent most productive on
        top_3_times = productive_by_hour.nlargest(3, 'Count')
        st.markdown(f'<div class="metric">Top 3 Times of Day Spent Most Productive On{top_3_times.to_html(index=False)}</div>', unsafe_allow_html=True)

    elif option == 'Distribution of my Feelings over the Past 2 Weeks':
        # Group by 'How I Feel' and count the number of instances of each feeling
        feelings_counts = df.groupby('How I feel').size()

        # Reset index to make 'How I Feel' a column again
        feelings_counts = feelings_counts.reset_index()

        # Rename the count column to 'Count'
        feelings_counts.columns = ['Feeling', 'Count']

        # Sort by 'Count' column in descending order
        feelings_counts = feelings_counts.sort_values(by='Count', ascending=False)

        # Add markdown to explain the plot
        st.markdown(f"### How I've been feeling\n\nThis plot shows the distribution of my feelings over the past 2 weeks.\n\n")

        # Plot histogram
        fig12 = px.histogram(feelings_counts, x='Feeling', y='Count', title='Distribution of my Feelings over the Past 2 Weeks')
        st.plotly_chart(fig12)

        # Add metric for top 3 emotions felt
        top_3_emotions = feelings_counts.nlargest(3, 'Count')
        col1, col2, col3 = st.columns(3)
        for i, emotion in enumerate(top_3_emotions['Feeling']):
            count = top_3_emotions.loc[top_3_emotions['Feeling'] == emotion, 'Count'].iloc[0]
            col = col1 if i == 0 else col2 if i == 1 else col3
            col.markdown(f'<div class="metric">{emotion} <br>{count} times</div>', unsafe_allow_html=True)