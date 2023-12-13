from openai import OpenAI
import pandas as pd
import json
import os

df = pd.read_excel('data/input/projects.xlsx')
projects = df['solar'].tolist()

for project in projects:
  print(project)

  file_path = 'data/output/project/solar/{}.csv'.format(project)

  def read_file(file_path):
    df_all = pd.read_csv(file_path)
    df = df_all.loc[:6]
    return {
      'title': df['title'].tolist(),
      'date': df['date'].tolist(),
      'text': df['text'].tolist()
    }

  file_contents = read_file(file_path)

  client = OpenAI(
    api_key="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",
  )

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
      {"role": "system", "content": f'''
       You are an energy investment analyst. 
       Your task is to read news articles and only return information which is directly relevant to specific solar manufacturing projects. 
       I want you to return the following information:

       Project name;
       Name of the Company running the project;
       Country location of the project (country);
       Area location of the project (city)
       Elements of the solar manufacturing value chain covered at the facility (polysilicon, ingot, wafer, cell, module); 
       Capital investment (in million euros, always return only an integer for this value);
       Government subsidies (did the project receive public subsidies, categorical variable with the possible answers: yes/no/uncertain);
       Government subsidies (in million euros);
       Government subsidies geography (this can take one categorical value between European, National, Regional);
       Capacity of the plant (in GW per year, always return only an integer for this value);
       Date on which the project was first announced;
       Investment date or expected investment date (when a company makes the first significant expense on a project, e.g. buying land, hiring consultants);
       Operation start date or expected operation start date (when the factory begins to produce);
       Current status of the project (announced, investment made, operational).

       When prompted, return only a formatted python dictionary with the above information. It is essential that the result can be read by a json.loads() function.  

       This is an example of the outcome I expect:
        "Project name": "ENEL Sicily"
        "Company": "ENEL"
        "Location (country)": "Italy"
        "Location (area)": "Sicily"
        "Manufacturing component(s)": "Cell, module"
        "Capital investment (in million euros)": 200
        "Government subsidies (yes/no/uncertain)": "yes"
        "Government subsidies (in million euros)": 50
        "Government subsidies geography (European, National, Regional)": "European"
        "Capacity (in GW/year)"; 5
        "Announcement date (actual or expected)": "01-03-2017
        "Investment date (actual or expected)": "15-09-2018"
        "Operation date (actual or expected): "01-04-2020"
        "Current status": "operational"
       '''},
      {"role": "user", "content": f"""Tell me about the {project} project. Here are relevant articles,
       they are formatted as a dictionary with article title, date of publication, and main text: {file_contents}. It is essential that you return only a formatted python dictionary, 
       make sure to always use double quotation marks. I want you to return any null values as "null".
"""}
    ],
    temperature=0.2
  )

  content = completion.choices[0].message.content
  #print(content)

  try:
    content_dict = json.loads(content)
  except json.JSONDecodeError:
    print(f"Failed to parse JSON string: {content}")
    raise

  df = pd.DataFrame([content_dict])

  output_folder = 'gpt_analyse/output/summarise_project/solar'
  os.makedirs(output_folder, exist_ok=True)
  output_file_name = f'{project}.csv'
  relative_output_path = os.path.join(output_folder, output_file_name)
  df.to_csv(relative_output_path, index=False)

# writing all files to a concatenated file
directory_path = "gpt_analyse/output/summarise_project/solar"
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


battery_prompt = f'''
       You are an energy investment analyst. 
       Your task is to read news articles and only return information which is directly relevant to specific battery manufacturing projects. 
       I want you to return the following information:

       Project name;
       Name of the Company running the project;
       Country location of the project (country);
       Area location of the project (city)
       Elements of the battery manufacturing value chain covered at the facility (cathode/anode active material manufacture, cell manufacture or fabrication, module assembly); 
       Capital investment (in billion euros, always return only an integer for this value);
       Government subsidies (did the project receive public subsidies, categorical variable with the possible answers: yes/no/uncertain);
       Government subsidies (in billion euros);
       Government subsidies geography (this can take one categorical value between European, National, Regional);
       Capacity of the plant (in GWh per year, always return only an integer for this value);
       Date on which the project was first announced;
       Investment date or expected investment date (when a company makes the first significant expense on a project, e.g. buying land, hiring consultants));
       Operation start date or expected operation start date (when the factory begins to produce batteries);
       Current status of the project (announced, investment made, operational).

       When prompted, return only a formatted python dictionary with the above information. It is essential that the result can be read by a json.loads() function.  

       This is an example of the outcome I expect:
        "Project name": "Valencia"
        "Company": "Northvolt"
        "Location (country)": "Sweden"
        "Location (area)": "Skellefteå"
        "Manufacturing component(s)": "Cell manufacturing, module assembly"
        "Capital investment (in billion euros)": 4
        "Government subsidies (yes/no/uncertain)": "yes"
        "Government subsidies (in billion euros)": 0.5
        "Government subsidies geography (European, National, Regional)": "European"
        "Capacity (in GWh/year)"; 40
        "Announcement date (actual or expected)": "01-03-2017
        "Investment date (actual or expected)": "15-09-2018"
        "Operation date (actual or expected): "01-04-2020"
        "Current status": "operational"
       '''