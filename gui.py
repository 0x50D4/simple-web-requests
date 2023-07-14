import dearpygui.dearpygui as dpg
import re
import network 

new_data = 1 # variable for tracking if we have new data
domain = ""

usr_input = default = "GET / HTTP/1.1\nHost: example.com\nConnection: close\n" # default request

def get_domain(data):
    """Getting the domain from the request for sockets"""
    
    try:
        # find the Host: domain, remove the Host: part and the \n from the end, and strip extra spaces
        return (re.findall("Host: {1}[^ \n]+[ ]{0,1}\n{1}", data)[0][:-1])[5:].strip()
    except:
        print("Couldn't find domain...")

def add_slashes(data):
    """adds the slashes \r to the request, so it works"""
    
    global domain
    data = re.sub("[\n]", " \n", data) # putting a space in front of every \n
    return re.sub("[^\r]{1}[\n]", "\r\n", data) # replacing space before \n with \r 

def text_callback(sender):
    """callback called upon entering text"""

    global usr_input, new_data
    new_data = 1 # setting new data to 1, so we know we have nwe data
    usr_input = dpg.get_value(sender) # returning the value of the text box into usr_input

def btn_callback():
    """callback called upon hitting send"""

    global usr_input, domain, new_data

    if new_data: # run if we have new data, without this we would get a loop upon launching the same request
        domain = get_domain(usr_input) # get domain for sockets
        usr_input = add_slashes(usr_input) + "\r\n" # add necessary characters, plus the trailing one
        new_data = 0 # set it so we know this is old data

    print(repr(usr_input)) # print user input with \n and \r
    print(usr_input) # print user input(the request) formatted
    dpg.configure_item("output", default_value=network.main(domain, usr_input)) # call the main netowrk function for the output textbox

def set_up_gui():
    dpg.create_context()
    dpg.create_viewport(title="Web requester", width=600, height=900, resizable=False)
    dpg.setup_dearpygui()
    
    with dpg.window(tag="Primary Window", width=600, height=900,  no_move=True, no_close=True, no_title_bar=True ):
        dpg.add_text("Web request sender")
        dpg.add_input_text(multiline=True, default_value=default, callback=text_callback, width=600, height= 400, tab_input=True)
        dpg.add_button(label="Send", callback=btn_callback)
        dpg.add_input_text(multiline=True, readonly=True, width = 600, height=400, tag="output")
        
    dpg.set_primary_window("Primary Window", True)
    
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

set_up_gui()
