import pandas as pd
import os

directory_path = "gpt_analyse/output/summarise_project/solar"
df = pd.read_excel('data/input/own_work_input.xlsx',sheet_name='Database')
df['project'] = df['Company'].astype(str) + ' ' + df['Plant'].astype(str)
projects = df['project'].tolist()
csv_files = [os.path.join(directory_path, f"{project}.csv") for project in projects]

# Read each CSV file into a dataframe
dataframes = []
for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Concatenate the dataframes into a single dataframe
concatenated_df = pd.concat(dataframes)

# Output the concatenated dataframe as a new CSV file
output_file = os.path.join(os.path.dirname(csv_files[0]), "Master.csv")
concatenated_df.to_csv(output_file, index=False)
