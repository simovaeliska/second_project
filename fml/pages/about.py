# pages/about.py
import streamlit as st
from data_loader import load_data

def show_about_project():
    st.title("About the Project")
    
    st.header("Project Overview by Ceci and Eliska")
    st.write(
        """
        An A/B test was conducted from 3/15/2017 to 6/20/2017 by the Vanguard team to evaluate the impact of a new digital interface.

        **Control Group**: Clients interacted with Vanguard’s traditional online process.  
        **Test Group**: Clients experienced the new, spruced-up digital interface.

        ### Project Timeline:
        - **Day 1 & 2 (Week 5)**  
          EDA & Data Cleaning  
          Client behavior analysis – identifying relations and forming hypotheses.

        - **Day 3 (Week 5)**  
          Performance Metrics  
          Success Indicators  
          Redesign Outcome

        - **Day 4 & 5 (Week 5)**  
          Hypothesis Testing  
          Completion Rate  
          Cost-Effectiveness Threshold  
          Additional Hypothesis Examples  
          Experiment Evaluation  
          Design Effectiveness  
          Duration Assessment  
          Further Data Needs

        - **Day 1 & 2 (Week 6)**  
          Tableau  
          Visualization Tasks

        - **Day 3 & 4 (Week 6)**  
          Further Data Analysis and Presentation Preparation
        """
    )

    # About Vanguard Group
    st.subheader("About Vanguard Group")
    st.write(
        """
        The Vanguard Group is one of the world’s largest investment management companies, founded in 1975 by John C. Bogle. It is renowned for pioneering low-cost index funds, which allow investors to track broad market indices with minimal fees. Vanguard’s investor-owned structure means that the company is owned by the funds it manages, aligning its interests with those of its investors. Today, Vanguard manages trillions of dollars in assets, offering a wide range of investment products including mutual funds, ETFs, and retirement plans, with a focus on long-term, passive investing strategies.
        """
    )

    # New Sub-heading: Digital Challenge and Our Role
    st.subheader("Digital Challenge and Our Role")
    st.write(
        """
        **A/B Test Objective:**  
        The goal of this experiment was to evaluate a new, modernized user interface (UI) designed to improve the online client journey through in-context prompts.

        **Experiment Details:**
        - **Control Group**: Clients used the traditional Vanguard user interface.
        - **Test Group**: Clients experienced the new, intuitive UI with contextual prompts designed to guide them through the online process.

        **Timeline:**  
        The experiment took place from **March 15, 2017 – June 20, 2017**.

        **Process Flow:**  
        Clients followed a sequence of steps starting from the initial page, progressing through three key steps, and finishing at the confirmation page.

        *As part of the CX (Customer Experience) team, our job was to evaluate whether the new UI leads to better user engagement and higher completion rates during online processes.*
        """
    )

    # **Did the new UI lead to higher completion rates?**
    st.write("**Did the new UI lead to higher completion rates?**")
    st.write(
        """
        The A/B test was designed to determine whether the new, intuitive UI with contextual prompts improved user engagement and completion rates compared to the traditional Vanguard user interface. The results from hypothesis testing and analysis will help answer this key question.
        """
    )

    # New Section: What Data We Have Been Working With
    st.subheader("What Data We Have Been Working With")
    st.write(
        """
        The analysis is based on a rich set of data that provides insights into both client demographics and their digital interactions with Vanguard's platform. Below is a summary of the key datasets:

        - **Client Profiles**: This includes demographic and account details such as:
          - **Client's Age**: The age of each client.
          - **Client's Tenure**: How long each client has been with Vanguard, in both years and months.
          - **Client's Balance**: The total balance held across all of a client's accounts with Vanguard.
          - **Number of Accounts**: The number of accounts the client holds with Vanguard.

        - **Digital Footprints**: This data captures the client's online activity at each step in the client journey:
          - **Process Steps**: The sequence of steps each client went through in their digital process (e.g., initial page, steps 1-3, and confirmation page).
          - **Date-Time Logs**: Timestamps for each action taken by the client during their online session, allowing us to track the client’s progression through each step.

        - **Experiment Roster**: This dataset indicates which group each client was assigned to (Control or Test), based on their unique **client_id**. It helps us compare the performance of the Control group (traditional UI) against the Test group (new UI with contextual prompts).
        """
    )

    st.header("Getting Started")
    st.write(
        """
        ## Metadata
        This comprehensive set of fields will guide your analysis, helping you uncover insights into client behavior and preferences.

        - **client_id**: A unique identifier for each client.
        - **variation**: Denotes whether a client was part of the experiment (Control or Test).
        - **visitor_id**: A unique ID for each client-device combination.
        - **visit_id**: A unique ID for each web visit/session.
        - **process_step**: The step in the digital process that the client is engaged in.
        - **date_time**: Timestamp of each web activity.
        - **clnt_tenure_yr**: The number of years a client has been with Vanguard.
        - **clnt_tenure_mnth**: The number of months a client has been with Vanguard.
        - **clnt_age**: The client’s age.
        - **gendr**: The client’s gender.
        - **num_accts**: The number of accounts the client holds with Vanguard.
        - **bal**: The total balance across all client accounts.
        - **calls_6_mnth**: The number of times the client reached out over the phone in the last 6 months.
        - **logons_6_mnth**: The number of times the client logged into Vanguard’s platform over the last 6 months.

        ## Bonus: Additional Tasks (Optional)
        If you have extra time after completing the core tasks, explore the following optional questions and activities:

        - **Client Behavior Analysis**: Dive deeper into the data to analyze client behavior patterns and trends.
        - **Power and Effect Size**: Perform power analysis to determine the sample size needed for a reliable test and compute the effect size.
        - **Streamlit Integration**: Add Streamlit widgets to your project to enable real-time analysis and visualization. Customize your app for interactivity.
        """
    )

    # **Data Cleaning & Merging Process** section
    st.subheader("Data Cleaning & Merging Process")
    st.write(
        """
        The data cleaning and merging process is crucial for ensuring the integrity and consistency of the dataset. Here's how we handled the data:

        **Clean Datasets**:
        - **Load Data**: We begin by loading the raw data from various sources.
        - **Drop Missing Values**: Any missing values in critical columns (like `client_id`, `process_step`, etc.) are removed to ensure that we only work with complete data.
        - **Rename Columns**: Columns are renamed to have consistent naming conventions and be more meaningful for analysis.
        - **Remove 'X' Gender Values**: Any rows with 'X' as a gender label are removed as this represents incomplete or erroneous data.
        - **Map Gender Codes to Labels**: Gender codes are mapped to more readable labels (e.g., 'M' -> 'Male', 'F' -> 'Female').
        - **Ensure Proper DateTime Format**: We ensure that the `date_time` column is in the correct format (i.e., datetime objects), allowing for time-based analysis.

        **Merge Datasets**:
        - **Merge Demographic Datasets**: We combine the demographic data (client information such as age, tenure, balance) into a single dataset.
        - **Concatenate Web Interactions Dataset**: The web interactions (client's steps through the online process) are merged with the demographic data based on the `client_id`.
        - **Final Merge on `client_id`**: After all data is cleaned and preprocessed, we merge all datasets on the common `client_id` column to create a comprehensive dataset.

        **Segment by Experiment Group**:
        - **Control and Test Groups**: The dataset is split into two groups based on the `variation` column: the Control group (clients using the traditional UI) and the Test group (clients using the new UI with contextual prompts).

        **Sort Data**:
        - **Sort by client_id, visit_id, process_step, and date_time**: This ensures that the data is ordered by the client's journey through the process, from their first visit to the confirmation step.

        **Age Group Categorization**:
        - **Assign Age Groups**: Based on defined age bins, we categorize clients into age groups (e.g., under 30, 30-39, 40-49, 50+). This categorization is applied to the `df_merged`, as well as to the `control` and `test` datasets to facilitate age-based analysis.
        """
    )
