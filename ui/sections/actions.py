import tkinter as tk

from config.constants import SPACING
from ui.widgets import RoundedButton

class ActionsSection: 

  def __init__(self, parent, colours, complete_callback, import_callback, view_callback):
    self.parent = parent
    self.colours = colours
    self.complete_callback = complete_callback
    self.import_callback = import_callback
    self.view_callback = view_callback

    self.section = None
    self.complete_btn = None
    self.import_btn = None
    self.view_btn = None

    self.create_widgets()

  def create_widgets(self):
    self.section = tk.Frame(self.parent, bg=self.colours['card'])
    self.section.pack(pady=(0, SPACING['lg']), fill='x')

    complete_container = tk.Frame(self.section, bg=self.colours['card'])
    complete_container.pack(pady=(0, SPACING['sm']))

    self.complete_btn = RoundedButton(
      complete_container,
      "Complete Selected",
      self.complete_callback,
      self.colours['success'],
      '#FFFFFF',
      self.colours['success_hover'],
      width=240,
      height=42,
      parent_bg=self.colours['card']
    )
    self.complete_btn.pack()

    separator = tk.Frame(self.section, bg=self.colours['border_light'], height=1)
    separator.pack(fill='x', pady=SPACING['md'])

    import_container = tk.Frame(self.section, bg=self.colours['card'])
    import_container.pack(pady=(0, SPACING['xs']))

    self.import_btn = RoundedButton(
      import_container,
      "Import Last Week's Goals",
      self.import_callback,
      self.colours['button_secondary'],
      self.colours['text_primary'],
      self.colours['hover'],
      width=240,
      height=38,
      parent_bg=self.colours['card']
    )
    self.import_btn.pack()

    view_container = tk.Frame(self.section, bg=self.colours['card'])
    view_container.pack()

    self.view_btn = RoundedButton(
      view_container,
      "View Last Week's Goals",
      self.view_callback,
      self.colours['button_secondary'],
      self.colours['text_primary'],
      self.colours['hover'],
      width=240,
      height=38,
      parent_bg=self.colours['card']
    )
    self.view_btn.pack()

  def update_theme(self, colours):
    self.colours = colours

    self.section.configure(bg=colours['card'])
    self.complete_btn.update_colors(
      colours['success'],
      '#FFFFFF',
      colours['success_hover'],
      colours['card']
    )

    self.import_btn.update_colors(
      colours['button_secondary'],
      colours['text_primary'],
      colours['hover'],
      colours['card']
    )

    self.view_btn.update_colors(
      colours['button_secondary'],
      colours['text_primary'],
      colours['hover'],
      colours['card']
    )