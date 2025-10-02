import tkinter as tk
from tkinter import messagebox, Scrollbar, Listbox
from goal_manager import GoalManager
import random
import sys
import subprocess

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

class CozyTheme: 
    def __init__(self):
        self.light = {
        'bg_primary': '#FFF8F0',
        'bg_secondary': '#F5F1EB',
        'surface': '#FFFFFF',
        'accent': '#D4A574',
        'text_primary': '#2F1B14',
        'text_secondary': '#5D4E37',
        'success': '#7B9A5A',
        'border': '#E6D7C3',
        'hover': '#E8D5B7',
        'button_primary': '#D4A574',
        'button_secondary': '#C8B99C',
        'select_bg': '#D3E4CD'
        }

        self.dark = {
        'bg_primary': '#1A1611',
        'bg_secondary': '#2A241F',
        'surface': '#332B26',
        'accent': '#E6C08A',
        'text_primary': '#F5F1EB',
        'text_secondary': '#D2B48C',
        'success': '#8FAA6F',
        'border': '#4A3F35',
        'hover': '#3D342A',
        'button_primary': '#B8956F',
        'button_secondary': '#9A8269',
        'select_bg': '#4A5D47'
        }

FONTS = {
    'title': ('SF Pro Display', 20, 'bold') if sys.platform == 'darwin' else ('Helvetica', 20, 'bold'),
    'subtitle': ('SF Pro Display', 16) if sys.platform == 'darwin' else ('Helvetica', 16),
    'body': ('SF Pro Text', 14) if sys.platform == 'darwin' else ('Helvetica', 14),
    'button': ('SF Pro Text', 12, 'bold') if sys.platform == 'darwin' else ('Helvetica', 12, 'bold'),
    'small': ('SF Pro Text', 11) if sys.platform == 'darwin' else ('Helvetica', 11),
}

SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
}
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cozy To-Do App 🌿")
        self.root.configure(bg="#fef6e4")
        self.root.geometry("550x650")
        self.root.minsize(400, 500)
        
        self.theme = CozyTheme()
        self.dark_mode = self.detect_sytem_dark_mode()
        

        self.goal_manager = GoalManager()
        self.today = self.goal_manager.today
        self.index_to_text = {}

        self.create_main_ui()
        # self.apply_current_theme()

        if sys.platform == 'darwin':
            self.root.after(1000, self.check_system_theme)
    
    def detect_sytem_dark_mode(self):
        try:
            if sys.platform == 'darwin':
                result = subprocess.run(
                    ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                    capture_output=True, text=True
                )
                return 'Dark' in result.stdout
        except Exception: 
            pass
        return False
    
    def check_system_theme(self):
        system_dark = self.detect_sytem_dark_mode()
        if system_dark != self.dark_mode:
            self.dark_mode = system_dark
            self.apply_current_theme()
        
        self.root.after(2000, self.check_system_theme)
    
    def get_current_colours(self):
        return self.theme.dark if self.dark_mode else self.theme.light
    
    def apply_current_theme(self):
        colours = self.get_current_colours()

        self.root.configure(bg=colours['bg_primary'])

        self.frame.configure(bg=colours['bg_secondary'])

        self.prompt_label.configure(bg=colours['bg_secondary'], fg=colours['text_primary'])
        self.title_label.configure(bg=colours['bg_primary'], fg=colours['text_primary'])

        self.entry.configure(
            bg=colours['surface'], 
            fg=colours['text_primary'], 
            insertbackground=colours['text_primary'],
            highlightbackground=colours['border'],
            highlightcolor=colours['accent'],
            )
        
        self.listbox.configure(
            bg=colours['surface'],
            fg=colours['text_primary'],
            selectbackground=colours['select_bg'],
            selectforeground=colours['text_primary'],
            highlightbackground=colours['border'],
            highlightcolor=colours['accent'],
        )

        button_configs =[
            (self.add_button, colours['button_primary']),
            (self.complete_button, colours['button_primary']),
            (self.import_last_week_button, colours['button_secondary']),
            (self.last_week_button, colours['button_secondary']),
            (self.toggle_button, colours['accent']),
        ]

        for button, bg_color in button_configs:
            button.configure(
                bg= bg_color, 
                fg = colours['text_primary'],
                activebackground=['hover'],
                activeforeground=colours['text_primary'],
                highlightbackground=colours['border'],
            )
    

    
    def toggle_theme(self): 
        self.dark_mode = not self.dark_mode
        self.apply_current_theme()

        # Update button text
        mode_text = "Light Mode" if self.dark_mode else "Dark Mode"
        self.toggle_button.configure(text=f"Switch to {mode_text}")
    
    def create_rounded_button(self, parent, text, command, bg_color, widft=140, height=35):
        button = tk.Button (
            parent,
            text=text,
            command=command,
            font=FONTS['button'],
            bg=bg_color,
            fg=self.get_current_colours()['text_primary'],
            activebackground=self.get_current_colours()['hover'],
            activeforeground=self.get_current_colours()['text_primary'],
            relief="flat",
            bd=0,
            padx=SPACING['md'],
            pady=SPACING['sm'],
            cursor="hand2"
        )
        return button

    def create_main_ui(self):
        self.frame = tk.Frame(self.root, bg="#fef6e4")
        self.frame.pack(padx=SPACING['lg'], pady=SPACING['lg'], fill="both", expand=True)
        
        today_prompt = random.choice(PROMPTS)
        self.prompt_label = tk.Label(
            self.frame,
            text = today_prompt,
            font= FONTS['title'],
            justify="center",
            wraplength=500, 
            bg="#fef6e4",
        )

        self.prompt_label.pack(pady=(SPACING['md'], SPACING['sm']))

        self.entry = tk.Entry(
            self.frame,
            width=40,
            font=FONTS['body'],
            bg="#ffffff",
            fg="#333",
            insertbackground="#333",
            bd=2,
            relief="flat",
            highlightthickness=2,
            highlightcolor="#D4A574",
        )
        self.entry.pack(pady=(SPACING['sm'], SPACING['xs']))
        self.entry.bind("<Return>", self.add_goal_event)

        colours = self.get_current_colours()
        self.add_button = self.create_rounded_button(
            self.frame, "Add Goal", self.add_goal, colours['button_primary']
        )
        self.add_button.pack(pady=(SPACING['xs'], SPACING['md']))

        listbox_frame = tk.Frame(self.frame, bg=colours['bg_primary'])
        listbox_frame.pack(pady=SPACING['sm'], fill="both", expand=True)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            width= 50,
            height=12, 
            font=FONTS['body'],
            bg="#ffffff",
            fg="#333",
            selectbackground="#d3e4cd",
            selectforeground="#333",
            relief="flat",
            highlightthickness=2,
            highlightcolor="#D4A574",
            bd=0,
        )

        self.listbox.pack(side=tk.LEFT, fill="both", expand=True, padx=(0,2)) 
        scrollbar.config(command=self.listbox.yview)

        button_frame = tk.Frame(self.frame, bg=colours['bg_primary'])
        button_frame.pack(pady=SPACING['md'], fill='x')

        self.complete_button = self.create_rounded_button(
            button_frame, "Mark Complete", self.mark_complete, colours['success']
        )
        self.complete_button.pack(pady=SPACING['xs'])

        self.import_last_week_button = self.create_rounded_button(
            button_frame, "Import Last Weeks Goals", self.import_last_week_goals, colours['button_secondary']
        )
        self.import_last_week_button.pack(pady=SPACING['xs'])

        self.last_week_button = self.create_rounded_button(
            button_frame, "View Last Weeks Goals", self.show_last_week_overlay, colours['button_secondary']
        )
        self.last_week_button.pack(pady=SPACING['xs'])

        mode_text = "Light mode" if self.dark_mode else "Dark Mode"
        self.toggle_button = self.create_rounded_button(
            button_frame, f"Switch to {mode_text}", self.toggle_theme, colours['accent']
        )
        self.toggle_button.pack(pady=(SPACING['md'], SPACING['xs']))

        self.frame.columnconfigure(0, weight=1)

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
            try:
                self.goal_manager.add_goal(text)
                self.load_today_goals()
                self.entry.delete(0, tk.END)

                original_bg = self.add_button.cget("bg")
                self.add_button.configure(bg=self.get_current_colours()['success'])
                self.root.after(150, lambda: self.add_button.configure(bg=original_bg))

            except Exception as e: 
                messagebox.showerror("Error", f"Failed to add goal: {str(e)}")


           
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
        overlay.geometry("400x400+100+100")
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
            width=40,
            font=("Helvetica", 12),
            selectbackground="#d3e4cd",
            selectforeground="#000",
            bg="#ffffff",
            fg="#333",
            relief="flat",
            bd=2
        )
        self.past_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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
