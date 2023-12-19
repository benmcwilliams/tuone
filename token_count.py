import tiktoken
import pandas as pd

def read_file(file_path):
    df_all = pd.read_csv(file_path)
    df = df_all.loc[:6]
    return {
    'title': df['title'].tolist(),
    'date': df['date'].tolist(),
    'text': df['text'].tolist()
    }

def num_tokens_from_string(string: str, encoding):
    """Returns the number of tokens in a text string."""
    return len(encoding.encode(string))

tech = 'battery'

df = pd.read_excel('data/input/projects.xlsx')
projects = df[tech].tolist()

for project in projects:
  
    file_path = 'data/output/project/{}/{}.csv'.format(tech,project)
    file_contents = read_file(file_path)
    file_string = str(file_contents)

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-1106")
    token_counts = num_tokens_from_string(file_string,encoding)

    print(project, token_counts)