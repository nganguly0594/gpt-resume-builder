import openai
import config

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
'''
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
'''

name = "Giana Xiao"

location = "Naperville, IL, US"

phone_number = "+1 (331) 701-1688"

email = "gianaxiao@gmail.com"

important_links = "www.linkedin.com/in/giana-xiao/"

skills = "English, Chinese, Spanish, Efficiency, Teamwork, Adaptability, Critical Thinking, HIPAA Compliance, Taking Vitals, Bloodwork Preparation, Pharmacy Technician, CPR Training"

education = "I go to University of Illinois Urbana-Champaign, my expected graduation is May 2027, I'm getting a BSLAS degree in MCB, and some relevant courses I'm taking are Integrative Biology and Statistics for Biology. My GPA is 3.9/4.0 and I was on the Dean's List in 2019 and 2020."

experiences = ["At CVS Pharmacy in Woodridge, IL, I worked as a Pharmacy Technician from December 2022 to August 2023. In this role, I prioritized providing excellent customer service to patients by addressing their medication and insurance-related queries. My responsibilities included overseeing various pharmacy areas, such as the pick-up kiosk, drive-thru lane, and packaging stations. I prepared medications for patients by accurately counting, pouring, labeling, and verifying doses. Additionally, I entered patient profiles, billing information, and prescription orders into the pharmacy's software system, ensuring efficient and accurate record-keeping and medication dispensing.",
               "At Villa St. Benedict in Lisle, IL, I worked as both a Server and Resident Assistant from August 2021 to October 2022. My role involved catering to the needs of residents within the on-site restaurant, where I aimed to create a positive and efficient dining experience. I interacted with older residents with patience and provided them with attentive and respectful service. In addition to my serving responsibilities, I also played a crucial part in training new servers, contributing to their successful onboarding and helping maintain the high standards of service at the facility.",
               "I served as a Medical Assistant Intern at Stat! Cardiologist in Lisle, IL, during the period of May 2021 to August 2021. In this role, I worked closely with a Nurse Practitioner, offering valuable support during a range of cardiac medical procedures. My responsibilities included gathering comprehensive patient histories and recording vital signs meticulously, ensuring the availability of detailed records for use in diagnosis and prognosis. I also demonstrated a strong commitment to safety protocols by preparing patient blood samples for laboratory work, highlighting my meticulous attention to detail in this critical aspect of patient care.",
               "At Dr. Rubin’s Mini Medical School in Naperville, IL, I worked as a Medical Apprentice from December 2020 to January 2021. During my tenure, I displayed a keen aptitude for surgical techniques in hands-on sessions, emphasizing precision through activities like dissections, suturing, and laparoscopic surgery simulations. Additionally, I enriched my medical knowledge by participating in a series of informative lectures that covered diverse medical and healthcare topics, including cardiology, neurology, and OB-GYN. This experience allowed me to gain practical skills and a broad understanding of various aspects of the medical field."]

projects = []

activities = ["I held a leadership position at Naperville Central DECA in Naperville: (September 2020 - May 2023) I was the VP of Service and in this role, I actively reached out to event coordinators and volunteer groups to establish collaborations, successfully organizing more than 15 service opportunities. My dedication to service allowed our club to make a meaningful impact in the community. I diligently maintained attendance and financial records, ensuring the smooth functioning of the club. I also provided essential organizational support to fellow board members.",
              "As an Executive Board Member at the Naperville Central Medical Club in Naperville, IL, from August 2021 to May 2023, my primary responsibility was delivering regular, informative presentations on a weekly basis. These presentations were designed to engage and inform participants in the Medical Club throughout the year. My role involved facilitating discussions and sharing valuable insights, contributing to the educational and interactive aspects of the club's activities."]

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
Expected Graduation Feb 2005
\"\"\"

Return EXACTLY 4 words including expected graduation and no punctuation.
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
        if not line.strip().isspace() and not '\"\"\"' in line:
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
        if not line.strip().isspace() and not '\"\"\"' in line:
            filtered_lines.append(line)


    experience_list = ["\n".join(filtered_lines), generate(project_date_prompt, 10)]

    return experience_list

formatted_projects = []

for project in projects:
    formatted_projects.append(format_project(project))

#Activity formatting
formatted_activities = []

for activity in activities:
    formatted_activities.append(format_experience(activity))

print("\nName:\n", extracted_name)
print("\nContact Info:\n", formatted_contact_info)
print("\nProfessional Summary:\n", synthesized_summary)
print("\nSkills:\n", organized_skills)
print("\nEducation History:\n", formatted_education)
print("\nWork Experiences:\n")
for i in formatted_experiences:
    print(i[1])
    print(i[0])
    print()
print("\nProjects:\n")
for i in formatted_projects:
    print(i[1])
    print(i[0])
    print()
print("\nActivities and Volunteer Experiences:\n")
for i in formatted_activities:
    print(i[1])
    print(i[0])
    print()