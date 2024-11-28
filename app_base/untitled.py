import streamlit as st
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

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

# Function to handle different pages
def handle_data_page(page: str, df: pd.DataFrame) -> None:
    """
    Handles the display of data-related pages based on user selection.
    
    Args:
    page (str): The selected page from the sidebar.
    df (pd.DataFrame): The DataFrame containing the loaded data.
    """
    if df is None:
        st.error("Data could not be loaded.")
        return

    if page == "Data Summary":
        st.subheader("CSV Data Overview")
        st.write(f"Number of rows: {df.shape[0]}")
        st.write(f"Number of columns: {df.shape[1]}")
        st.write("First 5 rows of the dataset:")
        st.dataframe(df.head())

    elif page == "Unique Values":
        show_unique_values_in_categorical_columns(df)

    elif page == "Basic Statistics":
        show_basic_statistics(df)

    elif page == "Demographics Analysis":
        show_demographics_analysis(df)

    elif page == "Hypothesis Testing":
        show_hypothesis_testing_page(df)

    elif page == "Process Duration Analysis":
        show_latest_starts(df)

    elif page == "Completion Time Analysis":
        calculate_and_display_completion_time(df)

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

        Client Behavior Analysis
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

# Function to calculate and display logs_calls_accounts if necessary
def calculate_logs_calls_accounts(df):
    # Perform the aggregation only when necessary
    return df.groupby(['gender', 'age_group']).agg({
        'num_accts': 'mean',
        'calls_6_mnth': 'mean',
        'logons_6_mnth': 'mean'
    }).reset_index().round(2)

def plot_demographics(data, x, y, hue, title, ylabel, filename, linestyle='-', marker='o'):
    """
    Helper function to create and save a line plot for demographic data.
    
    Args:
    data (DataFrame): The data to plot.
    x (str): The column name for the x-axis.
    y (str): The column name for the y-axis.
    hue (str): The column name for the hue (color differentiation).
    title (str): The title of the plot.
    ylabel (str): The label for the y-axis.
    filename (str): The filename to save the plot.
    linestyle (str): The line style for the plot (default is solid).
    marker (str): The marker style for the plot (default is 'o').
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        marker=marker,
        linestyle=linestyle,
        palette='coolwarm'
    )
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Age Group")
    plt.legend(title="Gender")
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

# New Aggregation for Number of Accounts, Calls, and Logons
logs_calls_accounts = df.groupby(['gender', 'age_group']).agg({
    'num_accts': 'mean',
    'calls_6_mnth': 'mean',
    'logons_6_mnth': 'mean'
}).reset_index().round(2)

# Plot for Average Number of Accounts
plot_demographics(
    data=logs_calls_accounts,
    x='age_group',
    y='num_accts',
    hue='gender',
    title="Average Number of Accounts",
    ylabel="Average Number of Accounts",
    filename="average_accounts.png"
)

# Plot for Calls in the Last 6 Months
plot_demographics(
    data=logs_calls_accounts,
    x='age_group',
    y='calls_6_mnth',
    hue='gender',
    title="Average Calls in Last 6 Months",
    ylabel="Average Calls",
    filename="average_calls.png",
    linestyle='--'
)

# Plot for Logons in the Last 6 Months
plot_demographics(
    data=logs_calls_accounts,
    x='age_group',
    y='logons_6_mnth',
    hue='gender',
    title="Average Logons in Last 6 Months",
    ylabel="Average Logons",
    filename="average_logs.png",
    linestyle=':'
)

st.write("Demographics analysis will be displayed here.")

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
def main() -> None:
    """
    Main function to run the Streamlit app for A/B Test Demo.
    
    Sets up the page configuration, loads data, and manages navigation
    through different pages of the app.
    """
    st.set_page_config(page_title="A/B Test Demo for Group 7")
    
    # Ensure df is loaded here before using it
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
        "Process Duration Analysis",
        "Completion Time Analysis"
    ])

    # Handle page navigation
    if page == "About the Project":
        show_about_project()
    else:
        handle_data_page(page, df)

    # Example of conditional logic if you need the logs_calls_accounts aggregation:
    if page == "Demographics Analysis":
        logs_calls_accounts = calculate_logs_calls_accounts(df)
        # Now you can use logs_calls_accounts for demographics analysis
        st.write(logs_calls_accounts)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()