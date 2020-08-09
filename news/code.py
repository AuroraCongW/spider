#!/usr/bin/env python
# coding: utf-8

# In[66]:


import json
import requests
import re
import time
from requests.exceptions import RequestException
from lxml import etree
from selenium import webdriver

def get_one_page(url):
    """
    get one page's html.
    """
    try:
        headers = {
            'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
            
        }
        response = requests.get(url,headers=headers)
        
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def write_to_file(content):
    """
    write dict to json file.
    """
    with open('results.json','a',encoding='utf-8') as f:
        f.write(json.dumps(content)+'\n')

def parse_one_page_url(html):
    """
    parse home page's article url.
    """
    pattern = re.compile('<dd.*?col-xs-12.*?="(.*?)">',re.S)
    items = re.findall(pattern,html)
    return items

def parse_one_page(html):
    """
    parse one article's title,date,source,content.
    """
    pattern = re.compile('<strong.*?articleTitle.*?>(.*?)</strong>.*?date.*?>(.*?)</span>.*?Source.*?href="(.*?)"',re.S)
    items = re.findall(pattern,html)
    html = etree.HTML(html)
    content = html.xpath("//div[@class='article-content']//text()")
    for item in items:
        return {
            'title':item[0],
            'date':item[1].strip(),
            'source':item[2],
            'content':"".join(content).strip()
        }
    
def get_urls(url):
    """
    get articles' url
    """
    browser = webdriver.Chrome()

    browser.get(url)

    urls = []
    for i in range(10):
        url = browser.find_element_by_xpath("//*[@id='articleList']/ul/li[%s]//a"%(i+1)).get_attribute('href')
        urls.append(url)

    browser.close()
    return urls

def main():
    infos = {}
    target_url = "http://www.ikcest.org/technology.htm"
    urls = get_urls(target_url)
    for i,url in enumerate(urls):
        text = get_one_page(url)
        info = parse_one_page(text)
        infos[i+1] = info
    write_to_file(infos)

if __name__=='__main__': 
    main()


# In[ ]:




