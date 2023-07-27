'''
Main file that will combine the data and the GUI.
'''

import data

import tkinter as tk
from tkinter import ttk

def main_window():
    lspci_selected = ''
    setpci_selected = ''
    devices_selected = ''

    def lspci_select(event):
        global lspci_selected
        selected_item = event.widget.selection()

        #True if selected_item is from the right treeview widget, since all functions get called
        #once an item is selected from a treeview
        if selected_item:
            setpci_tree.selection_remove(setpci_tree.selection())

            item_text = event.widget.item(selected_item, 'text')
            lspci_selected = item_text

            if devices_selected in data.lspci_opd_name:
                update_text_widget(text_widget, )

    def setpci_select(event):
        global setpci_selected
        selected_item = event.widget.selection()

        if selected_item:
            lspci_tree.selection_remove(lspci_tree.selection())
            devices_tree.selection_remove(devices_tree.selection())

            item_text = event.widget.item(selected_item, 'text')
            setpci_selected = item_text

    def devices_select(event):
        global devices_selected
        selected_item = event.widget.selection()

        if selected_item:
            item_text = event.widget.item(selected_item, 'text')
            devices_selected = item_text

    window = tk.Tk()

    #Start: Optioins Frame
    options_frame = create_frame(container = window)

    #lspci commands listed frame/treeview.
    lspci_frame = create_frame(container = options_frame)
    lspci_tree = create_treeview(container = lspci_frame, heading = 'lspci Options', data = data.lspci_opd_name + data.lspic_op_name)
    lspci_tree.grid(column = 0, row = 0)
    create_scrollbar(container = lspci_frame, widget = lspci_tree, column = 1)
    lspci_frame.grid(column = 0, row = 0, sticky = 'n')
    lspci_tree.bind('<<TreeviewSelect>>', lspci_select)

    #setpci commands listed frame/treeview.
    setpci_frame = create_frame(container = options_frame)
    setpci_tree = create_treeview(container = setpci_frame, heading = 'setpci Options', data = data.setpci_op_name)
    setpci_tree.grid(column = 0, row = 0)
    create_scrollbar(container = setpci_frame, widget = setpci_tree, column = 1)
    setpci_frame.grid(column = 0, row = 1, sticky = 'ns')
    setpci_tree.bind('<<TreeviewSelect>>', setpci_select)

    #Devices listed frame/treeview.
    devices_frame = create_frame(container = options_frame)
    devices_tree = create_treeview(container = devices_frame, heading = 'lspci Devices', data = data.slot_list)
    devices_tree.grid(column = 0, row = 0)
    create_scrollbar(container = devices_frame, widget = devices_tree, column = 1)
    devices_frame.grid(column = 1, row = 0, sticky = 'ns', rowspan = 2)
    devices_frame.grid_rowconfigure(0, weight = 1)
    devices_tree.bind('<<TreeviewSelect>>', devices_select)
    
    options_frame.grid(column = 0, row = 0, sticky = 'ns')
    #End

    #Start: Text widget frame for terminal.
    text_widget_frame = create_frame(window)

    text_widget = tk.Text(text_widget_frame, state = 'disabled')
    create_scrollbar(container = text_widget_frame, widget = text_widget, column = 1)
    text_widget.grid(column = 0, row = 0, sticky = 'ns')
    text_widget_frame.grid(column = 1, row = 0, sticky = 'ns')
    text_widget_frame.grid_rowconfigure(0, weight = 1)
    #End

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


main_window()