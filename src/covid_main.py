import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import operator

sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

def get_text_data():
    unpickled_data = pd.read_pickle("final_pickle.pkl")
    #print(unpickled_data)
    df=unpickled_data[['id','questionText','encoded_questions','answerText','sourceUrl','title']]
    return df


def get_video_data():
    unpickled_data = pd.read_pickle("/Users/ankitasinha/UCI_CLASS/Capstone Project/In-House-Search-Engine/src/final_video_pickle.pkl")
    df=unpickled_data[['id', 'Youtube link','Question','Transcript', 'encoded_questions']]
    df.rename( columns={'Youtube link':'youtube_link'}, inplace=True )
    df['id'] = df['id'].astype(str)
    return df

def get_sentence_embeding(sentences):
    preprocessed_text = sbert_model.encode(sentences)
    return preprocessed_text


def get_context_values(data):
    df = get_text_data()
    predicted_context=[]
    i=1
    for key, value in data.items():
      if i<6:
        context=df.iloc[key]['answerText']
        link=df.iloc[key]['sourceUrl']
        id =  df.iloc[key]['id']
        first_array=[]
        first_array.append(context)
        first_array.append(link)
        first_array.append(id)
        predicted_context.append(first_array)
        first_array=[]
        i+=1
    
    return predicted_context

def search_covid_text_dataset(question):
  df = get_text_data()
  #df['encoded_questions'] = df['question'].apply(lambda x: get_sentence_embeding([x]))
  #df['videos']= df['question'].apply(lambda x:get_videos([x]))
  # df.to_csv('/Users/ankitasinha/UCI_CLASS/Capstone Project/In-House-Search-Engine-main/data/csv_data/new_covid.csv')
  answers=[]
  similar_vector_values=[]
  similar_vector={}
  query = question
  # print(query)
  query_vectors = sbert_model.encode([query])
  for index, row in df.iterrows():
    ans = row['encoded_questions']
    similar_vector_values.append(np.sum(cosine_similarity(ans,query_vectors)))
    similar_vector[index]=np.sum(cosine_similarity(ans,query_vectors))

  #print(similar_vector_values)
  dx = np.argmax(np.array(similar_vector_values))
  sorted_d = dict( sorted(similar_vector.items(), key=operator.itemgetter(1),reverse=True))
  ans=get_context_values(sorted_d)
  return ans


def get_transcript_values(data):
    df = get_video_data()
    predicted_context = []
    i = 1
    for key, value in data.items():
        if i < 3:
            context = df.iloc[key]['Transcript']
            link = df.iloc[key]['youtube_link']
            id = df.iloc[key]['id']
            first_array = []
            first_array.append(context)
            first_array.append(link)
            first_array.append(id)
            predicted_context.append(first_array)
            first_array = []
            i += 1

    return predicted_context

def get_transcripts_stamp(question):
    df = get_video_data()
    similar_vector_values=[]
    similar_vector={}
    query = question
    query_vectors = sbert_model.encode([query])
    for index, row in df.iterrows():
        ans = row['encoded_questions']
        similar_vector_values.append(np.sum(cosine_similarity(ans,query_vectors)))
        similar_vector[index]=np.sum(cosine_similarity(ans,query_vectors))

    dx = np.argmax(np.array(similar_vector_values))
    sorted_d = dict( sorted(similar_vector.items(), key=operator.itemgetter(1),reverse=True))
    ans=get_transcript_values(sorted_d)
    return ans

def get_time_stamp(question):
  videos = get_transcripts_stamp(question)
  video_ans = []
  for index, value in enumerate(videos):
      predicted_transcript = value[0]
      sent_dict = {}

      video_split = predicted_transcript.splitlines()
      youtube_link = value[1]
      similar_vector_values = []
      for i in range(0, len(video_split),4):
          time = video_split[i]
          sent = video_split[i+1]
          if i+3 < len(video_split):
             sent = sent + " " + video_split[i+3]
          sent_dict[time] = sent
      transcript_df = pd.DataFrame(list(sent_dict.items()),columns = ['timestamp','sent'])
      transcript_df['encoded_transcript'] = transcript_df['sent'].apply(lambda x: get_sentence_embeding([x]))

      query = question
      query_vectors = sbert_model.encode([query])
      for index, row in transcript_df.iterrows():
          ans = row['encoded_transcript']
          similar_vector_values.append(np.sum(cosine_similarity(ans, query_vectors)))

      # print(similar_vector_values)
      dx = np.argmax(np.array(similar_vector_values))

      predicted_time = transcript_df.iloc[dx]['timestamp']
      video_ans.append([predicted_time, youtube_link, value[2] ])

  return video_ans


if __name__ == '__main__':
    question = "How long is the incubation period for covid-19?"
    text_ans = search_covid_text_dataset(question)
    print("text ans " , text_ans)
    video_time = get_time_stamp(question)

    print("video timestamps ", video_time)
