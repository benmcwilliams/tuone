from openai import OpenAI
import pandas as pd
import json

project = 'CALB Sines'

#file_contents = read_file('/Users/ben/Documents/bruegel/DATAn/WORKING/TUONE/tuone/article_scrape/output/project/{}.txt'.format(project))
file_path = 'C:/Users/Samsung/OneDrive/Desktop/Projects/tuone/tuone/data/output/project/{}.txt'.format(project)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

file_contents = read_file(file_path)

client = OpenAI(
    api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  messages=[
    {"role": "system", "content": f'''
     You are an energy investment analyst. 
     Your task is to read news article and only return information which is directly relevant to specific battery manufacturing projects. 
     Return the following information:
     Project name;
     Name of the Company running the project;
     Location of the project (country, city);
     Elements of the battery manufacturing value chain covered; 
     Capital investment (in billion euros);
     Government subsidies (yes/no/uncertain);
     Government subsidies (in billion euros);
     Government subsidies framework (European, National, Regional);
     Capacity of the plant (GWh/year);
     Date on which the project was first announced;
     Investment date or expected investment date;
     Manufactury plant construction start date or expected construction start date;
     Operation start date or expected operation start date;
     Current status of the project (announced, investment decision taken, under construction, operational).

     This is an example of the outcome I expect:
     Project name: Valencia
      Name of the Company running the project: Northvolt
      Location of the project (country, city): Sweden, Skellefteå
      Elements of the battery manufacturing value chain covered: Cell manufacturing
      Capital investment (in billion euros): 4
      Government subsidies (yes/no/uncertain): yes
      Government subsidies (in billion euros): 0.5
      Government subsidies framework (European, National, Regional): European
      Capacity of the plant (GWh/year): 16
      Date on which the project was first announced: 2017
      Investment date or expected investment date: 2018
      Manufactury plant construction start date or expected construction start date: 2018
      Operation start date or expected operation start date: 2020
      Current status of the project (announced, investment decision taken, under construction, operational): operational
     '''},
    {"role": "user", "content": f"""Tell me about the {project} project: {file_contents}. Format your output as a dictionary"""}
  ]
)

content = completion.choices[0].message.content
project_info_dict = json.loads(content)
df = pd.DataFrame([project_info_dict])

output_file_path = 'C:/Users/Samsung/OneDrive/Desktop/Projects/tuone/tuone/gpt_analyse/output/summarise_project/'
output_file_name = 'Test1.csv'
relative_output_path = f'{output_file_path}/{output_file_name}'
df.to_csv(relative_output_path, index=False) 