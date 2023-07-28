'''
Main file that will combine the data and the GUI.
'''


import tkinter as tk
from tkinter import ttk
import subprocess


 
def command(command:str, input:str = None):
    command = command.split()
    
    data = subprocess.run(command, capture_output = True, text = True, input = input) 
    
    return data.stdout

def pipe(command1:str, command2:str):
    command1 = command1.split()
    command2 = command2.split()

    command = subprocess.run(command1, capture_output = True, text = True)
    command = command.stdout
    command = subprocess.run(command2, capture_output = True, text = True, input = command)

    return command.stdout

def index_get_paragragh(data:str, select:int):
    command = ['awk', '-v', 'RS=', '-v', 'ORS=', 'NR==' + str(select + 1)]

    paragraph = subprocess.run(command, capture_output = True, text = True, input = data)

    return paragraph.stdout

def word_get_paragraph(data:str, word:str):
    command = ['awk', '-v', 'RS=', f'/\\y{word}\\y/']
    paragraph = subprocess.run(command, capture_output = True, text = True, input = data)

    return paragraph.stdout

def word_get_line(data:str, word:str):
    command = ['grep', '-w', f'{word}']
    line = subprocess.run(command, capture_output = True, text = True, input = data)

    return line.stdout

def main_window():

    def lspci_select(event):
        global lspci_selected
        selected_item = event.widget.selection()

        #True if selected_item is from the right treeview widget, since all functions get called
        #once an item is selected from a treeview
        if selected_item:
            setpci_tree.selection_remove(setpci_tree.selection())

            item_text = event.widget.item(selected_item, 'text')
            lspci_selected = item_text

            if lspci_selected in lspci_opd_name:
                update_text_widget(terminal, command(lspci_selected + device_selected))
            elif lspci_selected in lspic_op_name:
                update_text_widget(terminal, command(lspci_selected))

    def setpci_select(event):
        global setpci_selected
        selected_item = event.widget.selection()

        if selected_item:
            lspci_tree.selection_remove(lspci_tree.selection())
            devices_tree.selection_remove(devices_tree.selection())

            item_text = event.widget.item(selected_item, 'text')
            setpci_selected = item_text

    def device_select(event):
        global device_selected
        selected_item = event.widget.selection()

        if selected_item:
            item_text = event.widget.item(selected_item, 'text')
            device_selected = item_text

            if lspci_selected in lspci_opd_name:
                update_text_widget(terminal, command(lspci_selected + device_selected))
            elif lspci_selected in lspic_op_name:
                update_text_widget(terminal, command(lspci_selected))

    def filter_treeview(treeview, query, data):
        treeview.delete(*treeview.get_children())  # Clear the treeview
        filtered_data = [item for item in data if query.lower() in item.lower()]
        for item in filtered_data:
            treeview.insert('', 'end', text = item)
        alt_row_colours(treeview = treeview)

    def device_search(event):
        query = device_entry.get()
        filter_treeview(devices_tree, query, slot_list)

    def highlight_text(query):
        terminal.tag_remove("search", "1.0", tk.END)
        if query:
            start = "1.0"
            while True:
                start = terminal.search(query, start, stopindex=tk.END, count=tk.NONE, nocase=True)
                if not start:
                    break
                end = f"{start}+{len(query)}c"
                terminal.tag_add("search", start, end)
                start = end

    def terminal_search(event):
         query = terminal_entry.get()
         highlight_text(query)


    window = tk.Tk()

    #Start: Optioins Frame
    options_frame = create_frame(container = window)

    #lspci commands listed frame/treeview.
    lspci_frame = create_frame(container = options_frame)
    lspci_tree = create_treeview(container = lspci_frame, heading = 'lspci Options', data = lspci_opd_name + lspic_op_name)
    lspci_frame.grid(column = 0, row = 0, sticky = 'n')
    lspci_tree.bind('<<TreeviewSelect>>', lspci_select)

    #setpci commands listed frame/treeview.
    setpci_frame = create_frame(container = options_frame)
    setpci_tree = create_treeview(container = setpci_frame, heading = 'setpci Options', data = setpci_op_name)
    setpci_frame.grid(column = 0, row = 1, sticky = 'ns')
    setpci_tree.bind('<<TreeviewSelect>>', setpci_select)

    #Devices listed frame/treeview.
    devices_frame = create_frame(container = options_frame)
    devices_tree = create_treeview(container = devices_frame, heading = 'lspci Devices', data = slot_list)
    devices_frame.grid(column = 1, row = 0, sticky = 'ns', rowspan = 2)
    devices_frame.grid_rowconfigure(0, weight = 1)
    devices_tree.bind('<<TreeviewSelect>>', device_select)
    device_entry = create_search(devices_frame, '<KeyRelease>', device_search)
    device_entry.grid(column = 0, row = 1, sticky = 'ew')

    options_frame.grid(column = 0, row = 0, sticky = 'ns')
    #End: Options Frame

    #Start: Text widget frame for terminal.
    terminal_frame = create_frame(window)

    terminal = tk.Text(terminal_frame, state = 'disabled')
    create_scrollbar(container = terminal_frame, widget = terminal, column = 1)
    terminal.grid(column = 0, row = 0, sticky = 'ns')
    terminal_frame.grid(column = 1, row = 0, sticky = 'ns')
    terminal_entry = create_search(terminal_frame, '<KeyRelease>', terminal_search)
    terminal.tag_configure("search", background = "yellow")
    terminal_entry.grid(column = 0, row = 1, sticky = 'ew')

    terminal_frame.grid_rowconfigure(0, weight = 1)
    #End: Text widget frame for terminal.

    window.mainloop()

