import tkinter as tk
import requests
import re

# -- Emailable API key --
API_KEY = "INSERT_API_KEY_HERE"  # Replace with your Emailable API key

# -- Basic syntax check --
def is_valid_syntax(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# -- Email check using Emailable API --
def check_email(event=None):
    email = email_entry.get().strip()

    if not is_valid_syntax(email):
        result_label.config(text="Invalid email syntax.", fg="red")
        return

    result_label.config(text="Validating...", fg="black")
    root.update_idletasks()

    try:
        response = requests.get(
            "https://api.emailable.com/v1/verify",
            params={"email": email, "api_key": API_KEY},
            timeout=10
        )

        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        try:
            data = response.json()
        except ValueError:
            result_label.config(text="Invalid JSON response from API.", fg="red")
            return

        if response.status_code != 200:
            error_msg = data.get("error", {}).get("message", "Unknown error")
            result_label.config(text=f"API error: {error_msg}", fg="red")
            return

        state = data.get("state")
        reason = data.get("reason", "")
        is_catch_all = data.get("accept_all", False)

        if state == "deliverable":
            if is_catch_all:
                result_label.config(text="Deliverable, but domain is catch-all.", fg="blue")
            else:
                result_label.config(text="Email address is deliverable.", fg="green")
        elif state == "undeliverable":
            result_label.config(text="Email is undeliverable.", fg="red")
        elif state == "risky":
            result_label.config(text=f"Risky: {reason.replace('_', ' ')}.", fg="orange")
        else:
            result_label.config(text="Unknown result from API.", fg="red")

    except requests.RequestException as e:
        result_label.config(text=f"Request error: {str(e)}", fg="red")



# -- Context menu functionality --

def cut_text():
    email_entry.event_generate("<<Cut>>")

def copy_text():
    email_entry.event_generate("<<Copy>>")

def paste_text():
    email_entry.event_generate("<<Paste>>")

def select_all_text():
    email_entry.select_range(0, tk.END)

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

# -- GUI setup --

root = tk.Tk()
root.title("Email Verifier via Emailable API")

root.geometry("335x97")
root.resizable(False, False)

email_label = tk.Label(root, text="Enter Email Address:")
email_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

email_entry = tk.Entry(root, width=30)
email_entry.grid(row=0, column=1, padx=5, pady=5)

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Cut", command=cut_text)
context_menu.add_command(label="Copy", command=copy_text)
context_menu.add_command(label="Paste", command=paste_text)
context_menu.add_separator()
context_menu.add_command(label="Select All", command=select_all_text)
email_entry.bind("<Button-3>", show_context_menu)

check_button = tk.Button(root, text="Check", width=10, command=check_email)
check_button.grid(row=1, column=0, columnspan=2, pady=2)

result_label = tk.Label(root, text="", fg="black")
result_label.grid(row=2, column=0, columnspan=2, pady=2)

root.bind('<Return>', check_email)
root.mainloop()
