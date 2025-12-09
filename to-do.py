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
        'card': '#FEFEFE',
        'accent': '#D4A574',
        'accent_hover': '#B89558',
        'text_primary': '#2F1B14',
        'text_secondary': '#5D4E37',
        'text_muted': '#9B8D82',
        'success': '#7B9A5A',
        'success_hover': '#5A7A50',
        'border': '#E6D7C3',
        'border_light': '#F0E8DD',
        'hover': '#E8D5B7',
        'button_primary': '#D4A574',
        'button_secondary': '#C8B99C',
        'select_bg': '#D3E4CD',
        'shadow': '#00000008'
        }

        self.dark = {
        'bg_primary': '#1A1611',
        'bg_secondary': '#2A241F',
        'surface': '#332B26',
        'card': '#3D342A',
        'accent': '#E6C08A',
        'accent_hover': '#CBA66F',
        'text_primary': '#F5F1EB',
        'text_secondary': '#D2B48C',
        'success': '#8FAA6F',
        'success_hover': '#6F8F57',
        'border': '#4A3F35',
        'border_light': '#5D4E37',
        'hover': '#3D342A',
        'button_primary': '#B8956F',
        'button_secondary': '#9A8269',
        'select_bg': '#4A5D47',
        'shadow': '#00000020'
        }

FONTS = {
    'title': ('SF Pro Display', 20, 'bold') if sys.platform == 'darwin' else ('Helvetica', 20, 'bold'),
    'subtitle': ('SF Pro Display', 16) if sys.platform == 'darwin' else ('Helvetica', 16),
    'body': ('SF Pro Text', 14) if sys.platform == 'darwin' else ('Helvetica', 14),
    'button': ('SF Pro Text', 12, 'bold') if sys.platform == 'darwin' else ('Helvetica', 12, 'bold'),
    'small': ('SF Pro Text', 11) if sys.platform == 'darwin' else ('Helvetica', 11),
}

