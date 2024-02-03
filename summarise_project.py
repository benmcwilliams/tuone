from openai import OpenAI
import pandas as pd
import json
import os
from prompts import generate_prompt, battery_context, solar_context

prompt = '''
        I am an energy investment analyst. I'm ready to assist you in extracting and summarizing key information from your collection of articles on battery production projects in Europe. 
        I'll focus on identifying crucial details such as financial investments, project timelines, partnerships, technological milestones, and any notable environmental or sustainability practices. 
        I will return the relevant information into concise, human-like notes for your convenience in the structure of bullet points.
        '''

# set this tech to either 'solar' or 'battery'
tech = 'battery'
# context = {'solar':solar_context, 
#           'battery':battery_context}

# system_prompt = generate_prompt(context[tech])
# print(system_prompt)

df = pd.read_excel('data/input/projects.xlsx')
projects = df[tech].tolist()
#projects = projects[8:]

# Here we are calling for each project in the output folder. The content of each file is a csv file with the title, url, date and text of the article.
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


# Set your base directory
base_dir = r'data/output/project/battery'
projects = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

for project in projects:
    print(f"Processing {project}")
    file_path = os.path.join(base_dir, project, f'{project}.csv')
    
    # Read the content of the CSV file
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        articles = list(reader)
    
    # Process each article
    for article in articles:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
              {"role": "system", "content": prompt},
              {"role": "user", "content": f"""
              Here is the data extracted from the articles related to the {project} project. {file_contents}
              """
              }
            ],
            temperature=0.2)
        
        summary_points = completion.choices[0].message.content

        # Construct the dictionary for JSON
        output_dict = {
            'title': article['title'],
            'url': article['url'],
            'date': article['date'],
            'notes': summary_points
        }
        
        # Define the JSON output file path
        output_file_path = os.path.join(base_dir, project, f'{project}_summaries.json')
        
        # Save the output to a JSON file
        with open(output_file_path, mode='a', encoding='utf-8') as f_out:
            json.dump(output_dict, f_out, ensure_ascii=False, indent=4)
            f_out.write('\n')

    print(f"Completed processing for {project}")








# Here we are calling the OpenAI API to generate the summary of the article in bullet points. I would like to create as an output a txt file with 'note in the form of a bullet point',url
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
      {"role": "system", "content": prompt},
      {"role": "user", "content": f"""
       Here is the data extracted from the articles related to the {project} project. {file_contents}
       """
      }
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