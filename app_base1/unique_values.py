import streamlit as st

def show_unique_values_in_categorical_columns(df):
    st.title("Unique Values in Categorical Columns")
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not categorical_columns:
        st.warning("No categorical columns found in the file.")
        return

    st.subheader("Unique Values in Categorical Columns:")
    for column in categorical_columns:
        unique_values = df[column].unique()
        st.write(f"Column: {column}")
        st.write(f"Unique values: {unique_values}")