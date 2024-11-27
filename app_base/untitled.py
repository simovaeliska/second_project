import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Function to display the extracted information
def process_file(uploaded_file):
    # Read the file into a DataFrame
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.txt'):
        df = pd.read_csv(uploaded_file, delimiter='\t')  # Assuming tab-delimited .txt files
    else:
        st.error("Please upload a CSV or TXT file.")
        return

    # Convert date_time to datetime format
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')  # Coerce invalid formats to NaT

    # Extract column names and number of rows and columns
    column_names = df.columns.tolist()
    num_columns = df.shape[1]
    num_rows = df.shape[0]

    # Display basic file info
    st.subheader("File Information:")
    st.write(f"Number of Columns: {num_columns}")
    st.write(f"Number of Rows: {num_rows}")
    st.write(f"Column Names: {column_names}")
    
    # Optionally display the first few rows of the dataset
    st.subheader("Preview of the File:")
    st.write(df.head())

    # Process additional analysis
    if st.button("Show Unique Values in Categorical Columns"):
        show_unique_values_in_categorical_columns(df)

    if st.button("Show Basic Statistics"):
        show_basic_statistics(df)

    if st.button("Show Demographics Analysis"):
        show_demographics_analysis(df)

    if st.button("Show Tenure Analysis by Age and Gender"):
        show_tenure_plot(df)

    if st.button("Show Latest Starts Filtered"):
        show_latest_starts(df)

    if st.button("Calculate Completion Time and Filter Outliers"):
        calculate_and_display_completion_time(df)

    if st.button("Calculate Process Duration"):
        calculate_and_display_process_duration(df)

    if st.button("Calculate Process Duration Without Outliers"):
        calculate_process_duration_without_outliers(df)

    if st.button("Calculate Within-Visit Completion Rate"):
        calculate_within_visit_completion_rate(df)

    if st.button("Calculate Error Rate"):
        calculate_and_display_error_rate(df)

    if st.button("Calculate Bounce Rate"):
        calculate_and_display_bounce_rate(df)

# Function to calculate the drop-off (bounce) rate
def calculate_dropoff_rate(group):
    steps = ['start', 'step_1', 'step_2', 'step_3', 'confirm']
    dropoff_rates = {}  # To store the drop-off percentages at each step
    
    # Count the drop-offs at each step
    for i in range(len(steps) - 1):
        current_step = steps[i]
        next_step = steps[i + 1]
        # Find the total number of clients who started at current_step
        started = group[group['process_step'] == current_step]['client_id'].nunique()
        # Find the number of clients who reached the next step
        reached_next = group[group['process_step'] == next_step]['client_id'].nunique()
        # Calculate the drop-off rate as a percentage
        if started > 0:
            dropoff_rate = ((started - reached_next) / started) * 100
        else:
            dropoff_rate = 0
        
        dropoff_rates[current_step] = dropoff_rate
    
    return dropoff_rates

# Function to calculate and display the bounce rates
def calculate_and_display_bounce_rate(df):
    # Filter the control and test groups
    control_group_sorted = df[df['variation'] == 'Control']
    test_group_sorted = df[df['variation'] == 'Test']

    # Calculate drop-off rates for both groups
    control_dropoff_rate = calculate_dropoff_rate(control_group_sorted)
    test_dropoff_rate = calculate_dropoff_rate(test_group_sorted)

    # Display the drop-off rates for control group
    st.subheader("Control Group Bounce Rates (%):")
    for step, rate in control_dropoff_rate.items():
        st.write(f"{step}: {rate:.2f}%")
    
    # Display the drop-off rates for test group
    st.subheader("Test Group Bounce Rates (%):")
    for step, rate in test_dropoff_rate.items():
        st.write(f"{step}: {rate:.2f}%")

# Function to show unique values in categorical columns
def show_unique_values_in_categorical_columns(df):
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not categorical_columns:
        st.warning("No categorical columns found in the file.")
        return

    st.subheader("Unique Values in Categorical Columns:")
    for col in categorical_columns:
        unique_values = df[col].unique()
        st.write(f"Column: {col}")
        st.write(f"Unique Values: {unique_values}")
        st.write("------")

