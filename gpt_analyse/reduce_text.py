from io import StringIO
from openai import OpenAI

company = 'freyr'

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

file_contents = read_file('/Users/ben/Documents/bruegel/DATAn/WORKING/TUONE/tuone/article_scrape/output/company/{}.txt'.format(company))

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  messages=[
    {"role": "system", "content": f'''
     You are an energy investment analyst. 
     Your task is to read news article and identify information relevant to battery manufacturing projects ran by {company}. 
     Return a list of relevant sentences. 
     '''},
    {"role": "user", "content": f"""{file_contents}"""}
  ]
)

print(completion.choices[0].message)
