import requests
from bs4 import BeautifulSoup, SoupStrainer
import json

class NoEntry(Exception):
    pass

word = input("Enter a word to view the definition: ")
url = 'https://en.wiktionary.org/wiki/' + word
dictionary_response = requests.get(url)
soup = BeautifulSoup(dictionary_response.content, 'html.parser')

try:
    if soup.find('div', {'class': 'noarticletext'}) is not None:
        raise NoEntry
except NoEntry:
    print("Could not find matching entry in dictionary.")
else:
    all_parts = ['Noun', 'Verb', 'Adjective', 'Adverb', 'Preposition', 'Conjunction', 'Interjection']
    parts_of_speech = [] #list for now to check functionality
    for part_of_speech in soup.select('span.mw-headline'):
        if part_of_speech.text in all_parts and part_of_speech.text not in parts_of_speech:
            parts_of_speech.append(part_of_speech.text)
            print(part_of_speech.text)

    print(len(parts_of_speech))