SPACING = {
    'xs': 6,
    'sm': 10,
    'md': 16,
    'lg': 24,
    'xl': 32,
}

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color, fg_color, hover_color, **kwargs):
        width = kwargs.pop('width', 220)
        height = kwargs.pop('height', 44)
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, **kwargs)

        self.command = command
        self.bg_color = bg_color 
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.text = text
        self.is_hovered = False

        self.draw_button()

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def draw_button(self):
        self.delete("all")
        color = self.hover_color if self.is_hovered else self.bg_color

        x0, y0, x1, y1 = 2, 2, self.winfo_reqwidth() -2, self.winfo_reqheight() -2
        radius = 10

        self.create_arc(x0, y0, x0 + radius*2, y0 + radius*2, start=90, extent=90, fill=color, outline='')
        self.create_arc(x1 - radius*2, y0, x1, y0 + radius*2, start=0, extent=90, fill=color, outline='')
        self.create_arc(x0, y1 - radius*2, x0 + radius*2, y1, start=180, extent=90, fill=color, outline='')
        self.create_arc(x1 - radius*2, y1 - radius*2, x1, y1, start=270, extent=90, fill=color, outline='')

        self.create_rectangle(x0 + radius, y0, x1 - radius, y1, fill=color, outline='')
        self.create_rectangle(x0, y0 + radius, x1, y1 - radius, fill=color, outline='')

        self.create_text((self.winfo_reqwidth()//2, self.winfo_reqheight()//2), text=self.text, fill=self.fg_color, font=FONTS['button'])

    def on_click(self, event):
        if self.command:
            self.command()
    
    def on_enter(self, event):
        self.is_hovered = True
        self.draw_button()
        self.configure(cursor="hand2")
    
    def on_leave(self, event):
        self.is_hovered = False
        self.draw_button()
        self.configure(cursor="")

    def update_colors(self, bg_color, fg_color, hover_color):
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.draw_button()

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cozy To-Do App 🌿")
        self.root.configure(bg="#fef6e4")
        self.root.geometry("580x720")
        self.root.minsize(480, 600)
        
        self.theme = CozyTheme()
        self.dark_mode = self.detect_sytem_dark_mode()
        

        self.goal_manager = GoalManager()
        self.today = self.goal_manager.today
        self.index_to_text = {}

        self.create_main_ui()
        self.apply_current_theme()

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

        if hasattr(self, 'main_container'):
            self.main_container.configure(bg=colours['bg_primary'])
        if hasattr(self, 'header_frame'):
            self.header_frame.configure(bg=colours['bg_primary'])
        if hasattr(self, 'content_frame'):
            self.content_frame.configure(bg=colours['bg_secondary'])

        if hasattr(self, 'prompt_label'):
            self.prompt_label.configure(bg=colours['bg_primary'], fg=colours['text_primary'])
        if hasattr(self, 'date_label'):
            self.date_label.configure(bg=colours['bg_primary'], fg=colours['text_secondary'])


        
        if hasattr(self, 'entry'):
            self.entry.configure(
                bg=colours['surface'], 
                fg=colours['text_primary'], 
                insertbackground=colours['text_primary'],
                highlightbackground=colours['border'],
                highlightcolor=colours['accent'],
            )
        if hasattr(self, 'listbox'):
            self.listbox.configure(
                bg=colours['surface'],
                fg=colours['text_primary'],
                selectbackground=colours['select_bg'],
                selectforeground=colours['text_primary'],
                highlightbackground=colours['border'],
                highlightcolor=colours['accent'],
        )

        #Button Updatesssssss
        if hasattr(self, 'add_button'):
            self.add_button.update_colors(colours['accent'], '#FFFFFF', colours['accent_hover'])
        if hasattr(self, 'complete_button'):
            self.complete_button.update_colors(colours['success'], '#FFFFFF', colours['success_hover'])
        if hasattr(self, 'import_last_week_button'):
            self.import_last_week_button.update_colors(colours['button_secondary'], colours['text_primary'], colours['hover'])
        if hasattr(self, 'last_week_button'):
            self.last_week_button.update_colors(colours['button_secondary'], colours['text_primary'], colours['hover'])
        if hasattr(self, 'toggle_button'):
            mode_emoji = "☀️" if self.dark_mode else "🌙"
            self.toggle_button.configure(
                text=mode_emoji,
                bg=colours['surface'],
                fg=colours['accent'],
                activebackground=colours['hover'],
                activeforeground=colours['accent'],
        )

    
    def toggle_theme(self): 
        self.dark_mode = not self.dark_mode
        self.apply_current_theme()


    def create_main_ui(self):
        colours = self.get_current_colours()

        self.main_container = tk.Frame(self.root, bg=colours['bg_primary'])
        self.main_container.pack(fill= "both", expand=True, padx=20, pady=20)

        self.header_frame = tk.Frame(self.main_container, bg=colours['bg_primary'])
        self.header_frame.pack(fill="x", pady=(0, SPACING['lg']))

        from datetime import datetime
        today_str = datetime.now().strftime("%A, %B %d")
        self.date_label = tk.Label(
            self.header_frame,
            text=today_str.upper(),
            font=FONTS['small'],
            fg=colours['text_muted'],
            bg=colours['bg_primary'],
        )
        self.date_label.pack(pady=(0, SPACING['xs']))


        
        today_prompt = random.choice(PROMPTS)
        self.prompt_label = tk.Label(
            self.header_frame,
            text = today_prompt,
            font= FONTS['title'],
            justify="center",
            wraplength=500, 
            bg="#fef6e4",
        )

        self.prompt_label.pack(pady=(SPACING['md'], SPACING['sm']))

        mode_emoji = "☀️" if self.dark_mode else "🌙"
        self.toggle_button = tk.Button(
            self.header_frame, 
            text=mode_emoji,
            command=self.toggle_theme,
            font=('Arial', 16),
            bg=colours['surface'],
            fg=colours['accent'],
            activebackground=colours['hover'],
            activeforeground=colours['accent'],
            relief="flat",
            bd=0,
            width=3,
            height=1,
            cursor="hand2"
        )
        self.toggle_button.place(relx=1.0, rely=0.0, anchor="ne")

        self.content_card = tk.Frame(
            self.main_container,
            bg=colours['card'],
            relief="flat",
            bd=0
        )
        self.content_card.pack(fill="both", expand=True)

        self.input_section = tk.Frame(self.content_card, bg=colours['card'])
        self.input_section.pack(pady=SPACING['lg'], padx=SPACING['md'], fill="x")

        self.entry = tk.Entry(
            self.input_section,
            width=40,
            font=FONTS['body'],
            bg=colours['surface'],
            fg=colours['text_primary'],
            insertbackground=colours['accent'],
            bd=0,
            relief="flat",
            highlightthickness=2,
            highlightcolor=colours['accent'],
            highlightbackground=colours['border'],
        )

        self.entry.pack(fill="x", pady=12)
        self.entry.bind("<Return>", self.add_goal_event)

        add_btn_container = tk.Frame(self.input_section, bg=colours['card'])
        add_btn_container.pack(pady=(SPACING['sm'], 0))

        self.add_button = RoundedButton(
            add_btn_container,
            "Add Goal",
            self.add_goal,
            colours['accent'],
            '#FFFFFF',
            colours['accent_hover'],
            width=200,
            height=42
        )
        self.add_button.pack()

        seperator = tk.Frame(self.content_card, bg=colours['border'], height=1)
        seperator.pack(fill="x", pady=SPACING['md'])

        self.list_section = tk.Frame(self.content_card, bg=colours['card'])
        self.list_section.pack(fill="x", padx=SPACING['lg'], pady=SPACING['md'])

        self.empty_label = tk.Label(
            self.list_section,
            text="No goals yet, add one :)",
            font= FONTS['body'],
            fg=colours['text_muted'],
            bg=colours['card'],
        )

        scrollbar = tk.Scrollbar(self.list_section)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            self.list_section,
            yscrollcommand=scrollbar.set,
            font=FONTS['body'],
            bg=colours['surface'],
            fg=colours['text_primary'],
            selectbackground=colours['select_bg'],
            selectforeground=colours['text_primary'],
            relief="flat",
            highlightthickness=2,
            highlightcolor=colours['accent'],
            highlightbackground=colours['border'],
            bd=0,
            selectmode=tk.MULTIPLE,
        )

        self.listbox.pack(side=tk.LEFT, fill="both", expand=True) 
        scrollbar.config(command=self.listbox.yview)

        self.button_section = tk.Frame(self.content_card, bg=colours['card'])
        self.button_section.pack(pady=SPACING['lg'], padx=SPACING['lg'], fill='x')

        complete_container = tk.Frame(self.button_section, bg=colours['card'])
        complete_container.pack(pady=(0, SPACING['sm']))

        self.complete_button = RoundedButton(
            complete_container,
            "Mark as Complete",
            self.mark_complete,
            colours['success'],
            '#FFFFFF',
            colours['success_hover'],
            width=240,
            height=42
        )
        self.complete_button.pack()

        seperator2 = tk.Frame(self.button_section, bg=colours['border'], height=1)
        seperator2.pack(fill="x", pady=SPACING['md'])

        import_container = tk.Frame(self.button_section, bg=colours['card'])
        import_container.pack(pady=(0, SPACING['xs']))

        self.import_last_week_button = RoundedButton(
            import_container,
            "Import Last Weeks Goals",
            self.import_last_week_goals,
            colours['button_secondary'],
            colours['text_primary'],
            colours['hover'],
            width=240,
            height=38
        )

        self.import_last_week_button.pack()

        view_container = tk.Frame(self.button_section, bg=colours['card'])
        view_container.pack()

        self.last_week_button = RoundedButton(
            view_container,
            "View Last Week's Goals",
            self.show_last_week_overlay,
            colours['button_secondary'],
            colours['text_primary'],
            colours['hover'],
            width=240,
            height=38
        )
        self.last_week_button.pack()

        self.load_today_goals()
        self.suggest_yesterday_goals()
    
    def update_empty_state(self):
        if self.listbox.size() == 0:
            self.empty_label.pack()
        else:
            self.empty_label.pack_forget()


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
