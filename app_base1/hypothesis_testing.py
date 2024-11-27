#hypothesis_testing.py

import pandas as pd
import streamlit as st
from scipy import stats

def two_proportion_z_test(p1, p2, n1, n2):
    # Calculate the pooled proportion
    P = (p1 * n1 + p2 * n2) / (n1 + n2)
    
    # Calculate the standard error
    SE = (P * (1 - P) * (1 / n1 + 1 / n2)) ** 0.5
    
    # Calculate the z-statistic
    z = (p1 - p2) / SE
    
    # Calculate the p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))  # Two-tailed test
    
    return z, p_value

def show_hypothesis_testing_page(df):
    st.title("Hypothesis Testing for Completion Rates")
    
    # Ensure the relevant columns are available in the DataFrame
    available_columns = df.columns
    st.write(f"Available columns in the dataset: {available_columns}")

    # Check if 'completion_rate' is present, and if not, calculate it
    if 'completion_rate' not in available_columns:
        # Assuming 'completed_visits' and 'started_visits' are available for calculation
        if 'completed_visits' in available_columns and 'started_visits' in available_columns:
            df['completion_rate'] = df['completed_visits'] / df['started_visits'] * 100
        else:
            st.error("Missing required columns ('completed_visits' or 'started_visits') to calculate 'completion_rate'.")
            return

    # Separate the control and test groups
    control_group = df[df['variation'] == 'Control']
    test_group = df[df['variation'] == 'Test']

    # Assuming 'process_step' is a column to group by
    steps = ['confirm', 'step_1', 'step_2', 'step_3']

    # Loop through each step and perform hypothesis testing
    for step in steps:
        st.subheader(f"Step: {step}")
        
        # Get completion rates for both control and test groups for the current step
        control_completions = control_group[control_group['process_step'] == step]['completion_rate'].values[0]
        test_completions = test_group[test_group['process_step'] == step]['completion_rate'].values[0]
        
        control_total = control_group[control_group['process_step'] == step]['started_visits'].values[0]
        test_total = test_group[test_group['process_step'] == step]['started_visits'].values[0]

        # Calculate proportions (completion rate)
        p_control = control_completions / 100  # Convert completion rate to a proportion
        p_test = test_completions / 100  # Convert completion rate to a proportion
        
        # Perform the two-proportion z-test
        z_stat, p_value = two_proportion_z_test(p_control, p_test, control_total, test_total)
        
        # Displaying the results
        st.write(f"Z-statistic: {z_stat:.4f}")
        st.write(f"P-value: {p_value:.4f}")
        
        # Hypothesis testing interpretation
        if p_value < 0.05:
            st.write(f"**Reject the null hypothesis**: There is a significant difference in completion rates between control and test group for step: {step}.")
        else:
            st.write(f"**Fail to reject the null hypothesis**: There is no significant difference in completion rates between control and test group for step: {step}.")
        st.write("\n")

    # ----------------------------------------
    # Additional Hypothesis Testing: Tenure
    st.subheader("Hypothesis Test: Tenure")
    
    # Remove duplicates based on 'client_id' to get unique clients
    control_uniqe = control_group.drop_duplicates(subset='client_id')
    test_unique = test_group.drop_duplicates(subset='client_id')

    # Extract the tenure data for both groups
    control_tenure = control_uniqe['clnt_tenure_yr']
    test_tenure = test_unique['clnt_tenure_yr']
        
    # Perform two-sample t-test for tenure
    _, p_value_tenure = st.ttest_ind(control_tenure, test_tenure, equal_var=True)  # assuming equal variance

    # Display the results
    st.write(f"Average Tenure in Control group: {control_tenure.mean():.2f} years")
    st.write(f"Average Tenure in Test group: {test_tenure.mean():.2f} years")
    st.write(f"T-statistic: {_:.4f}")
    st.write(f"P-value: {p_value_tenure:.4f}")

    # Hypothesis test: Is there a significant difference in tenure between the two groups?
    if p_value_tenure < 0.05:
        st.write("**Reject the null hypothesis**: The average tenure is significantly different between the Test and Control groups.")
    else:
        st.write("**Fail to reject the null hypothesis**: The average tenure is not significantly different between the two groups.")
    
    st.write("\n")

    # ----------------------------------------
    # Additional Hypothesis Testing: Age
    st.subheader("Hypothesis Test: Age")
    
    # Extract the age data for both groups
    control_age = control_uniqe['clnt_age']
    test_age = test_unique['clnt_age']

    # Perform two-sample t-test for age
    _, p_value_age = st.ttest_ind(control_age, test_age, equal_var=True)  # assuming equal variance

    # Display the results
    st.write(f"Control Group Mean Age: {control_age.mean():.2f} years")
    st.write(f"Test Group Mean Age: {test_age.mean():.2f} years")
    st.write(f"T-statistic: {_:.4f}")
    st.write(f"P-value: {p_value_age:.4f}")

    # Hypothesis test: Is there a significant difference in age between the two groups?
    if p_value_age < 0.05:
        st.write("**Reject the null hypothesis**: The average age is different between the Test and Control groups.")
    else:
        st.write("**Fail to reject the null hypothesis**: The average age is not significantly different between the Test and Control groups.")
    
    st.write("\n")