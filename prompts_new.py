# battery_context = {
#     'tech':'battery',
#     'value_chain': 'Elements of the battery manufacturing value chain covered at the facility (cathode/anode active material manufacture, cell manufacture or fabrication, module assembly)',
#     'capacity_unit': 'GWh/year',
#     'example': ''' 
#             "Project name": "Valencia"
#             "Company": "Northvolt"
#             "Location (country)": "Sweden"
#             "Location (area)": "Skellefteå"
#             "Manufacturing component(s)": "Cell manufacturing, module assembly"
#             "Investment": "yes"
#             "Investment type": "Expansion"
#             "Existing Capacity (in GWh/year)"; 10
#             "Planned Future Capacity (in GWh/year)"; 40
#             "Capital investment (in billion euros)": 4
#             "Jobs": 2000,
#             "Announcement date": "01-03-2017
#             "Investment date": "15-09-2018"
#             "Operation date: " "
#             "Current status": "investment made"
#             '''
# }

# solar_context = {
#     'tech':'solar',
#     'value_chain': 'Elements of the solar manufacturing value chain covered at the facility (polysilicon production, ingot/wafer manufacture, cell manufacture or fabrication, module assembly)',
#     'capacity_unit': 'GW/year',
#     'example':'''   
#             "Project name": "ENEL Sicily"
#             "Company": "ENEL"
#             "Location (country)": "Italy"
#             "Location (area)": "Sicily"
#             "Manufacturing component(s)": "Cell manufacturing, Module assembly"
#             "Investment": "yes"
#             "Investment type": "Expansion"
#             "Current Capacity (in GW/year)"; 0
#             "Future Capacity (in GW/year)"; 4
#             "Capital investment (in million euros)": 2000
#             "Jobs": 3000,
#             "Announcement date": "01-03-2017
#             "Investment date": "15-09-2018"
#             "Operation date: "01-04-2020"
#             "Current status": "operational"   '''
# }
# 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

def generate_prompt(context_dict):
    return f'''
        I am an energy investment analyst. I'm ready to assist you in extracting and summarizing key information from your collection of articles on battery production projects in Europe. 
        I'll focus on identifying crucial details such as financial investments, project timelines, partnerships, technological milestones, and any notable environmental or sustainability practices. 
        I will return the relevant information into concise, human-like notes for your convenience in the structure of bullet points.
        '''

#prompt = generate_prompt(solar_context)
#print(prompt)

prompt = '''
        I am an energy investment analyst. I'm ready to assist you in extracting and summarizing key information from your collection of articles on battery production projects in Europe. 
        I'll focus on identifying crucial details such as financial investments, project timelines, partnerships, technological milestones, and any notable environmental or sustainability practices. 
        I will return the relevant information into concise, human-like notes for your convenience in the structure of bullet points.
        '''