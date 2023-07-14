import socket

def initialize_client(domain, port):
    """Initialize client for connection"""

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((domain, port))
    client.settimeout(5)
    return client

def send_and_recv_data(request, client):
    """Send and recv data from server"""
    
    try:
        client.sendall(request.encode())
    except:
        print("[-] Fatal error while sending data...")
        return("Fatal error while sending data.") 
    response = b""

    try:
        while True:
            chunk = client.recv(4096)
            if len(chunk) == 0:
                break
            response = response + chunk
    except socket.timeout as e:
        print(e)
        return e

    return response.decode("ISO-8859-1") # this seems to work out most

def main(domain, request):
   
    # TODO: add a function for https (pain)
    client = initialize_client(domain, 80) 
    response = send_and_recv_data(request, client)

    return response

