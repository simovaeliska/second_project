import streamlit as st
import pandas as pd
from scipy import stats

# Function to load the CSV file and show information
@st.cache_data
def load_data():
    url = r"C:\Users\Cecilia\Downloads\ironhack\coursework\group_work\group_project_week5_6\second_project\data\clean\combined_cleaned_data.csv"
    try:
        df = pd.read_csv(url)
        return df
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
        return None

# Function to show the About the Project page
def show_about_project():
    st.title("About the Project")
    
    st.header("Project Overview")
    st.write(
        """
        An A/B test was set into motion from 3/15/2017 to 6/20/2017 by the Vanguard team.

        Control Group: Clients interacted with Vanguard’s traditional online process.
        Test Group: Clients experienced the new, spruced-up digital interface.

        * Day 1 & 2 (Week 5)
        EDA & Data Cleaning
        Client behavior analysis - explained below (trying to find relations and come up with hypothesis)
        * Day 3 (Week 5)
        Performance Metrics
        Success Indicators
        Redesign Outcome
        * Day 4 & 5 (Week 5)
        Hypothesis Testing
        Completion Rate
        Completion Rate with a Cost-Effectiveness Threshold
        Other Hypothesis Examples
        Experiment Evaluation
        Design Effectiveness
        Duration Assessment
        Additional Data Needs
        * Day 1 & 2 (Week 6)
        Tableau
        Tableau Tasks
        * Day 3 & 4 (Week 6)
        """
    )

    st.header("Getting Started")
    st.write(
        """
        ## Metadata
        This comprehensive set of fields will guide your analysis, helping you unravel the intricacies of client behavior and preferences.

        - **client_id**: Every client’s unique ID.
        - **variation**: Indicates if a client was part of the experiment.
        - **visitor_id**: A unique ID for each client-device combination.
        - **visit_id**: A unique ID for each web visit/session.
        - **process_step**: Marks each step in the digital process.
        - **date_time**: Timestamp of each web activity.
        - **clnt_tenure_yr**: Represents how long the client has been with Vanguard, measured in years.
        - **clnt_tenure_mnth**: Further breaks down the client’s tenure with Vanguard in months.
        - **clnt_age**: Indicates the age of the client.
        - **gendr**: Specifies the client’s gender.
        - **num_accts**: Denotes the number of accounts the client holds with Vanguard.
        - **bal**: Gives the total balance spread across all accounts for a particular client.
        - **calls_6_mnth**: Records the number of times the client reached out over a call in the past six months.
        - **logons_6_mnth**: Reflects the frequency with which the client logged onto Vanguard’s platform over the last six months.

        ## Bonus: Additional Tasks (Optional)
        If you complete all of the tasks and have some extra time before the presentation, you can explore the following additional questions and tasks:

        # Client Behavior Analysis
        Power and Effect Size
        Streamlit
        Add Streamlit to your project to achieve Customization and Real-time Analysis
        """
    )

# Function to show unique values in categorical columns
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

# Function to show basic statistics for numeric columns
def show_basic_statistics(df):
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.empty:
        st.warning("No numeric columns found in the file.")
        return
    
    st.subheader("Basic Statistics for Numeric Columns:")
    statistics = numeric_df.describe().T  # Transpose for better readability
    st.write(statistics)

