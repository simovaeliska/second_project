import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set the page title and layout
st.set_page_config(page_title="A/B Test Demo for Group 7")

# Custom CSS for styling (to set the page background color to white and bordeaux headers)
st.markdown("""
    <style>
        /* Set background color for entire page to white */
        body {
            background-color: white;
            color: black;
        }
        /* Set bordeaux color for all headers */
        h1, h2, h3, h4, h5, h6 {
            color: #800000;  /* Bordeaux color */
        }
        /* Ensure text remains black */
        .stText {
            color: black;  /* Ensure black text */
        }
        /* Set a bordeaux background for buttons */
        .stButton {
            color: black;
            background-color: #800000;  /* Bordeaux button */
        }
        .stMarkdown {
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# Title and header for the app
st.title("A/B Test Demo for Group 7")
st.header("Welcome to the function gathering for week 5 and 6")

# Sidebar navigation
st.sidebar.header("Navigation")
app_mode = st.sidebar.selectbox("Choose a mode", [
    "Home", "About", "Unique Values in Categorical Columns", "Basic Statistics", 
    "Drop-off Rate Calculation", "Bounce Rate Calculation", "Demographics Analysis", "Contact"
])

# Function to display basic statistics for numeric columns
def show_basic_statistics(df):
    if df is None:
        st.error("No data available.")
        return
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        st.warning("No numeric columns found in the file.")
        return
    st.subheader("Basic Statistics for Numeric Columns:")
    statistics = numeric_df.describe().T  # Transpose for better readability
    st.write(statistics)
    
    # Create a bar chart for the numerical data
    st.subheader("Bar Chart of Numeric Data")
    numeric_df.plot(kind='bar', figsize=(10, 6), colormap='Blues')
    plt.title('Bar Chart of Numeric Data')
    plt.xlabel('Columns')
    plt.ylabel('Values')
    st.pyplot()

# Function to show unique values in categorical columns
def show_unique_values_in_categorical_columns(df):
    if df is None:
        st.error("No data available.")
        return
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if not categorical_columns:
        st.warning("No categorical columns found in the file.")
        return
    st.subheader("Unique Values in Categorical Columns:")
    for col in categorical_columns:
        unique_values = df[col].unique()
        st.write(f"Column: {col}")
        st.write(f"Unique Values: {unique_values}")
        st.write("------")

# Function to calculate the drop-off (bounce) rate
def calculate_dropoff_rate(group):
    steps = ['start', 'step_1', 'step_2', 'step_3', 'confirm']
    dropoff_rates = {}  # To store the drop-off percentages at each step
    for i in range(len(steps) - 1):
        current_step = steps[i]
        next_step = steps[i + 1]
        # Find the total number of clients who started at current_step
        started = group[group['process_step'] == current_step]['client_id'].nunique()
        # Find the number of clients who reached the next step
        reached_next = group[group['process_step'] == next_step]['client_id'].nunique()
        # Calculate the drop-off rate as a percentage
        if started > 0:
            dropoff_rate = ((started - reached_next) / started) * 100
        else:
            dropoff_rate = 0
        dropoff_rates[current_step] = dropoff_rate
    return dropoff_rates

# Streamlit page for drop-off rate calculation
def display_dropoff_rate_page(df):
    if df is None:
        st.error("No data available.")
        return

    st.title("Drop-off (Bounce) Rate Calculation")

    if 'client_id' in df.columns and 'process_step' in df.columns:
        st.write("Data loaded successfully. Calculating drop-off rates...")

        # Calculate the drop-off rates
        dropoff_rates = calculate_dropoff_rate(df)

        # Display the drop-off rates
        st.subheader("Drop-off Rates at Each Step")
        for step, rate in dropoff_rates.items():
            st.write(f"Drop-off rate at {step}: {rate:.2f}%")

        # Plot the drop-off rates
        st.subheader("Drop-off Rate Visualization")
        steps = list(dropoff_rates.keys())
        rates = list(dropoff_rates.values())

        plt.figure(figsize=(8, 6))
        plt.bar(steps, rates, color='darkred')
        plt.title('Drop-off Rates at Each Step')
        plt.xlabel('Steps')
        plt.ylabel('Drop-off Rate (%)')
        st.pyplot()
    else:
        st.error("The file must contain 'client_id' and 'process_step' columns.")

# Streamlit page for bounce rate calculation
def display_bounce_rate_page(df):
    if df is None:
        st.error("No data available.")
        return

    st.title("Bounce Rate Calculation")

    if 'variation' in df.columns:
        st.write("Data loaded successfully. Calculating bounce rates...")

        # Filter the control and test groups
        control_group_sorted = df[df['variation'] == 'Control']
        test_group_sorted = df[df['variation'] == 'Test']

        # Calculate drop-off rates for both groups
        control_dropoff_rate = calculate_dropoff_rate(control_group_sorted)
        test_dropoff_rate = calculate_dropoff_rate(test_group_sorted)

        # Display the drop-off rates for control group
        st.subheader("Control Group Bounce Rates (%):")
        for step, rate in control_dropoff_rate.items():
            st.write(f"{step}: {rate:.2f}%")
        
        # Display the drop-off rates for test group
        st.subheader("Test Group Bounce Rates (%):")
        for step, rate in test_dropoff_rate.items():
            st.write(f"{step}: {rate:.2f}%")

        # Plot the comparison between the groups
        st.subheader("Bounce Rate Comparison Visualization")
        steps = list(control_dropoff_rate.keys())
        control_rates = list(control_dropoff_rate.values())
        test_rates = list(test_dropoff_rate.values())

        fig = px.bar(x=steps, y=[control_rates, test_rates], barmode='group', labels={'x': 'Steps', 'y': 'Bounce Rate (%)'})
        fig.update_layout(title='Bounce Rate Comparison Between Control and Test Group')
        st.plotly_chart(fig)

    else:
        st.error("The file must contain 'variation' column.")

# Function to show demographics analysis
def show_demographics_analysis(df):
    if df is None:
        st.error("No data available.")
        return
    
    if 'gender' in df.columns:
        st.subheader("Gender Distribution:")
        gender_counts = df['gender'].value_counts()
        st.write(gender_counts)

        # Plot the gender distribution
        fig = px.pie(gender_counts, names=gender_counts.index, values=gender_counts.values, title="Gender Distribution")
        st.plotly_chart(fig)

    age_column = 'clnt_age' if 'clnt_age' in df.columns else 'age'
    
    if age_column in df.columns:
        st.subheader("Age Distribution:")
        bins = [0, 30, 40, 50, 100]
        labels = ['Under 30', '30-39', '40-49', '50 and above']
        df['age_group'] = pd.cut(df[age_column], bins=bins, labels=labels)

        age_group_counts = df['age_group'].value_counts()
        st.write(age_group_counts)

        # Plot the age distribution
        fig = px.bar(age_group_counts, x=age_group_counts.index, y=age_group_counts.values, title="Age Group Distribution")
        st.plotly_chart(fig)

        st.subheader("Basic Statistics for Age:")
        age_stats = df[age_column].describe()
        st.write(age_stats)
    else:
        st.warning("No 'age' or 'clnt_age' column found in the file.")

# Handle file upload only on the Home page
if app_mode == "Home":
    st.write("This is the home page of the A/B Test demo.")
    
    # File uploader widget (only on Home page)
    uploaded_file = st.file_uploader("Upload a CSV file for analysis", type="csv")

    if uploaded_file is not None:
        try:
            # Read the uploaded file into a DataFrame
            df = pd.read_csv(uploaded_file)
            st.write(f"Data loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
        except Exception as e:
            st.error(f"Error reading the file: {e}")

# Add other pages logic here (based on selected mode)
if app_mode == "Unique Values in Categorical Columns":
    show_unique_values_in_categorical_columns(df)
elif app_mode == "Basic Statistics":
    show_basic_statistics(df)
elif app_mode == "Drop-off Rate Calculation":
    display_dropoff_rate_page(df)
elif app_mode == "Bounce Rate Calculation":
    display_bounce_rate_page(df)
elif app_mode == "Demographics Analysis":
    show_demographics_analysis(df)
elif app_mode == "About":
    st.write("This app analyzes A/B testing results and provides insights based on demographic, statistical, and drop-off rate data.")
