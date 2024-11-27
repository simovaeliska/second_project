#demographics.py

import pandas as pd
import streamlit as st

def show_demographics_analysis(df):
    # Ensure 'age_column' exists in your DataFrame, for example 'clnt_age'
    age_column = 'clnt_age'  # Adjust to your dataset column name

    # Create age groups for demographics analysis
    bins = [18, 30, 40, 50, 60, 100]  # Adjust the age ranges as needed
    labels = ['18-29', '30-39', '40-49', '50-59', '60+']
    
    # Create a new column 'age_group' in the DataFrame
    df['age_group'] = pd.cut(df[age_column], bins=bins, labels=labels, right=False)

    # Display age group counts
    st.subheader("Demographics: Age Groups")
    st.write(df['age_group'].value_counts())
    
    # Check if 'clnt_gender' and 'clnt_region' columns exist in the DataFrame
    available_columns = df.columns
    st.write(f"Available columns in the dataset: {available_columns}")

    # Display 'clnt_gender' and 'clnt_region' if they exist
    if 'clnt_gender' in available_columns and 'clnt_region' in available_columns:
        st.subheader("Additional Demographics Info")
        st.write(df[['clnt_age', 'clnt_gender', 'clnt_region']].head())  # Modify based on your dataset
    else:
        st.warning("Some demographic columns ('clnt_gender', 'clnt_region') are missing in the dataset.")
        st.write("Displaying available demographic columns:")
        # Modify this part to display any other columns you want to analyze
        st.write(df[['clnt_age']].head())  # Adjust as needed
