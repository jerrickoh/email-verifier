import tkinter as tk
from validate_email import validate_email

def check_email(event=None):
    email = email_entry.get()
    if validate_email(email, verify=True):
        result_label.config(text="The email address is deliverable.", fg="green")
    else:
        result_label.config(text="The email address is not deliverable.", fg="red")

def cut_text():
    email_entry.event_generate("<<Cut>>")

def copy_text():
    email_entry.event_generate("<<Copy>>")

def paste_text():
    email_entry.event_generate("<<Paste>>")

def select_all_text():
    email_entry.select_range(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Email Verifier v2.5")

# Create widgets
email_label = tk.Label(root, text="Enter Email Address:")
email_label.grid(row=0, column=0, padx=10, pady=5)

email_entry = tk.Entry(root, width=30)
email_entry.grid(row=0, column=1, padx=10, pady=5)

# Create a context menu for the email entry field
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Cut", command=cut_text)
context_menu.add_command(label="Copy", command=copy_text)
context_menu.add_command(label="Paste", command=paste_text)
context_menu.add_separator()
context_menu.add_command(label="Select All", command=select_all_text)

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

email_entry.bind("<Button-3>", show_context_menu)

check_button = tk.Button(root, text="Check Deliverability", command=check_email)
check_button.grid(row=1, column=0, columnspan=2, pady=5)

result_label = tk.Label(root, text="", fg="black")
result_label.grid(row=2, column=0, columnspan=2, pady=5)

# Bind the Enter key to the check_email function
root.bind('<Return>', check_email)

# Start the GUI main loop
root.mainloop()
