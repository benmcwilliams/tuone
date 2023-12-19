from openai import OpenAI
import pandas as pd
import json
import os
from prompts import generate_prompt, battery_context, solar_context

# set this tech to either 'solar' or 'battery'
tech = 'battery'
context = {'solar':solar_context, 
          'battery':battery_context}

system_prompt = generate_prompt(context[tech])
print(system_prompt)

df = pd.read_excel('data/input/projects.xlsx')
projects = df[tech].tolist()
#projects = projects[8:]

for project in projects:
  print(project)
  file_path = 'data/output/project/{}/{}.csv'.format(tech,project)

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
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": f"""Tell me about the {project} project. Here are relevant articles,
       they are formatted as a dictionary with article title, date of publication, and main text: {file_contents}. It is essential that you return only a formatted python dictionary, make sure to always use double quotation marks. Return any null values as "null".
"""}
    ],
    temperature=0.2
  )

  content = completion.choices[0].message.content

  try:
    content_dict = json.loads(content)
  except json.JSONDecodeError:
    print(f"Failed to parse JSON string: {content}")
    raise

  df = pd.DataFrame([content_dict])

  output_folder = f'gpt_analyse/output/summarise_project/{tech}'
  os.makedirs(output_folder, exist_ok=True)
  output_file_name = f'{project}.csv'
  relative_output_path = os.path.join(output_folder, output_file_name)
  df.to_csv(relative_output_path, index=False)