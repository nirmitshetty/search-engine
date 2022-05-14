import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

def get_data():
    df = pd.read_csv("/Users/ankitasinha/UCI_CLASS/Capstone Project/In-House-Search-Engine-main/data/csv_data/new_covid.csv")
    df=df[['question','answer','source','country', 'link', 'encoded_questions']]
    df['encoded_questions'] = df['encoded_questions'].astype(float)
    return df

def get_sentence_embeding(sentences):
  preprocessed_text = sbert_model.encode(sentences)
  return preprocessed_text

def search_covid_dataset(question):
    df = get_data()
    # df['encoded_questions'] = df['question'].apply(lambda x: get_sentence_embeding([x]))
    # df.to_csv('/Users/ankitasinha/UCI_CLASS/Capstone Project/In-House-Search-Engine-main/data/csv_data/new_covid.csv')
    similar_vector_values = []

    query = question
    # print(query)
    query_vectors = sbert_model.encode([query])
    for index, row in df.iterrows():
        ans = row['encoded_questions']
        similar_vector_values.append(np.sum(cosine_similarity(ans, query_vectors)))

    # print(similar_vector_values)
    dx = np.argmax(np.array(similar_vector_values))

    predicted_ans = df.iloc[dx][['answer','link']]

    return predicted_ans

if __name__ == '__main__':
    question = "What is the source of the virus?"
    ans = search_covid_dataset(question)
    print(ans)