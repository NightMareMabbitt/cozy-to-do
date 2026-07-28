import tkinter as tk
from tkinter import Scrollbar, Listbox

from config.fonts import FONTS
from config.constants import SPACING

class GoalsListSection:
  #Goals List section with Listbox and empty state

  def __init__(self, parent, colours):
    self.parent = parent
    self.colours = colours

    self.section = None
    self.listbox = None
    self.empty_label = None

    self.create_widgets()

  def create_widgets(self):
    #Create list widgets
    self.section = tk.Frame(self.parent, bg=self.colours['card'])
    self.section.pack(pady=(0, SPACING['md']), padx=SPACING['lg'], fill=tk.BOTH, expand=True)

    #Empty State Label
    self.empty_label = tk.Label(
      self.section,
      text="No goals yet. Add your first goal to get started!",
      font=FONTS['body'],
      fg=self.colours['text_muted'],
      bg=self.colours['card'],
    )

    #Scrollbar
    scrollbar = Scrollbar(self.section)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #Listbox
    self.listbox = tk.Listbox(
      self.section,
      yscrollcommand=scrollbar.set,
      font=FONTS['body'],
      bg=self.colours['surface'],
      fg=self.colours['text_primary'],
      selectbackground=self.colours['select_bg'],
      selectforeground=self.colours['text_primary'],
      relief='flat',
      highlightthickness=2,
      highlightcolor=self.colours['accent'],
      highlightbackground=self.colours['border'],
      bd=0,
      selectmode=tk.MULTIPLE
    )

    self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=self.listbox.yview)

  def update_empty_state(self):
      #Show/hide empty state based on listbox content
      if self.listbox.size() == 0:
        self.empty_label.pack(expand=True)
      else:
        self.empty_label.pack_forget()
    
  def clear(self):
      self.listbox.delete(0, tk.END)

  def add_item(self, text):
      self.listbox.insert(tk.END, text)

  def get_selection(self):
      #Get selected indices
      return self.listbox.curselection()

  def update_theme(self, colours):
      self.colours = colours

      self.section.configure(bg=colours['card'])
      self.empty_label.configure(fg=colours['text_muted'], bg=colours['card'])
      self.listbox.configure(
        bg=colours['surface'],
        fg=colours['text_primary'],
        selectbackground=colours['select_bg'],
        selectforeground=colours['text_primary'],
        highlightcolor=colours['accent'],
        highlightbackground=colours['border']
      )