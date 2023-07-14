from urllib import parse
import subprocess

def encode(data):
    return parse.quote_plus(data)

def decode(data):
    return parse.unquote_plus(data)

def length(data):
    return str(len(data))

def parse_url(url):
    print(url)
    if url[:5] == "https":
        url = url[8:]
    elif url[:4] == "http":
        url = url[7:]
    if url[-1] == "/":
        url = url[:-1]
    return url
    
