# -*- coding: utf-8 -*-
"""Emotion_Detector_Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CCecFHk-UOWIhEHo9kVrB21jSTpsJHAz
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset=pd.read_csv('emotions.csv')

dataset = dataset.drop(columns=['Clean_Text','Unnamed: 0'])

dataset.head()

dataset.shape

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
for i in range(0, 34792):
  text = re.sub('[^a-zA-Z]', ' ', dataset['Text'][i])
  text = text.lower()
  text = text.split()
  ps = PorterStemmer()
  all_stopwords = stopwords.words('english')
  all_stopwords.remove('not')
  text = [ps.stem(word) for word in text if not word in set(all_stopwords)]
  text = ' '.join(text)
  corpus.append(text)

import sklearn
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)
X = cv.fit_transform(corpus).toarray()

y = dataset.iloc[:, 0].values

y

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)

dataset.info()

# Sample input
x1 = "This book was so interesting it made me happy"

# Assuming 'classifier' is your pre-built and pre-trained model
# and 'cv' is your fitted CountVectorizer

def prediction(ex1):
    # Ensure the input is a string
    ex1 = str(ex1)

    # Text preprocessing
    new_text = re.sub('[^a-zA-Z]', ' ', ex1)
    new_text = new_text.lower()
    new_text = new_text.split()

    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')

    new_text = [ps.stem(word) for word in new_text if word not in set(all_stopwords)]
    new_text = ' '.join(new_text)

    # Transform the input text
    X_prediction = cv.transform([new_text]).toarray()

    # Predict using the pre-trained classifier
    y_prediction = classifier.predict(X_prediction)
    return y_prediction

# Run the prediction function
print(prediction(x1))

import pickle
filename='train_model.sav'
pickle.dump(classifier,open(filename,'wb'))
loaded_model=pickle.load(open('train_model.sav','rb'))

with open('count_vectorizer.pkl', 'wb') as f:
    pickle.dump(cv, f)

"""Now we will make a predictive system using the loaded model"""

x1 = "This book was so interesting it made me happy"

# Assuming 'classifier' is your pre-built and pre-trained model
# and 'cv' is your fitted CountVectorizer

def prediction(ex1):
    # Ensure the input is a string
    ex1 = str(ex1)

    # Text preprocessing
    new_text = re.sub('[^a-zA-Z]', ' ', ex1)
    new_text = new_text.lower()
    new_text = new_text.split()

    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')

    new_text = [ps.stem(word) for word in new_text if word not in set(all_stopwords)]
    new_text = ' '.join(new_text)

    # Transform the input text
    X_prediction = cv.transform([new_text]).toarray()

    # Predict using the pre-trained loaded model
    y_prediction = loaded_model.predict(X_prediction)
    return y_prediction

# Run the prediction function
print(prediction(x1))