# Function to show basic statistics of numeric columns
def show_basic_statistics(df):
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.empty:
        st.warning("No numeric columns found in the file.")
        return
    
    st.subheader("Basic Statistics for Numeric Columns:")
    statistics = numeric_df.describe().T  # Transpose for better readability
    st.write(statistics)

# Function to show demographics analysis
def show_demographics_analysis(df):
    if 'gender' in df.columns:
        st.subheader("Gender Distribution:")
        gender_counts = df['gender'].value_counts()
        st.write(gender_counts)

    age_column = 'clnt_age' if 'clnt_age' in df.columns else 'age'
    
    if age_column in df.columns:
        st.subheader("Age Distribution:")
        bins = [0, 30, 40, 50, 100]
        labels = ['Under 30', '30-39', '40-49', '50 and above']
        df['age_group'] = pd.cut(df[age_column], bins=bins, labels=labels)

        age_group_counts = df['age_group'].value_counts()
        st.write(age_group_counts)

        st.subheader("Basic Statistics for Age:")
        age_stats = df[age_column].describe()
        st.write(age_stats)
    else:
        st.warning("No 'age' or 'clnt_age' column found in the file.")

# Function to show the plot for tenure analysis by age and gender
def show_tenure_plot(df):
    if 'clnt_tenure_yr' not in df.columns or 'age_group' not in df.columns or 'gender' not in df.columns:
        st.warning("The dataset is missing necessary columns for the tenure analysis (clnt_tenure_yr, age_group, gender).")
        return

    grouped = df.groupby(['age_group', 'gender'], as_index=False).agg({'clnt_tenure_yr': 'mean'})

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=grouped, x='age_group', y='clnt_tenure_yr', hue='gender')
    plt.title('Average Tenure by Age and Gender')
    plt.xlabel('Age group')
    plt.ylabel('Average tenure in years')
    plt.legend(title='Gender')
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)

# Function to filter the latest "start" process step
def show_latest_starts(df):
    starts_only = df[df['process_step'] == 'start']
    latest_starts = starts_only.loc[starts_only.groupby('client_id')['date_time'].idxmax()]

    confirmation_only = df[df['process_step'] == 'confirm']
    latest_confirms = confirmation_only.loc[confirmation_only.groupby('client_id')['date_time'].idxmax()]

    latest_start_confirms = pd.merge(latest_starts, latest_confirms, on='client_id', suffixes=('_start', '_confirm'))

    latest_start_confirms['process_duration'] = latest_start_confirms['date_time_confirm'] - latest_start_confirms['date_time_start']

    st.subheader("Process Duration Analysis:")
    avg_duration = latest_start_confirms['process_duration'].mean()
    mode_duration = latest_start_confirms['process_duration'].mode()[0]
    median_duration = latest_start_confirms['process_duration'].median()

    st.write(f"Average Duration: {avg_duration}")
    st.write(f"Mode Duration: {mode_duration}")
    st.write(f"Median Duration: {median_duration}")

# Function to calculate and display completion time for each step
def calculate_and_display_completion_time(df):
    control_group = df[df['variation'] == 'Control']
    control_group = control_group.sort_values(by=['client_id', 'date_time'])

    control_group['next_step_time'] = control_group.groupby('client_id')['date_time'].shift(-1)
    control_group = control_group.dropna(subset=['next_step_time'])
    control_group['completion_time'] = control_group['next_step_time'] - control_group['date_time']

    control_group['completion_time_minutes'] = control_group['completion_time'].dt.total_seconds() / 60

    st.write("Average Completion Time by Process Step (Control Group):")
    avg_completion_time = control_group.groupby('process_step')['completion_time_minutes'].mean().reset_index()
    st.write(avg_completion_time)

# Start the Streamlit app
st.title("Data Analysis and Visualization App")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV or TXT file", type=["csv", "txt"])

# Process the file if uploaded
if uploaded_file is not None:
    process_file(uploaded_file)
else:
    st.info("Please upload a CSV or TXT file to begin analysis.")