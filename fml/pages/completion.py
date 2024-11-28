#pages/completion.py
import streamlit as st
import pandas as pd

def show_completion_time(df):
    st.title("Completion Time Analysis")
    
    # Ensure 'date_time' column is in datetime format
    if 'date_time' not in df.columns:
        st.error("Missing 'date_time' column in the dataset.")
        return
    
    # Coerce errors to NaT (Not a Time)
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')  
    df = df.dropna(subset=['date_time'])

    # Sort the dataset by 'client_id', 'visit_id', and 'date_time' to ensure chronological order
    df = df.sort_values(by=['client_id', 'visit_id', 'date_time'])
    
    # Split into control and test groups
    control_group = df[df['variation'] == 'Control']
    test_group = df[df['variation'] == 'Test']
    
    def calculate_completion_time_with_visits(group_df):
        group_df = group_df.sort_values(by=['client_id', 'visit_id', 'date_time'])
        group_df['next_step_time'] = group_df.groupby(['client_id', 'visit_id'])['date_time'].shift(-1)
        group_df = group_df.dropna(subset=['next_step_time'])
        group_df['completion_time'] = group_df['next_step_time'] - group_df['date_time']
        return group_df[['client_id', 'visit_id', 'process_step', 'date_time', 'next_step_time', 'completion_time']]

    def filter_outliers(group_df):
        group_df['completion_time_minutes'] = group_df['completion_time'].dt.total_seconds() / 60
        Q1 = group_df['completion_time_minutes'].quantile(0.25)
        Q3 = group_df['completion_time_minutes'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return group_df[
            (group_df['completion_time_minutes'] >= lower_bound) &
            (group_df['completion_time_minutes'] <= upper_bound)
        ]

    control_group_completion_times = calculate_completion_time_with_visits(control_group)
    test_group_completion_times = calculate_completion_time_with_visits(test_group)
    
    control_group_filtered = filter_outliers(control_group_completion_times)
    test_group_filtered = filter_outliers(test_group_completion_times)
    
    avg_completion_time_control = control_group_filtered.groupby('process_step')['completion_time_minutes'].mean().reset_index()
    avg_completion_time_test = test_group_filtered.groupby('process_step')['completion_time_minutes'].mean().reset_index()
    
    st.subheader("Average Completion Time for Control Group (Minutes) - After Outlier Removal")
    st.dataframe(avg_completion_time_control)

    st.subheader("Average Completion Time for Test Group (Minutes) - After Outlier Removal")
    st.dataframe(avg_completion_time_test)
    
    st.subheader("Comparison of Average Completion Time by Process Step")
    comparison_df = pd.merge(avg_completion_time_control, avg_completion_time_test, on='process_step', suffixes=('_control', '_test'))
    st.dataframe(comparison_df)

    # Optional visualization
    # st.bar_chart(comparison_df.set_index('process_step')[['completion_time_minutes_control', 'completion_time_minutes_test']])

    st.subheader("Insights & Interpretation")
    st.write("""
    In this section, we derive insights based on the completion times between the Control and Test groups.
    """)