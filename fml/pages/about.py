# pages/about.py
import streamlit as st

def show_about_project():
    st.title("About the Project")
    
    st.header("Project Overview")
    st.write(
        """
        An A/B test was set into motion from 3/15/2017 to 6/20/2017 by the Vanguard team.

        Control Group: Clients interacted with Vanguard’s traditional online process.
        Test Group: Clients experienced the new, spruced-up digital interface.

        * **Day 1 & 2 (Week 5)**  
          EDA & Data Cleaning  
          Client behavior analysis - explained below (trying to find relations and come up with hypotheses)

        * **Day 3 (Week 5)**  
          Performance Metrics  
          Success Indicators  
          Redesign Outcome

        * **Day 4 & 5 (Week 5)**  
          Hypothesis Testing  
          Completion Rate  
          Completion Rate with a Cost-Effectiveness Threshold  
          Other Hypothesis Examples  
          Experiment Evaluation  
          Design Effectiveness  
          Duration Assessment  
          Additional Data Needs

        * **Day 1 & 2 (Week 6)**  
          Tableau  
          Tableau Tasks

        * **Day 3 & 4 (Week 6)**
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

        - Client Behavior Analysis
        - Power and Effect Size
        - Streamlit  
          Add Streamlit to your project to achieve Customization and Real-time Analysis
        """
    )