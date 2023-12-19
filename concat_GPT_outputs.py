import pandas as pd
import os

tech = 'battery'
version = 'v8'

df = pd.read_excel('data/input/projects.xlsx')
projects = df[tech].tolist()
print(projects)

directory_path = f"gpt_analyse/output/summarise_project/{tech}"

# reading in existing csv files 
csv_files = [os.path.join(directory_path, f"{project}.csv") for project in projects]

# Read each CSV file into a dataframe
dataframes = []
for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Concatenate the dataframes into a single dataframe
concatenated_df = pd.concat(dataframes)

# Output the concatenated dataframe as a new CSV file
output_file = os.path.join(os.path.dirname(csv_files[0]), f"Master_{tech}_{version}.csv")
concatenated_df.to_csv(output_file, index=False)