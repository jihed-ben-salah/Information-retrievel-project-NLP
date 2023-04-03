from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import torch
from transformers import pipeline
import json
from transformers import AutoTokenizer, CamembertForQuestionAnswering

with open('/home/rima/esprit2023-nlu-DataMachines/gov_websites/gov_websites/spiders/context.json', 'r') as f:
    data = json.load(f)

corpus=[]

for i in range(len(data)):
    if data[i]['context'] is not None and data[i]['context']!='\n\t':
        corpus.append(data[i]['context'])
    if data[i]['context2'] is not None and data[i]['context']!='\n\t':
        corpus.append(data[i]['context2'])


# Define the question
question = input('Give your question here: ') 


from stop_words import get_stop_words

french_stop_words = get_stop_words('french')
vectorizer = TfidfVectorizer(stop_words=french_stop_words)

corpus_tfidf = vectorizer.fit_transform(corpus)

# Compute the TF-IDF scores for the question
question_tfidf = vectorizer.transform([question])

# Compute the cosine similarity between the question and each document in the corpus
cos_similarities = cosine_similarity(question_tfidf, corpus_tfidf)

# Select the document with the highest cosine similarity as the best context for the question
best_doc_idx = cos_similarities.argmax()
best_doc = corpus[best_doc_idx]


print("Meilleur contexte pour la question '{}': '{}'".format(question, best_doc))

nlp = pipeline("question-answering", model="deepset/roberta-base-squad2", tokenizer="deepset/roberta-base-squad2")


result = nlp(question=question, context=best_doc)
print("\nRéponse: ",result)
