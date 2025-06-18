import tkinter as tk
import smtplib
import dns.resolver

def smtp_check(email):
    try:
        domain = email.split('@')[1]
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)

        server = smtplib.SMTP(timeout=10)
        server.connect(mx_record)
        server.helo(server.local_hostname)  # Send HELO command
        server.mail('your_email@example.com')  # Use any valid sender email here
        code, message = server.rcpt(email)
        server.quit()

        # 250 is success code for recipient OK
        if code == 250:
            return True
        else:
            return False
    except Exception as e:
        print(f"SMTP check error: {e}")
        return False

def check_email(event=None):
    email = email_entry.get().strip()

    if '@' not in email or '.' not in email.split('@')[-1]:
        result_label.config(text="Invalid email syntax.", fg="red")
        return

    try:
        # Check if domain has MX records
        domain = email.split('@')[1]
        dns.resolver.resolve(domain, 'MX')
    except Exception:
        result_label.config(text="Domain not found or no MX records.", fg="red")
        return

    # Run SMTP deliverability check
    if smtp_check(email):
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
root.title("Email Verifier v3")

# Create widgets
email_label = tk.Label(root, text="Enter Email Address:")
email_label.grid(row=0, column=0, padx=10, pady=5)

email_entry = tk.Entry(root, width=30)
email_entry.grid(row=0, column=1, padx=10, pady=5)

# Context menu for the entry field
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

root.bind('<Return>', check_email)
root.mainloop()
