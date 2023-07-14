import dearpygui.dearpygui as dpg
import re
import network 
import tools
import time
import threading

new_data = 1 # variable for tracking if we have new data
domain = ""

class default_values:
    ww = 200
    wh = 60

dv = default_values()


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

def do_network(domain, usr_input):
   dpg.configure_item("output", default_value=network.main(domain, usr_input)) 

def btn_callback():
    """callback called upon hitting send"""
    global usr_input, domain, new_data

    if new_data: # run if we have new data, without this we would get a loop upon launching the same request
        domain = get_domain(usr_input) # get domain for sockets
        usr_input = add_slashes(usr_input) + "\r\n" # add necessary characters, plus the trailing one
        new_data = 0 # set it so we know this is old data

    print(repr(usr_input)) # print user input with \n and \r
    print(usr_input) # print user input(the request) formatted
    x = threading.Thread(target=do_network, args=(domain, usr_input,)) # call the main netowrk function for the output textbox
    x.start()

def encode_popup():
    dpg.show_item("encode-popup")

def decode_popup():
    dpg.show_item("decode-popup")

def length_popup():
    dpg.show_item("length-popup")

def encode_data(sender, value, userdata):
    input = userdata[0]
    output = userdata[1]
    dpg.set_value(output, tools.encode(dpg.get_value(input)))

def decode_data(sender, value, userdata):
    input = userdata[0]
    output = userdata[1]
    dpg.set_value(output, tools.decode(dpg.get_value(input)))

def length_data(sender, value, userdata):
    input = userdata[0]
    output = userdata[1]
    dpg.set_value(output, tools.length(dpg.get_value(input)))

def set_up_gui():
    dpg.create_context()
    dpg.create_viewport(title="Web requester", width=600, height=900, resizable=True)
    dpg.setup_dearpygui()
    
    # the main window
    with dpg.window(tag="Primary Window", width=600, height=900,  no_move=True, no_close=True, no_title_bar=True ):
        dpg.add_spacer(height=10)
        dpg.add_input_text(multiline=True, default_value=default, callback=text_callback, width=600, height= 400, tab_input=True)
        dpg.add_button(label="Send", callback=btn_callback)
        dpg.add_input_text(multiline=True, readonly=True, width = 600, height=400, tag="output")
        
    dpg.set_primary_window("Primary Window", True)

    # menu bar
    with dpg.viewport_menu_bar():
        with dpg.menu(label="Tools"):
            dpg.add_menu_item(label="Encode", callback=encode_popup)
            dpg.add_menu_item(label="Decode", callback=decode_popup)
            dpg.add_menu_item(label="Length", callback=length_popup)
   

    # encoding window
    with dpg.window(label="Encode", width=dv.ww, height=dv.wh, tag="encode-popup", show=False):
        u_input = dpg.add_input_text(hint="Enter some encodable text") 
        output = dpg.add_input_text(readonly=True)
        dpg.add_button(label="Encode", callback=encode_data, user_data=[u_input, output])
    
    # decoding window
    with dpg.window(label="Decode", width=dv.ww, height=dv.wh, tag="decode-popup", show=False):
        u_input = dpg.add_input_text(hint="Enter some decodable text")
        output = dpg.add_input_text(readonly=True)
        dpg.add_button(label="Decode", callback=decode_data, user_data=[u_input, output])

    # decoding window
    with dpg.window(label="Length", width=dv.ww, height=dv.wh, tag="length-popup", show=False):
        u_input = dpg.add_input_text(hint="Enter some text")
        output = dpg.add_input_text(readonly=True)
        dpg.add_button(label="Length", callback=length_data, user_data=[u_input, output])

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

set_up_gui()
