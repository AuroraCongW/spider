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

WEBSITE = "Fox News"

def input_search(browser,url,keyword):
    url = url
    browser.get(url)
    input_box = browser.find_element_by_xpath('//*[@class="search-form"]/input')
    input_box.clear()
    input_box.send_keys(keyword)
    time.sleep(25)
    input_box.send_keys(Keys.ENTER)
    time.sleep(80)
    html = browser.page_source
    return html

def parse_home_page(html,keyword):
    hub = []
    html = etree.HTML(html)
    articles = html.xpath('//*[@class="article"]')
    for article in articles:
        cover = article.xpath('.//img/@src')
        title = article.xpath('.//h2/a/text()')
        url = article.xpath('.//h2/a/@href')
        subtitle = article.xpath('./div/div//a/text()')
        article = {
            "cover": join_list(cover),
            "title": join_list(title),
            "url": join_list(url),
            "subtitle":join_list(subtitle),
            "keyword": keyword,
            "website": WEBSITE
        }
        hub.append(article)

    return hub

def search_article(browser,url):
    browser.get(url)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight*0.75)")
    time.sleep(5)
    return browser.page_source

def get_an_article(browser,url):
    try:
        html = search_article(browser,url)
    except:
        print("time out")
        return -1
    dic = {}
    html = etree.HTML(html)
    date = html.xpath('//*[@class="article-date"]/time/text()')
    author = html.xpath('//*[@class="author-byline"]/span/span/a/text()')
    content = html.xpath('//*[@class="article-body"]/p/text()')
    comment = html.xpath('//*[@data-spot-im-class="comments-count"]/text()')
    topic = html.xpath('//*[@class="eyebrow"]/a/text()')
    dic["author"] = join_list(author)
    dic["content"] = join_list(content)
    dic["comment"] = join_list(comment)
    dic["topic"] = join_list(topic)
    dic["date"] = join_list(date)
    return dic

def parse_all_article(browser, whole_hub):
    data = []
    for article_info in whole_hub:
        url = article_info["url"]
        article_detail = get_an_article(browser,url)
        if article_detail != -1:
            sum_article_info = dict(article_info, **article_detail)
            print(sum_article_info)
            data.append(sum_article_info)
    return data

def main(url,keyword):
    browser = init()
    page_source = input_search(browser, url, keyword)
    hub = parse_home_page(page_source,keyword)
    data = parse_all_article(browser,hub)
    write_to_csv(data,website=str(WEBSITE),keyword=keyword)
    browser.close()

if __name__ == '__main__':
    url = get_url(WEBSITE)
    keywords = get_keywords()

    print(keywords[6])
    main(url, keywords[6])


