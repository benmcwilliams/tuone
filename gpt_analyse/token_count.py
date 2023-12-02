import tiktoken
company = 'catl'

# read in text file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

file_contents = read_file('/Users/ben/Documents/bruegel/DATAn/WORKING/TUONE/tuone/article_scrape/output/company/{}.txt'.format(company))

# count tokens 
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def num_tokens_from_string(string: str, encoding):
    """Returns the number of tokens in a text string."""
    return len(encoding.encode(string))

token_counts = num_tokens_from_string(file_contents,encoding)

print(token_counts)