# data_loader.py
import pandas as pd
import streamlit as st

def load_data(file_path):
    """
    Load data from the provided file path and return the dataframe.
    """
    try:
        # Read the data into a DataFrame
        df = pd.read_csv(r"C:\Users\Cecilia\Downloads\ironhack\coursework\group_work\group_project_week5_6\second_project\data\clean\combined_cleaned_data1.csv")
        return df
    except Exception as e:
        # Handle any errors during data loading
        print(f"Error loading data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error