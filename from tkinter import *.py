from tkinter import *


def login_success():
    # Replace this with your desired action after successful login
    # (e.g., open a new window for the quiz)
    print("Login successful!")
    # You can call your start_quiz function here


def login_attempt():
    username = username_entry.get()
    password = password_entry.get()

    # Implement your login validation logic here
    # (e.g., check username and password against a database or predefined values)

    if username == "Alxproject" and password == "Alx2024":
        login_success()
        # Hide the login window
        login_window.destroy()
    else:
        # Display error message for incorrect login
        error_label.config(text="Invalid username or password!")


login_window = Tk()
login_window.title("Login")
login_window.geometry("300x200")
login_window.minsize(300, 200)

# Username label and entry
username_label = Label(login_window, text="Username:")
username_label.pack(pady=10)
username_entry = Entry(login_window)
username_entry.pack()

# Password label and entry (with asterisk masking)
password_label = Label(login_window, text="Password:")
password_label.pack(pady=10)
password_entry = Entry(login_window, show="*")
password_entry.pack()

# Error label (initially hidden)
error_label = Label(login_window, text="")
error_label.pack()

# Login button
login_button = Button(login_window, text="Login", command=login_attempt)
login_button.pack(pady=10)

login_window.mainloop()