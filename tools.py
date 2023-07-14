from urllib import parse

def encode(data):
    return parse.quote_plus(data)

def decode(data):
    return parse.unquote_plus(data)

