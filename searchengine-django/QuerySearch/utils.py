from enum import auto
from functools import cache
from .trie import *
from .models import autocomplete
import redis,json
from datetime import timedelta

redis_client=redis.Redis(host='localhost',port=6379, db=0)
redis_client.flushdb()
word_list = []

full_name_root = Node()
middle_name_root = Node()
last_name_root = Node()

def readDB():
    '''
    with open(os.getcwd()+'/../data/test_data_sample.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        counter=0
        for w in reader:
            #print(w)
            full_name = ""
            word_list.append(w)
            #print("Added : " + w[0] + "Index in list : " + str(counter))
            #first_name_root.add_word(w[0].lower(),index_in_list=counter)
            full_name += w[0].lower()
            if len(w) > 1:
                middle_name_root.add_word(w[1].lower(),index_in_list=counter)
                full_name += w[1].lower() 
            if len(w) > 2:
                last_name_root.add_word(w[2].lower(),index_in_list=counter)
                full_name += w[2].lower()
            full_name_root.add_word(full_name, index_in_list=counter)
            counter+=1
    '''

    reader = autocomplete.objects.all()
    counter=0
    for row in reader:
        
        w=[row.first_name]

        if row.middle_name is not None:
            w.append(row.middle_name)
        if row.last_name is not None:
            w.append(row.last_name)
        #print(w)
        full_name = ""
        word_list.append(w)
        #print("Added : " + w[0] + "Index in list : " + str(counter))
        #first_name_root.add_word(w[0].lower(),index_in_list=counter)
        full_name += w[0].lower()
        if len(w) > 1:
            middle_name_root.add_word(w[1].lower(),index_in_list=counter)
            full_name += w[1].lower() 
        if len(w) > 2:
            last_name_root.add_word(w[2].lower(),index_in_list=counter)
            full_name += w[2].lower()
        full_name_root.add_word(full_name, index_in_list=counter)
        counter+=1

def getName(index):
    name = ""
    l = len(word_list[index])
    for i in range(0,l):
        name = name + " " + word_list[index][i]
    return name.strip()
    

def convert_into_list_of_dict(list_of_names):
    result=[]
    for word in list_of_names:
        result.append({"name": word})
    return result


def get_from_trie(root, query):
    index_list = root.auto_complete_word(query.lower())
    name_list = [getName(i) for i in index_list]
    name_list.sort(key=lambda x: len(x))
    return name_list


def get_results(query):
    
    if redis_client.exists(f"autocomplete_{query}"):
        print("fetched from cache")
        final_result=json.loads(redis_client.get(f"autocomplete_{query}"))
        
    else:    
        print("fetched from API")
        full_name_result = get_from_trie(full_name_root, query)
        #print("full name",full_name_result)
        middle_name_result = get_from_trie(middle_name_root, query)
        #print("middle name",middle_name_result)
        last_name_result = get_from_trie(last_name_root, query)
        #print("last name",last_name_root,last_name_result)
        final_result = full_name_result + middle_name_result + last_name_result
        final_result=convert_into_list_of_dict(final_result)

        #print("*"*5,final_result)
        redis_client.set(f"autocomplete_{query}",json.dumps(final_result))
        #redis_client.expire(f"autocomplete_{query}",timedelta(seconds=30))
    
    redis_client.expire(f"autocomplete_{query}",timedelta(seconds=30))

    return final_result


def process_term(query):
    
    # If search term consists if spaces then 
    name_list = query.split(' ')
    result = ""
    for name in name_list:
        result = result + name.lower()
    return result

    return query.lower()

readDB()