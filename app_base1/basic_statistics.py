import streamlit as st

def show_basic_statistics(df):
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.empty:
        st.warning("No numeric columns found in the file.")
        return
    
    st.subheader("Basic Statistics for Numeric Columns:")
    statistics = numeric_df.describe().T  # Transpose for better readability
    st.write(statistics)