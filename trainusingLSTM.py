

### importing the libraries
import pandas as pd
import pickle
from urllib.parse import urlparse, urlencode

import tensorflow as tf
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense


import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import numpy as np

###set the random seed
tf.random.set_seed(42)
np.random.seed(42)



###read and process the data
df = pd.read_csv('finaldata.csv')
x= df['url']
y = df['label']

voc_size = 10000
messages = x.copy()

ps = PorterStemmer()
corpus = []
for i in range(0, len(messages)):
    review = re.sub('[^a-zA-Z]',' ',urlparse(messages[i]).netloc)
    review = review.lower()
    review = review.split()
    review=' '.join(review)
    corpus.append(review)

onehot_repr=[one_hot(words,voc_size)for words in corpus]
sent_length = 50
embedded_docs= pad_sequences(onehot_repr,padding='pre',maxlen=sent_length)

x_final = np.array(embedded_docs)
y_final  = np.array(y)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x_final,y_final,test_size=0.20,random_state=42)


#make the model and train it
embedding_vector_features=100
model = Sequential()
model.add(Embedding(voc_size,embedding_vector_features,input_length=sent_length))
model.add(LSTM(100))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])


model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=10,batch_size=64)

y_pred=model.predict(x_test) 
classes_y=np.round(y_pred).astype(int)

model.save('model.h5')


    
from sklearn.metrics import confusion_matrix
confusion_n = confusion_matrix(y_test,classes_y)
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, classes_y))
