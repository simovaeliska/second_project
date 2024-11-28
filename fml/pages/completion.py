#pages/completion.py
import streamlit as st
import pandas as pd  # Ensure pandas is imported

def show_completion_time(df):
    st.title("Completion Time Analysis")
    
    # Ensure the 'date_time' column is in datetime format
    if 'date_time' not in df.columns:
        st.error("Missing 'date_time' column in the dataset.")
        return
    
    # Coerce errors to NaT (Not a Time)
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')  

    # Drop rows where 'date_time' is NaT after coercion
    df = df.dropna(subset=['date_time'])

    # Calculate the completion time for each process step
    df['next_step_time'] = df.groupby('client_id')['date_time'].shift(-1)
    
    # Ensure 'next_step_time' is not NaT before computing completion time
    df = df.dropna(subset=['next_step_time'])

    df['completion_time'] = df['next_step_time'] - df['date_time']
    
    # Display average completion time per process step
    st.subheader("Average Completion Time Per Process Step")
    st.write(df.groupby('process_step')['completion_time'].mean())

    # Now, calculate completion rate for within-visit and client-based analysis
    st.subheader("Completion Rate by Visit")
    control_group = df[df['variation'] == 'Control']
    test_group = df[df['variation'] == 'Test']
    
    # Completion rate based on visit_id
    def calculate_within_visit_completion_rate(group):
        # Total unique visits that started
        started_visits = group[group['process_step'] == 'start']['visit_id'].nunique()

        # Unique visits that completed each step
        completed_visits = (
            group[group['process_step'] != 'start']
            .groupby('process_step')['visit_id']
            .nunique()
            .reset_index(name='completed_visits')
        )

        # Add the total started visits as a constant column
        completed_visits['started_visits'] = started_visits

        # Calculate the completion rate
        completed_visits['completion_rate'] = (
            completed_visits['completed_visits'] / completed_visits['started_visits']
        ) * 100

        return completed_visits

    # Calculate completion rates for the control and test groups
    control_completion_rate = calculate_within_visit_completion_rate(control_group)
    test_completion_rate = calculate_within_visit_completion_rate(test_group)

    # Display completion rates for control and test groups
    st.write("Control Group Completion Rate by Visit:")
    st.dataframe(control_completion_rate)

    st.write("Test Group Completion Rate by Visit:")
    st.dataframe(test_completion_rate)

    # Completion rate based on client_id
    def calculate_within_visit_completion_rate_by_client(group):
        # Total unique visits that started
        started_visits = group[group['process_step'] == 'start']['client_id'].nunique()

        # Unique visits that completed each step
        completed_visits = (
            group[group['process_step'] != 'start']
            .groupby('process_step')['client_id']
            .nunique()
            .reset_index(name='completed_visits')
        )

        # Add the total started visits as a constant column
        completed_visits['started_visits'] = started_visits

        # Calculate the completion rate
        completed_visits['completion_rate'] = (
            completed_visits['completed_visits'] / completed_visits['started_visits']
        ) * 100

        return completed_visits

    # Calculate completion rates for the control and test groups based on client_id
    control_completion_rate_id = calculate_within_visit_completion_rate_by_client(control_group)
    test_completion_rate_id = calculate_within_visit_completion_rate_by_client(test_group)

    # Display completion rates for control and test groups based on client_id
    st.write("Control Group Completion Rate by Client:")
    st.dataframe(control_completion_rate_id)

    st.write("Test Group Completion Rate by Client:")
    st.dataframe(test_completion_rate_id)

    # Completion rate by age group
    def calculate_within_visit_completion_rate_by_age(group):
        # Total unique visits that started
        started_visits = group[group['process_step'] == 'start']['client_id'].nunique()

        # Unique visits that completed each step, grouped by age_group
        completed_visits = (
            group[group['process_step'] != 'start']
            .groupby(['process_step', 'age_group'])['client_id']
            .nunique()
            .reset_index(name='completed_visits')
        )

        # Add the total started visits as a constant column
        completed_visits['started_visits'] = started_visits

        # Calculate the completion rate
        completed_visits['completion_rate'] = (
            completed_visits['completed_visits'] / completed_visits['started_visits']
        ) * 100

        return completed_visits

    # Calculate completion rates for the control and test groups based on age group
    control_completion_rate_by_age = calculate_within_visit_completion_rate_by_age(control_group)
    test_completion_rate_by_age = calculate_within_visit_completion_rate_by_age(test_group)

    # Display completion rates by age group
    st.write("Control Group Completion Rate by Age:")
    st.dataframe(control_completion_rate_by_age)

    st.write("Test Group Completion Rate by Age:")
    st.dataframe(test_completion_rate_by_age)