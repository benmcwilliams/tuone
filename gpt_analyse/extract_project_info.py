from openai import OpenAI

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Read the contents of your text file
file_contents = read_file('/Users/ben/Documents/bruegel/BING/northvolt.txt')

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": f"Context {file_contents}"},
    {"role": "user", "content": "Return specific project information: project name, country, specific location, current project status, technology used, capital investment, capacity. There may be multiple projects"}
  ]
)

print(completion.choices[0].message)
