import streamlit as st
import pandas as pd
import numpy as np
from streamlit.web import cli as stcli
from streamlit import runtime
import sys

# Function to calculate visit time differences (refactor from the previous code)
def calculate_completion_time_by_visit(group_df):
    group_df['next_step_time'] = group_df.groupby('client_id')['date_time'].shift(-1)
    group_df = group_df.dropna(subset=['next_step_time'])
    group_df['visit_time_diff'] = group_df['next_step_time'] - group_df['date_time']
    return group_df[['client_id', 'age_group', 'process_step', 'date_time', 'next_step_time', 'visit_time_diff']]

# Title of the app
st.title('Client Visit Time Analysis')

# Upload CSV File
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read uploaded CSV file into a DataFrame
    df_merged = pd.read_csv(uploaded_file)

    # Display the first few rows of the uploaded dataset
    st.subheader('Preview of the uploaded data:')
    st.write(df_merged.head())

    # Convert date_time column to datetime if it's not already
    df_merged['date_time'] = pd.to_datetime(df_merged['date_time'], errors='coerce')

    # Define age bins and labels
    bins = [0, 30, 40, 50, 100]
    labels = ['Under 30', '30-39', '40-49', '50 and above']

    # Categorize ages into the defined bins and add a new 'age_group' column
    df_merged['age_group'] = pd.cut(df_merged['clnt_age'], bins=bins, labels=labels)

    # Filter for the test group only
    test_group = df_merged[df_merged['variation'] == 'Test']

    # Sort by client_id and date_time to ensure chronological order of visits
    test_group = test_group.sort_values(by=['client_id', 'date_time'])

    # Apply the function to calculate visit time differences for the test group
    test_group_visit_times = calculate_completion_time_by_visit(test_group)

    # Display the result in the app
    st.subheader('Visit Time Differences for Test Group:')
    st.write(test_group_visit_times)

    # Optionally save the result to a CSV file
    st.download_button(
        label="Download visit times data",
        data=test_group_visit_times.to_csv(index=False),
        file_name="test_group_visit_times.csv",
        mime="text/csv"
    )

else:
    st.info('Please upload a CSV file to start the analysis.')