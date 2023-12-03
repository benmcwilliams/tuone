from io import StringIO
from openai import OpenAI

project = 'CALB Sines'

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

file_contents = read_file('/Users/ben/Documents/bruegel/DATAn/WORKING/TUONE/tuone/article_scrape/output/project/{}.txt'.format(project))

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
     Company running the project;
     Location of the project;
     Elements of the battery manufacturing value chain covered; 
     Capital investment;
     Any government subsidies the project has recieved;
     Capacity of the plant;
     Date on which the project was first announced;
     Date on which an investment decision was taken, if not yet taken - when is it expected;
     Date on which construction of the manufacturing factory began, if not yet taken - when is it expected;
     Date on which the manufacturing plant began operations, if not yet taken - when is it expected;
     Current status of the project (announced, investment decision taken, under construction, operational);
     Return a maximum 300 word summary. 
     '''},
    {"role": "user", "content": f"""Tell me about the {project} project: {file_contents}"""}
  ]
)

print(completion.choices[0].message)
