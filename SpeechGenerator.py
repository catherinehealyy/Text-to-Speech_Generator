"""
Text-to-phoneme converter:  convert the tokens in the spoken text to pronunciation tokens which will be a sequence of
phonemes

Prosody analyzer: add additional factors to the data set such as pitch, timing, speaking rate, and emphasis
These aspects of a language separate robotic flat speech to a more natural fluid speech, include crossfades,
accounting for unwanted pauses and abruptly starting sounds

Waveform producer: take all the information generated and create the waveforms required for each token, create the
output for the inputted text.

"""
import nltk
from nltk.stem.porter import *
from nltk.corpus import cmudict
import sound_dict_generator
import numpy as np

class SG:
    normalized_words = []
    pronunciation_tokens = []
    post_prosody = []
    cmud = cmudict.dict()
    sound_dict = sound_dict_generator.Synth().diphones

    # THIS IS USED FOR TESTING
    def __init__(self):
        self.normalized_words = ['<beginning>', 'hello', 'there', '<break,comma,1>', 'how', 'are',
                                 'you', 'doing', '<break,sent_end,2>', 'i', 'am', 'good', '<end>']
        # self.normalized_words = ['doctor', 'rabbits', 'email', 'is', 'i', 'l', 'u', 'v', 'c', 'a', 'r' 'r',
        # 'o' 't' 's', 'three', 'zero', 'five', 'at', 'g', 'mail', 'dot', 'c', 'o', 'm', '<break,sent_end,2>', 'you',
        # 'can', 'checkout', 'his', 'website', '<break,comma,1>', 'r', 'a', 'b', 'b', 'i', 't', 'd', 'r', 'dot', 'g',
        # 'o', 'v', '<break,sent_end,2>', 'he', 'uses', 'forty', 'milliliters', 'beakers', 'to', 'find', 'tilde',
        # 'volume', '<break,sent_end,2>', 'he', 'has', '<currency>', 'negative', 'three', 'dollars', 'in', 'his',
        # 'bank', 'account', '<break,sent_end,2>']

    # def __init__(self, n_w: list):
    #     self.normalized_words = n_w

    def text_to_phoneme(self):
        skip = 0
        for w in self.normalized_words:  # get the token from normalized_words
            if w in self.cmud:
                phone = self.cmud[w][0]  # convert tokens to its phoneme form
                for i in range(len(phone)):
                    phone[i] = re.sub("[^a-zA-Z\\s\-]", "", phone[i]).lower()
                self.pronunciation_tokens.append(phone)  # add the phoneme form of the word to pronunciation_tokens
            elif w[0] == '<' and w[-1] == '>':
                self.pronunciation_tokens.append([w])
            else:
                for i in range(len(w)):
                    if skip > 0:
                        skip -= 1
                        continue
                    try:
                        phone = self.cmud[w[i:i+4].lower()][0]
                        skip = 3
                    except KeyError:
                        try:
                            phone = self.cmud[w[i:i+3].lower()][0]
                            skip = 2
                        except KeyError:
                            try:
                                phone = self.cmud[w[i:i+2].lower()][0]
                                skip = 1
                            except KeyError:
                                phone = self.cmud[w[i].lower()][0]
                    for i in range(len(phone)):
                        phone[i] = re.sub("[^a-zA-Z\\s\-]", "", phone[i]).lower()
                    self.pronunciation_tokens.append(phone)
                # TODO: figure out what to do with words not in the cmu dictonary
                #       Possibilities: should we get the root?, use the google converter?


    def prosody_analyzer(self):
        temp = []
        for w in self.pronunciation_tokens:
            if w[0] == "<beginning>" or w[0] == "<end>":
                temp.append('pau')
            elif w[0] == "<break,comma,1>":
                temp.append('pau')
                temp.append('pau')
            elif w[0] == "<break,semicolon,1.5>" or w[0] == "<break,colon,1.5>":
                temp.append('pau')
                temp.append('pau')
                temp.append('pau')
            elif w[0] == "<break,sent_end,2>" or w[0] == "<break,question,2>" or w[0] == "<break,exclamation,2>":
                temp.append('pau')
                temp.append('pau')
                temp.append('pau')
                temp.append('pau')
            else:
                for p in w:
                    temp.append(p)
        for i in range(len(temp)):
            if i != len(temp)-1:
                self.post_prosody.append(temp[i] + '-' + temp[i+1])
        print(self.post_prosody)

        # TODO: add the additional factors to the sounds to create normal sounding speech
        #  in the sound_dict there are different pause times based on the type of pause it is - the issue is that in the
        #  diphones folder there is only one pause-phoneme length for each phoneme so if we can figure out some way to
        #  change that that would make it sound a lot better

        # TODO: add additional factors to the data set such as pitch, timing, speaking rate, and emphasis
        #  there are sentence tags at the beginning of sentences ending with ! and ? so finding a way to manipulate the
        #  sounds with factors (pitch, timing, speaking rate, emphasis) based on that would help a lot too

        # TODO: currently theres no contingency for when the prosody_analyzer encounters the beginning sentence tags
        #  for ! and ?, should they be left in and the tone dealt with in build_d()??


def build_d():
    global array
    sound_dict = sound_dict_generator.Synth().diphones
    p_t = p_t_c.post_prosody
    for w in p_t:
        try:
            array = np.append(array, (sound_dict[w]))
        except KeyError:
            pass
    print(array)

if __name__ == "__main__":
    p_t_c = SG()
    p_t_c.text_to_phoneme()
    p_t_c.prosody_analyzer()

    out = sound_dict_generator.sound_dict(rate=16000)

    array = []

    build_d()

    out.data = array.astype(np.int16)

    out.play()


