import tkinter as tk
from tkinter import messagebox, Scrollbar, Listbox
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
        self.root.geometry("450x500")
        self.root.minsize(360, 420)
        self.dark_mode = False
        

        self.goal_manager = GoalManager()
        self.today = self.goal_manager.today
        # self.index_to_text = {}

        self.create_main_ui()
    
    def toggle_theme(self): 
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            # Dark Mode
            bg = "#1e1e1e",
            fg = "#f5f5f5",
            entry_bg  = "#2c2c2c",
            list_bg = "#2a2a2a",
            button_bg = "#3e4e50"
            select_bg = "#526760"
        else:
            # Light Mode
            bg = "#fef6e4"
            fg = "#333"
            entry_bg = "#ffffff"
            list_bg = "#ffffff"
            button_bg = "#f3d2c1"
            select_bg = "#d3e4cd"
        
        self.root.configure(bg=bg)
        self.frame.configure(bg=bg)
        self.title_label.configure(bg=bg, fg=fg)
        self.entry.configure(bg=entry_bg, fg=fg, insertbackground=fg)

        self.listbox.configure(bg=list_bg, fg=fg, selectbackground=select_bg, highlightcolor=select_bg)

        for btn in [self.add_button, self.complete_button, 
                    self.import_last_week_button, self.last_week_button, self.toggle_button]:
            btn.configure(bg=button_bg, fg=fg, activebackground=button_bg, activeforeground=fg)
    
    def create_button(self, parent, text, command, bg="#f3d2c1"):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Helvetica", 12),
            bg=bg,
            fg="#333",
            activebackground="#f3d2c1",
            activeforeground="#000",
            relief="flat",
            bd=2,
            padx=10,
            pady=4
        )

    def create_main_ui(self):
        # Frame for todays tasks  
        self.frame = tk.Frame(root, bg="#fef6e4")
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        today_prompt = random.choice(PROMPTS)
        prompt_text = f"{today_prompt}\n({self.today})"

        self.title_label = tk.Label(
            self.frame, 
            text=prompt_text, 
            font=("Helvetica", 18, "bold"), 
            justify="center"
            )
        self.title_label.pack(pady=(10, 5))

        self.title_label = tk.Label(
            self.frame, 
            text=f"Today's Goals ({self.today})", 
            font=("Helvetica", 16, "bold"), 
            bg="#fef6e4"
        )
        self.title_label.pack(pady=(10, 5))

        self.entry = tk.Entry(
            self.frame, 
            width=32,
            font=("Helvetica", 13),
            bg="#ffffff",
            fg="#333",
            insertbackground="#000",
            bd=2,
            relief="flat")

        self.entry.pack(pady=(6))
        self.entry.bind("<Return>", self.add_goal_event)

        self.add_button = self.create_button(self.frame, "Add Goal", self.add_goal)
        self.add_button.pack(pady=(4, 10))

        self.listbox = tk.Listbox(
            self.frame, 
            selectmode=tk.MULTIPLE,
            width=50, 
            bg="#ffffff",
            fg="#333",
            selectbackground="#d3e4cd",
            selectforeground="#000",
            relief="flat",
            highlightcolor="#d3e4cd",
            highlightthickness=0, 
            bd=2
            )
        self.listbox.pack(pady=(5))

        self.complete_button = self.create_button(self.frame,
        "Mark Selected Complete", 
        self.mark_complete
        )
        self.complete_button.pack(pady=(8, 4))

        self.import_last_week_button = self.create_button(
            self.frame, 
            "Import Last Week's Goals", 
            self.import_last_week_goals, 
            bg="#f3d2c1"
        )
        self.import_last_week_button.pack(pady=(4))

        self.last_week_button = self.create_button(
            self.frame, 
            "View Last Weeks Goals", 
            self.show_last_week_overlay, 
            bg="#d3e4cd"
        )
        self.last_week_button.pack(pady=(4, 10))

        self.toggle_button = self.create_button(
            self.frame, 
            "Toggle Rainy Mode", 
            self.toggle_theme, 
            bg="#cddafd"
        )

        self.toggle_button.pack(pady=(4, 10))

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.load_today_goals()
        self.suggest_yesterday_goals()

    def load_today_goals(self):
        self.listbox.delete(0, tk.END)
        self.index_to_text = {}

        for idx,goal in enumerate(self.goal_manager.get_today_goals()):
            text = goal["text"]
            if "imported_from" in goal:
                display = f"🌧️ {text}" #Highlight imported goals
            else:
                display = text
            self.listbox.insert(tk.END, display)
            self.index_to_text[idx] = text #Store original text for mapping

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
        selected_texts = [self.index_to_text[i] for i in selected if i in self.index_to_text]
        self.goal_manager.mark_goals_complete(selected_texts)
        self.load_today_goals()

    def suggest_yesterday_goals(self):
        incomplete = self.goal_manager.get_incomplete_yesterday_goals()
        if incomplete:
            msg="You didn't complete these yesterday:\n\n"
            msg += "\n".join(f"- {g}" for g in incomplete) 
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
    
    def import_last_week_goals(self):
        imported =self.goal_manager.import_last_week_goals()
        if imported:
            messagebox.showinfo("Goals Imported", f"{len(imported)} goals added from last week🌧️")
        else:
            messagebox.showinfo("All done", "No imcomplete goals from last week to import! ✨")
        self.load_today_goals()
    
    def show_last_week_overlay(self):
        overlay =tk.Toplevel(self.root)
        overlay.title("Last Week's Goals")
        overlay.geometry("350x300+100+100")
        overlay.configure(bg="#ffffff")
        overlay.transient(self.root)
        overlay.grab_set()

        tk.Label(overlay, text="Last Week's Goals", font=("Helvetica", 16, "bold"), bg="#ffffff").pack(pady=10)

        frame = tk.Frame(overlay, bg="#ffffff")
        frame.pack(padx=10, pady=10, fill="both", expand=True) 

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.past_listbox = Listbox(
            frame, 
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 12),
            selectbackground="#d3e4cd",
            selectforeground="#000",
            bg="#ffffff",
            fg="#333",
            relief="flat",
            bd=2
        )
        self.past_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=self.past_listbox.yview)

        past_goals = self.goal_manager.get_incomplete_last_week_goals()
        self.past_goal_map = {}

        for i, goal in enumerate(past_goals):
            display = f"{goal['text']}  from {goal['date']}"
            self.past_listbox.insert(tk.END, display)
            self.past_goal_map[i] = goal

        import_button = tk.Button(overlay, text="Import Selcted", command=lambda: self.import_selected_goals(overlay), bg="#f3d2c1")
        import_button.pack()

    def import_selected_goals(self, overlay):
        selected = self.past_listbox.curselection()
        imported_texts = [self.past_goal_map[i]["text"] for i in selected]

        if imported_texts:
            for g in self.goal_manager.get_incomplete_last_week_goals():
                if g["text"] in imported_texts:
                    self.goal_manager.add_goal(g["text"], imported_from=g["date"])
            self.load_today_goals()

        overlay.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
