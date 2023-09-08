'''
Main file that will combine the data and the GUI.
'''

import tkinter as tk
from tkinter import ttk, simpledialog
import subprocess
import csv

sudo_password = ''
csv_data = []


def command(command:str, input:str = None):
    """Executes a bash command containing no pipe (|).
    
    Parameters
    commmand : str
        This is the command that will be executed.
    input : str = None
        The information you want the command to act on. (can be empty).

    Returns
        data.stdout : str
            The output of thebash command in a string.
    """
    if sudo_password:
        data = sudo_mode(command)
    else:
        data = subprocess.run(command, shell = True, capture_output = True, text = True, input = input) 

    return data.stdout


def sudo_mode(insert_command:str):          #Note: This uses the shell = True option
    """Enables sudo mode for a command.

    Parameters
    insert_command : str
        The command executed in sudo mode.

    Returns
    output : str
        The command in sudo mode.   
    """
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
    """The same as | in bash command. command1 | command2.

    Parameters
    command1 : str
        First command.
    command2 : str
        Second command.

    Returns
    command.stdout : str
        The output of the command.   
    """
    command1 = command1.split()
    command2 = command2.split()

    command = subprocess.run(command1, capture_output = True, text = True)
    command = command.stdout
    command = subprocess.run(command2, capture_output = True, text = True, input = command)

    return command.stdout


def index_get_paragragh(data:str, select:int):
    """Retrievs a pargraph from text.

    Parameters
    data : str
        This is the text from where the paragraph is retrieved from.
    select : int
        This is the location of the paragraph 1st, 2nd etc.

    Returns
    paragraph.stdout : str
        The paragraph from the text.
    """
    command = ['awk', '-v', 'RS=', '-v', 'ORS=', 'NR==' + str(select + 1)]

    paragraph = subprocess.run(command, capture_output = True, text = True, input = data)

    return paragraph.stdout


def word_get_paragraph(data:str, word:str):
    """Retrieves a paragraph based on the first word in it.

    Parameters
    data : str
        This is the text from where the paragraph is retrieved from.
    word : str
        This is the first word of the paragraph.

    Returns
    paragraph.stdout : str
        The paragraph from the text.
    """
    command = ['awk', '-v', 'RS=', f'/\\y{word}\\y/']
    paragraph = subprocess.run(command, capture_output = True, text = True, input = data)

    return paragraph.stdout


def word_get_line(data:str, word:str):
    """Gets the line from text, with the matching first word.

    Parameters
    data : str
        This is the text from where the line is retrieved from.
    word : str
        This is the first word of the line.

    Returns
    line.stdout : str
        The line from the text.
    """
    command = ['grep', '-w', f'{word}']
    line = subprocess.run(command, capture_output = True, text = True, input = data)

    return line.stdout


def retrieve_text(text_widget:object):
    """Return text(str) from text widget."""
    text = text_widget.get("1.0", "end-1c")  # Retrieve all text excluding the trailing newline character
    print(text)


