import requests
import pandas as pd

#feed = pd.DataFrame()

# get auth token
def get_auth_token():
    url_auth = 'http://interview.agileengine.com/auth'
    body = { "apiKey": "23567b218376f79d9415" }
    resp = requests.post(url_auth, json=body)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('POST ERROR {}'.format(resp.status_code))
    
    if resp.json()['auth'] != True:
        #auth error
        raise Exception("authentication error")
    
    return(resp.json()['token'])

def get_page_feed(**kwargs):
    #optional parameter page number
    page_num = kwargs.get('page', 1)

    auth_token = get_auth_token()
    hed = {'Authorization': 'Bearer ' + auth_token}
    endpoint = 'http://interview.agileengine.com'
    get_image = '/images'

    page = '?page=' + str(page_num)
    #get photo feed
    resp = requests.get(endpoint+get_image+page, headers=hed)
    if resp.status_code != 200:
        #something went wrong.
        raise Exception('GET /images/ {}'.format(resp.status_code)) 
    
    photo_feed = resp.json()
    return(photo_feed)


def get_photo_byid(id):
    auth_token = get_auth_token()
    hed = {'Authorization': 'Bearer ' + auth_token}
    endpoint = 'http://interview.agileengine.com'
    get_image = '/images/'
    get_id = str(id)
    #get photo by id
    resp = requests.get(endpoint+get_image + get_id, headers=hed)
    if resp.status_code != 200:
        #something went wrong.
        raise Exception('GET /images/id {}'.format(resp.status_code)) 
    
    photo = resp.json()
    return(photo)

def get_all_feed():
    
    pictures = pd.DataFrame()
    pic_info = pd.DataFrame()
    flag = True
    page = 1
    while flag:
        page_feed = get_page_feed(page=page)
        pic = pd.json_normalize(page_feed['pictures'])
        pictures = pictures.append(pic,ignore_index=True)
        flag = page_feed['hasMore']
        page = page + 1

    print("all pictures ok")

    for i, row in pictures.iterrows():
        photo_id = row[0]
        print(i,photo_id)
        pic_info = pic_info.append(pd.json_normalize(get_photo_byid(photo_id)))
    pic_info = pic_info.drop(['cropped_picture'], axis=1)
    pictures = pictures.set_index('id')
    pictures = pictures.join(pic_info.set_index('id'), on='id')
    pictures.to_csv("pictures.csv")
    return(pictures)


    