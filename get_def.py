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

    all_parts = [
        'Noun', 
        'Verb', 
        'Adjective', 
        'Adverb', 
        'Preposition', 
        'Conjunction', 
        'Interjection'
        ]

    forms = []
    for form in soup.select('span.mw-headline'):
        if form.text in all_parts and form.text not in forms:
            forms.append(form.text)
            block = [form.text]
            elem = form.parent
            while True:
                if elem.name == 'p':
                    print(elem.text)
                    block.append(elem.text)
                if elem.name == 'ol':
                    list_of_def = {
                        'list': elem
                    }
                    block.append(list_of_def)
                    forms.append(block)
                    break
                else:
                    elem = elem.next_sibling.next_sibling
  

    