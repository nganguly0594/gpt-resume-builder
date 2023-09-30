from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Spacer, Table
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph

def createPDF(CONTENTLIST):
    #Sets all the font sizes and types
    styles = getSampleStyleSheet()
    custom_styles = {
        'Title': ParagraphStyle(
            name='Title',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=16,
        ),
        'SectionTitle': ParagraphStyle(
            name='SectionTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
        ),
        'Bold': ParagraphStyle(
            name='Bold',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
        ),
        'Italic': ParagraphStyle(
            name='Italic',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=10,
        ),
        'Regular': ParagraphStyle(
            name='Regular',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
        )
    }

    #Creates a letter size pdf
    pdf = SimpleDocTemplate('resume.pdf', pagesize=letter)

    # Creates a PageTemplate with custom margins
    MARGIN = 0.5 * inch
    FRAME = Frame(x1=MARGIN, y1=MARGIN, width=letter[0] - (MARGIN * 2), height=letter[1] - (MARGIN * 2))

    pdf.addPageTemplates([PageTemplate(frames=FRAME)])

    #Creates a list of flowable items
    flowables = []

    #Handles an error with quotations
    def filter_string(input_string):
        lines = input_string.splitlines()

        filtered_lines = [line for line in lines if '"""' not in line]

        result_string = '\n'.join(filtered_lines)

        return result_string

    #Adds the name of the user
    flowables.append(Paragraph(filter_string(CONTENTLIST['Name']).replace('"', ''), style=custom_styles['Title']))
    flowables.append(Spacer(1, 11))

    #Adds the user's contact info
    contact_parts = filter_string(CONTENTLIST['Contact Info']).split(" | ")
    
    new_parts = []

    for part in contact_parts:
        part = part.strip()
        if 'gmail' in part:
            part = '<a href="mailto:' + part + '">' + part + '</a>'
        elif '.com' in part:
            part = '<a href="https://' + part + '">' + part + '</a>'
        new_parts.append(part)

    new_contact_info = ' | '.join(new_parts)

    flowables.append(Paragraph(new_contact_info, style=custom_styles['Regular']))
    flowables.append(Spacer(1, 11))

    #Adds the user's professional summary
    flowables.append(Paragraph("PROFESSIONAL SUMMARY", style=custom_styles['SectionTitle']))
    flowables.append(Spacer(1, 5))
    flowables.append(Paragraph(filter_string(CONTENTLIST['Summary']).replace('"', ''), style=custom_styles['Regular']))
    flowables.append(Spacer(1, 11))

    #Adds the skills
    flowables.append(Paragraph("SKILLS", style=custom_styles['SectionTitle']))
    flowables.append(Spacer(1, 5))
    
    for skill in filter_string(CONTENTLIST['Skills']).split("\n"):
        flowables.append(Paragraph(skill, style=custom_styles['Regular']))
    
    flowables.append(Spacer(1, 11))
    
    #Adds the education section
    flowables.append(Paragraph("EDUCATION", style=custom_styles['SectionTitle']))
    flowables.append(Spacer(1, 5))

    education_parts = CONTENTLIST['Education'].split("\n")

    education_data = [[Paragraph(education_parts[0], custom_styles['Bold']), Paragraph(CONTENTLIST['Education Date'], custom_styles['Bold'])]]
    education_table = Table(education_data, colWidths=[5.9 * inch, 1.6 * inch])
    flowables.append(education_table)

    for i in range(len(education_parts)):
        if i == 0:
            continue
        flowables.append(Paragraph(education_parts[i][2:], custom_styles['Regular'], bulletText='•'))

    flowables.append(Spacer(1, 11))

    #Adds the experiences section
    flowables.append(Paragraph("EXPERIENCE", style=custom_styles['SectionTitle']))
    flowables.append(Spacer(1, 5))

    for work in CONTENTLIST['Work Experiences']:
        work_parts = work[0].split("\n")

        work_data = [[Paragraph(work_parts[0], custom_styles['Bold']), Paragraph(work[1], custom_styles['Bold'])]]
        work_table = Table(work_data, colWidths=[5.9 * inch, 1.6 * inch])
        flowables.append(work_table)

        flowables.append(Paragraph(work_parts[1], style=custom_styles['Italic']))

        for i in range(len(work_parts)):
            if i == 0 or i == 1:
                continue

            flowables.append(Paragraph(work_parts[i][2:], custom_styles['Regular'], bulletText='•'))

        flowables.append(Spacer(1, 11))

    #Adds the projects section
    if not CONTENTLIST.get('Projects', 0) == 0:
        flowables.append(Paragraph("PROJECTS", style=custom_styles['SectionTitle']))
        flowables.append(Spacer(1, 5))

        for project in CONTENTLIST['Projects']:
            project_parts = project[0].split("\n")

            project_data = [[Paragraph(project_parts[0], custom_styles['Bold']), Paragraph(project[1], custom_styles['Bold'])]]
            project_table = Table(project_data, colWidths=[5.9 * inch, 1.6 * inch])
            flowables.append(project_table)

            for i in range(len(project_parts)):
                if i == 0:
                    continue
                flowables.append(Paragraph(project_parts[i][2:], custom_styles['Regular'], bulletText='•'))

            flowables.append(Spacer(1, 11))

    #Adds the activities section
    if not CONTENTLIST.get('Activities', 0) == 0:
        flowables.append(Paragraph("ACTIVITIES", style=custom_styles['SectionTitle']))
        flowables.append(Spacer(1, 5))

        for activity in CONTENTLIST['Activities']:
            activity_parts = activity[0].split("\n")

            activity_data = [[Paragraph(activity_parts[0], custom_styles['Bold']), Paragraph(activity[1], custom_styles['Bold'])]]
            activity_table = Table(activity_data, colWidths=[5.9 * inch, 1.6 * inch])
            flowables.append(activity_table)

            flowables.append(Paragraph(activity_parts[1], style=custom_styles['Italic']))

            for i in range(len(activity_parts)):
                if i == 0 or i == 1:
                    continue
                flowables.append(Paragraph(activity_parts[i][2:], custom_styles['Regular'], bulletText='•'))

            flowables.append(Spacer(1, 11))

    pdf.build(flowables)