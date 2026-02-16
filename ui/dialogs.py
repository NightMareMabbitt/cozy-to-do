import tkinter as tk
from tkinter import Listbox, Scrollbar
from config.fonts import FONTS
from config.constants import SPACING
from ui.widgets import RoundedButtton

class LastWeeksGoalsDialog:

    def __init__(self, parent, colours, goal_manager, on_import_callback):
        self.parent = parent
        self.colours = colours
        self.goal_manager = goal_manager
        self.on_import_callback = on_import_callback

        self.create_dialog()
    
    def create_dialog(self):
        self.overlay= tk.Toplevel(self.parent)
        self.overlay.title("Last Week's Goals")
        self.overlay.geometry("400x300")
        self.overlay.configure(bg=self.colours['bg_primary'])
        self.overlay.transient(self.parent)
        self.overlay.grab_set()

        tk.Label(self.overlay, text="Last Week's Goals", font=FONTS['medium'], bg=self.colours['bg_primary'], fg=self.colours.get('text_primary', '#000')).pack(pady=SPACING)

        frame = tk.Frame(self.overlay, bg=self.colours['bg_primary'])
        frame.pack(padx=SPACING['sm'], pady=SPACING['sm'], fill=tk.BOTH, expand=True)

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

        import_button = tk.Button(self.overlay, text="Import Selected", command=self.import_selected, bg="#f3d2c1")
        import_button.pack(pady=SPACING['sm'])

    def import_selected(self):
        selected = self.past_listbox.curselection()
        imported_texts = [self.past_goal_map[i]["text"] for i in selected]

        if imported_texts:
            for g in self.goal_manager.get_incomplete_last_week_goals():
                if g["text"] in imported_texts:
                    self.goal_manager.add_goal(g["text"], imported_from=g["date"])

        # notify parent to refresh its list and close
        try:
            self.on_import_callback()
        except Exception:
            pass
        self.overlay.destroy()


        


