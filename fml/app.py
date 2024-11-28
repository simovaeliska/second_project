# app.py
import streamlit as st
from data_loader import load_data  # assuming load_data is in the data_loader.py file
from pages import about, summary, unique_values, stats, demographics, hypothesis, duration, completion

def main():
    """
    Main function to run the Streamlit app for A/B Test Demo.
    
    Sets up the page configuration, loads data, and manages navigation
    through different pages of the app.
    """
    st.set_page_config(page_title="A/B Test Demo for Group 7")
    
    # Load the data here
    df = load_data()

    # If df is None, show an error and don't continue
    if df is None:
        st.error("Data could not be loaded.")
        return

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", [
        "About the Project", 
        "Data Summary", 
        "Unique Values", 
        "Basic Statistics", 
        "Demographics Analysis", 
        "Hypothesis Testing",
        "Process Duration Analysis",  # Make sure the Process Duration Analysis is listed here
        "Completion Time Analysis"
    ])

    # Handle page navigation and pass the df to the page
    if page == "About the Project":
        about.show_about_project()
    elif page == "Data Summary":
        summary.show_data_summary(df)
    elif page == "Unique Values":
        unique_values.show_unique_values_in_categorical_columns(df)
    elif page == "Basic Statistics":
        stats.show_basic_statistics(df)
    elif page == "Demographics Analysis":
        demographics.show_demographics(df)  # This matches the function name in demographics.py
    elif page == "Process Duration Analysis":
        duration.show_process_duration(df)  # Ensure this matches the function name in duration.py
    elif page == "Hypothesis Testing":
        hypothesis.show_hypothesis_testing_page(df)  # Ensure this matches the function name in hypothesis.py
    elif page == "Completion Time Analysis":
        completion.show_completion_time(df)  # Make sure the function matches the one in completion.py


if __name__ == "__main__":
    main()