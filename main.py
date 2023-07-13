import socket
from sys import argv

print(f"Usage: {argv[0]} [domain] [subdomain] [GET/POST] [data]\n")

if (len(argv) > 1):
    domain = argv[1]
else:
    domain = input("Enter a domain: ")

if (len(argv) > 2):
    subdomain = argv[2]
else:
    # subdomain = input("Enter a subdomain: ")
    subdomain = ""

if (len(argv) > 3):
    req_type = argv[3]
else:
    req_type = input("You need to enter a request type: ") 

if (len(argv) > 4):
    content = argv[4]
    length = len(content)
else:
    content = ""
    length = 0

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


def work_on_data(content):
    """Responsible for handling two cases: there is data/there is no data"""

    length = len(content)

    if length == 0:
        length = ""
        content_type = ""
    else:
        length = "Content-Length: " + str(length) 
        content_type = "Content-Type: " + "application/x-www-form-urlencoded" 
    return length, content_type

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


def prep_request(domain, subdomain, req_type, stuff):
    """Set the request up, with paramteres"""

    request = f"{req_type} /{subdomain} HTTP/1.1\r\n{domain}Connection: close\r\n{stuff}"

    return request
              
def post_request(domain, subdomain, req_type, content=""):
    domain = work_on_domain(domain)

    # connect the client
    client = initialize_client(domain) 

    domain = "Host: " + domain + "\r\n" 
    ua = "User-Agent: " + "soda/123" + "\r\n"
    
    # Check if there is data, if there is not, do not use content type and such
    length, content_type = work_on_data(content)
    content = "\r\n" + content
    stuff = add_all_list(length, content_type, ua, content)     
    
    # prepare and send data
    request = prep_request(domain, subdomain, req_type, stuff) 
    response = send_and_recv_data(request, client)
    return response

response = post_request(domain, subdomain, req_type, content)
print(f"[+] Got response: \n{response}")
