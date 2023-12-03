### Summarise pipeline
### Build your database :) 

summarise_company = 'Northvolt'

version = 'v1'

summarise_company_system_message = f''' You are an energy investment analyst. 
     Your task is to read news article and only return information which is directly relevant to individual manufacturing projects ran by {summarise_company}. 
     Look for information regarding project name, project location, capital investment, plant capacity, 
     type of technology, dates at which announcements were made, dates at which investments were made, dates at which construction 
     and/or operations began, status of the plant (operational, under construction, investment decision taken, or only announced), 
     Return a maximum 300 word summary '''

summarise_company_user_message = "Everything you would like to write before file_contents (ie the scraped data of the company) appears"

summarise_company_model_used = "gpt-3.5-turbo-1106"

### Output csv file pipeline 