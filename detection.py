import string

import numpy as np 
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

#downloading stopwords set
nltk.download('stopwords')

df = pd.read_csv('spam_ham_dataset.csv')

#replace line breaks with space
df['text'] = df['text'].apply(lambda x: x.replace('\r\n', ' '))

stemmer = PorterStemmer()
corpus = []

stopwords_set = set(stopwords.words('english'))

#without punctuation and then stemming words, convert all to lowercase
for i in range(len(df)):
    text = df['text'].iloc[i].lower()
    text = text.translate(str.maketrans('', '', string.punctuation)).split()
    text = [stemmer.stem(word) for word in text if word not in stopwords_set]
    text = ' '.join(text)
    corpus.append(text)
 
#vectorize the data  
vectorizer = CountVectorizer()

X = vectorizer.fit_transform(corpus).toarray()
y = df.label_num

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#classifier
clf = RandomForestClassifier(n_jobs=-1)

clf.fit(X_train, y_train)

print(clf.score(X_test, y_test))

#make a function for this
#get an email to check
email_to_classify = df.text.values[10]
email_text = email_to_classify.lower().translate(str.maketrans('', '', string.punctuation)).split()
email_text = [stemmer.stem(word) for word in text if word not in stopwords_set]
email_text = ' '.join(email_text)

email_corpus = [email_text]

X_email = vectorizer.transform(email_corpus)

# 0 - not spam
# 1 - spam
print(clf.predict(X_email)) 