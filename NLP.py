import nltk
import pathlib
import num2word
from urllib import request


class NLP:
    words = []
    structured_words = []
    normalized_words = []

    def __init__(self):
        if pathlib.Path("text_to_speech.txt").exists():
            with open("text_to_speech.txt", "r") as text:
                some_text = text.read()
        else:
            option = input("How would you like to input the text? \n A) Through a URL \n B) By typing it in \n")
            print(option)
            if option.lower() == "a":
                url = ''
                url = input("Please enter the url of the website you want spoken.\n")
                lines = ''
                try:
                    response = request.urlopen(url)
                    raw = response.read().decode('utf8')
                except request.HTTPError as exception:
                    print(exception)
                for i in range(len(raw)):
                    if raw[i] == ">" and raw[i + 1] != "<":
                        if raw[i - 8:i] == "<script>":
                            continue
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
            elif option.lower() == "b":
                some_text = input("Please enter the text you would like converted to speech.\n")

        self.words = nltk.word_tokenize(some_text)

    def structure_analyzer(self):

        for i in range(len(self.words)):
            if self.words[i] == '.':
                self.structured_words.append('<break,sent_end,2>')
            elif self.words[i] == '?':
                for j in range(len(self.structured_words) - 1, 0, -1):
                    if self.structured_words[j][:2] == '<b':
                        self.structured_words.insert(j + 1, "<question>")
                        break
                self.structured_words.append('<break,question,2>')
            elif self.words[i] == '!':
                for j in range(len(self.structured_words) - 1, 0, -1):
                    if self.structured_words[j][:2] == '<b':
                        self.structured_words.insert(j + 1, "<exclamation>")
                        break
                self.structured_words.append('<break,exclamation,2>')
            elif self.words[i] == ',':
                self.structured_words.append('<break,comma,1>')
            elif self.words[i] == ';':
                self.structured_words.append('<break,semicolon,1.5>')
            elif self.words[i] == ':':
                self.structured_words.append('<break,colon,1.5>')
            elif self.words[i][0] == "'":
                del self.structured_words[-1]
                new_str = self.words[i - 1] + self.words[i]
                self.structured_words.append(new_str)
            else:
                self.structured_words.append(self.words[i])
