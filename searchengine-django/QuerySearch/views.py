
from django.http import HttpResponse
import json
from .covid_faq import *

    
def querySearch(request,query):
    
    print(query)
    
    res1=search_covid_text_dataset(query)
    #print(res1)
    
    res2 = get_time_stamp(query, json.loads(res1))
    #print(res2)
    print("returned")   

    return HttpResponse(json.dumps(json.loads(res1)+json.loads(res2)))

def getQuestions(request):
    l=[]
    for q in list(covid.objects.all().values('question')):
        l.append(q['question'].strip('\n'))
    
    for q in list(video.objects.all().values('Question')):
        l.append(q['Question'])

    #print(l)
    return HttpResponse(json.dumps(l))