# Function to show demographics analysis
def show_demographics_analysis(df):
    # Display column names to debug and confirm if they exist
    st.write("Columns in the dataset:", df.columns)

    # Ensure 'client_id', 'clnt_age', 'gender', and 'variation' columns exist in your DataFrame
    required_columns = ['client_id', 'clnt_age', 'gender', 'variation']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"Required columns are missing: {', '.join(missing_columns)}")
        return
    
    # Create age groups for demographics analysis
    bins = [18, 30, 40, 50, 60, 100]  # Adjust the age ranges as needed
    labels = ['18-29', '30-39', '40-49', '50-59', '60+']
    
    # Group by 'client_id' and assign age groups to 'age_group'
    df['age_group'] = pd.cut(df['clnt_age'], bins=bins, labels=labels, right=False)
    
    # Group by 'client_id' and create a gender column based on 'gender'
    df['gender_group'] = df['gender']
    
    # Keep 'variation' as is (without creating a separate column) to represent Test/Control groups
    df['variation_group'] = df['variation'].apply(lambda x: 'Test' if x == 1 else 'Control')

    # Display age group counts by 'client_id'
    st.subheader("Demographics: Age Groups")
    st.write(df.groupby('client_id')['age_group'].first().value_counts())

    # Display gender group counts by 'client_id'
    st.subheader("Demographics: Gender Distribution")
    st.write(df.groupby('client_id')['gender_group'].first().value_counts())

    # Display Test/Control group counts by 'client_id' using the 'variation' column
    st.subheader("Demographics: Test/Control Group Distribution")
    st.write(df.groupby('client_id')['variation'].first().apply(lambda x: 'Test' if x == 1 else 'Control').value_counts())

    # Show the top 5 rows with client demographics (age, gender, variation)
    st.subheader("Top 5 Rows of Client Demographics (Age, Gender, Group)")
    st.write(df[['client_id', 'age_group', 'gender_group', 'variation_group']].drop_duplicates().head())

    # Display available columns for further analysis
    st.write(f"Available columns in the dataset: {df.columns}")
    
    # Display all client details (age, gender, group) if needed
    st.subheader("Client Demographic Details")
    st.write(df[['client_id', 'clnt_age', 'gender', 'variation']].head())

# Function for two-proportion z-test
def two_proportion_z_test(p1, p2, n1, n2):
    P = (p1 * n1 + p2 * n2) / (n1 + n2)
    SE = (P * (1 - P) * (1 / n1 + 1 / n2)) ** 0.5
    z = (p1 - p2) / SE
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))  # Two-tailed test
    return z, p_value

# Function to show hypothesis testing page
def show_hypothesis_testing_page(df):
    st.title("Hypothesis Testing for Completion Rates")
    
    available_columns = df.columns
    st.write(f"Available columns in the dataset: {available_columns}")

    if 'completion_rate' not in available_columns:
        if 'completed_visits' in available_columns and 'started_visits' in available_columns:
            df['completion_rate'] = df['completed_visits'] / df['started_visits'] * 100
        else:
            st.error("Missing required columns ('completed_visits' or 'started_visits') to calculate 'completion_rate'.")
            return

    control_group = df[df['variation'] == 'Control']
    test_group = df[df['variation'] == 'Test']

    steps = ['confirm', 'step_1', 'step_2', 'step_3']

    for step in steps:
        st.subheader(f"Step: {step}")
        
        control_completions = control_group[control_group['process_step'] == step]['completion_rate'].values[0]
        test_completions = test_group[test_group['process_step'] == step]['completion_rate'].values[0]
        
        control_total = control_group[control_group['process_step'] == step]['started_visits'].values[0]
        test_total = test_group[test_group['process_step'] == step]['started_visits'].values[0]

        p_control = control_completions / 100
        p_test = test_completions / 100
        
        z_stat, p_value = two_proportion_z_test(p_control, p_test, control_total, test_total)
        
        st.write(f"Z-statistic: {z_stat:.4f}")
        st.write(f"P-value: {p_value:.4f}")
        
        if p_value < 0.05:
            st.write(f"**Reject the null hypothesis**: There is a significant difference in completion rates between control and test group for step: {step}.")
        else:
            st.write(f"**Fail to reject the null hypothesis**: There is no significant difference in completion rates between control and test group for step: {step}.")
        st.write("\n")

    st.subheader("Hypothesis Test: Tenure")
    
    control_unique = control_group.drop_duplicates(subset='client_id')
    test_unique = test_group.drop_duplicates(subset='client_id')

    control_tenure = control_unique['clnt_tenure_yr']
    test_tenure = test_unique['clnt_tenure_yr']
        
    t_stat, p_value_tenure = stats.ttest_ind(control_tenure, test_tenure, equal_var=True)

    st.write(f"Average Tenure in Control group: {control_tenure.mean():.2f} years")
    st.write(f"Average Tenure in Test group: {test_tenure.mean():.2f} years")
    st.write(f"T-statistic: {t_stat:.4f}")
    st.write(f"P-value: {p_value_tenure:.4f}")

    if p_value_tenure < 0.05:
        st.write("**Reject the null hypothesis**: There is a significant difference in tenure between control and test groups.")
    else:
        st.write("**Fail to reject the null hypothesis**: There is no significant difference in tenure between control and test groups.")

