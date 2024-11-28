# data_loader.py
# data_loader.py
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    url = r"C:\Users\Cecilia\Downloads\ironhack\coursework\group_work\group_project_week5_6\second_project\data\clean\combined_cleaned_data1.csv"
    try:
        df = pd.read_csv(url)
        return df
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
        return None