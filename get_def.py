import requests
from bs4 import BeautifulSoup
import re

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
    # The parts of speach in the english language.
    all_parts = [
        'Noun', 
        'Verb', 
        'Adjective', 
        'Adverb', 
        'Preposition', 
        'Conjunction', 
        'Interjection'
        ]

    # Loop through all headers in dictionary entry that 
    # contain a part of speach, adding to list of forms for that
    # word if not already there - repeats mean it is a different
    # language. Ex: First "Noun" header is in the English section,
    # which is what we want. Next "Noun" is in a different language
    # section, i.e., "French" or "Old English".
    # There are no sections separating languages, so this is a work-
    # around for determining when to stop scanning document.
    unique_forms = []
    defintion = []
    for form in soup.select('span.mw-headline'):
        if form.text in all_parts and form.text not in unique_forms:
            unique_forms.append(form.text)
            section = [form.text]
            elem = form.parent
            while True:
                if elem.name == 'p':
                    section.append(elem.text)
                if elem.name == 'ol':
                    for ul in elem.select('ul'):
                        ul.decompose()
                    for dd in elem.select('dd'):
                        dd.decompose()
                    for dl in elem.select('dl'):
                        dl.decompose()

                    list_of_def = []
                    for li in elem.select('li'):
                        li = re.sub(r'\n\s*\n', r'\n\n', li.get_text().strip(), flags=re.M)
                        list_of_def.append(li)
                   
                    section.append(list_of_def)
                    defintion.append(section)
                    break
                else:
                    elem = elem.next_sibling.next_sibling
    
    # Display word and its definition.
    print("Definition of",word,":\n")
    i = 0
    while i < len(defintion):
        print("\n")
        print(defintion[i][0])
        print(defintion[i][1])
        j = 1
        for li in defintion[i][2]:
            print("  ",str(j),li)
            j+=1
        i+=1
  
# remove all children from dom or <dl>
# note: make a flag that returns shortened definiton
