### Summarise pipeline
### Build your database :) 

summarise_company = 'Northvolt'

version = 'v1'

summarise_company_system_message = f''' You are an energy investment analyst. 
     Your task is to read news article and only return information which is directly relevant to individual manufacturing projects ran by {summarise_company}. 
     '''

summarise_company_user_message = f"List battery manufacturing projects which {summarise_company} is involved in in Europe"

summarise_company_model_used = "gpt-3.5-turbo-1106"

### Output csv file pipeline 