import sys

FONTS = {
    'hero': ('SF Pro Display', 28, 'bold') if sys.platform == 'darwin' else ('Segoe UI', 32, 'bold'),
    'title': ('SF Pro Display', 20, 'bold') if sys.platform == 'darwin' else ('Segoe UI', 20, 'bold'),
    'subtitle': ('SF Pro Display', 16) if sys.platform == 'darwin' else ('Segoe UI', 16),
    'body': ('SF Pro Text', 14) if sys.platform == 'darwin' else ('Segoe UI', 14),
    'body_bold': ('SF Pro Text', 14, 'bold') if sys.platform == 'darwin' else ('Segoe UI', 14, 'bold'),
    'button': ('SF Pro Text', 12, 'bold') if sys.platform == 'darwin' else ('Segoe UI', 12, 'bold'),
    'small': ('SF Pro Text', 11) if sys.platform == 'darwin' else ('Segoe UI', 11),
    'timer_large': ('SF Pro Display', 48, 'bold') if sys.platform == 'darwin' else ('Segoe UI', 48, 'bold'),
    'timer_small': ('SF Pro Display', 24, 'bold') if sys.platform == 'darwin' else ('Segoe UI', 24, 'bold'),
    'icon_large': ('Segoe UI', 48),
    'icon_medium': ('Segoe UI', 32),
    'icon_small': ('Segoe UI', 18),             
}
