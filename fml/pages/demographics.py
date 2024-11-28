# pages/demographics.py
import pandas as pd
import plotly.express as px
import streamlit as st

# Function to perform demographic analysis
def analyze_demographics(df):
    """
    Function to perform demographic analysis and generate interactive plots using Plotly.
    """
    # Ensure 'clnt_age' is present and numeric
    if 'clnt_age' not in df.columns:
        st.error("The DataFrame does not contain the 'clnt_age' column.")
        return

    if not pd.api.types.is_numeric_dtype(df['clnt_age']):
        st.error("The 'clnt_age' column is not numeric.")
        return

    # Create the 'age_group' column based on 'clnt_age' ranges
    bins = [0, 18, 30, 40, 50, 60, 100]  # Define the age group ranges
    labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '60+']  # Age group labels
    df['age_group'] = pd.cut(df['clnt_age'], bins=bins, labels=labels, right=False)

    # Debugging: Show first few rows of the dataframe to confirm 'age_group' column
    st.write("First few rows of the dataframe with 'age_group':")
    st.write(df[['clnt_age', 'age_group']].head())

    # Check if 'age_group' column exists now
    if 'age_group' not in df.columns:
        st.error("The 'age_group' column was not created.")
        return

    # Aggregating based on 'gender' and 'age_group'
    logs_calls_accounts = df.groupby(['gender', 'age_group']).agg({
        'num_accts': 'mean',
        'calls_6_mnth': 'mean',
        'logons_6_mnth': 'mean'
    }).reset_index().round(2)

    # Debugging: Show the aggregated result
    st.write("Aggregated data (grouped by 'gender' and 'age_group'):")
    st.write(logs_calls_accounts)

    # Plot for Average Number of Accounts
    fig1 = px.line(
        logs_calls_accounts, 
        x='age_group', 
        y='num_accts', 
        color='gender',
        title="Average Number of Accounts by Age Group and Gender",
        labels={'num_accts': 'Average Number of Accounts'},
        markers=True
    )
    st.plotly_chart(fig1)

    # Plot for Calls in the Last 6 Months
    fig2 = px.line(
        logs_calls_accounts, 
        x='age_group', 
        y='calls_6_mnth', 
        color='gender',
        title="Average Calls in Last 6 Months by Age Group and Gender",
        labels={'calls_6_mnth': 'Average Calls in Last 6 Months'},
        line_shape='linear',
        markers=True
    )
    st.plotly_chart(fig2)

    # Plot for Logons in the Last 6 Months
    fig3 = px.line(
        logs_calls_accounts, 
        x='age_group', 
        y='logons_6_mnth', 
        color='gender',
        title="Average Logons in Last 6 Months by Age Group and Gender",
        labels={'logons_6_mnth': 'Average Logons in Last 6 Months'},
        line_shape='linear',
        markers=True
    )
    st.plotly_chart(fig3)

# Function to display the demographics analysis in Streamlit
def show_demographics(df):
    """
    Show Demographics Analysis in the Streamlit app.
    This function is used to call the analysis and display the results.
    """
    st.title("Demographics Analysis")

    # Perform the demographic analysis (aggregation and plotting)
    analyze_demographics(df)

    # Add some explanation or results display here
    st.write("Demographics analysis will be displayed here, including charts and tables.")