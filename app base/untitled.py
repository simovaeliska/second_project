import streamlit as st
import pandas as pd
import numpy as np
from streamlit.web import cli as stcli
from streamlit import runtime
import sys

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

    # Button to show basic statistics for numeric columns
    if st.button("Show Basic Statistics"):
        show_basic_statistics(df)

    # Button to show demographics (gender and age) statistics
    if st.button("Show Demographics Analysis"):
        show_demographics_analysis(df)
    
    # Button to show unique values in categorical columns
    if st.button("Show Unique Values in Categorical Columns"):
        show_unique_values_in_categorical_columns(df)

# Function to show basic statistics of numeric columns
def show_basic_statistics(df):
    # Filter only numeric columns for statistics
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.empty:
        st.warning("No numeric columns found in the file.")
        return
    
    # Display the basic statistics using pandas describe()
    st.subheader("Basic Statistics for Numeric Columns:")
    statistics = numeric_df.describe().T  # Transpose for better readability
    st.write(statistics)

# Function to show demographics analysis
def show_demographics_analysis(df):
    # Analyzing Gender distribution
    if 'gender' in df.columns:
        st.subheader("Gender Distribution:")
        gender_counts = df['gender'].value_counts()
        st.write(gender_counts)

        # Basic statistics for gender (if any numeric data exists in these groups)
        if df['gender'].nunique() > 1:
            st.write("Gender distribution is based on counts.")
    else:
        st.warning("No 'gender' column found in the file.")

    # Analyzing Age Group distribution (assuming the presence of 'age' or 'clnt_age' column)
    age_column = 'clnt_age' if 'clnt_age' in df.columns else 'age'  # Default to 'clnt_age' or 'age'
    if age_column in df.columns:
        st.subheader("Age Distribution:")
        # Bin the age into groups for analysis
        bins = [0, 30, 40, 50, 100]  # Age bins
        labels = ['Under 30', '30-39', '40-49', '50 and above']  # Age group labels
        df['age_group'] = pd.cut(df[age_column], bins=bins, labels=labels)

        # Display count of each age group
        age_group_counts = df['age_group'].value_counts()
        st.write(age_group_counts)

        # Basic statistics for age groups
        st.subheader("Basic Statistics for Age:")
        age_stats = df[age_column].describe()  # Get statistics for age column
        st.write(age_stats)

    else:
        st.warning("No 'age' or 'clnt_age' column found in the file.")

# Function to show unique values in categorical columns
def show_unique_values_in_categorical_columns(df):
    # Select categorical columns
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not categorical_columns:
        st.warning("No categorical columns found in the file.")
        return

    # Display unique values for each categorical column
    st.subheader("Unique Values in Categorical Columns:")
    for col in categorical_columns:
        unique_values = df[col].unique()
        st.write(f"Column: {col}")
        st.write(f"Unique Values: {unique_values}")
        st.write("------")

# App title
st.title("File Column Extractor and Viewer")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV or TXT file", type=["csv", "txt"])

# Process the file if uploaded
if uploaded_file is not None:
    process_file(uploaded_file)
else:
    st.info("Please upload a CSV or TXT file to extract column names, file information, basic statistics, demographics analysis, and unique values analysis.")
