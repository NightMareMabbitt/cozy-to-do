import sys

FONTS = {
    'title': ('SF Pro Display', 20, 'bold') if sys.platform == 'darwin' else ('Helvetica', 20, 'bold'),
    'subtitle': ('SF Pro Display', 16) if sys.platform == 'darwin' else ('Helvetica', 16),
    'body': ('SF Pro Text', 14) if sys.platform == 'darwin' else ('Helvetica', 14),
    'button': ('SF Pro Text', 12, 'bold') if sys.platform == 'darwin' else ('Helvetica', 12, 'bold'),
    'small': ('SF Pro Text', 11) if sys.platform == 'darwin' else ('Helvetica', 11),
}
