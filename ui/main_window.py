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
        self.root.title("Cozy To-Do App 🌿")
        self.root.geometry("600x750")
        self.root.minsize(500, 650)

        setup_dpi_awareness()

        self.theme = CozyTheme()
        self.dark_mode = detect_sytem_dark_mode()

        self.goal_manager = GoalManager()
        self.today = self.goal_manager.today
        self.index_to_text = {}

        self.create_main_ui()
        self.apply_current_theme()

        if sys.platform == 'darwin':
            self.root.after(1000, self.check_system_theme)

    def get_current_colours(self):
        return self.theme.dark if self.dark_mode else self.theme.light

    def apply_current_theme(self):
        colours = self.get_current_colours()
        self.root.configure(bg=colours['bg_primary'])
     

        # update header widgets if they exist
        if hasattr(self, 'main_container'):
            self.main_container.configure(bg=colours['bg_primary'])
        if hasattr(self, 'header_frame'):
            self.header_frame.configure(bg=colours['bg_primary'])
        if hasattr(self, 'content_card'):
            self.content_card.configure(bg=colours['card'])
        if hasattr(self, 'input_section'):
            self.input_section.configure(bg=colours['card'])
        if hasattr(self, 'list_section'):
            self.list_section.configure(bg=colours['card'])
        if hasattr(self, 'button_section'):
            self.button_section.configure(bg=colours['card'])

        if hasattr(self, 'prompt_label'):
            self.prompt_label.configure(bg=colours['bg_primary'], fg=colours['text_primary'])
        if hasattr(self, 'date_label'):
            self.date_label.configure(bg=colours['bg_primary'], fg=colours['text_muted'])

        if hasattr(self, 'entry'):
            self.entry.configure(
                bg=colours['surface'], 
                fg=colours['text_primary'], 
                insertbackground=colours['accent'],
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

        # Update custom buttons
        if hasattr(self, 'add_button'):
            self.add_button.update_colors(colours['accent'], '#FFFFFF', colours['accent_hover'], colours['card'])
        if hasattr(self, 'complete_button'):
            self.complete_button.update_colors(colours['success'], '#FFFFFF', colours['success_hover'], colours['card'])
        if hasattr(self, 'import_last_week_button'):
            self.import_last_week_button.update_colors(colours['button_secondary'], colours['text_primary'], colours['hover'], colours['card'])
        if hasattr(self, 'last_week_button'):
            self.last_week_button.update_colors(colours['button_secondary'], colours['text_primary'], colours['hover'], colours['card'])
        
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
       colours = self.get_current_colours()

       self.main_container = tk.Frame(self.root, bg=colours['bg_primary'])
       self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

       self.header_frame = tk.Frame(self.main_container, bg=colours['bg_primary'])
       self.header_frame.pack(fill="x", pady=(0, SPACING['lg']))

       today_str = datetime.now().strftime("%A, %B %d")
       self.date_label = tk.Label(
        self.header_frame,
        text=today_str.upper(),
        font=FONTS['label'],
        fg=colours['text_muted'],
        bg=colours['bg_primary']
       )

       self.date_label.pack(pady=(0, SPACING['xs']))

       today_prompt = random.choice(PROMPTS)
       self.prompt_label = tk.Label(
        self.header_frame, 
        text=today_prompt,
        font=FONTS['title']
        justify="center",
        wrapLemgth=540,
        bg=colours['bg_primary'],
        fg=colours['text_primary']
       )

       self.prompt_label.pack(pady=(0, SPACING['md']))

       mode_emoji = "☀️" if self.dark_mode else "🌙"
       self.toggle_button = tk.Button(
        self.header_frame,
        text=mode_emoji,
        command=self.toggle_theme,
        font=('Arial', 16)
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
        
        self.toggle_button.place(relx=1.0, rely=0, anchor= "ne")

        sefl.content_card = tk.Frame(
            self.main_container, 
            bg=colours['card'], 
            bd=0, 
            relief="flat"
        )
        self.content_card.pack(fill="both", expand=True)

        self.input_section = tk.Frame(self.content_card, bg=colours['card'])
        self.input_section.pack(pady=(SPACING['lg'], SPACING['md'], padx=SPACING['lg'], fill="x"))

        self.entry = tk.Entry(
            self.input_section,
            font=FONTS['body'],
            bg=colours['surface'],
            fg=colours['text_primary'],
            insertbackground=colours['accent'],
            bd=0,
            relief="flat",
            highlightthickness=2,
            highlightbackground=colours['border'],
            highlightcolor=colours['accent'],
        )
        self.entry.pack(fill="x", ipady=12)
        self.entry.bind("<Return>",self.add_goal_event)

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
            height=42,
            parent_bg=colours['card']
        )

        self.add_button.pack()

        seperator = tk.Frame(self.content_card, bg=colours['border-light'], height=1)
        seperator.pack(pady=(0, SPACING['md']), padx=SPACING['lg'], fill="both", expand=True)

        self.list_section = tk.Frame(self.content_card, bg=colours['card'])
        self.list_section.pack(pady=(0, SPACING['md']), padx=SPACING['lg'], fill="both", expand=True)

        self.empty_label = tk.Label(
            self.list_section, 
            text="No goals yet, add one above",
            font=FONTS['body'],
            fg=colours['text_muted'],
            bg=colours['card']
        )  

        scrollbar = t.Scrollbar(self.list_section)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lsistbox = tk.Listbox(
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
            selectmode=tk.MULTIPLE
        )
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True)
        srollbar.config(command=slef.listbox.yview)

        self.button_section = tk.Frame(self.content_card, bg=colours['card'])
        self.button_section.pack(pady=(0, SPACING['lg']),padx=SPACING['lg'], fill="x")

        complete_container = tk.Frame(self.button_sectiom, bg=colours['card'])
        complete_container.pack(pady=(0, SPACING['sm']))

        self.complete_button = RoundedButton(
            complete_container, 
            "Mark Complete", 
            self.mark_complete, 
            colours['success'],
            '#FFFFFF',
            colours['success_hover'],
            width=240,
            height=42,
            parent_bg=colours['card']
        )
        self.complete_button.pack()

        button_seperator = tk.Frame(self.button_section, bg=colours['border_light'], height=1)
        button_seperator.pack(fill="x", pady=SPACING['md'])

        import_container = tk.Frame(self.buton_section, bg=colours['card'])
        import_container.pack(pady=(SPACING['xs'], 0))

        self.import_last_week_button = RoundedButton(
            import_container,
            "Import last week's goals",
            self.import_last_week_goals,
            colours['button_secondary'],
            colours['text_primary'],
            colours['hover'],
            width=240,
            height=38,
            parent_bg=colours['card']
        )
        self.import_last_week_button.pack()


        view_container = tk.Frame(self.button_section, bg=colours['card'])
        view_container.pack()

        self.last_week_button = RoundedButton(
            view_container,
            "View last week's goals",
            self.show_last_week_overlay,
            colours['button_secondary'],
            colours['text_primary'],
            colours['hover'],
            width=240,
            height=38,
            parent_bg=colours['card']
        )
        self.last_week_button.pack()

        self.load_today_goals()
        self.suggest_yesterday_goals()


    def update_empty_state(self):
        if self.listboc.size() == 0:
            self.empty_label.pack(expand=True)
        else:
            self.empty_label.pack_forget()
    

    def load_todays_goals(self):
        self.listbox.delete(o, tk.END)
        self.index_to_text = {}

        for idx, goal on enumerate(self.goal_manager.get_todays_goals()):
            text = goal['text']
            if "imported_from" in goal:
                display = f"{text}"
            else:
                display f". {text}"
            self.listbox.insert(tk.END, display)
            self,index_to_text[idx] = text

        self.update_empty_state()
    
    def add_goal_event(self, event):
        self.add_goal()
    
    def add_goal(self):
        text = self.entry.get().strip()
        if text:
            try:
                self.goal_manager.add_goal(text)
                self.entry.delete(0, tk.END)
                self.load_today_goals()

                #Visual feedback
                original_colours = (self.add_button.bg_colour, self.add_button.fg_colour, self.add_button.hover_colour)
                success_colour = self.get_current_colours()['success']
                self.add_button.update_colours(success_colour, '#FFFFFF', success_colour)
                self.add_button.text = "Added!"
                self.add_button.draw_button()

                def reset():
                    self.add_button.text = "Add Goal"
                    self.add_button.update_colours(*original_colours)
                
                self.root.after(1000, reset)
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add goal: {str(e)}")

    def mark_complete(self):
        selected =  self.listbox.curselection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select at least one goal to mark as complete.")
            return

        selected_texts = [self.index_to_text[i] for i in selected if i in self.index_to_text]
        self.goal_manager.mark_goals_complete(selected_texts)
        self.load_today_goals()

        original_text = self.complete_button.text
        self.complete_button.text = "Completed!"
        self.complete_button.draw_button()

        def reset():
            self.complete_button.text = original_text
            self.complete_button.draw_button()
        
        self.root.after(1500, reset)

    def suggest_yesterdays_goals(self):
        try:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            incomplete_goals = [
                g for g in self.goal_manager.goals
                if g["date"] == yesterday and not g["completed"]
            ]

            if incomplete_goals:
                incomplete_goals = [g["text"] for g in incomplete_goals]
                msg = "You didn't complete these goals yesterday:\n\n"
                msg += "\n".join(f"- {text}" for text in incomplete_goals)
                msg += "\n\nConsider adding them again today?"

                if messagebox.askyesno("Yesterday's Goals", msg):
                    imported = self.goal_manager.get_incomplete_yesterday_goals()
                    self.load_today_goals()
                
        except Exception as e:
        pass

    def import_last_week_goals(self):
        imported = self.goal_manager.import_last_week_goals()
        if imported:
            messagebox.showinfo("Imported", f"Imported {len(imported)} goals from last week!")
        else:
            messagebox.showinfo("All caught up", "No incomplete goals from last week to import!")
        self.load_today_goals()
    
    def show_last_week_overlay(self):
        colours = self.get_current_colours()

        overlay = tk.Toplevel(self.root)
        overlay.title("Last Week's Goals")
        overlay.geometry("520x600")
        overlay.configure(bg=colours['bg_primary'])
        overlay.transient(self.root)
        overlay.grab_set()
        

        #Main Container
        main = tk.Frame(overlay, bg=colours['bg_primary'])
        main.pack(fill="both", expand=True, padx=20, pady=20)

        #Header
        header = tk.Frame(main, bg=colours['bg_primary'])
        header.pack(fill="x", pady=(0, SPACING['lg']))

        tk.Label(
            header, 
            text="Last Week's Goals",
            font=FONTS['title'],
            bg=colours['bg_primary'],
            fg=colours['text_primary']
        ).pack()

        #Content Card
        content= tk.Frame(main, bg=colours['card'])
        content.pack(fill="both", expand=True)

        #Listbox
        list_frame = tk.Frame(content, bg=colours['card'])
        list_frame.pack(pady=SPACING['lg'],padx=SAPCING['lg'], fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.past_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=FONTS['body'],
            selectbackground=colours['select_bg'],
            selectforeground=colours['text_primary'],
            bg=colours['surface'],
            fg=colours['text_primary'],
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightcolor=colours['accent'],
            highlightbackground=colours['border'],
            selectmode=tk.MULTIPLE
        )

        self.past_listbox,pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config=(command=self.past_listbox.yview)

        #Load goals
        past_goals = self.goal_manager.get_incomplete_last_week_goals()
        self.past_goal_map = {}

        for i, goal in enumerate(past_goals):
            display = f"• {goal['text']}  ({goal['date']})"
            self.past_listbox.insert(tk.END, display)
            self.past_goal_map[i] = goal
        
        #Buttons
        btn_frame = tk.Frame(content, bg=colours['card'])
        btn_frame.pack(padx=SPACING['lg'], pady=(0, SPACING['lg'], fill="x"))

        import_container = tk.Frame(btn_frame, bg=colours['card'])
        import_container.pack(pady=(0, SPACING['xs']))

        import_btn = RoundedButton(
            import_container,
            "Import Selected",
            lambda: self.import_selected_goals(overlay)
            colours['accent'],
            '#FFFFFF',
            colours['accent_hover'],
            width=240,
            height=42,
            parent_bg=colours['card']
        )
        import_btn.pack()

        close_container = tk.Frame(btn_frame, bg=colours['card'])
        close_container.pack()

        close_btn = RoundedButton(
            close_container,
            "Close",
            overlay.destroy,
            colours['button_secondary'],
            colours['text_primary'],
            colours['hover'],
            width=240,
            height=38,
            parent_bg=colours['card']
        )
        close_btn.pack()

    def import_selected_goals(self, overlay):
        selected = self.past_listbox.curselection()
        imported_texts = [self.past_goal_map[i]["text"] for i in selected]

        if imported_texts:
            for g in self.goal_manager.get_incomplete_last_week_goals():
                if g["text"] in imported_texts:
                    self.goal_manager.add_goal(g["text"], imported_from=g["date"])
            self.load_today_goals()
            messagebox.showinfo("Success", f"Imported {len(imported_texts)} goal(s)!")

        
        overlay.destroy()

        


