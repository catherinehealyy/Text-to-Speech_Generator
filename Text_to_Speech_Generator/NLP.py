'''
Parser: extract the required information from the input, such as its content and document tree
Structure analyzer: distinguishes the breaks and continuations in a text (most commonly by using punctuation) if  the structure date is not already provided for by the input
Text normalizer: translate the written text as spoken text
'''

written_text = ''  # as tokens?
spoken_text = ''  # as tokens?


def __init__(self, text: str, doctype: str):
    self.written_text = text


def __init__(self, text: list):
    self.written_text.join(text)


