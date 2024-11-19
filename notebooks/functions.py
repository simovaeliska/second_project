#Neccessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# clean df_final_demo
def clean_df_final_demo():
    #key fields client_id, clnt_age, gender, num_accts, balance, clnt_tenure_yr
    df_copy = pd.read_csv("df_final_demo.txt")
    df_copy = df_copy.dropna()
    corrected_columns = {"gendr" : "gender", "bal" : "balance"}
    df_copy.rename(columns=corrected_columns, inplace = True)
    return df_copy

# clean df_experiment_clients
def clean_df_experiment_clients():
    df_copy = pd.read_csv("df_final_experiment_clients.txt")
    df_copy = df_copy.dropna() # dropping the NaN values
    df_copy.rename(columns={'Variation': 'variation'}, inplace=True)
    return df_copy
