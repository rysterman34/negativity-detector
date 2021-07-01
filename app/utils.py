import json
import os, pickle
import pandas as pd
from string import punctuation
import nltk
from nltk.corpus import stopwords
english_stopwords=stopwords.words('english')
nltk.download('wordnet') 
nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


## TO DO 
# ADD tokenizer and model
#LOAD KERAS MODEL
from tensorflow import keras
model = keras.models.load_model('group-model')

# loading
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


def get_base_url(port):
    info = json.load(open(os.path.join(os.environ['HOME'], ".smc", "info.json"), 'r'))
    project_id = info['project_id']
    base_url = "/%s/port/%s/" % (project_id, port)
    return base_url

def allowed_file(filename, ALLOWED_EXTENSIONS=set(['png', 'jpg', 'jpeg'])):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
#function to add correct and or comma
def and_syntax(alist):
    if len(alist) == 1:
        alist = "".join(alist)
        return alist
    elif len(alist) == 2:
        alist = " and ".join(alist)
        return alist
    elif len(alist) > 2:
        alist[-1] = "and " + alist[-1]
        alist = ", ".join(alist)
        return alist
    else:
        return
    
def clean_text(message):
    # first, put text into lowercase
    lower_message = message.lower()
    #remove punctuation
    splitted_message = lower_message.split()
    for ind, word in enumerate(splitted_message):
        new_string=''
        for char in word:
            if char not in punctuation:
                new_string += char
        splitted_message[ind] = new_string
    final = ' '.join(splitted_message)
    return final

def remove_stop_words(message, stopwords):
    words = message.split()
    good_words = []
    for word in words:
        if (word not in stopwords) and (word[0] != "@") and (word[0:4].lower() != "http") and (word.lower() != '#'):
            good_words.append(word)
    return ' '.join(good_words)

def remove_hashtags_atSigns_links(message):
    words = message.split()
    good_words = []
    for word in words:
        if word[0] == "#":
            good_words.append(word[1:])
        elif word[0] != "@":
             if word[0:7] != "http://":
                good_words.append(word)
    return ' '.join(good_words)

def cleanup(message):
    return clean_text(remove_stop_words((message), english_stopwords))

def lemmatizeText(message):
    words = nltk.word_tokenize(message)
    nw = []
    for word in words:
        nw.append(lemmatizer.lemmatize(word))
    return ' '.join(nw)


def predict_text(text):
    text2seqResult=tokenizer.texts_to_sequences([text])
    padded_seq = pad_sequences(text2seqResult, maxlen=35)
    probability = model.predict(padded_seq)
    label = int(probability.round().item())
    return probability,label
