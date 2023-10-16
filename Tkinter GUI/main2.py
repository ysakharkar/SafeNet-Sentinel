import tkinter as tk
from tkinter import filedialog
import threading
import subprocess
import re
import webbrowser
from tkinter import ttk
from functools import partial


exclude = ['deleted old file', 'Successfully appended the outputs of the commands to mySoftwares.txt']
map = {}

def scan_software():
    scanning_now()

    result = subprocess.run(["python", r'C:\Users\arcad\OneDrive\Desktop\Persistent Project\Database Testing\tryingWithMaps2.py'], capture_output=True, text=True)

    output = result.stdout.replace('\\n', '\n')
    output = output.splitlines()
    filtered_output = ""

    for line in output:
        if line not in exclude:
            filtered_output += line + '\n'

    update_with_links(filtered_output)

    root.after(0, scanning_done())




def update_with_links(output):

    lines = output.split("\n")

    for line in lines:
        if 'CVE' in line:
            info = line.split("!")

            map[info[0]] = []
            print(f'adding key {info[0]} to map of length {len(info[0])}')
            
            for s in info:
                print(s + " " + info[0])
                map.get(info[0]).append(s)

            result_text.insert(tk.END, info[0] + '\n')
            # result_text.tag_configure("hyperlink", foreground="blue", underline=True, font=("Georgia", 10))
            # result_text.tag_bind("hyperlink", "<Button-1>", partial(on_hyperlink_click))
            # result_text.tag_bind("hyperlink", "<Enter>", on_hyperlink_enter)
            # result_text.tag_bind("hyperlink", "<Leave>", on_hyperlink_leave)
        else:
            map[line] = []
            map.get(line).append("")
            result_text.insert(tk.END, line + '\n')


def on_hyperlink_click(event):
    index = result_text.index("@%s,%s" % (event.x, event.y))
    line = result_text.get("%s linestart" % index, "%s lineend" % index)
    if line:
        webbrowser.open(line)

def on_hyperlink_enter(event):
    result_text.config(cursor="hand2")

def on_hyperlink_leave(event):
    result_text.config(cursor="arrow")

def scanning_now():
    scan_label.config(text="Scanning 3272 CVEs... please wait")


def scanning_done():
    scan_label.config(text="Done scanning")
    info_text.set("Select an item to see more information.")

def show_info(item):

    toDisplay = ""
    
    for s in map.get(item[:-1]):
        toDisplay += s
        toDisplay += "\n"

    info_text.set(toDisplay)


root = tk.Tk()
root.title("Software Scanner")
root.geometry("500x500")

root.call('source', r'./Azure/azure.tcl')
root.call('set_theme', 'dark')

root.call()

# Add title label at the top
title_label = tk.Label(root, text="SafeNet Sentinel", font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

# Create a Text widget to display the results
result_text = tk.Listbox(root, width=100, height=40, bg="gray46")
scrollbar = ttk.Scrollbar(root, command=result_text.yview)
result_text.configure(yscrollcommand=scrollbar.set)
result_text.pack()

# Create the "Scan" button
scan_button = tk.Button(root, text="Scan", command=lambda: threading.Thread(target=scan_software).start(), cursor="hand2", font=("Georgia", 12, "bold"))
scan_button.pack()

# Create the label to show the scanning message
scan_label = tk.Label(root, text="Not scanning yet", fg="white", font=("Georgia", 12, "bold"))
scan_label.pack()

info_label = tk.Label(root, text="")
info_label.pack()
info_text = tk.StringVar()
info_text.set("")
info_display = ttk.Label(root, textvariable=info_text, wraplength=500)
info_display.pack()


result_text.bind("<<ListboxSelect>>", lambda event: show_info(result_text.get(tk.ACTIVE)))


root.mainloop()