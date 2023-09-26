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

prompt = """Say this is a test."""
max_tokens = 5
mylist = generate(prompt, max_tokens)

for i in mylist:
    print(i)