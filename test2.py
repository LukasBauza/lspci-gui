import tkinter as tk
from tkinter import ttk

def show_selected_row(event):
    selected_item = tree.selection()[0]
    item_text = tree.item(selected_item, 'values')[0]  # Only retrieve the first column's value
    selected_label.config(text=f"Selected Row: {item_text}")

root = tk.Tk()
root.title("Treeview Example")

# Create TreeView
tree = ttk.Treeview(root, columns=("Column1", "Column2"), show="headings")
tree.heading("Column1", text="Column 1")
tree.heading("Column2", text="Column 2")
tree.column("Column1", width=150)
tree.column("Column2", width=150)

# Insert sample data
data = [("Row 1 Data 1", "Row 1 Data 2"),
        ("Row 2 Data 1", "Row 2 Data 2"),
        ("Row 3 Data 1", "Row 3 Data 2")]

for row in data:
    tree.insert("", "end", values=row)

tree.pack()

# Label to display selected row information
selected_label = tk.Label(root, text="")
selected_label.pack()

# Bind selection event to the TreeView
tree.bind("<<TreeviewSelect>>", show_selected_row)

root.mainloop()
