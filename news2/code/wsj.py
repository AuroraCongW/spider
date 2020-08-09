import time
from lxml import etree
from selenium import webdriver
from utils.file import write_to_csv
from utils.list2str import join_list
from utils.date import choice_date
from utils.keywords import get_keywords
from utils.url import get_url
from utils.chrome_init import init
from selenium.webdriver.common.keys import Keys
from utils.nextpage import pagenumber
from utils.https import com_http
import json

WEBSITE = "Wall Street journal"



def input_search(browser,url,keyword):
    url = url
    browser.get(url)
    input_box = browser.find_element_by_xpath('//*[@class="KeywordSearchInput"]')
    input_box.clear()
    input_box.send_keys(keyword)
    time.sleep(2)
    input_box.send_keys(Keys.ENTER)
    time.sleep(4)
    html = browser.page_source
    # print(html)
    return html

def parse_home_page(html,keyword):

    hub = []
    html = etree.HTML(html)
    page_number = html.xpath('//*[@class="results-count"]/text()')[1].split()[1]
    print(page_number)
    articles = html.xpath('//*[@class="items hedSumm"]/li')
    # print(len(articles))
    for article in articles:
        cover = article.xpath('.//img/@src')
        title = article.xpath('.//h3/a/text()')
        url = article.xpath('.//h3/a/@href')
        topic = article.xpath('.//div[1]/ul/li//text()')
        author = article.xpath('.//ul/li[1]/span/text()')
        date = article.xpath('.//div[@class="article-info"]/ul//time/text()')
        printheadline = article.xpath('.//div/h4/text()')
        summary = article.xpath('.//p/text()')
        article = {
            "cover": join_list(cover),
            "title": join_list(title),
            "url": com_http(join_list(url)),
            "keyword": keyword,
            "website": WEBSITE,
            "topic": join_list(topic),
            "author": join_list(author),
            "date": join_list(date),
            "printheadline": join_list(printheadline)
        }
        print(article)
        hub.append(article)
    with open('temp.csv','w+') as file:
        file.write(json.dumps(hub))
    return hub, page_number

def parse_all_home_page(browser,page_number,keyword):
    whole_hub = []
    if page_number == 0:
        return whole_hub
    initial_number = 1

    while True:
        if initial_number == page_number:
            hub, _ = parse_home_page(browser.page_source, keyword)
            whole_hub.extend(hub)
            return whole_hub
        else:
            hub, _ = parse_home_page(browser.page_source, keyword)
            whole_hub.extend(hub)
            print("please goto next page",initial_number+1)
            time.sleep(30)
            # Next = browser.find_element_by_xpath('//*[@class="next-page"]/a')
            # Next.send_keys(Keys.ENTER)
            initial_number+=1


def search_article(browser, url):
    browser.get(url)
    return browser.page_source

def get_an_article(browser, url):
    html = search_article(browser,url)
    dic = {}
    html = etree.HTML(html)
    subtitle = html.xpath('//header//h2/text()')
    content = html.xpath('//*[@class="wsj-snippet-body"]/p/text()')
    dic["content"] = join_list(content)
    dic["subtitle"] = join_list(subtitle)
    return dic

def parse_all_article(browser, whole_hub):
    data = []
    for article_info in whole_hub:
        url = article_info["url"]
        article_detail = get_an_article(browser,url)
        time.sleep(2)
        sum_article_info = dict(article_info, **article_detail)
        print(sum_article_info)
        data.append(sum_article_info)
    return data

def main(url,keyword):
    browser = init()
    page_source = input_search(browser, url, keyword)
    _, page_number = parse_home_page(page_source, keyword)
    # print(page_number)
    whole_hub = parse_all_home_page(browser, int(page_number), keyword)
    data = parse_all_article(browser, whole_hub)
    write_to_csv(data, website=str(WEBSITE), keyword=keyword)
    browser.close()

if __name__ == '__main__':
    url = get_url(WEBSITE)
    keywords = get_keywords()
    main(url, keywords[6])