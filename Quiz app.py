import sqlite3
from tkinter import *
from tkinter import messagebox

# Database setup
def create_tables():
    conn = sqlite3.connect('quiz_app.db')
    c = conn.cursor()

    # Create table for users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0
                )''')

    # Create table for quizzes
    c.execute('''CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
                )''')

    # Create table for questions
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                answer TEXT NOT NULL,
                FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
                )''')

    # Create table for quiz history
    c.execute('''CREATE TABLE IF NOT EXISTS quiz_history (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                quiz_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                date_taken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
                )''')

    conn.commit()
    conn.close()

create_tables()

# Global variables
current_user_id = None
current_question = 0
current_quiz_id = 1  # Example quiz_id for demonstration

question = {
	"An elementary school teacher wishes to assess the results of her new reading approach on third grade students. She/he randomly chooses a third grade reading class out of six. She/he teaches the class using the new approach, and compares students' reading scores from before the start of the new approach to their reading scores after using the new approach": ['There was a significant effect of the new approach.', 'There was no significant effect of the new approach.', 'The effect cannot be determined', 'The effect of the new approach was negative'],
	"She/he also reports the size of the difference between the means as a measure of the effect of the new reading approach on the students' reading scores. The effect size(s) suggest": ['The new approach had no effect on students reading scores', 'The new approach had a large effect on students reading scores.', 'The new approach had a small effect on students reading scores'],
	"If a significant difference was found between the classes, to determine which class scored higher, she/he would observe": ['The significance value', 'The effect size', 'The means', 'standard deviations']
}
# define answer list
ans = ['The effect of the new approach was negative', 'The new approach had a small effect on students reading scores', 'The means']

# User authentication functions
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    conn = sqlite3.connect('quiz_app.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
    conn.close()

def login_user():
    global current_user_id
    username = entry_username.get()
    password = entry_password.get()
    conn = sqlite3.connect('quiz_app.db')
    c = conn.cursor()
    c.execute("SELECT id, is_admin FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    if user:
        current_user_id = user[0]
        messagebox.showinfo("Success", "Login successful!")
        if user[1] == 1:
            admin_dashboard()
        else:
            start_quiz()
    else:
        messagebox.showerror("Error", "Invalid credentials")
    conn.close()

def register_screen():
    global entry_username
    global entry_password

    register = Toplevel(root)
    register.title("Register")

    Label(register, text="Username").pack()
    entry_username = Entry(register)
    entry_username.pack()

    Label(register, text="Password").pack()
    entry_password = Entry(register, show='*')
    entry_password.pack()

    Button(register, text="Register", command=register_user).pack()

def login_screen():
    global entry_username
    global entry_password

    login = Toplevel(root)
    login.title("Login")

    Label(login, text="Username").pack()
    entry_username = Entry(login)
    entry_username.pack()

    Label(login, text="Password").pack()
    entry_password = Entry(login, show='*')
    entry_password.pack()

    Button(login, text="Login", command=login_user).pack()

# Quiz functions
def start_quiz():
    start_button.forget()
    next_button.pack()
    next_question()

def next_question():
    global current_question
    if current_question < len(question):
        check_ans()
        user_ans.set('None')
        c_question = list(question.keys())[current_question]
        clear_frame()
        Label(f1, text=f"Question : {c_question}", padx=15, font="calibre 12 normal").pack(anchor=NW)
        for option in question[c_question]:
            Radiobutton(f1, text=option, variable=user_ans, value=option, padx=28).pack(anchor=NW)
        current_question += 1
    else:
        next_button.forget()
        check_ans()
        clear_frame()
        output = f"Your Score is {user_score.get()} out of {len(question)}"
        Label(f1, text=output, font="calibre 25 bold").pack()
        Label(f1, text="Thanks for Participating", font="calibre 18 bold").pack()
        end_quiz()

def check_ans():
    if current_question > 0:
        temp_ans = user_ans.get()
        if temp_ans != 'None' and temp_ans == ans[current_question-1]:
            user_score.set(user_score.get()+1)

def end_quiz():
    conn = sqlite3.connect('quiz_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO quiz_history (user_id, quiz_id, score) VALUES (?, ?, ?)",
              (current_user_id, current_quiz_id, user_score.get()))
    conn.commit()
    conn.close()

def clear_frame():
    for widget in f1.winfo_children():
        widget.destroy()

# Admin functions
def admin_dashboard():
    admin = Toplevel(root)
    admin.title("Admin Dashboard")

    Button(admin, text="Add Quiz", command=add_quiz_screen).pack()
    Button(admin, text="Add Question", command=add_question_screen).pack()

def add_quiz_screen():
    quiz_screen = Toplevel(root)
    quiz_screen.title("Add Quiz")

    Label(quiz_screen, text="Quiz Name").pack()
    entry_quiz_name = Entry(quiz_screen)
    entry_quiz_name.pack()

    def add_quiz():
        quiz_name = entry_quiz_name.get()
        conn = sqlite3.connect('quiz_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO quizzes (name) VALUES (?)", (quiz_name,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Quiz added successfully!")
        quiz_screen.destroy()

    Button(quiz_screen, text="Add Quiz", command=add_quiz).pack()

def add_question_screen():
    question_screen = Toplevel(root)
    question_screen.title("Add Question")

    Label(question_screen, text="Quiz ID").pack()
    entry_quiz_id = Entry(question_screen)
    entry_quiz_id.pack()

    Label(question_screen, text="Question").pack()
    entry_question = Entry(question_screen)
    entry_question.pack()

    Label(question_screen, text="Answer").pack()
    entry_answer = Entry(question_screen)
    entry_answer.pack()

    def add_question():
        quiz_id = entry_quiz_id.get()
        question_text = entry_question.get()
        answer = entry_answer.get()
        conn = sqlite3.connect('quiz_app.db')
        c = conn.cursor()
        c.execute("INSERT INTO questions (quiz_id, question_text, answer) VALUES (?, ?, ?)",
                  (quiz_id, question_text, answer))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Question added successfully!")
        question_screen.destroy()

    Button(question_screen, text="Add Question", command=add_question).pack()

# Main application setup
if __name__ == "__main__":
    root = Tk()
    root.title("Quiz App")
    root.geometry("850x520")
    root.minsize(800, 400)

    user_ans = StringVar()
    user_ans.set('None')
    user_score = IntVar()
    user_score.set(0)

    Label(root, text="Quiz App", font="calibre 40 bold", relief=SUNKEN, background="cyan", padx=10, pady=9).pack()
    Label(root, text="", font="calibre 10 bold").pack()
    start_button = Button(root, text="Start Quiz", command=start_quiz, font="calibre 17 bold")
    start_button.pack()

    f1 = Frame(root)
    f1.pack(side=TOP, fill=X)

    next_button = Button(root, text="Next Question", command=next_question, font="calibre 17 bold")

    Button(root, text="Register", command=register_screen, font="calibre 17 bold").pack()
    Button(root, text="Login", command=login_screen, font="calibre 17 bold").pack()

    root.mainloop()