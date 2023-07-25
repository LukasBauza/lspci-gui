'''
Main file that will combine the data and the GUI.
'''

import data

import tkinter as tk
from tkinter import ttk

def main_window():
    window = tk.Tk()

    #Start: Optioins Frame
    #lspci commands listed.
    options_frame = create_frame(container = window)

    lspci_tree = create_treeview(container = options_frame, heading = 'lspci Options')
    lspci_tree.grid(column = 0, row = 0, sticky = 'ns')
    lspci_tree.grid_rowconfigure(0, weight = 1)

    #setpci commands listed.
    setpci_tree = create_treeview(container = options_frame, heading = 'setpci Options')
    setpci_tree.grid(column = 1, row = 0, sticky = 'ns')
    setpci_tree.grid_rowconfigure(0, weight = 1)

    #Devices listed.
    devices_tree = create_treeview(container = options_frame, heading = 'Devices', data = data.devices_list)
    devices_tree.grid(column = 2, row = 0, sticky = 'ns')
    devices_tree.grid_rowconfigure(0, weight = 1)
    
    options_frame.grid(column = 0, row = 0, sticky = 'ns')
    options_frame.grid_rowconfigure(0, weight = 1)
    #End

    #Start: Text widget frame
    text_widget_frame = create_frame(window)
    text_widget = tk.Text(text_widget_frame, state = 'disabled')
    create_scrollbar(container = text_widget_frame, widget = text_widget, column = 1)
    text_widget.grid(column = 0, row = 0)
    text_widget_frame.grid(column = 1, row = 0)
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
    treeview_frame = create_frame(container = container)
    treeview = ttk.Treeview(treeview_frame)
    treeview.heading('#0', text = heading)
    treeview.grid(column = 0, row = 0, sticky = 'ns')

    create_scrollbar(container = treeview_frame, widget = treeview, column = 1)

    for item in data:
        treeview.insert('', 'end', text = item)
    
    return treeview_frame

def create_scrollbar(container:object, widget:object, column:int):
    scrollbar = ttk.Scrollbar(container, orient = tk.VERTICAL, command = widget.yview)
    scrollbar.grid(column = column, row = 0, sticky = 'ns')

    widget.configure(yscrollcommand = scrollbar.set)

main_window()