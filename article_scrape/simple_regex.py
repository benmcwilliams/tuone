import re

def extract_projects(file_path):
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Define regex pattern for project names
    # Example pattern: 'Project [Capitalized Words]' or 'Initiative: [Any Words]'
    project_pattern = r'project\s[A-Z][a-z]+|\b[A-Z][a-z]+\sproject\b|Initiative:\s[\w\s]+'

    # Find all matches
    projects = re.findall(project_pattern, text)

    # Post-process: Remove duplicates and clean names
    projects = list(set(projects))  # Remove duplicates
    projects = [project.strip() for project in projects]  # Clean whitespace

    return projects

# Example usage
file_path = 'freyr.txt'
project_list = extract_projects(file_path)
for project in project_list:
    print(project)

print('yello')