#pages/hypothesistestcompletionrate.py
import streamlit as st
import pandas as pd
import scipy.stats as stats

def define_completion_column(df):
    """
    Define the 'completion' column based on specific process steps.
    """
    # Define completion as a variable (not a column)
    df['completion'] = df['process_step'].apply(lambda x: 1 if x in ['confirm', 'completed'] else 0)
    return df

def show_page(df):
    """
    Function to display hypothesis testing results for completion rates
    between Control and Test groups.
    """
    # Define the 'completion' column if not already defined
    if 'completion' not in df.columns:
        df = define_completion_column(df)

    # Ensure the necessary columns exist
    if 'completion' not in df.columns:
        st.error("The 'completion' column is missing from the dataset.")
        return
    if 'variation' not in df.columns:
        st.error("The 'variation' column is missing from the dataset.")
        return

    # Filter the control and test groups from the dataframe
    control_group = df[df['variation'] == 'Control']
    test_group = df[df['variation'] == 'Test']

    # Calculate completion rates for both groups
    control_rate = control_group['completion'].mean()
    test_rate = test_group['completion'].mean()

    # Display the completion rates
    st.subheader("Completion Rates")
    st.write(f"Control Group Completion Rate: {control_rate:.2%}")
    st.write(f"Test Group Completion Rate: {test_rate:.2%}")

    # Perform a hypothesis test to compare completion rates (e.g., z-test for proportions)
    # Null hypothesis: The completion rates are equal
    # Alternative hypothesis: The completion rates are different

    n_control = len(control_group)
    n_test = len(test_group)

    control_successes = control_group['completion'].sum()
    test_successes = test_group['completion'].sum()

    # Perform z-test for proportions
    success_counts = [control_successes, test_successes]
    sample_sizes = [n_control, n_test]
    
    z_stat, p_value = stats.proportions_ztest(success_counts, sample_sizes)

    # Display p-value and decision
    st.subheader("Hypothesis Test Results")
    st.write(f"P-value for comparison of completion rates: {p_value:.4f}")

    if p_value < 0.05:
        st.write("The difference in completion rates is statistically significant.")
    else:
        st.write("The difference in completion rates is not statistically significant.")

    # Optional: Plot completion rates for visual comparison
    st.subheader("Completion Rates Comparison")
    comparison_df = pd.DataFrame({
        'Group': ['Control', 'Test'],
        'Completion Rate': [control_rate, test_rate]
    })
    
    st.bar_chart(comparison_df.set_index('Group')['Completion Rate'])

    st.subheader("Hypothesis Testing Explanation")
    st.write("""
    In this test, we are comparing the completion rates between the Control and Test groups.
    
    - **Null Hypothesis (H₀):** The completion rates for both groups are the same.
    - **Alternative Hypothesis (H₁):** The completion rates for both groups are different.
    
    A p-value less than 0.05 indicates that the null hypothesis can be rejected, meaning the difference in completion rates is statistically significant.
    """)