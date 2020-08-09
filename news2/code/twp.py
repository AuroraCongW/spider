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

WEBSITE = "the Washington Post"


def input_search(browser,url,keyword):
    url = url
    browser.get(url)
    input_box = browser.find_element_by_xpath('//*[@id="main-content"]/div/div/div[1]/form[1]/div/div/input')
    input_box.clear()
    input_box.send_keys(keyword)
    input_box.send_keys(Keys.ENTER)
    time.sleep(6)
    html = browser.page_source
    return html

def parse_home_page(html,keyword):
    hub = []
    html = etree.HTML(html)
    ul = html.xpath('//*[@class="pb-results-container"]/div')
    for li in ul[1:]:
        cover = li.xpath('.//img/@src')
        title = li.xpath('.//p/a/text()')
        url = li.xpath('.//p/a/@href')
        date = li.xpath('.//div/span/text()')
        article = {
            "cover": join_list(cover),
            "title": join_list(title),
            "date": join_list(date),
            "url": join_list(url),
            "keyword": keyword,
            "website": WEBSITE
        }
        if choice_date(join_list(date)):
            hub.append(article)
    number = html.xpath('//form/div/span[1]/text()')
    if len(number) == 0:
        return [],0

    return hub,int(number[0])

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
            Next = browser.find_element_by_xpath('//*[@id="main-content"]//ul/li[last()-1]/a')
            Next.send_keys(Keys.ENTER)
            initial_number+=1
            time.sleep(5)




def search_article(browser,url):
    browser.get(url)
    return browser.page_source

def get_an_article(browser,url):
    html = search_article(browser,url)
    dic = {}
    html = etree.HTML(html)
    author = html.xpath('//*[@class = "author-name font-bold link blue hover-blue-hover"]//text()')
    content = html.xpath('//*[@class="article-body"]//text()')
    comment = html.xpath('//*[@href="#comments-wrapper"]/text()')
    topic = html.xpath('//*[@class="font-bold link blue"]/text()')
    dic["author"] = join_list(author)
    dic["content"] = join_list(content)
    dic["comment"] = join_list(comment)
    dic["topic"] = join_list(topic)
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
    _,item_number = parse_home_page(page_source,keyword)
    page_number = pagenumber(item_number,10)
    whole_hub = parse_all_home_page(browser,page_number,keyword)
    data =  parse_all_article(browser,whole_hub)
    write_to_csv(data,website=str(WEBSITE),keyword=keyword)
    browser.close()



if __name__ == '__main__':
    url = get_url(WEBSITE)
    keywords = get_keywords()
    print(keywords[6])
    main(url,keywords[6])

