import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta
import random

PROMPTS = [
    "What is one small step you can take today?",
    "What would make today feel successful?",
    "What is one thing you can do to take care of yourself today?",
    "What is something you can do today that will make you happy?",
    "What do you wanna achieve today?",
    "What's on the agenda for today?",
    "What's the plan for today?",
     "What are you hoping to get done?",
    "What's on your mind for today?",
    "Anything you'd like to accomplish today?",
]

DATA_FILE = "goals.json"

def load_goals():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_goals(goals):
    with open(DATA_FILE, "w") as f:
        json.dump(goals, f, indent=2)

def get_date_string(offset=0):
    return (datetime.today() + timedelta(days=offset)).strftime("%Y-%m-%d")

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cozy To-Do App 🌿")
        self.root.configure(bg="#fef6e4")

        self.all_goals = load_goals()
        self.today = get_date_string()

        self.frame = tk.Frame(root, bg="#fef6e4")
        self.frame.pack(padx=20, pady=20)

        today_prompt = random.choice(PROMPTS)
        prompt_text = f"{today_prompt}  ({self.today})"
        self.title_label = tk.Label(self.frame, text=prompt_text, font=("Helvetica", 18, "bold"), bg="#fef6e4")
        self.title_label.pack()

        self.title_label = tk.Label(self.frame, text=f"Today's Goals ({self.today})", font=("Helvetica", 16, "bold"), bg="#fef6e4")
        self.title_label.pack()

        self.entry = tk.Entry(self.frame, width=40)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.add_goal_event)

        self.add_button = tk.Button(self.frame, text="Add Goal", command=self.add_goal, bg="#f3d2c1")
        self.add_button.pack(pady=5)

        self.listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, width=50, bg="#fef6e4", highlightthickness=0, bd=0)
        self.listbox.pack(pady=5)

        self.complete_button = tk.Button(self.frame, text="Mark Selected Complete", command=self.mark_complete, bg="#f3d2c1")
        self.complete_button.pack(pady=5)

        self.load_today_goals()
        self.suggest_yesterday_goals()

    def load_today_goals(self):
        self.listbox.delete(0, tk.END)
        for goal in self.all_goals:
            if goal["date"] == self.today and not goal["completed"]:
                self.listbox.insert(tk.END, goal["text"])
                
    def add_goal_event(self, event):
        self.add_goal()

    def add_goal(self):
        text = self.entry.get().strip()
        if text:
            self.all_goals.append({"date": self.today, "text": text, "completed": False})
            save_goals(self.all_goals)
            self.load_today_goals()
            self.entry.delete(0, tk.END)

    def mark_complete(self):
        selected = self.listbox.curselection()
        selected_texts = [self.listbox.get(i) for i in selected]
        for goal in self.all_goals:
            if goal["date"] == self.today and goal["text"] in selected_texts:
                goal["completed"] = True
        save_goals(self.all_goals)
        self.load_today_goals()

    def suggest_yesterday_goals(self):
        yesterday = get_date_string(-1)
        incomplete = [g["text"] for g in self.all_goals if g["date"] == yesterday and not g["completed"]]
        if incomplete:
            msg = "You didn't complete these yesterday:\n\n"
            msg += "\n".join(f"- {text}" for text in incomplete)
            msg += "\n\nAdd them to today?"
            if messagebox.askyesno("Suggestions 🌱", msg):
                for text in incomplete:
                    self.all_goals.append({"date": self.today, "text": text, "completed": False})
                save_goals(self.all_goals)
                self.load_today_goals()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
