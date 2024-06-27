import requests
import json
import sentencepiece as spm
from collections import Counter
from math import log
import time
from tqdm import tqdm
import numpy as np
def saveAllExistingPageToDict(urls,currentFilePath):
    allData={}
    failedCount=0
    if currentFilePath:
        try:
            f=open(currentFilePath)
            allData=json.load(f)
        except Exception as e:
            print('Error:',e)
    for i in tqdm(range(len(urls))):
        url=urls[i]
        if url in allData:
            continue
        
        response = requests.get(url)
        if response.status_code == 200:
            allData[url]=response.text
        else:
            failedCount+=1
            print('Failed:',url)
        time.sleep(2)
        with open(currentFilePath, 'w+') as outfile:
            json.dump(allData, outfile)
    return allData 
            
def bpe_encode(text):
    sp = spm.SentencePieceProcessor()
    sp.Load("tokenizer2.model")
    return sp.encode(text,out_type=str)
def bpe_decode(text):
    sp = spm.SentencePieceProcessor()
    sp.Load("tokenizer2.model")
    return sp.decode(text)

def get_top_keywords(para, n=20):
    """
    Calculates the TF-IDF and returns the top n keywords for each article in the dictionary 'para'.
    
    Args:
    para (dict): A dictionary where the keys are URLs and the values are lists of tokenized words.
    n (int): The number of top keywords to return for each article.
    
    Returns:
    dict: A dictionary where the keys are URLs and the values are lists of the top n keywords.
    """
    top_keywords = {}

    # Convert the dictionary of articles to a NumPy array
    articles = np.array([article for article in para.values()])
    num_articles = len(para)

    # Calculate term frequencies (TF)
    tf = np.apply_along_axis(lambda x: dict(zip(*np.unique(x, return_counts=True))), axis=1, arr=articles)

    # Calculate document frequencies (DF)
    df = {token: np.sum(1 for art in articles if token in art) for token in np.unique(articles.flatten())}

    # Calculate TF-IDF
    for url, article in para.items():
        tfidf = {token: tf[i][token] * log(num_articles / df[token]) for i, token in enumerate(article)}
        top_keywords[url] = sorted(tfidf, key=tfidf.get, reverse=True)[:n]

    return top_keywords

    