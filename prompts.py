battery_context = {
    'tech':'battery',
    'value_chain': 'Elements of the battery manufacturing value chain covered at the facility (cathode/anode active material manufacture, cell manufacture or fabrication, module assembly)',
    'capacity_unit': 'GWh/year',
    'example': ''' 
            "Project name": "Valencia"
            "Company": "Northvolt"
            "Location (country)": "Sweden"
            "Location (area)": "Skellefteå"
            "Manufacturing component(s)": "Cell manufacturing, module assembly"
            "Investment": "yes"
            "Investment type": "Expansion"
            "Existing Capacity (in GWh/year)"; 10
            "Planned Future Capacity (in GWh/year)"; 40
            "Capital investment (in billion euros)": 4
            "Jobs": 2000,
            "Announcement date": "01-03-2017
            "Investment date": "15-09-2018"
            "Operation date: " "
            "Current status": "investment made"
            '''
}

solar_context = {
    'tech':'solar',
    'value_chain': 'Elements of the solar manufacturing value chain covered at the facility (polysilicon production, ingot/wafer manufacture, cell manufacture or fabrication, module assembly)',
    'capacity_unit': 'GW/year',
    'example':'''   
            "Project name": "ENEL Sicily"
            "Company": "ENEL"
            "Location (country)": "Italy"
            "Location (area)": "Sicily"
            "Manufacturing component(s)": "Cell manufacturing, Module assembly"
            "Investment": "yes"
            "Investment type": "Expansion"
            "Current Capacity (in GW/year)"; 0
            "Future Capacity (in GW/year)"; 4
            "Capital investment (in million euros)": 2000
            "Jobs": 3000,
            "Announcement date": "01-03-2017
            "Investment date": "15-09-2018"
            "Operation date: "01-04-2020"
            "Current status": "operational"   '''
}

def generate_prompt(context_dict):
    return f'''
        You are an energy investment analyst. Your task is to read news articles and summarise information which is directly relevant to specific {context_dict['tech']} manufacturing projects in Europe. I want you to return the following project-specific information:

        Project name;
        Name of company responsible for the project;
        Location of the project (country);
        Location of the project (area within country, e.g. city);
        {context_dict['value_chain']}; 
        Capacity of the existing plant (in {context_dict['capacity_unit']}, return only an integer for this value);
        Investment (yes/no, is there a planned investment in the plant?);
        Investment type (Expansion or New Build, is the investment expanding an existing plant or building a new plant?)
        Planned increased capacity of the plant (in {context_dict['capacity_unit']} by how much will the investment increase capacity of the plant, return only an integer for this value);
        Capital investment (in million euros, return only an integer for this value);
        Number of jobs which will be created by the investment (return only an integer for this value);
        Date on which plans for the project were first announced (the earliest date on which a news article was published about the project);
        Investment date (the earliest date on which the first significant project expense is made, e.g. buying land, beginning construction. If no investment has been made yet, return null);
        Operation start date (the date on which the factory began or is expected to begin producing batteries, if the factory is not yet operational, return null);
        Current status of the project (announced, investment made, operational).

        When prompted, return only a formatted python dictionary with the above information. It is essential that the result can be read by a json.loads() function.  

        This is an example of the outcome I expect:
        {context_dict['example']}
        '''

prompt = generate_prompt(solar_context)
print(prompt)