import pandas as pd
import os

df = pd.read_excel('data/input/projects.xlsx')
projects = df['solar'].tolist()
projects = projects[:23]
print(projects)

# writing all files to a concatenated file
directory_path = "gpt_analyse/output/summarise_project"
csv_files = [os.path.join(directory_path, f"{project}.csv") for project in projects]

# Read each CSV file into a dataframe
dataframes = []
for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Concatenate the dataframes into a single dataframe
concatenated_df = pd.concat(dataframes)

# Output the concatenated dataframe as a new CSV file
output_file = os.path.join(os.path.dirname(csv_files[0]), "Master_solar.csv")
concatenated_df.to_csv(output_file, index=False)