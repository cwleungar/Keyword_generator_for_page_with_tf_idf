import utils
from bs4 import BeautifulSoup
import json
import requests
def getUrls():
    headers = {'User-Agent': 'bot'}
    response = requests.get("https://www.mi-expert.com" + '/sitemap.xml', headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')  # Use 'lxml-xml' parser
    pages = soup.find_all('loc')
    ret=[]
    for page in pages:
        url=page.text
        url=url.replace('https://www.mi-expert.com','https://www.mi-expert.com:8443')
        ret.append(url)
    ret=filter(lambda x: '/item/' in x or '/blogitem/' in x,ret)

    return list(ret)



def main():

    urls = getUrls()
    allData=utils.saveAllExistingPageToDict(urls,'data.json')
    para ={}
    for url, text in allData.items():
        para[url] = utils.bpe_encode(text)
    print("finished encoding")
    top_keywords = utils.get_top_keywords(para)
    print("finished getting top keywords")
    ans={}
    for url, keywords in top_keywords.items():
        ans[url] = [utils.bpe_decode(keyword) for keyword in keywords]
    json.dump(ans, open('top_keywords.json', 'w'))

if __name__ == "__main__":
    main()