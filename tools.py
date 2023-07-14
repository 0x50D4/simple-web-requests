from urllib import parse
import subprocess

def encode(data):
    return parse.quote_plus(data)

def decode(data):
    return parse.unquote_plus(data)

def length(data):
    return str(len(data))

def parse_url(url):
    if url[0:5] == "https":
        url = url[7:]
    elif url[0:4] == "http":
        url = url[6:]
    if url[-1] == "/":
        url = url[:-1]

def copy_to_clipboard(data):
    subprocess.Popen(['/bin/sh', '-c', f'printf "{data}" | xclip -selection c'])
    

def parse_and_clipboard(data):
    data = parse_url(data)
    copy_to_clipboard(data)
    return f"Copied {length(data)} chars"    

