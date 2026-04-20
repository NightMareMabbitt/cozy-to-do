import tkinter as tk
import random
from datetime import datetime

from config.fonts import FONTS
from config.constants import SPACING, PROMPTS

class HeaderSection: 
  def __init__(self, parent, colours, dark_mode, toggle_callback):
    self.parent = parent
    self.colours = colours
    self.dark_mode = dark_mode
    self.toggle_callback = toggle_callback
    
    self.frame = None
    self.date_label = None
    self.prompt_label = None
    self.toggle_button = None

    self.create_widgets()

  def create_widgets(self):
    # Create Header Widgets
    self.frame = tk.Frame(self.parent, bg=self.colours['bg_primary'])
    self.frame.pack(fill='x', pady=(0, SPACING['lg']))

    #Date Label
    today_str = datetime.now().strftime("%A, %B %d")
    self.date_label = tk.Label(
        self.header_frame,
        text=today_str.upper(),
        font=FONTS['small'],
        fg=colours['text_muted'],
        bg=colours['bg_primary'],
        )
    self.date_label.pack(pady=(0, SPACING['xs']))

      #Prompt
    today_prompt = random.choice(PROMPTS)
    self.prompt_label = tk.Label(
            self.header_frame,
            text=today_prompt,
            font=FONTS['title'],
            justify="center",
            wraplength=540,
            bg=colours['bg_primary'],
            fg=colours['text_primary'],
        )

    self.prompt_label.pack(pady=(SPACING['md'], SPACING['sm']))
    
    #Dark Mode Toggle
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

    def update_theme(self, colours, dark_mode):
        self.colours = colours
        self.dark_mode = dark_mode

        self.frame.config(bg=colours['bg_primary'])
        self.date_label.config(fg=colours['text_muted'], bg=colours['text_muted'])
        self.prompt_label.config(fg=colours['text_primary'], bg=colours['text_primary'])
        
        mode_emoji = "☀️" if self.dark_mode else "🌙"
        self.toggle_button.config(
            text=mode_emoji,
            bg=colours['surface'],
            fg=colours['accent'],
            activebackground=colours['hover'],
            activeforeground=colours['accent']
        )