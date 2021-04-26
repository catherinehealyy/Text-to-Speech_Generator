import pyaudio
import numpy as np
import wave
import math
import random
from time import sleep
import pylab as pl
import pathlib
import os

random.seed()

# This is needed for rescaling
MAX_AMP = 2**15 - 1

class sound_dict(pyaudio.PyAudio):
    #diphones = []

    def __init__(self, channels=1, rate=48000, chunk=256, format=pyaudio.paInt16):
        # Initialise the parent class
        pyaudio.PyAudio.__init__(self)
        # Set the format to that specified
        self.chan = channels
        self.rate = rate
        self.chunk = chunk
        self.format = format
        self.nptype = np.int16
        # Set the curent data to an empty array of the correct type
        self.data = np.array([], dtype=self.nptype)
        # No streams are open at the moment
        self.istream = None
        self.ostream = None
        # a counter for referencing the data in chunks
        self.chunk_index = 0

    def play(self):
        # Open an outputstream
        self.open_output_stream()
        # Reset the chunk counter to 0
        self.chunk_index = 0
        print("Playing...")
        # Loop (potentially forever)
        while True:
            # Try to put output a chunk
            try:
                self.put_chunk()
            # If we run out of data to output, break out of the loop
            except IndexError:
                break

        sleep(0.4)  # hack to work around a bug in some (non-blocking) audio hardware
        print("Stopped playing")
        # Close the output stream
        self.close_output_stream()

    def load(self, file):
        wf = wave.open("diphones/" + file, "rb")

        # Get information from the files header
        self.format = self.get_format_from_width(wf.getsampwidth())
        self.nptype = np.int16
        self.chan = wf.getnchannels()
        self.rate = wf.getframerate()

        # Set the internal data attribute to an empty array of the right type
        self.data = np.array([], dtype=self.nptype)

        # Read a chunk of data from the file
        raw = wf.readframes(self.chunk)

        # Loop while there is data in the file
        while raw:
            # Convert the raw data to a numpy array
            array = np.frombuffer(raw, dtype=np.int16)
            # Append the array to the class data attribute
            self.data = np.append(self.data, array)
            # Read the next chunk, ready for the next loop iteration
            raw = wf.readframes(self.chunk)
        # Close the file
        wf.close()

    def open_output_stream(self):
        self.ostream = self.open(format=self.format,
                                 channels=self.chan,
                                 rate=self.rate,
                                 output=True)
        self.chunk_index = 0

    def close_output_stream(self):
        self.ostream.close()
        self.ostream = None

    def put_chunk(self):
        slice_from = self.chunk_index*self.chunk
        slice_to = slice_from + self.chunk
        # Slicing a numpy array out of bounds doesn't seem to raise an
        # index error, so we explicitly test and raise the error ourselves
        if slice_to > self.data.shape[0]:
            raise IndexError
        array = self.data[slice_from:slice_to]
        self.ostream.write(array.tostring())
        self.chunk_index += 1

    def test(self):
        print("test")




class Synth:
    def __init__(self):
        self.diphones = {}
        self.diphones_wavs = self.create_dict()

    def create_dict(self):
        if not pathlib.Path("diphones").exists():
            print("The diphone file is not available.")
            return

        tmpaudio = sound_dict(rate=16000)

        for root, dirs, files in os.walk("diphones", topdown=False):
            for file in files:
                diphone = file[:-4]
                tmpaudio.load(file)
                self.diphones[diphone] = tmpaudio.data
        # TODO: fix the times in nlp
        length = 16000 * 0.1  # sample rate = 16000, 100ms = 0.1s
        self.diphones['<beginning>'] = np.zeros(int(length), tmpaudio.nptype)
        self.diphones['<space>'] = np.zeros(int(length), tmpaudio.nptype)
        self.diphones['<end>'] = np.zeros(int(length), tmpaudio.nptype)
        length = 16000 * 0.2
        self.diphones['<break,comma,1>'] = np.zeros(int(length), tmpaudio.nptype)
        length = 16000 * 0.3
        self.diphones['<break,semicolon,1.5>'] = np.zeros(int(length), tmpaudio.nptype)
        self.diphones['<break,colon,1.5>>'] = np.zeros(int(length), tmpaudio.nptype)
        length = 16000 * 0.4
        self.diphones['<break,sent_end,2>'] = np.zeros(int(length), tmpaudio.nptype)
        self.diphones['<break,question,2>'] = np.zeros(int(length), tmpaudio.nptype)
        self.diphones['<break,exclamation,2>'] = np.zeros(int(length), tmpaudio.nptype)







