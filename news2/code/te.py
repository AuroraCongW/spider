import time
from lxml import etree
from utils.file import write_to_csv
from utils.list2str import join_list
from utils.date import choice_date
from utils.keywords import get_keywords
from utils.url import get_url
from utils.chrome_init import init
from selenium.webdriver.common.keys import Keys
from utils.nextpage import pagenumber

WEBSITE = "Huffpost"

def input_search(browser,url,keyword):
    url = url
    browser.get(url)
    input_box = browser.find_element_by_xpath('//*[@id="yschsp"]')
    input_box.clear()
    input_box.send_keys(keyword)
    input_box.send_keys(Keys.ENTER)
    time.sleep(3)
    html = browser.page_source
    return html


def parse_home_page(html,keyword):
    hub = []
    html = etree.HTML(html)
    # next = html.xpath('//*[@class="next"]/@href')
    ul = html.xpath('//*[@class="compArticleList"]/li')
    for li in ul[1:]:
        cover = li.xpath('a/img/@src')
        topic = li.xpath('span/text()')
        title = li.xpath('h4/a/text()')
        url = li.xpath('h4/a/@href')
        author = li.xpath('div/p/span[1]/text()')
        date = li.xpath('div/p/span[2]/text()')
        article = {
            "cover":join_list(cover),
            "topic":join_list(topic),
            "title":join_list(title),
            "author":join_list(author),
            "date":join_list(date),
            "url":join_list(url),
            "keyword":keyword,
            "website":WEBSITE
        }
        if choice_date(join_list(date)):
            hub.append(article)

    item_number = html.xpath('//*[@id="left"]/div/ol/li/div/div/span/text()')
    if len(item_number) == 0:
        return [],0
    number = int(item_number[0].split()[0].replace(',', ''))
    print(hub,number)
    return hub,number

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
            time.sleep(1)
            try:
                Next = browser.find_element_by_xpath('//*[@class="next"]')
                Next.send_keys(Keys.ENTER)
            except:
                print("skip")
                pass
            initial_number+=1


def search_article(browser,url):
    browser.get(url)
    return browser.page_source

def get_an_article(browser,url):
    html = search_article(browser,url)
    dic = {}
    html = etree.HTML(html)
    subtitle = html.xpath('//*[@class="headline__subtitle"]/text()')
    content = html.xpath('//*[@class="content-list-component yr-content-list-text text"]//text()')
    dic["subtitle"] = join_list(subtitle)
    dic["content"] = join_list(content)
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
    page_number = pagenumber(item_number,N=9)
    whole_hub = parse_all_home_page(browser,page_number,keyword)
    data =  parse_all_article(browser,whole_hub)
    write_to_csv(data,website=str(WEBSITE),keyword=keyword)
    browser.close()


if __name__ == '__main__':
    url = get_url(WEBSITE)
    keywords = get_keywords()
    for keyword in keywords:
        print(keyword)
        main(url, keyword)

