import tkinter as tk
from config.fonts import FONTS
from config.constants import RADIUS

class RoundedButton(tk.Canvas):
  def __init__(self, parent, text, command, bg_color, text_color='#FFFFF', **kwargs):
    width =kwargs.pop('width', 120)
    height = kwargs.pop('height', 48)
    parent_bg = kwargs.pop('parent_bg', '#FFFFFF')
    hover_color = kwargs.pop('hover_color', None)

    self.bg_color = bg_color
    self.text_color = text_color
    self.hover_color = hover_color
    self.text = text
    self.command = command
    self.is_hovered = False

    super().__init__(parent, width-width, height=height, bg=parent_bg, highlightthickness=0, cursor='hand2')

    

