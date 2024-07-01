# Sensei Resume
This is a prototype ChatGPT-based web application capable of producing a simple resume in pdf format with some GPT prompts that the user answers. The prompt engineering causes slight variations in the output, but it provides a high quality first draft to work with.

[Real Tested Resume Example](https://github.com/nganguly0594/gpt-resume-builder/blob/main/static/resume.jpg)

Go to the website and fill in all the required text fields and wait for about a minute (depending on how much information you input) and it will download the pdf straight to your device. The program uses GPT 4 with engineered prompts to extract data and format it in a clean resume format with articulate wording. Then it uses ReportLab to create a resume, where the links are clickable and everything is formatted based on a specific resume template. The web deployment was completed using the Flask back-end microframework and it was deployed on Render's free tier (site may take some time to load).
