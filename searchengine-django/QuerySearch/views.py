from django.shortcuts import render

from django.http import HttpResponse,JsonResponse

from .utils import *
import time
from .tfidf import *


def home(request):
    
    res=json.loads(find_tfidf("a"))
    return render(request, 'index.html',{'res':res})

    #return HttpResponse("hi")
    return render(request, 'index.html',{})


def gen_search_json(request):
    
    start_time = time.time()
    query = request.GET.get("q")
    #print("request get",query)
    query = process_term(query)
    #print("process term", query)
    results = get_results(query.strip())
    #print("get_results",results)
    resp = JsonResponse({"results":results[:10]})  # top 10 results
    resp.headers['Access-Control-Allow-Origin'] = '*'
    end_time = time.time()
    #print("Response time : " + str(end_time - start_time))
    return resp
    
    
def querySearch(request,query):
    
    print(query)
    
    res=find_tfidf(query)
    #print(res)
    return HttpResponse(json.dumps(res))
    #return render(request, 'index.html',{'res':res})
