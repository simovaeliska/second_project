import streamlit as st
import pandas as pd
from file_info import show_file_info
from unique_values import show_unique_values_in_categorical_columns
from basic_statistics import show_basic_statistics
from demographics import show_demographics_analysis
from hypothesis_testing import show_hypothesis_testing_page

# Set up Streamlit app layout
st.set_page_config(page_title="A/B Test Demo for Group 7")

# Initialize session state to manage pages
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'df' not in st.session_state:
    st.session_state.df = None

# Navigation buttons function
def navigation_buttons():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("Home"):
            st.session_state.page = 'home'
    
    with col2:
        if st.button("File Info"):
            st.session_state.page = 'file_info'
    
    with col3:
        if st.button("Unique Values"):
            st.session_state.page = 'unique_values'
    
    with col4:
        if st.button("Basic Statistics"):
            st.session_state.page = 'basic_statistics'
    
    with col5:
        if st.button("Demographics"):
            st.session_state.page = 'demographics'
    
    with col6:
        if st.button("Hypothesis Testing"):
            st.session_state.page = 'hypothesis_testing'

# Home page: File Upload and Project Presentation
def show_home_page():
    st.title("Welcome to A/B Test Demo for Group 7")
    
    # Add project presentation text
    st.subheader("The Digital Challenge")
    st.write("""
        The digital world is evolving, and so are Vanguard’s clients. Vanguard believed that a more intuitive and modern User Interface (UI), 
        coupled with timely in-context prompts (cues, messages, hints, or instructions provided to users directly within the context of their 
        current task or action), could make the online process smoother for clients. The critical question was: 
        Would these changes encourage more clients to complete the process?
    """)
    
    # File upload section
    st.write("Please upload your file to start")
    uploaded_file = st.file_uploader("Upload your file (CSV or TXT)", type=['csv', 'txt'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df  # Store the dataframe in session state
        navigation_buttons()  # Display navigation buttons
        show_file_info(df)

# File Info Page
def show_file_info_page(df):
    navigation_buttons()  # Display navigation buttons
    show_file_info(df)

# Unique Values Page
def show_unique_values_page(df):
    navigation_buttons()  # Display navigation buttons
    show_unique_values_in_categorical_columns(df)

# Basic Statistics Page
def show_basic_statistics_page(df):
    navigation_buttons()  # Display navigation buttons
    show_basic_statistics(df)

# Demographics Analysis Page
def show_demographics_page(df):
    navigation_buttons()  # Display navigation buttons
    show_demographics_analysis(df)

# Hypothesis Testing Page
def show_hypothesis_testing_page_function(df):
    navigation_buttons()  # Display navigation buttons
    show_hypothesis_testing_page(df)

# Main app logic to render the selected page
if st.session_state.page == 'home':
    show_home_page()

elif st.session_state.page == 'file_info':
    if st.session_state.df is not None:
        show_file_info_page(st.session_state.df)
    else:
        st.warning("Please upload a file to proceed.")

elif st.session_state.page == 'unique_values':
    if st.session_state.df is not None:
        show_unique_values_page(st.session_state.df)
    else:
        st.warning("Please upload a file to proceed.")

elif st.session_state.page == 'basic_statistics':
    if st.session_state.df is not None:
        show_basic_statistics_page(st.session_state.df)
    else:
        st.warning("Please upload a file to proceed.")

elif st.session_state.page == 'demographics':
    if st.session_state.df is not None:
        show_demographics_page(st.session_state.df)
    else:
        st.warning("Please upload a file to proceed.")

elif st.session_state.page == 'hypothesis_testing':
    if st.session_state.df is not None:
        show_hypothesis_testing_page_function(st.session_state.df)
    else:
        st.warning("Please upload a file to proceed.")