import openai
from pdf_creator import createPDF

def process_info(INFOLIST):
    #API key to use OpenAI
    with open("api_key.txt", "r") as file:
        openai.api_key = file.read().strip()

    #Text generation function
    def generate(PROMPT, MAX_TOKENS):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": PROMPT}
            ],
            max_tokens=MAX_TOKENS
        )
        
        return response['choices'][0]['message']['content'].strip()

    name = INFOLIST['name']
    location = INFOLIST['city']
    phone_number = INFOLIST['phone']
    email = INFOLIST['email']
    important_links = INFOLIST.get('links', 'none')
    skills = INFOLIST['skills']
    education = INFOLIST['education']

    def filter_none_strings(input_list):
        new_list = []

        for i in input_list:
            if not 'none' in i and len(i.strip()) > 0:
                new_list.append(i)
        
        return new_list

    work1 = INFOLIST.get('experience-one', 'none')
    work2 = INFOLIST.get('experience-two', 'none')
    work3 = INFOLIST.get('experience-three', 'none')
    work4 = INFOLIST.get('experience-four', 'none')

    unfiltered_experiences = [work1, work2, work3, work4]

    experiences = filter_none_strings(unfiltered_experiences)

    proj1 = INFOLIST.get('project-one', 'none')
    proj2 = INFOLIST.get('project-two', 'none')
    proj3 = INFOLIST.get('project-three', 'none')
    proj4 = INFOLIST.get('project-four', 'none')

    unfiltered_projects = [proj1, proj2, proj3, proj4]

    projects = filter_none_strings(unfiltered_projects)

    act1 = INFOLIST.get('activity-one', 'none')
    act2 = INFOLIST.get('activity-two', 'none')
    act3 = INFOLIST.get('activity-three', 'none')
    act4 = INFOLIST.get('activity-four', 'none')

    unfiltered_activities = [act1, act2, act3, act4]

    activities = filter_none_strings(unfiltered_activities)

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

    Write me a 2 sentence professional summary for my resume similar to the example below. Make it less than 100 tokens, and it should be very vague and high level and shouldn't list my coursework, skills, projects, experiences, or activities. Start with "I am a..." and don't include any quotations.

    \"\"\"
    I am a Computer Science freshman at University of Illinois Urbana-Champaign with strong fundamentals in object-oriented programming, machine learning models, and front-end web development. I am especially passionate about tackling everyday problems with AI solutions and I am looking for opportunities to learn about and apply new technologies.
    \"\"\"
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
