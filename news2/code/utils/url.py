def get_url(website):
    if website=="Wall Street journal":
        return "https://www.wsj.com/search/term.html?KEYWORDS=U.S-China%20trade%20and%20COVID-19&min-date=2020/07/01&max-date=2020/07/31&isAdvanced=true&daysback=90d&andor=AND&sort=date-desc&source=wsjarticle,wsjblogs,wsjvideo,interactivemedia,sitesearch,wsjpro"
    if website=="Fox News":
        return "https://www.foxnews.com/search-results/search?q=U.S.-China%20trade%20and%20COVID-19"
    if website=="the Washington Post":
        return "https://www.washingtonpost.com/newssearch/?query=U.S.-China%20trade%20and%20COVID-19&sort=Relevance&datefilter=60%20Days"
    if website=="Huffpost":
        return "https://search.huffpost.com/search;_ylt=AwrJ7J2Mcipfs9cAG6JsBmVH;_ylu=X3oDMTEzajVvczlrBGNvbG8DYmYxBHBvcwMxBHZ0aWQDBHNlYwNwYWdpbmF0aW9u?p=U.S-China+trade+and+COVID-19&pz=10&fr=huffpost&bct=0&b=1&pz=10&bct=0&xargs=0"