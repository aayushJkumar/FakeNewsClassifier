# -*- coding: utf-8 -*-
"""FakeNewsClassifierUsingLSTM

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FHaCAUGmnRvpXSwRbRJ0wqArUdhVN-Kp
"""

!pip install opendatasets

!pip install -q kaggle

import pandas as pd
import numpy as np
import opendatasets as od

od.download("https://www.kaggle.com/c/fake-news/data#")

df=pd.read_csv("/content/fake-news/train.csv")

df.head()

((df.isnull().sum())/(len(df)))*100

df=df.dropna()

y=df['label']
y.head()

x=df[['title','author','text']]

print(x.shape)
print(y.shape)

import tensorflow as tf

tf.__version__

from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense

voc_size=5000
msg=x.copy()

msg.reset_index(inplace=True)

msg.head()

import nltk
import re
from nltk.corpus import stopwords
nltk.download('stopwords')

from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()
nltk.download('popular')
corpus = []
for i in range(0, len(msg)):
    print(i)
    review = re.sub('[^a-zA-Z]', ' ', msg['title'][i])
    review = review.lower()
    review = review.split()
    
    review = [lemmatizer.lemmatize(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    corpus.append(review)

onehot_repr=[one_hot(words,voc_size)for words in corpus] 
onehot_repr

sent_length=20
embedded_docs=pad_sequences(onehot_repr,padding='pre',maxlen=sent_length)
print(embedded_docs)

embedding_vector_features=40
model=Sequential()
model.add(Embedding(voc_size,embedding_vector_features,input_length=sent_length))
model.add(LSTM(100))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
print(model.summary())

X_final=np.array(embedded_docs)
y_final=np.array(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_final, y_final, test_size=0.33, random_state=42)

model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=50,batch_size=64)

from tensorflow.keras.layers import Dropout
## Creating model
embedding_vector_features=40
model=Sequential()
model.add(Embedding(voc_size,embedding_vector_features,input_length=sent_length))
model.add(Dropout(0.3))
model.add(LSTM(100))
model.add(Dropout(0.3))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=50,batch_size=64)

y_pred=model.predict(X_test)
classes_x=np.argmax(y_pred,axis=1)

from sklearn.metrics import confusion_matrix

classes_x

from sklearn.metrics import confusion_matrix,accuracy_score
print(confusion_matrix(classes_x,y_test))
print(accuracy_score(classes_x,y_test))

predictions = (model.predict(X_test) > 0.5).astype("int32")

print(confusion_matrix(predictions,y_test))
print(accuracy_score(predictions,y_test))