def show_latest_starts(df):
    # Filter out the 'start' process steps
    starts_only = df[df['process_step'] == 'start']
    latest_starts = starts_only.loc[starts_only.groupby('client_id')['date_time'].idxmax()]

    # Filter out the 'confirm' process steps
    confirmation_only = df[df['process_step'] == 'confirm']
    latest_confirms = confirmation_only.loc[confirmation_only.groupby('client_id')['date_time'].idxmax()]

    # Merge the latest start and confirm steps
    latest_start_confirms = pd.merge(latest_starts, latest_confirms, on='client_id', suffixes=('_start', '_confirm'))

    # Ensure 'date_time' columns are in datetime format
    latest_start_confirms['date_time_start'] = pd.to_datetime(latest_start_confirms['date_time_start'], errors='coerce')
    latest_start_confirms['date_time_confirm'] = pd.to_datetime(latest_start_confirms['date_time_confirm'], errors='coerce')

    # Drop rows where either 'date_time_start' or 'date_time_confirm' is NaT
    latest_start_confirms = latest_start_confirms.dropna(subset=['date_time_start', 'date_time_confirm'])

    # Calculate process duration
    latest_start_confirms['process_duration'] = latest_start_confirms['date_time_confirm'] - latest_start_confirms['date_time_start']

    # If you want the duration in minutes
    latest_start_confirms['process_duration_minutes'] = latest_start_confirms['process_duration'].dt.total_seconds() / 60

    st.subheader("Process Duration Analysis:")
    avg_duration = latest_start_confirms['process_duration_minutes'].mean()
    mode_duration = latest_start_confirms['process_duration_minutes'].mode()[0]
    median_duration = latest_start_confirms['process_duration_minutes'].median()

    st.write(f"Average Duration: {avg_duration:.2f} minutes")
    st.write(f"Mode Duration: {mode_duration:.2f} minutes")
    st.write(f"Median Duration: {median_duration:.2f} minutes")

# Function to calculate and display completion time for each step
def calculate_and_display_completion_time(df):
    control_group = df[df['variation'] == 'Control']
    control_group = control_group.sort_values(by=['client_id', 'date_time'])

    control_group['next_step_time'] = control_group.groupby('client_id')['date_time'].shift(-1)
    control_group = control_group.dropna(subset=['next_step_time'])
    control_group['completion_time'] = control_group['next_step_time'] - control_group['date_time']

    control_group['completion_time_minutes'] = control_group['completion_time'].dt.total_seconds() / 60

    st.write("Average Completion Time by Process Step (Control Group):")
    avg_completion_time = control_group.groupby('process_step')['completion_time_minutes'].mean().reset_index()
    st.write(avg_completion_time)

# Page navigation setup
def main():
    st.set_page_config(page_title="A/B Test Demo for Group 7")
    
    df = load_data()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", [
        "About the Project", 
        "Data Summary", 
        "Unique Values", 
        "Basic Statistics", 
        "Demographics Analysis", 
        "Hypothesis Testing",
        "Process Duration Analysis",
        "Completion Time Analysis"
    ])

    if page == "About the Project":
        show_about_project()

    elif page == "Data Summary":
        if df is not None:
            st.subheader("CSV Data Overview")
            st.write(f"Number of rows: {df.shape[0]}")
            st.write(f"Number of columns: {df.shape[1]}")
            st.write("First 5 rows of the dataset:")
            st.dataframe(df.head())
        else:
            st.error("Data could not be loaded.")

    elif page == "Unique Values":
        if df is not None:
            show_unique_values_in_categorical_columns(df)
        else:
            st.error("Data could not be loaded.")

    elif page == "Basic Statistics":
        if df is not None:
            show_basic_statistics(df)
        else:
            st.error("Data could not be loaded.")

    elif page == "Demographics Analysis":
        if df is not None:
            show_demographics_analysis(df)
        else:
            st.error("Data could not be loaded.")

    elif page == "Hypothesis Testing":
        if df is not None:
            show_hypothesis_testing_page(df)
        else:
            st.error("Data could not be loaded.")

    elif page == "Process Duration Analysis":
        if df is not None:
            show_latest_starts(df)
        else:
            st.error("Data could not be loaded.")

    elif page == "Completion Time Analysis":
        if df is not None:
            calculate_and_display_completion_time(df)
        else:
            st.error("Data could not be loaded.")

# Run the app
if __name__ == "__main__":
    main()