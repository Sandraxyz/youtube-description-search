import os
import sys
import config
import json
from googleapiclient.discovery import build
#imports the build function that allows for search queries

api_key = config.api_key
cse_id = config.cse_id
service = build("youtube", "v3", developerKey=api_key)

def search(query_term, max_page_cnt):
    def get_video_info(video_id):
        result = service.videos().list(part='snippet', id=video_id).execute()
        try:
            return result['items'][0]
        except:
            return None
    def get_video_list(search_results):
        video_list = []
        for item in search_results['items']:
            video_id = item['id']['videoId']
            video_info = get_video_info(video_id)
            if video_info:
                video_list.append(video_info)

        return video_list

    def music_search(search_results_2):
        def get_video_info(video_id):
            result = service.search().list(part="snippet", type="video", q=query_term, videoCategoryId="10", maxResults=50).execute()
            try:
                return result['items'][0]
            except:
                return None

    prevResults = []
    count = 1
    index_name = "youtubesearch"+query_term+".json"
    if os.path.exists(index_name):
        with open(index_name) as f:
              prevResults = json.load(f)
    else:
        query_results = service.search().list(q = query_term, part="snippet", type="video", maxResults=50).execute()
        video_list = get_video_list(query_results)
        prevResults.extend(video_list)
        while query_results['nextPageToken']!='' and count < max_page_cnt:
            token=query_results['nextPageToken']
            query_results=service.search().list(q = query_term, part="snippet",type="video", maxResults=50, pageToken=token).execute()
            video_list=get_video_list(query_results)
            prevResults.extend(video_list)
            count+=1
        fileName = "youtubesearch" + query_term +".json"

        with open(fileName,'w', encoding = 'utf-8') as f:
            json.dump(prevResults, f, ensure_ascii = False, indent=4)
    return prevResults

    results = []  

    tempResults = service.search().list(part="snippet", q=query_term, type="video", maxResults=50).execute()
    video_list = get_video_list(tempResults)
    results.extend(video_list)
    count = 1
    while tempResults['nextPageToken'] != '' and count < max_page_cnt:
        token = tempResults['nextPageToken']
        tempResults = service.search().list(part="snippet", q=query_term, type="video", maxResults=50, pageToken=token).execute()
        video_list = get_video_list(tempResults)
        results.extend(video_list)

        count += 1

    fileName = "youtube_search_"+query_term+".json"
    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4) 

    return results

if __name__ == '__main__':
    arg1 = sys.argv[0]
    #check the number of arguments in the command
    if len(sys.argv) == 2:
        #get the first argument (that the user provided)
        query_term = sys.argv[1]
        print("query: "+query_term)

        results = search(query_term, 1)

        fileName = "youtube_search_"+query_term+".json"
        with open(fileName, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        #print(results['items'][0])
    else:
        print("usage: " + arg1 + " [search_term]")
        