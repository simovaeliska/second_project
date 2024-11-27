import streamlit as st

def show_file_info(df):
    st.subheader("File Information:")
    st.write(f"Number of Columns: {df.shape[1]}")
    st.write(f"Number of Rows: {df.shape[0]}")
    st.write(f"Column Names: {df.columns.tolist()}")
    st.subheader("Preview of the File:")
    st.write(df.head())