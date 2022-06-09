import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import operator,redis,json

redis
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
redis_client=redis.Redis(host='localhost',port=6379, db=0)

def get_text_data():
    #df = pd.read_csv("static/covid.csv")
    #df=pd.DataFrame(list(covid.objects.all().values('id', 'question','answer','name','source','category','link')))
    
    unpickled_data = pd.read_pickle("static/final_pickle.pkl")
    #print(unpickled_data)
    df=unpickled_data[['id','questionText','encoded_questions','answerText','sourceUrl', 'title']]
    return df


def get_video_data():
    #df = pd.read_csv("static/video_data2.csv")
    #df=pd.DataFrame(list(video.objects.all().values('VID', 'Youtube_link','Question','Transcript','Description','Title')))
    #df.rename( columns={'VID':'id','Youtube_link':'youtube_link'}, inplace=True )

    unpickled_data = pd.read_pickle("static/final_video_pickle_ankita.pkl")
    df=unpickled_data[['id', 'Youtube link','Question','Transcript', 'encoded_questions','Description', 'Title']]
    df.rename( columns={'Youtube link':'youtube_link'}, inplace=True )
    df['id'] = df['id'].astype(str)
    return df


def get_sentence_embeding(sentences):
    preprocessed_text = sbert_model.encode(sentences)
    return preprocessed_text


def get_context_values(data):
    df = get_text_data()
    predicted_context = []
    i = 1
    for key, value in data.items():
        if i < 6:
            context = df.iloc[key]['answerText']
            link = df.iloc[key]['sourceUrl']
            id =  df.iloc[key]['id']
            title= df.iloc[key]['title']

            predicted_context.append([context,link,id,title])
            i += 1

    return predicted_context


def search_covid_text_dataset(question):

    if redis_client.exists(f"bert_text_{question}"):

        print('fetched from cache')
        #redis_client.expire(f"bert_text_{question}",timedelta(seconds=60))
        return redis_client.get(f"bert_text_{question}")

    df = get_text_data()
    
    similar_vector_values = []
    similar_vector = {}
    query = question
    # print(query)
    query_vectors = sbert_model.encode([query])
    for index, row in df.iterrows():
        ans = row['encoded_questions']
        similar_vector_values.append(np.sum(cosine_similarity(ans, query_vectors)))
        similar_vector[index] = np.sum(cosine_similarity(ans, query_vectors))

    # print(similar_vector_values)
    #dx = np.argmax(np.array(similar_vector_values))
    sorted_d = dict(sorted(similar_vector.items(), key=operator.itemgetter(1), reverse=True))
    pred_ans = get_context_values(sorted_d)
    
    for ans in pred_ans:
        ans[2]=int(ans[2])
        ans.append("text")

    pred_ans=json.dumps(pred_ans)

    print('fetching from api')
    redis_client.set(f"bert_text_{question}",pred_ans)
    #redis_client.expire(f"bert_text_{question}",timedelta(seconds=60))

    return pred_ans

def get_transcript_values(data):
    df = get_video_data()
    predicted_context = []
    i = 1
    for key, value in data.items():
        if i < 3:
            context = df.iloc[key]['Transcript']
            link = df.iloc[key]['youtube_link']
            desc = df.iloc[key]['Description']
            title = df.iloc[key]['Title']
           
            predicted_context.append([context, link, title, desc])
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

    sorted_d = dict( sorted(similar_vector.items(), key=operator.itemgetter(1),reverse=True))
    ans=get_transcript_values(sorted_d)
    return ans


def get_time_stamp(question):

    if redis_client.exists(f"bert_video_{question}"):
        print('fetched from cache')
        #redis_client.expire(f"bert_video_{question}",timedelta(seconds=60))
        return redis_client.get(f"bert_video_{question}")

    videos = get_transcripts_stamp(question)
    video_ans = []
    for index, value in enumerate(videos):
        
        predicted_transcript = value[0]
        sent_dict = {}

        video_split = predicted_transcript.splitlines()
        youtube_link = value[1]
        title=value[2]
        desc=value[3]
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
        video_ans.append([predicted_time, youtube_link,title,desc])

    video_ans=json.dumps(video_ans)

    print('fetching from api')
    redis_client.set(f"bert_video_{question}",video_ans)
    #redis_client.expire(f"bert_video_{question}",timedelta(seconds=60))

    return video_ans


if __name__ == '__main__':
    print("main called")
    question = "What is a novel coronavirus?"
    #text_ans = search_covid_text_dataset(question)
    
    #print("text ans " , text_ans)
    video_time = get_time_stamp(question)
    print("video timestamps ", video_time)
