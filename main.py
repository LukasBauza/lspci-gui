'''
Main file that will combine the data and the GUI.
'''

import tkinter as tk
from tkinter import ttk, simpledialog
import subprocess
import csv
import os

sudo_password = ''
csv_data = []
 
def command(command:str, input:str = None):
    if sudo_password:
        data = sudo_mode(command)
    else:
        command = command.split()
        data = subprocess.run(command, capture_output = True, text = True, input = input) 
    return data.stdout

def sudo_mode(insert_command:str):          #Note: This uses the shell = True option
    if sudo_password:
        command = f"echo '{sudo_password}' | sudo -S {insert_command}"
        try:
            output = subprocess.run(command, shell = True, capture_output= True, text=True)
            print("Command executed successfully with sudo.")
            return output
        except subprocess.CalledProcessError as e:
            print("Error executing command with sudo:", e)
    else:
        print("No sudo password entered.")
    
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

def retrieve_text(text_widget:object):
    text = text_widget.get("1.0", "end-1c")  # Retrieve all text excluding the trailing newline character
    print(text)

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
        treeview.delete(*treeview.get_children())  #Clear the treeview
        filtered_data = [item for item in data if query.lower() in item.lower()]
        for item in filtered_data:
            treeview.insert('', 'end', text = item)
        alt_row_colours(treeview = treeview)

    def device_search(event):
        query = devices_entry.get()
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

    def get_custom_command(event):
        custom_command = command_entry.get()
        command_entry.delete(0, "end")  # Clear the entry widget
        update_text_widget(terminal, command(custom_command))   #Note: The command doesnt take in |

    def save_sudo():
        global sudo_password
        sudo_password = simpledialog.askstring('Sudo Password', 'Enter our sudo password:', show = '*')
    
    window = tk.Tk()

    #Start: Options Frame
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
    devices_tree.bind('<<TreeviewSelect>>', device_select)
    devices_frame.grid(column = 1, row = 0, sticky = 'ns', rowspan = 2)
    devices_frame.grid_rowconfigure(0, weight = 1)
    
    devices_entry_frame = create_label_frame(devices_frame, 'Search Devices')
    devices_entry = create_search(devices_entry_frame, '<KeyRelease>', device_search)
    devices_entry.grid(column = 0, row = 0, sticky = 'ew')
    devices_entry_frame.grid(column = 0, row = 1, sticky = 'ew')
    devices_entry_frame.grid_columnconfigure(0, weight = 2)

    options_frame.grid(column = 0, row = 0, sticky = 'ns')
    options_frame.grid_rowconfigure(0, weight = 1)
    #End: Options Frame

    #Start: Text widget frame for terminal.
    terminal_frame = create_frame(window)

    terminal = tk.Text(terminal_frame, state = 'disabled', wrap = 'word')
    create_scrollbar(container = terminal_frame, widget = terminal, column = 1)
    terminal.grid(column = 0, row = 0, sticky = 'ns')
    terminal.tag_configure("search", background = "light blue")
    
    terminal_entry_frame = create_label_frame(terminal_frame, 'Search Terminal')
    terminal_entry = create_search(terminal_entry_frame, '<KeyRelease>', terminal_search)
    terminal_entry.grid(column = 0, row = 1, sticky = 'ew')
    terminal_entry_frame.grid(column = 0, row = 1, sticky = 'ew')
    terminal_entry_frame.grid_columnconfigure(0, weight = 1)
    
    terminal_frame.grid(column = 1, row = 0, sticky = 'ns')
    terminal_frame.grid_rowconfigure(0, weight = 1)
    #End: Text widget frame for terminal.

    #Start: Command entry frame.
    command_entry_frame = create_label_frame(window, 'Enter Command')
    command_entry = ttk.Entry(command_entry_frame)
    command_entry.bind('<Return>', get_custom_command)
    command_entry.grid(column = 0, row = 0, sticky = 'ew')
    command_entry_frame.grid(column = 0, row = 1, sticky = 'ew')
    command_entry_frame.grid_columnconfigure(0, weight = 1)
    #End: Command entry frame.

    #Start: Options
    menu_bar = tk.Menu(window)
    window['menu'] = menu_bar
    menu_options = tk.Menu(menu_bar, tearoff = False)
    menu_bar.add_cascade(menu = menu_options, label = 'Options')
    menu_options.add_command(label = 'Save Terminal Data')
    menu_options.add_command(label = 'Edit Custom Commands', command = custom_window)
    menu_options.add_command(label = 'Sudo Mode', command = save_sudo)
    #End: Options

    window.mainloop()

def custom_window():
    window = tk.Tk()

    csv_file_name = 'custom_commands.csv'
    treeview_data = []

    try:
        with open(csv_file_name, mode='r') as file:
            reader = csv.reader(file)

            # Iterate through each row in the CSV file
            for row in reader:
                treeview_data.append(row[0])

    except FileNotFoundError:
        print('File not found')

    def save(event):
        global treeview_custom
        csv_add_data = []
        if treeview_entry.get() != '':
            csv_add_data.append(treeview_entry.get())
            treeview_data.append(treeview_entry.get())
            treeview_entry.delete(0, "end")

            with open(csv_file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(csv_add_data)
                csv_add_data = []
        
            treeview_custom = create_treeview(container = treeview_frame, heading = 'Custom Commands', data = treeview_data)
            
    treeview_frame = create_frame(window)
    treeview_custom = create_treeview(container = treeview_frame, heading = 'Custom Commands', data = treeview_data)
    treeview_custom.grid(column = 0, row = 0)

    entry_frame = create_label_frame(treeview_frame, 'Command to Save')
    treeview_entry = ttk.Entry(entry_frame)
    treeview_entry.bind('<Return>', save)
    treeview_entry.grid(column = 0, row = 1, sticky = 'ew')
    entry_frame.grid(column = 0, row = 1, sticky = 'ew')
    entry_frame.grid_columnconfigure(0, weight = 1)
    
    treeview_frame.grid(column = 0, row = 0)


    window.mainloop()

def create_frame(container:object):
    frame = ttk.Frame(container)

    #Styling for the frame
    style = ttk.Style()
    style.configure('frame_style.TFrame', borderwidth = 2)
    frame.configure(style = 'frame_style.TFrame')

    return frame

def create_label_frame(container:object, title:str):
    label_frame = ttk.Labelframe(container, text = title)

    #Styling for the frame
    style = ttk.Style()
    style.configure('lf_style.TLabelframe.Label', font=("Helvetica", 10, "bold"))
    label_frame.configure(style = 'lf_style.TLabelframe')

    return label_frame

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