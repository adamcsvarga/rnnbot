#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 15:27:06 2017

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
# enable multi-threaded training
theano.config.openmp = True

corpus = [w.lower() for w in brown.words()[:int(len(brown.words())*.025)]]
allwords = list(set(corpus))

myrange = range(0, len(allwords))
myzip = zip(allwords, myrange)
worddict = dict(myzip)
myzip = zip(myrange, allwords)
dictword = dict(myzip)
fulltext = [worddict[word] for word in corpus]

seqlen = 10
dataX = []
dataY = []
for i in range(0, len(fulltext) - seqlen, 1):
    dataX.append(fulltext[i:i+seqlen])
    dataY.append(fulltext[i+seqlen])

y = to_categorical(dataY)

x = np.reshape(dataX, (len(dataX), seqlen, 1))
x = x/float(len(worddict))


model = Sequential()
model.add(LSTM(256, input_shape=(x.shape[1], x.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
### define the checkpoint
#filepath="10word-{epoch:02d}-{loss:.4f}.hdf5"
#checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
#callbacks_list = [checkpoint]
### fit the model
#model.fit(x, y, nb_epoch=80, batch_size=128, callbacks=callbacks_list)

# load model
model.load_weights('10word-79-1.7100.hdf5')
model.compile(loss="categorical_crossentropy", optimizer="adam")



## tweet generation
with open('twitterbot.txt', 'w'):
     pass
for j in range(0, 30):
    output = dataX[np.random.randint(0, len(dataX) - 1)]
    output_str = ""
    
    while len(output_str) <= 140:
        candidate = np.reshape(output, (1, seqlen, 1)) 
        candidate = candidate /float(len(worddict))
        prediction = model.predict(candidate)
        ## introduce some noise in order to avoid always picking the same word
        answer = np.random.choice(a=list(dictword.keys()), p=prediction[0, :])
        #answer = np.argmax(prediction)
        # append to output & output string
        output.append(answer)
        output_str += dictword[answer] + ' '
        output = output[1:]

    ## delete stuff after last space
    output_str = ' '.join(output_str.split()[:-1])
    with open('twitterbot.txt', 'a+') as target:
        target.write(output_str + '\n')
    
