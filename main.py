import socket
from sys import argv
import argparse

parser = argparse.ArgumentParser(description="A program for simple web requests")
parser.add_argument("domain",help="The domain name to send the request to")
parser.add_argument("request_type", help="GET or POST request")
parser.add_argument("-s", "--subdomain", help="if there is a subdomain you want")
parser.add_argument("-p", "--post_content", help="what kind of content you want in the post request.")
parser.add_argument("-g", "--get_content", help="What kind of get content you want")

args = parser.parse_args()

domain = args.domain 
req_type = args.request_type

if args.subdomain:
    subdomain = args.subdomain

if args.post_content:
    post_content = args.post_content

if args.get_content:
    get_content = args.get_content

socket.timeout(10)
arg_list = []


def send_and_recv_data(request, client):
    """Using the client send and recv data"""

    client.sendall(request.encode())
    print(f"[+] Sent: \n{request}\n")

    # recieve data, we use this method because it gets everything for sure
    response = b""
    try: 
        while True:
            chunk = client.recv(4096)
            if len(chunk) == 0:
                break
            response = response + chunk
    except socket.timeout as e:
        print("[-] Socket timed out :(")

    http_response = response.decode("ISO-8859-1") 
    return http_response


def work_on_get(content):
    if content:
        content = "?" + content
    else:
        content = ""

    return content


def work_on_post(content):
    """Responsible for handling two cases: there is data/there is no data"""

    if content:
        length = "Content-Length: " + str(len(content))
        content_type = "Content-Type: " + "application/x-www-form-urlencoded"
    else:
        length = "" 
        content_type = ""

    if content:
        content = "\r\n" + content
    else:
        content = ""

    return length, content_type, content

def work_on_domain(domain):
    """Function to remove http,https and / at end"""

    if (domain[:5] == "https"):
        domain = domain[8:]
    elif  (domain[:4] == "http"):
        domain = domain[7:]
    if (domain[-1] == "/"):
        domain = domain[:-1]
    return domain 

def initialize_client(domain):
    """Use sockets to initialize a connection to the webserver"""
    
    port = 80
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((domain, port))
    return client

def add_all_list(*arg):
    for x in arg:
        if (str(x) != ""):
            arg_list.append(str(x) + "\r\n")
        else:
            arg_list.append(str(x))
    return "".join(arg_list)


def prep_request(domain, subdomain, req_type, stuff, get_content):
    """Set the request up, with paramteres"""

    request = f"{req_type} /{subdomain}{get_content} HTTP/1.1\r\n{domain}Connection: close\r\n{stuff}"

    return request
              
def post_request(domain, subdomain, req_type, get_content, post_content):
    domain = work_on_domain(domain)

    # connect the client
    client = initialize_client(domain) 

    domain = "Host: " + domain + "\r\n" 
    ua = "User-Agent: " + "soda/123" + "\r\n"
    
    length, content_type, post_content = work_on_post(post_content)
    get_content = work_on_get(get_content)

    stuff = add_all_list(length, content_type, ua, post_content)     
    
    # prepare and send data
    request = prep_request(domain, subdomain, req_type, stuff, get_content) 
    response = send_and_recv_data(request, client)
    return response

response = post_request(args.domain, args.subdomain, args.request_type, args.get_content, args.post_content)
print(f"[+] Got response: \n{response}")
