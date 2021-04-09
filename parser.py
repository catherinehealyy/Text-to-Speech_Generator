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
    url = input("Enter the url of the website you want spoken or press enter: ")
    for u in url:
        response = request.urlopen(u)
        raw = raw + response.read().decode('utf8')

    lines = nltk.line_tokenize(some_text)
    words = nltk.word_tokenize(some_text)
    return words


parser()