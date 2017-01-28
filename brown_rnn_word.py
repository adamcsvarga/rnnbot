#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 15:27:06 2017

Word-based RNN LM training

@author: vurga
"""

from nltk.corpus import brown
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Dropout
from keras.callbacks import ModelCheckpoint
import numpy as np
import theano
## Enable multi-threaded training
theano.config.openmp = True

## Load data and get list of unique words
corpus = [w.lower() for w in brown.words()[:int(len(brown.words())*.025)]] ## use only 2.5% due to memory issues (ca. 250k words)
allwords = list(set(corpus))

## Create word -> int and int -> word mappings
myrange = range(0, len(allwords))
myzip = zip(allwords, myrange)
worddict = dict(myzip)
myzip = zip(myrange, allwords)
dictword = dict(myzip)
## Map text to ints
fulltext = [worddict[word] for word in corpus]

## Create training data
seqlen = 10 ## use 10 words to predict next
dataX = []
dataY = []
for i in range(0, len(fulltext) - seqlen, 1):
    dataX.append(fulltext[i:i+seqlen])
    dataY.append(fulltext[i+seqlen])

## Convert to 1-hot encoding
y = to_categorical(dataY)

## Reshape and normalize
x = np.reshape(dataX, (len(dataX), seqlen, 1))
x = x/float(len(worddict))

## Build model: LSTM w\ 256 units & 0.2 dropout + output softmax layer
model = Sequential()
model.add(LSTM(256, input_shape=(x.shape[1], x.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

## Train the model for 80 epochs
model.fit(x, y, nb_epoch=80, batch_size=128)
model.save("word_model_80.hdf5")

# Load and compile model if there's a previously trained one available
#model.load_weights('word_model_80.hdf5')
#model.compile(loss="categorical_crossentropy", optimizer="adam")

## Tweet generation
with open('twitterbot.txt', 'w'):
     pass
## Get 30 tweets     
for j in range(0, 30):
    ## Initial random sequence to use as the seed of generation
    output = dataX[np.random.randint(0, len(dataX) - 1)]
    output_str = ""
    
    ## Max length should be 140 characters
    while len(output_str) <= 140:
        ## Reshape and normalize seed
        candidate = np.reshape(output, (1, seqlen, 1)) 
        candidate = candidate /float(len(worddict))
        ## Get prediction
        prediction = model.predict(candidate)
        ## Introduce some noise in order to avoid always picking the same word
        answer = np.random.choice(a=list(dictword.keys()), p=prediction[0, :])
        ## Append to output string
        output.append(answer)
        output_str += dictword[answer] + ' '
        ## Shift seed for next prediction
        output = output[1:]

    ## Delete stuff after last space and write to file
    output_str = ' '.join(output_str.split()[:-1])
    with open('twitterbot.txt', 'a+') as target:
        target.write(output_str + '\n')
    
