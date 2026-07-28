import tkinter as tk

from config.fonts import FONTS
from config.constants import SPACING
from ui.widgets import RoundedButton

class InputSection:
  #Input section with entry field and add button

  def __init__(self, parent, colours, add_callback, return_callback):
   self.parent = parent
   self.colours = colours
   self.add_callback = add_callback
   self.return_callback = return_callback

   self.section = None
   self.entry = None
   self.add_button = None

   self.create_widgets()

  def create_widgets(self):
    #Create input widgets
    self.section = tk.Frame(self.parent, bg=self.colours['card'])
    self.section.pack(pady=(SPACING['lg'], SPACING['md']), padx=SPACING['lg'], fill='x')

    self.entry = tk.Entry(
      self.section,
      font=FONTS['body'],
      bg=self.colours['surface'],
      fg=self.colours['text_primary'],
      insertbackground=self.colours['accent'],
      bd=0,
      relief='flat',
      highlightthickness=2,
      highlightcolor=self.colours['accent'],
      highlightbackground=self.colours['border']
    )
    self.entry.pack(fill='x', ipady=12)
    self.entry.bind('<Return>', self.return_callback)

    #Add Button container

    add_btn_container = tk.Frame(self.section, bg=self.colours['card'])
    add_btn_container.pack(pady=(SPACING['sm'], 0))
    
    self.add_button = RoundedButton(
      add_btn_container,
      "✨Add Goal",
      self.add_callback,
      self.colours['accent'],
      '#FFFFFF',
      self.colours['accent_hover'],
      width=200,
      height=42,
      parent_bg=self.colours['card']
    )

    self.add_button.pack()

  def get_text(self):
    return self.entry.get().strip()

  
  def clear(self):
    self.entry.delete(0, tk.END)

  def update_theme(self, colours):
    self.colours = colours

    self.section.configure(bg=colours['card'])
    self.entry.configure(
      bg=colours['surface'],
      fg=colours['text_primary'],
      insertbackground=colours['accent'],
      highlightbackground=colours['border'],
      highlightcolor=colours['accent']
    )
    self.add_button.update_colors(
      colours['accent'],
      '#FFFFFF',
      colours['accent_hover'],
      colours['card']
    )
