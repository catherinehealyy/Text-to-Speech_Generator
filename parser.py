import nltk
import pathlib
from urllib import request

def parser():
    some_text = ''
    if pathlib.Path("text_to_speech.txt").exists():
        with open("text_to_speech.txt", "r") as text:
            some_text = text.read()
    else:
        some_text = input("Enter the text you want converted to speech: ")
    url = ''
    url = input("Enter the url of the website you want spoken or press enter: ")
    print(url)
    if url != '':
        lines = ''
        response = request.urlopen(url)
        raw = response.read().decode('utf8')
        for i in range(len(raw)):
            if raw[i] == ">" and raw[i + 1] != "<":
                act = ''
                for j in range(len(raw)):
                    if i + j + 1 >= len(raw):
                        break
                    act = act + raw[i + j + 1]
                    if act[j] == '<':
                        act = act[:len(act) - 1]
                        break
                lines = lines + act
        some_text = lines
    words = nltk.word_tokenize(some_text)
    return words
