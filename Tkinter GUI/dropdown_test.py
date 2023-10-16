import tkinter as tk
from tkinter import ttk

def show_info(item):
    info_label.config(text=f"More information about {item}:")
    # Replace the following line with the actual information retrieval based on the selected item
    info_text.set("This is additional information about {}".format(item))

root = tk.Tk()
root.title("Item Information")

item_list = ["Item 1", "Item 2", "Item 3", "Item 4"]

listbox = tk.Listbox(root)
for item in item_list:
    listbox.insert(tk.END, item)
listbox.pack()

info_label = tk.Label(root, text="")
info_label.pack()

info_text = tk.StringVar()
info_text.set("Select an item to see more information.")
info_display = ttk.Label(root, textvariable=info_text, wraplength=300)
info_display.pack()

listbox.bind("<<ListboxSelect>>", lambda event: show_info(listbox.get(tk.ACTIVE)))

root.mainloop()