import os
import csv
import json
import pickle
import pandas as pd
import math
import emoji
import regex

test_dir = '/Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads'

def get_file_path(dirName):
    '''

    :param dirName: direction of the directory of all data
    :return: a list of file directions in that directory
    '''
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    # print('listoffiles',listOfFiles)
    return listOfFiles
def get_post_addresses(list_of_files):
    '''

    :param list_of_files: a list of all files in directory
    :return: a dictionary of all posts from source to reply and tweet and reddit post with the
    format of { id : address}
    '''
    posts_id_address = {}
    for elem in list_of_files:
        elem = str(elem)
        parts = elem.split('/')
        if (parts[-1] != "annotation.json")  and (parts[-1] != "raw.json") and (parts[-1] != "structure.json") and parts[-1].endswith('.json'):
            posts_id_address[parts[-3]] = elem
    return posts_id_address
def get_tweets_addresses(list_of_files):
    # TODO add code to get replies and structure of replies
    '''

    :param list_of_files: a list of all files in directory
    :return: a list of all source tweets
    '''
    tweets = []
    for elem in list_of_files:
        elem = str(elem)
        parts = elem.split('/')
        if parts[-2] == "source-tweets" and parts[-1].endswith('.json'):
            tweets.append(elem)
    # print('tweets',tweets)
    return tweets
def single_topic(topic_dir):
    list_of_files=get_file_path(topic_dir)
    post_addresses=get_post_addresses(list_of_files)
    id_text_class={}
    topic_name=""
    for post in post_addresses:
        address_of_posts= post_addresses[post]
        parts = address_of_posts.split('/')
        if parts[-2]=='source-tweets':
            tag= parts[-4]
            post_id=post
            with open(address_of_posts) as f:
                tweet = json.load(f)
                text = tweet['text']
            id_text_class[post]={
                "text":text,
                "tag":tag
            }
        topic_name=parts[-5]
    return id_text_class,topic_name
def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list
def context_features(text):
    length=len(text)
    capital_ratio=(sum(1 for c in text if c.isupper()))/(sum(map(str.islower, text))+1)
    question_mark=0
    if '?'in text:
        question_mark=1
    exclamation_point=0
    if '!' in text:
        exclamation_point=1
    counter = split_count(text)
    if not counter:
        has_emoji=0
    else :
        has_emoji=1
    return [length,capital_ratio,question_mark,exclamation_point,has_emoji]
def make_source_df(list_of_tweets):
    '''
    get from the list of tweets addresses tweets and extract all features to for feature selection
    :param list_of_tweets: a list of addresses of tweets
    :return: a json/pickle/pandas df of :
    ID  TEXT    features    CLASS(rumour not rumour)
    features:

    '''
    # classification 1 -> rumours
    # classification 0 -> non-rumours
    #TODO add text based features here too to select the right features
    id_feature_class = {}
    for address in list_of_tweets:
        parts = address.split('/')
        tweet_id = parts[-3]
        print(address)

        with open(address) as f:
            tweet = json.load(f)
            # context based features
            context=context_features(tweet['text'])
            classification = 0
            if parts[-4] == "rumours":
                classification = 1
            # network based features
            id_feature_class[tweet_id] = {"classification": classification, "text": tweet['text'],
                                          "favorite_count_log": math.log(tweet['favorite_count']+1),
                                          "retweet_count": math.log(tweet['retweet_count']+1),
                                          "verified": tweet['user']['verified'],
                                          "followers": tweet['user']['followers_count'],
                                          "follow_ratio": (tweet['user']['followers_count']+1)/(tweet['user']['friends_count']+1),
                                          "length":context[0],
                                          "capital_ratio":context[1],
                                          "question_mark":context[2],
                                          "exclamation_point":context[3],
                                          "has_emoji":context[4],
                                          "hashtag_count":len(tweet['entities']['hashtags'])
                                          }
            if not tweet['entities']['urls']:
                id_feature_class[tweet_id]['has_url']=0
            else:
                id_feature_class[tweet_id]['has_url']=1
            if "media" in tweet['entities']:
                id_feature_class[tweet_id]['media_type'] = tweet['entities']['media'][0]['type']
            else:
                id_feature_class[tweet_id]['media_type'] = 'none'

    with open('source_id_feature_class_test.json', 'w') as fp:
        json.dump(id_feature_class, fp)
    return id_feature_class
def test(dirname):
    list_of_files = get_file_path(dirname)
    list_of_tweets=get_tweets_addresses(list_of_files)
    return make_source_df(list_of_tweets)
def make_panda_df(id_text_class,output_dir):
    '''

    :param dir: input address of json of id_feature_class.json
    :return: a pickle of pandafied dataframe of to visualize data
    '''
    data = id_text_class
    data_pd = pd.DataFrame.from_dict(data)
    output_address = output_dir
    output = data_pd.T.to_json(output_address)
if __name__ == "__main__":
    Charliehebdo="/Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads/charliehebdo-all-rnr-threads/"
    Ebola_Essien="/Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads/ebola-essien-all-rnr-threads"
    Ferguson="/Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads/ferguson-all-rnr-threads"
    Germanwings_crash=" /Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads/germanwings-crash-all-rnr-threads"
    Gurlitt="/Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads/gurlitt-all-rnr-threads"
    Ottawashooting="/Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads/ottawashooting-all-rnr-threads"
    Prince_Toronto="/Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads/prince-toronto-all-rnr-threads"
    Putin_missing="/Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads/putinmissing-all-rnr-threads"
    Sydneysiege="/Users/macbook/Desktop/reasearch/tweets_data_set_2018/all-rnr-annotated-threads/sydneysiege-all-rnr-threads"
    topic_addresses=[Charliehebdo,Ebola_Essien,Ferguson,Germanwings_crash,Gurlitt,Ottawashooting,Prince_Toronto,Putin_missing,Sydneysiege]
    all_topics={}
    for i in range(len(topic_addresses)):
        id_text_class, name = single_topic(topic_addresses[i])
        all_topics[i]=id_text_class
        make_panda_df(id_text_class,name+".json")
    data = all_topics
    pickle.dump(all_topics, open("all_topics.p", "wb"))



