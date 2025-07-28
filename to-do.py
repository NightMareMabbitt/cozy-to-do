import tkinter as tk
from tkinter import messagebox
from goal_manager import GoalManager
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

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cozy To-Do App 🌿")
        self.root.configure(bg="#fef6e4")

        self.goal_manager = GoalManager()
        self.today = self.goal_manager.today

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

        self.last_week_button = tk.Button(self.frame, text="View Last Weeks Goals", command=self.show_last_week_goals, bg="#d3e4cd")
        self.last_week_button.pack(pady=5)

        self.load_today_goals()
        self.suggest_yesterday_goals()

    def load_today_goals(self):
        self.listbox.delete(0, tk.END)
        for goal in self.goal_manager.get_today_goals():
            self.listbox.insert(tk.END, goal["text"])

    def add_goal_event(self, event):
        self.add_goal()

    def add_goal(self):
        text = self.entry.get().strip()
        if text:
            self.goal_manager.add_goal(text)
            self.load_today_goals()
            self.entry.delete(0, tk.END)
           
    def mark_complete(self):
        selected = self.listbox.curselection()
        selected_texts = [self.listbox.get(i) for i in selected]
        self.goal_manager.mark_goals_complete(selected_texts)
        self.load_today_goals()

    def suggest_yesterday_goals(self):
        incomplete = self.goal_manager.get_incomplete_yesterday_goals()
        if incomplete:
            msg="You didn't complete these yesterday:\n\n"
            msg += "\n".join(f"- {g['text']}" for g in incomplete)
            msg += "\n\nAdd them to today?"
            if messagebox.askyesno("Suggestions ", msg):
                self.goal_manager.import_yesterday_goals()
                self.load_today_goals()
    
    def show_last_week_goals(self):
        last_week = self.goal_manager.get_last_week_goals()
        self.listbox.delete(0, tk.END)

        if not last_week:
            self.listbox.insert(tk.END, "No goals from the last 7 days. ✨")
            return

            last_week.sort(key=lambda g: g["date"])

        current_date = ""
        for goal in last_week:
            if goal["date"] != current_date:
                current_date = goal["date"]
                self.listbox.insert(tk.END, f"🌧️ {current_date}")
        status = "✓" if goal["completed"] else "•"
        self.listbox.insert(tk.END, f"  {status} {goal['text']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
