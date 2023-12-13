### Summarise pipeline
### Build your database :) 

summarise_company = 'Freyr'

version = 'v1'

summarise_company_system_message = f''' You are an energy investment analyst. 
     Your task is to read news article and return a list of names of projects ran by {summarise_company}. 
     '''

summarise_company_user_message = f"List battery manufacturing projects which {summarise_company} is involved in in Europe. Your output is a list of project names."

summarise_company_model_used = "gpt-3.5-turbo-1106"

### Output csv file pipeline 