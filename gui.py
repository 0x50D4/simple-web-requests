import dearpygui.dearpygui as dpg
import re
import network 

usr_input = ""
new_data = 1 

usr_input = default = "GET / HTTP/1.1\nHost: example.com\nConnection: close\n"

domain = ""
def get_domain(data):
    try:
        return (re.findall("Host: {1}[^ \n]+[ ]{0,1}\n{1}", data)[0][:-1])[5:].strip()
    except:
        print("Couldn't find domain...")


def add_slashes(data):
    global domain
    data = re.sub("[\n]", " \n", data)
    return re.sub("[^\r]{1}[\n]", "\r\n", data)

def text_callback(sender):
    global usr_input, new_data
    new_data = 1
    usr_input = dpg.get_value(sender)

def btn_callback():
    global usr_input, domain, new_data
    if new_data:
        domain = get_domain(usr_input)
        usr_input = add_slashes(usr_input) + "\r\n"
        new_data = 0 
    print(repr(usr_input))
    print(usr_input)
    dpg.configure_item("output", default_value=network.main(domain, usr_input))
 
dpg.create_context()
dpg.create_viewport(title="Web requester", width=600, height=900, resizable=False)
dpg.setup_dearpygui()

with dpg.window(tag="Primary Window", width=600, height=900,  no_move=True, no_close=True, no_title_bar=True ):
    dpg.add_text("Web request sender")
    input = dpg.add_input_text(multiline=True, default_value=default, callback=text_callback, width=600, height= 400, tab_input=True)
    dpg.add_button(label="Send", callback=btn_callback)
    dpg.add_input_text(multiline=True, readonly=True, width = 600, height=400, tag="output")
    
dpg.set_primary_window("Primary Window", True)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
