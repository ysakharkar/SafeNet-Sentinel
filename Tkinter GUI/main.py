import tkinter as tk
from tkinter import filedialog
import threading
import subprocess
import re
import webbrowser
from tkinter import ttk
from functools import partial


exclude = ['deleted old file', 'Successfully appended the outputs of the commands to mySoftwares.txt']


def scan_software():
    scanning_now()

    result = subprocess.run(["python", r'C:\Users\arcad\OneDrive\Desktop\Persistent Project\Database Testing\tryingWithMaps.py'], capture_output=True, text=True)

    output = result.stdout.replace('\\n', '\n')
    output = output.splitlines()
    filtered_output = ""

    for line in output:
        if line not in exclude:
            filtered_output += line + '\n'

    update_with_links(filtered_output)

    root.after(0, scanning_done())




def update_with_links(output):
    result_text.delete(1.0, tk.END)

    lines = output.split("\n")

    for line in lines:
        if 'nvd.nist.gov' in line:
            result_text.insert(tk.END, line + '\n', "hyperlink")
            result_text.tag_configure("hyperlink", foreground="blue", underline=True, font=("Georgia", 10))
            result_text.tag_bind("hyperlink", "<Button-1>", partial(on_hyperlink_click))
            result_text.tag_bind("hyperlink", "<Enter>", on_hyperlink_enter)
            result_text.tag_bind("hyperlink", "<Leave>", on_hyperlink_leave)
        else:
            result_text.insert(tk.END, line + '\n', "bold")


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


root = tk.Tk()
root.title("Software Scanner")
root.geometry("500x500")

root.call('source', r'./Azure/azure.tcl')
root.call('set_theme', 'dark')

root.call()

# Create a Text widget to display the results
result_text = tk.Text(root, width=100, height=50, bg="gray46")
scrollbar = ttk.Scrollbar(root, command=result_text.yview)
result_text.configure(yscrollcommand=scrollbar.set)
result_text.tag_configure("bold", font=("Georgia", 12, "bold"), foreground="black", underline=True)
result_text.pack()

# Create the "Scan" button
scan_button = tk.Button(root, text="Scan", command=lambda: threading.Thread(target=scan_software).start(), cursor="hand2", font=("Georgia", 12, "bold"))
scan_button.pack()

# Create the label to show the scanning message
scan_label = tk.Label(root, text="Not scanning yet", fg="white", font=("Georgia", 12, "bold"))
scan_label.pack()


root.mainloop()