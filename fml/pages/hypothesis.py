#pages/hypothesis.py
import streamlit as st
import scipy.stats as stats

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
    
    # Check if 'completion_rate' exists, otherwise create it
    if 'completion_rate' not in df.columns:
        if 'completed_visits' in df.columns and 'started_visits' in df.columns:
            df['completion_rate'] = df['completed_visits'] / df['started_visits'] * 100
        else:
            st.error("Missing required columns ('completed_visits' or 'started_visits') to calculate 'completion_rate'.")
            return  # Exit function if required columns are missing
    
    # Separate control and test groups based on 'variation' column
    if 'variation' not in df.columns:
        st.error("Missing 'variation' column to distinguish between control and test groups.")
        return

    control_group = df[df['variation'] == 'Control']
    test_group = df[df['variation'] == 'Test']
    
    if control_group.empty or test_group.empty:
        st.error("Missing data for control or test group.")
        return

    steps = ['confirm', 'step_1', 'step_2', 'step_3']

    # Iterate through the steps to perform hypothesis testing for completion rates
    for step in steps:
        st.subheader(f"Step: {step}")
        
        control_completions = control_group[control_group['process_step'] == step]['completion_rate'].mean()
        test_completions = test_group[test_group['process_step'] == step]['completion_rate'].mean()
        
        control_total = control_group[control_group['process_step'] == step]['started_visits'].sum()
        test_total = test_group[test_group['process_step'] == step]['started_visits'].sum()

        if control_total == 0 or test_total == 0:
            st.warning(f"No visits started for control or test group at step {step}. Skipping hypothesis test for this step.")
            continue
        
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
    
    # Drop duplicates based on 'client_id' to ensure we are comparing unique clients
    control_unique = control_group.drop_duplicates(subset='client_id')
    test_unique = test_group.drop_duplicates(subset='client_id')

    # Ensure 'clnt_tenure_yr' exists in the dataset
    if 'clnt_tenure_yr' not in df.columns:
        st.error("Missing 'clnt_tenure_yr' column for tenure analysis.")
        return
    
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