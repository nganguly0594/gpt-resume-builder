import openai

openai.api_key = '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'

def ask_openai():
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt="Say this is a test",
        max_tokens=7,
        temperature=0
    )

    return response['choices'][0].text.strip()

print(ask_openai())