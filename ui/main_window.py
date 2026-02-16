import tkinter as tk
from tkinter import messagebox
import random
import sys
from datetime import datetime

from config.theme import CozyTheme
from config.fonts import FONTS
from config.constants import SPACING, PROMPTS

from ui.widgets import RoundedButtton, EmptyStateLabel
from ui.dialogs import LastWeeksGoalsDialog
from managers.goal_manager import GoalManager
from utils.system import detect_sytem_dark_mode, setup_dpi_awareness


class ToDoApp:
    def __init__(self, root):
        self.root = root
        setup_dpi_awareness()

        self.root.title("Cozy To-Do App 🌿")
        self.theme = CozyTheme()
        self.dark_mode = detect_sytem_dark_mode()

        self.goal_manager = GoalManager()
        self.today = self.goal_manager.today
        self.index_to_text = {}

        # top-level container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)

        self.create_main_ui()
        self.apply_current_theme()

        if sys.platform == 'darwin':
            self.root.after(1000, self.check_system_theme)

    def get_current_colours(self):
        return self.theme.dark if self.dark_mode else self.theme.light

    def apply_current_theme(self):
        colours = self.get_current_colours()
        self.root.configure(bg=colours['bg_primary'])
        self.main_container.configure(bg=colours['bg_primary'])

        # update header widgets if they exist
        if hasattr(self, 'header_frame'):
            self.header_frame.configure(bg=colours['bg_primary'])
        if hasattr(self, 'date_label'):
            self.date_label.configure(bg=colours['bg_primary'], fg=colours['text_muted'])
        if hasattr(self, 'prompt_label'):
            self.prompt_label.configure(bg=colours['bg_primary'], fg=colours['text_primary'])
        if hasattr(self, 'toggle_button'):
            self.toggle_button.configure(bg=colours['surface'], fg=colours['accent'], activebackground=colours['hover'], activeforeground=colours['accent'])

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        emoji = "☀️" if self.dark_mode else "🌙"
        if hasattr(self, 'toggle_button'):
            self.toggle_button.configure(text=emoji)
        self.apply_current_theme()

    def check_system_theme(self):
        try:
            new_dark = detect_sytem_dark_mode()
            if new_dark != self.dark_mode:
                self.dark_mode = new_dark
                self.apply_current_theme()
        finally:
            # poll again
            self.root.after(2000, self.check_system_theme)

    def create_main_ui(self):
        self._create_header()
        self._create_content_card()
        self._create_input_section()
        self._create_list_section()
        self._create_button_section()

        # placeholders for real loading logic
        if hasattr(self.goal_manager, 'load_today_goals'):
            try:
                self.goal_manager.load_today_goals()
            except Exception:
                pass

    def _create_header(self):
        colours = self.get_current_colours()

        self.header_frame = tk.Frame(self.main_container, bg=colours['bg_primary'])
        self.header_frame.pack(fill="x", pady=(0, SPACING['lg']))

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
            text=today_prompt,
            font=FONTS['title'],
            justify="center",
            wraplength=500,
            bg=colours['bg_primary'],
            fg=colours['text_primary'],
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

    def _create_content_card(self):
        # placeholder for content area
        colours = self.get_current_colours()
        self.content_card = tk.Frame(self.main_container, bg=colours['card'], bd=0)
        self.content_card.pack(fill="both", expand=False, padx=SPACING['md'], pady=(0, SPACING['md']))

    def _create_input_section(self):
        # placeholder input
        colours = self.get_current_colours()
        frame = tk.Frame(self.content_card, bg=colours['card'])
        frame.pack(fill="x", pady=SPACING['sm'])

        self.input_var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=self.input_var, font=FONTS['body'], bd=1)
        entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, SPACING['sm']))

        add_btn = tk.Button(frame, text="Add", command=self.add_goal, bg=colours['button_primary'])
        add_btn.pack(side=tk.RIGHT)

    def _create_list_section(self):
        colours = self.get_current_colours()
        self.list_frame = tk.Frame(self.content_card, bg=colours['card'])
        self.list_frame.pack(fill="both", expand=True)

        # listbox with scrollbar
        scrollbar = tk.Scrollbar(self.list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.goals_listbox = tk.Listbox(
            self.list_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.MULTIPLE,
            font=FONTS['body'],
            bg=colours['card'],
            fg=colours['text_primary'],
            bd=0,
            highlightthickness=0
        )
        self.goals_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.goals_listbox.yview)

        self.empty_label = EmptyStateLabel(self.list_frame, colours)
        self.empty_label.pack(pady=SPACING['sm'])

    def _create_button_section(self):
        colours = self.get_current_colours()
        btn_frame = tk.Frame(self.main_container, bg=colours['bg_primary'])
        btn_frame.pack(fill="x", pady=SPACING['sm'])

        import_btn = tk.Button(btn_frame, text="Import Last Week", command=self.show_last_week_overlay, bg=colours['button_secondary'])
        import_btn.pack(side=tk.LEFT, padx=SPACING['sm'])

        mark_btn = tk.Button(btn_frame, text="Mark Complete", command=self.mark_complete, bg=colours['button_primary'])
        mark_btn.pack(side=tk.RIGHT, padx=SPACING['sm'])

        refresh_btn = tk.Button(btn_frame, text="Refresh", command=self.load_today_goals, bg=colours['button_secondary'])
        refresh_btn.pack(side=tk.RIGHT, padx=SPACING['sm'])

    # Event handlers (placeholders)
    def add_goal(self):
        text = self.input_var.get().strip() if hasattr(self, 'input_var') else ''
        if not text:
            messagebox.showinfo("Empty", "Please enter a goal text.")
            return
        try:
            self.goal_manager.add_goal(text)
        except Exception:
            pass
        self.input_var.set("")
        self.load_today_goals()

    def mark_complete(self):
        if not hasattr(self, 'goals_listbox'):
            return
        sel = self.goals_listbox.curselection()
        texts = [self.index_to_text.get(i) for i in sel]
        texts = [t for t in texts if t]
        if not texts:
            messagebox.showinfo("Select", "Please select goals to mark complete.")
            return
        try:
            self.goal_manager.mark_goals_complete(texts)
        except Exception:
            pass
        self.load_today_goals()

    def import_last_week_goals(self):
        try:
            imported = self.goal_manager.import_last_week_goals()
            count = len(imported)
            if count:
                messagebox.showinfo("Imported", f"Imported {count} goals from last week.")
        except Exception:
            messagebox.showerror("Error", "Failed to import goals.")
        self.load_today_goals()

    def show_last_week_overlay(self):
        dialog = LastWeeksGoalsDialog(
            self.root,
            self.get_current_colours(),
            self.goal_manager,
            self.load_today_goals
        )

    def load_today_goals(self):
        colours = self.get_current_colours()
        if not hasattr(self, 'goals_listbox'):
            return

        self.goals_listbox.delete(0, tk.END)
        self.index_to_text.clear()

        goals = self.goal_manager.get_today_goals()
        if not goals:
            self.empty_label.lift()
            return
        else:
            self.empty_label.lower()

        for i, g in enumerate(goals):
            display = g.get('text')
            self.goals_listbox.insert(tk.END, display)
            self.index_to_text[i] = g.get('text')
