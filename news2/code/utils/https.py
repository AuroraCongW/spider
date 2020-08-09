def com_http(url):
    base = "https://www.wsj.com"
    if url[:4] == "http":
        return url
    else:
        return base + url