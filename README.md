# Project overview

An A/B test was set into motion from 3/15/2017 to 6/20/2017 by the Vanguard team.

Control Group: Clients interacted with Vanguard’s traditional online process.
Test Group: Clients experienced the new, spruced-up digital interface.

* Day 1 & 2 (Week 5):
EDA & Data Cleaning
Client behavior analysis - explained below (trying to find relations and come up with hypothesis)
* Day 3 (Week 5):
Performance Metrics
Success Indicators
Redesign Outcome
* Day 4 & 5 (Week 5):
Hypothesis Testing
Completion Rate
Completion Rate with a Cost-Effectiveness Threshold
Other Hypothesis Examples
Experiment Evaluation
Design Effectiveness
Duration Assessment
Additional Data Needs
* Day 1 & 2 (Week 6):
Tableau
Tableau Tasks
* Day 3 & 4 (Week 6)

# Getting Started
## Metadata
This comprehensive set of fields will guide your analysis, helping you unravel the intricacies of client behavior and preferences.

* client_id: Every client’s unique ID.
* variation: Indicates if a client was part of the experiment.
* visitor_id: A unique ID for each client-device combination.
* visit_id: A unique ID for each web visit/session.
* process_step: Marks each step in the digital process.
* date_time: Timestamp of each web activity.
* clnt_tenure_yr: Represents how long the client has been with Vanguard, measured in years.
* clnt_tenure_mnth: Further breaks down the client’s tenure with Vanguard in months.
* clnt_age: Indicates the age of the client.
* gendr: Specifies the client’s gender.
* num_accts: Denotes the number of accounts the client holds with Vanguard.
* bal: Gives the total balance spread across all accounts for a particular client.
* calls_6_mnth: Records the number of times the client reached out over a call in the past six months.
* logons_6_mnth: Reflects the frequency with which the client logged onto Vanguard’s platform over the last six months.

# Bonus: Additional Tasks (Optional)
If you complete all of the tasks and have some extra time before the presentation, you can explore the following additional questions and tasks:

# Client Behavior Analysis
Power and Effect Size
Streamlit
Add Streamlit to your project to achieve Customization and Real-time Analysis

# Hypothesis Testing
Completion Rate with a Cost-Effectiveness Threshold

## Hypothesis: "Does the introduction of the new UI design result in a minimum 5% increase in the completion rate compared to the existing design, making it cost-effective?"

* two-sample t-test yielded a p-value of 0.2009, which is greater than the significance level of 0.05
* fail to reject the null hypothesis, indicating no strong evidence that the Test group's completion rate is genuinely different from the Control group's
* the completion rate increase of 9.82% between the Test and Control, exceeds the 5% threshold set by Vanguard, new UI design could be considered worthwhile from a business perspective

## Bounce rate hypothesis
* Hypothesis: “The bounce rate of the Test group is lower than the Control group across all steps”
* Result: Test group showed a statistically significant lower bounce rate only at Step 1, even if the Test group’s bounce rate is visibly lower, statistical significance depends on other factors as well as sample size or variability

# Dataset 
...

## Main dataset issues

- ...
- ...
- ...

## Solutions for the dataset issues
...

# Conclussions
...

# Next steps
...