def main_window():
    """Holds widgets needed for main_window"""
    def lspci_select(event):
        """Runs the corrosponding lspci command, when its selected in the lspci treeview.

        Parameters
        event : tkinter.Event (class)
            Contains information about the event. Used as event.widget, to retrieves the widget
            that activated that event.

        Returns

        """
        global command_selected
        selected_item = event.widget.selection()

        #True if selected_item is from the right treeview widget, since all functions get called
        #once an item is selected from a treeview this is because it works on a frame.
        if selected_item:
            setpci_tree.selection_remove(setpci_tree.selection())
            custom_tree.selection_remove(custom_tree.selection())

            item_text = event.widget.item(selected_item, 'text')
            command_selected = item_text

            if command_selected in lspci_opd_name and device_selected != "":
                update_text_widget(terminal, command(command_selected + device_selected))
            elif command_selected in lspic_op_name:
                update_text_widget(terminal, command(command_selected))


    def setpci_select(event):
        """Runs the corrosponding setpci command, when its selected in the setpci treeview.

        Parameters
        event : tkinter.Event (class)
            Contains information about the event. Used as event.widget , to retrieves the widget
            that activated that event.

        Returns

        """
        global command_selected, device_selected, setpci_option
        selected_item = event.widget.selection()

        if selected_item:
            lspci_tree.selection_remove(lspci_tree.selection())
            #devices_tree.selection_remove(devices_tree.selection())
            custom_tree.selection_remove(custom_tree.selection())

            command_selected = event.widget.item(selected_item, 'text')
            #device_selected = ""
            if command_selected in setpci_opd_name and device_selected != "":
                setpci_option = simpledialog.askstring('Config setpci', 'Enter configuration for selected device:') 
                update_text_widget(terminal, command(command_selected + device_selected + " " + setpci_option))
                print(command_selected + device_selected + " " + setpci_option)
            elif command_selected in setpci_op_name:
                update_text_widget(terminal, command(command_selected))


    def device_select(event):
        """Gets the selected device from the treeview and runs its corrosponging command.

        Parameters
        event : tkinter.Event (class)
            Contains information about the event. Used as event.widget , to retrieves the widget
            that activated that event.

        Returns

        """
        global device_selected, setpci_option
        selected_item = event.widget.selection()[0]

        if selected_item:
            custom_tree.selection_remove(custom_tree.selection())

            device_selected = event.widget.item(selected_item, 'values')[0]

            if command_selected in lspci_opd_name:
                update_text_widget(terminal, command(command_selected + device_selected))
            elif command_selected in lspic_op_name:
                update_text_widget(terminal, command(command_selected))
            elif command_selected in setpci_opd_name and device_selected != "":
                setpci_option = simpledialog.askstring('Config setpci', 'Enter configuration for selected device:') 
                update_text_widget(terminal, command(command_selected + device_selected + " " + setpci_option))


    def custom_selected(event):
        """Gets the selected command from the custom command treeview and executes it.

        Parameters
        event : tkinter.Event (class)
            Contains information about the event. Used as event.widget , to retrieves the widget
            that activated that event.

        Returns

        """
        selected_item = event.widget.selection()

        if selected_item:
            setpci_tree.selection_remove(setpci_tree.selection())
            lspci_tree.selection_remove(lspci_tree.selection())
            devices_tree.selection_remove(devices_tree.selection())
            device_selected = ""

            command_selected = event.widget.item(selected_item, 'values')
            command_selected = command_selected[0]
            
            update_text_widget(terminal, command(command_selected))


    def device_search(event):
        query = devices_entry.get()

        devices_tree.delete(*devices_tree.get_children())

        for item in slot_vendor:
            if query.lower() in item[0].lower() or query.lower() in item[1].lower():
                devices_tree.insert("", "end", values=item)
        alt_row_colours(devices_tree)


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
    
    # Start custom_commands/csv file methods
    csv_file_name = 'custom_commands.csv'
    new_data = []

    def load_csv():
        try:
            with open(csv_file_name, mode='r') as file:
                reader = csv.reader(file)
                # Iterate through each row in the CSV file
                for row in reader:
                    custom_tree.insert('', 'end', values = row)           # Treeview in custom_window
            alt_row_colours(treeview = custom_tree)
        except FileNotFoundError:
            print('No custom_commands.csv, creating custom_commands.csv once a command is saved')


    def add_data(event):
        if custom_entry.get() != '':
            new_data.append(custom_entry.get())
            custom_tree.insert('', 'end', values = new_data)
            custom_entry.delete(0, 'end')
            alt_row_colours(treeview = custom_tree)

            with open(csv_file_name, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(new_data)
                new_data.clear()


    def remove_item(event):
        selected_items = custom_tree.selection()
        for item in selected_items:
            values = custom_tree.item(item, "values")
            custom_tree.delete(item)
            alt_row_colours(treeview = custom_tree)

            # Update CSV file by rewriting the file without the deleted row
            with open(csv_file_name, "r") as file:
                lines = file.readlines()

            with open(csv_file_name, "w", newline="") as file:
                writer = csv.writer(file)
                for line in lines:
                    if line.strip() != values[0]:
                        writer.writerow([line.strip()])
    # End custom_commands/csv file methods

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
    setpci_tree = create_treeview(container = setpci_frame, heading = 'setpci Options', data = setpci_op_name + setpci_opd_name)
    setpci_frame.grid(column = 0, row = 1, sticky = 'ns')
    setpci_tree.bind('<<TreeviewSelect>>', setpci_select)

    devices_frame = create_frame(container = options_frame)
    # cant use create_treeview as 2 columns is needed
    # show="headings", stops the default column from shownig (#0)
    devices_tree = ttk.Treeview(devices_frame, columns=("Slot", "Vendor"), show="headings")
    devices_tree.heading("Slot", text="Slot") 
    devices_tree.heading("Vendor", text="Vendor")
    devices_tree.column("Slot", width = 100)
    devices_tree.column("Vendor", width = 500)
    for item in slot_vendor:
        devices_tree.insert("", "end", values=item)
    alt_row_colours(devices_tree)
    create_scrollbar(container = devices_frame, widget = devices_tree, column = 1)
    devices_tree.grid(column = 0, row=0, sticky="ns")
    devices_frame.grid(column = 1, row = 0, sticky = "ns", rowspan=2)
    devices_frame.grid_rowconfigure(0, weight=1)
    devices_tree.bind("<<TreeviewSelect>>", device_select)
    
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
    
    # Start: Custom commands treeview widget
    custom_frame = create_frame(window)
    custom_tree= ttk.Treeview(custom_frame, columns=("Commands"), show="headings")      #Couldnt use the create_treeview function as it returns a frame (cant edit data)
    custom_tree.heading("Commands", text="Custom Commands")
    create_scrollbar(container = custom_frame, widget = custom_tree, column = 1)
    custom_tree.grid(column = 0, row = 0, sticky = 'ns')
    custom_tree.bind("<BackSpace>", remove_item)
    custom_tree.bind("<Double-1>", custom_selected)

    entry_frame = create_label_frame(custom_frame, 'Command to Save')
    custom_entry = ttk.Entry(entry_frame)
    custom_entry.bind('<Return>', add_data)
    custom_entry.grid(column = 0, row = 1, sticky = 'ew')
    entry_frame.grid(column = 0, row = 1, sticky = 'ew')
    entry_frame.grid_columnconfigure(0, weight = 1)
    
    custom_frame.grid(column = 2, row = 0, sticky = 'ns')
    custom_frame.grid_rowconfigure(0, weight = 1)

    load_csv()
    # End: Custom commands treeview widget

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
    #menu_options.add_command(label = 'Edit Custom Commands', command = custom_window)
    menu_options.add_command(label = 'Sudo Mode', command = save_sudo)
    #End: Options

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

slot = pipe('lspci -vvv', 'awk -v RS= {print$1}')    # Cant use grep as ther are 2 Device rows
slot_list = slot.split('\n')
slot_list = list(filter(None, slot_list))
nested_slot = [[item] for item in slot_list]

vendor = pipe("lspci -vmm", "grep -w Vendor")
vendor = vendor.replace('Vendor:\t', '')
vendor_list = vendor.split("\n")
vendor_list = list(filter(None, vendor_list))
nested_vendor = [[item] for item in vendor_list]

slot_vendor = nested_slot
for index in range(len(nested_slot)):
    slot_vendor[index].append(vendor_list[index])
    slot_vendor[index] = tuple(slot_vendor[index])

#Device specific commands
lspci_opd_name = ['lspci -vs', 'lspci -vvvs', 'lspci -nvmms', 'lspci -xxxs']

setpci_opd_name = ['setpci -v -s ', 'setpci -vD -s ']

#Non device specific commands
lspic_op_name  = ['lspci -tv']

setpci_op_name = ['setpci --dumpregs']

main_window()
