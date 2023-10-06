import tkinter as tk

def show_popup():
    popup = tk.Toplevel(root)
    popup.title("Popup Window")

    # Create a label to display text in the popup window
    text_label = tk.Label(popup, text="This is some text in the pop-up window.")
    text_label.pack(padx=20, pady=20)

    # Add a button to close the popup window
    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack()

root = tk.Tk()
root.title("Main Window")

# Create a button to open the popup window
popup_button = tk.Button(root, text="Open Popup", command=show_popup)
popup_button.pack(padx=20, pady=20)

root.mainloop()