def create_frame(container:object):
    frame = ttk.Frame(container)

    #Styling for the frame
    style = ttk.Style()
    style.configure('frame_style.TFrame', borderwidth = 2, relief = 'groove')
    frame.configure(style = 'frame_style.TFrame')

    return frame

def create_treeview(container:object, heading:str, data:list = []):
    treeview = ttk.Treeview(container)
    treeview.heading('#0', text = heading)
    treeview.grid(column = 0, row = 0, sticky = 'ns')

    for item in data:
        treeview.insert('', 'end', text = item)

    create_scrollbar(container = container, widget = treeview, column = 1)

    alt_row_colours(treeview = treeview)
    
    return treeview

def create_scrollbar(container:object, widget:object, column:int):
    scrollbar = ttk.Scrollbar(container, orient = tk.VERTICAL, command = widget.yview)
    scrollbar.grid(column = column, row = 0, sticky = 'ns')

    widget.configure(yscrollcommand = scrollbar.set)

def alt_row_colours(treeview:object):
    tag_even = 'even'
    tag_odd = 'odd'

    treeview.tag_configure(tag_even, background = 'white')
    treeview.tag_configure(tag_odd, background = 'light gray')

    for index, item_id in enumerate(treeview.get_children()):
        tag = tag_even if index % 2 == 0 else tag_odd
        treeview.item(item_id, tags = tag)

def update_text_widget(widget:object, info:str):
    widget.config(state = 'normal')
    widget.delete('1.0', tk.END)
    widget.insert(tk.END, info)
    widget.config(state = 'disabled')

def create_search(container:object, event:str, command):
    search = ttk.Entry(container)
    search.bind(event, command)  # Bind the event to the search function

    return search

lspci_selected = ''
setpci_selected = ''
device_selected = ''

devices = pipe('lspci -vmm', 'grep -w Device')
devices = devices.replace('Device:\t', '')
devices_list = devices.split('\n')
devices_list = list(filter(None, devices_list))    #Removes empty items in list.

slot = pipe('lspci -vvv', 'awk -v RS= {print$1}')
slot_list = slot.split('\n')
slot_list = list(filter(None, slot_list))

#Device specific commands
lspci_opd_name = ['lspci -vs', 'lspci -vvvs', 'lspci -nvmms', 'lspci -xxxs']

#Non device specific commands
lspic_op_name  = ['lspci -tv']

setpci_op_name = ['setpci --dumpregs']

main_window()