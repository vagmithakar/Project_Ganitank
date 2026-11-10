##youtube_id()
url =""
list_url = []
video_id = ""
def youtube_id(url):
    url = url.strip()
    
    if "watch?v=" in url:
        list_url = url.split("watch?v=")
        id = list_url[1]
        list(id)
        list_id = id[0:12]
        video_id = str(list_id)
        #checking for length of yt id
        if len(video_id) == 11:
            return video_id
        else:
            return None
        
    elif "youtu.be/" in url:
        list_url = url.split("youtu.be/")
        id = list_url[1]
        list(id)
        list_id = id[0:12]
        video_id = str(list_id)
        #checking for length of yt id
        if len(video_id) == 11:
            return video_id
        else:
            return None
        
    elif "/shorts/" in url:
        list_url = url.split("/shorts/")
        id = list_url[1]
        list(id)
        list_id = id[0:12]
        video_id = str(list_id)
        #checking for length of yt id
        if len(video_id) == 11:
            return video_id
        else:
            return None
            
    else:
        return None
    
"""video_id = youtube_id("https://example.com/video")
if video_id is None:
    clean_link = None
else:
    clean_link = "https://www.youtube.com/watch?v=" + video_id"""
    
    
    
