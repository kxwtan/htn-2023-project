import cohere # run pip install cohere before you run this
from dotenv import load_dotenv
import os

load_dotenv("../.env")


def generateWarning():
    co = cohere.Client(os.getenv("COHERE_KEY"))
    story = co.generate('''
    In a funny way, give a warning for getting too close to something.
    ''',
                stop_sequences=['\n', "."], max_tokens=300)
    print(story.generations[0].text)
    return story.generations[0].text
