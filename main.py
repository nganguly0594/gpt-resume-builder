import openai
import config
from pdf_creator import createPDF

#API key to use OpenAI
openai.api_key = config.OPENAI_API_KEY

#Text generation function
def generate(PROMPT, MAX_TOKENS):
    response = openai.Completion.create(
        #Newest free GPT model
        model='gpt-3.5-turbo-instruct',

        #Customized prompt
        prompt=PROMPT,

        #Maximum number of tokens for response
        max_tokens=MAX_TOKENS
    )
    
    return response['choices'][0].text.strip()

#Get all the required information from the user
with open('questions.txt', 'r') as f:
    questions = f.readlines()

#Pose question to user
def ask(QUESTION_NUMBER):
    question = questions[QUESTION_NUMBER].strip() + ' '
    return input(question)

name = ask(0)
print()
location = ask(1)
print()
phone_number = ask(2)
print()
email = ask(3)
print()
important_links = ask(4)
print()
skills = ask(5)
print()
education = ask(6)
print()

#Used to collect long answer question responses
def collect_long_answers(QUESTION_NUMBER):
    answers = []
    
    print(questions[QUESTION_NUMBER].strip() + ' ')

    while True:
        experience = input("\nPlease provide your experience or type 'Done' to finish:\n")
        if experience.strip().lower() == 'done':
            break
        answers.append(experience)
    
    return answers

experiences = collect_long_answers(7)
print()
projects = collect_long_answers(8)
print()
activities = collect_long_answers(9)
print()

#All the following code is to format the info for exporting to pdf

#Name extraction
name_prompt = """\"\"\"
""" + name + """
\"\"\"

Respond in ONLY 2 words with the name in the above text without punctuation.
"""
extracted_name = generate(name_prompt, 10)

#Contact info formatting
contact_prompt = """\"\"\"
""" + location + """ """ + phone_number + """ """ + email + """ """ + important_links + """
\"\"\"

Format the above information into the below format:

\"\"\"
City, State Abbreviation, Country | +1 (xxx) xxx-xxxx | Personal Email | Important Link | Important Link
\"\"\"

The links shouldn't be linked and if the full home address is provided then only take the city and get the state and country from that. Return it without saying anything else and not in code.
"""
formatted_contact_info = generate(contact_prompt, 80)

#Professional summary synthesis
summary_prompt = """\"\"\"\nEducation History:\n""" + education + """\nSkills:\n""" + skills + """\nWork Experience:\n"""

for i in experiences:
    summary_prompt += i + "\n"

summary_prompt += """\nProjects:\n"""

for i in projects:
    summary_prompt += i + "\n"

summary_prompt += """\nActivities and Volunteer Experience:\n"""

for i in activities:
    summary_prompt += i + "\n"

summary_prompt += """\n\"\"\"

Write me a 2 sentence professional summary for my resume. Make sure to include my school, major, and expected year of graduation, and a very very brief abstraction of what I'm interested in and say that I'm seeking jobs.
"""
synthesized_summary = generate(summary_prompt, 100)

#Skills organization
skills_prompt = """\"\"\"\n""" + skills + """\n\"\"\"

Using the list of skills above, create a resume skills section in the same format as provided below:

\"\"\"
X: Skill 1, Skill 2, Skill 3
Y: Skill 1, Skill 2, Skill 3
Z: Skill 1, Skill 2, Skill 3
\"\"\"

The skill sections can include things such as Languages, Competencies, Professional Skills, Certifications, and Licenses. Make sure the similar skills are on the same line as the category title. Return it without saying anything else.
"""
organized_skills = generate(skills_prompt, 100)

#Education formatting
education_prompt = """\"\"\"\n""" + education + """\n\"\"\"

Format the above information into the below format:

\"\"\"
Type of Degree (Only Abbreviation), Major (Only full form), School/Institution
- GPA, achievements, honors, awards (everything in ONLY 1 bullet point)
- Relevant coursework: Course 1, Course 2, etc.
\"\"\"

If there is no information on GPA, achievements, honors, or awards then only include bullet point 2. Make sure there is type of degree, major, and school. Return it without saying anything else and not in code.
"""
education_date_prompt = """\"\"\"\n""" + education + """\n\"\"\"

Extract the above graduation date into the same format as below:

\"\"\"
Expected Feb 2005
\"\"\"

Return EXACTLY 3 words including expected and no punctuation.
"""
formatted_education = generate(education_prompt, 75)
extracted_education_date = generate(education_date_prompt, 10)

#Experience formatting
def format_experience(EXPERIENCE):
    experience_prompt = """\"\"\"\n""" + EXPERIENCE + """\n\"\"\"

    Format the above information into a resume work experience like the below format with each thing on a different line:

    \"\"\"
    ONLY Company Name
    Position/Role
    ONLY 3 descriptive bullet points talking about the experience with buzzwords
    \"\"\"

    The bullet points should end without periods. Return it without saying anything else.
    """

    experience_date_prompt = """\"\"\"\n""" + EXPERIENCE + """\n\"\"\"

    Format the above dates of the experience into a 3 letter month and year with a dash separating them like below:

    \"\"\"
    Jan 2005 - Sep 2006
    \"\"\"

    Return it without saying anything else.
    """

    unprocessed_experience = generate(experience_prompt, 100)

    lines = unprocessed_experience.split("\n")
    filtered_lines = []
    for line in lines:
        if not len(line.strip()) == 0 and not '"""' in line:
            filtered_lines.append(line)


    experience_list = ["\n".join(filtered_lines), generate(experience_date_prompt, 10)]

    return experience_list

formatted_experiences = []

for work in experiences:
    formatted_experiences.append(format_experience(work))

#Project formatting
def format_project(PROJECT):
    project_prompt = """\"\"\"\n""" + PROJECT + """\n\"\"\"

    Format the above information into a resume project experience like the below format with each thing on a different line:

    \"\"\"
    ONLY Project Name
    ONLY 3 descriptive bullet points talking about the experience with buzzwords
    \"\"\"

    The bullet points should end without periods. Return it without saying anything else.
    """

    project_date_prompt = """\"\"\"\n""" + PROJECT + """\n\"\"\"

    Format the above dates of the experience into a 3 letter month and year with a dash separating them like below:

    \"\"\"
    Jan 2005 - Sep 2006
    \"\"\"

    Return it without saying anything else.
    """

    unprocessed_project = generate(project_prompt, 100)

    lines = unprocessed_project.split("\n")
    filtered_lines = []
    for line in lines:
        if not len(line.strip()) == 0 and not '"""' in line:
            filtered_lines.append(line)


    project_list = ["\n".join(filtered_lines), generate(project_date_prompt, 10)]

    return project_list

formatted_projects = []

for project in projects:
    formatted_projects.append(format_project(project))

#Activity formatting
formatted_activities = []

for activity in activities:
    formatted_activities.append(format_experience(activity))

#Compile all the information
FULLCONTENTLIST = {'Name': extracted_name,
                   'Contact Info': formatted_contact_info,
                   'Summary': synthesized_summary,
                   'Skills': organized_skills,
                   'Education': formatted_education,
                   'Education Date': extracted_education_date,
                   'Work Experiences': formatted_experiences}

if not len(formatted_projects) == 0:
    FULLCONTENTLIST['Projects'] = formatted_projects

if not len(formatted_activities) == 0:
    FULLCONTENTLIST['Activities'] = formatted_activities

#Build the PDF
createPDF(FULLCONTENTLIST)