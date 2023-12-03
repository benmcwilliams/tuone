from io import StringIO
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

from functions import read_file
from constants import summarise_company, summarise_company_model_used, summarise_company_system_message
from constants import summarise_company_user_message, version

api_key = os.getenv('OPENAI_API_KEY')
file_contents = read_file('C:/Users/Samsung/OneDrive/Desktop/Projects/tuone/tuone/data/output/company/{}.txt'.format(summarise_company))

client = OpenAI()
user_message = summarise_company_user_message + f"{file_contents}"

completion = client.chat.completions.create(
  model=summarise_company_model_used,
  messages=[
    {"role": "system", "content": summarise_company_system_message},
    {"role": "user", "content": user_message}]
)

output_file_path = f'gpt_analyse/output/summarise_company/{summarise_company}_{version}'
with open(output_file_path, 'w') as file:
    file.write(completion.choices[0].message.content)