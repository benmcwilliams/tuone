import os
import glob
import pandas as pd
import json
from datetime import datetime
from openai import OpenAI
# Assuming you have a way to initialize your OpenAI client
# from openai import OpenAI 

# Define the directories
csv_dir = 'C:/Users/Samsung/OneDrive/Desktop/github/tuone/data/output/project/battery'
json_dir = os.path.join(csv_dir, 'json')
txt_dir = os.path.join(csv_dir, 'txt')

# Ensure the output directories exist
os.makedirs(json_dir, exist_ok=True)
os.makedirs(txt_dir, exist_ok=True)

# Get the list of CSV files in the directory
csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))

client = OpenAI(
    api_key="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",
  )

for csv_file in csv_files:
    # Extract the filename without the extension to use for naming JSON and txt files
    base_filename = os.path.splitext(os.path.basename(csv_file))[0]
    
    df = pd.read_csv(csv_file)

    ##### Extracting the information from the articles #####

    output_data = [] 
    prompt = '''
    I am an energy investment analyst. I'm ready to assist you in extracting and summarizing key information from your collection of articles on battery production projects in Europe. 
    I will return the relevant information into concise, human-like notes. If the information of one or more of the sections is not available, I will write N/A. The notes will be structured into the following sections:
    - Location - in which country and area is the project located. 
    - Capacity - information about the planned capacity of the project. If the project has just began operations, or is expanding, how much of the capacity is currently operational? Units are GW. 
    - Investment amounts - how much capital has been invested into the proejct, or has been announced as a planned investment? Has the project received any subsidies, and from whom? 
    - Project progress - a summary of the project's progress as it moves from a first announcement, to the signing of some preliminary paperwork like Memoranda of Understanding with national governments, as it purchases land, as it begins construction, and as finally the project starts producing batteries. 
    - Project type - is the project a new build where it is constructed from scratch, is it an expansion at an existing battery site, or is it a conversion of a factory that used to produce something else (eg automobile parts) 
    - Value chain stages - there are a few stages that go into manufacturing a battery. Which of the following stages are covered at the facility: 1) cathode and anode manufacturing, 2) cell fabrication, where cathode and anode are combined with an electrolyte, 3) module assembly.
    I will not add any information other than what is covered in the sections, my answer will start with the Location section.
    '''

    for index, article in df.iterrows():
        # Extracting the text content of the article
        file_contents = article['text']
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"""
                Here is the data extracted from the articles related to the project. {file_contents}
                """
                }
            ],
            temperature=0.2)
        
        summary_points = completion.choices[0].message.content

        # Construct the dictionary for JSON
        output_dict = {
            'title': article['title'],
            'url': article['url'],
            'date': article['date'],
            'notes': summary_points
        }
        # Append the dictionary to the list
        output_data.append(output_dict)

    # Write the list of dictionaries to a JSON file
    json_filename = os.path.join(json_dir, f"{base_filename}.json")
    with open(json_filename, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)
    
    print(f"Data extraction and saving to JSON for {base_filename} completed.")

    ##### Consolidating the information #####

    # Helper function to extract the domain name
    def extract_domain_name(url):
        # Remove 'http://' or 'https://' and split the URL to get the domain
        domain = url.split('//')[-1]
        # Split the domain to remove 'www.' if it exists
        domain_parts = domain.split('.')
        if domain_parts[0] == 'www':
            domain_parts.pop(0)
        # Return the first part of the domain (e.g., 'eib' from 'eib.org')
        return domain_parts[0]

    # Helper function to format the date
    def format_date(date_str):
        if date_str and isinstance(date_str, str):  # Check if date_str is a string and not None
            # Define possible date formats
            date_formats = [
                '%Y-%m-%d %H:%M:%S%z',  # Format with timezone
                '%Y-%m-%d %H:%M:%S',    # Format without timezone
                '%Y-%m-%d'               # Format with only date
            ]
            for fmt in date_formats:
                try:
                    # Try to parse the date string with the current format
                    date_obj = datetime.strptime(date_str, fmt)
                    # If successful, format the date as 'year-month-day' and return
                    return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    continue  # If current format doesn't match, try next format
        return "No date provided"  # Return this if no format matched or date_str is not a string or is None

    # Define the sections you want to extract
    sections = ["Location", "Capacity", "Investment amounts", "Project progress", "Project type", "Value chain stages"]

    # Initialize a dictionary to hold the consolidated information
    consolidated_info = {section: [] for section in sections}

    # Process each article
    for article in output_data:
        url = article['url']
        domain_name = extract_domain_name(url)  # Extract the domain name from the URL
        formatted_date = format_date(article['date'])  # Format the date
        notes = article['notes'].split('\n\n')  # Split the notes into sections based on your structure

        # Process each section in the notes
        for note in notes:
            note_lines = note.strip().split('\n')
            if note_lines:  # Check if there's any content in the note
                section_title = note_lines[0].replace(':', '').strip()  # Get the section title
                if section_title in sections:
                    # Add the content of the section to the consolidated info
                    # Include the domain name, URL, and formatted date at the start of the bullet point
                    consolidated_info[section_title].append(
                        f"- [{domain_name}]({url}, {formatted_date}): " + ' '.join(note_lines[1:])
                    )

    # Write the consolidated information to a text file
    txt_filename = os.path.join(txt_dir, f"{base_filename}.txt")
    with open(txt_filename, 'w', encoding='utf-8') as out_file:
        for section, notes in consolidated_info.items():
            out_file.write(f"{section}:\n")
            for note in notes:
                out_file.write(f"{note}\n")
            out_file.write("\n")
    
    print(f"Consolidated information for {base_filename} has been written to TXT.")

print("All files have been processed.")
