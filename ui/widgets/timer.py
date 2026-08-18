import tkinter as tk
from config.fonts import FONTS


class CircularTimer(tk.Canvas):
    """Circular timer display matching Figma design."""
    
    def __init__(self, parent, colors, **kwargs):
        self.colors = colors
        super().__init__(parent, width=300, height=300,
                        bg=colors.get('card_bg'), highlightthickness=0)
        
        self.time_remaining = 25 * 60  # 25 minutes in seconds
        self.total_time = 25 * 60
        self.is_running = False
        
        self.draw_timer()
    
    def draw_timer(self):
        """Draw the circular timer."""
        self.delete('all')
        cx, cy, radius = 150, 150, 120
        
        # Background circle
        self.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
                        outline=self.colors.get('timer_border'),
                        width=12, fill=self.colors.get('timer_bg'))
        
        # Progress arc (if timer is running)
        if self.time_remaining < self.total_time:
            progress = (self.total_time - self.time_remaining) / self.total_time
            extent = -360 * progress
            self.create_arc(cx-radius, cy-radius, cx+radius, cy+radius,
                           start=90, extent=extent,
                           outline=self.colors.get('accent'),
                           width=12, style='arc')
        
        # Time text
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_text = f"{minutes:02d}:{seconds:02d}"
        
        self.create_text(cx, cy-20, text=time_text,
                        font=FONTS['timer_large'],
                        fill=self.colors.get('text_primary'))
        
        # Status text
        status = "Focus time!" if self.is_running else "Ready to focus"
        self.create_text(cx, cy+40, text=status,
                        font=FONTS['timer_small'],
                        fill=self.colors.get('text_secondary'))
    
    def set_duration(self, minutes):
        """Set timer duration."""
        self.time_remaining = minutes * 60
        self.total_time = minutes * 60
        self.draw_timer()
    
    def start(self):
        """Start the timer."""
        self.is_running = True
        self.draw_timer()
    
    def pause(self):
        """Pause the timer."""
        self.is_running = False
        self.draw_timer()
    
    def reset(self):
        """Reset the timer."""
        self.is_running = False
        self.time_remaining = self.total_time
        self.draw_timer()
    
    def tick(self):
        """Decrease timer by one second."""
        if self.is_running and self.time_remaining > 0:
            self.time_remaining -= 1
            self.draw_timer()