import tkinter as tk
from config.fonts import FONTS

class RoundedButtton(tk.Canvas):
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

class EmptyStateLabel(tk.Label):
    def __init__(self, parent, colours):
        super().__init__(
            parent, 
            text="No goals yet. Add one above!",
            font=FONTS['body'],
            fg=colours['text_muted'],
            bg=colours['card']
        )
