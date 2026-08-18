class CozyTheme: 
    def __init__(self):
        self.light = {
        'bg_primary': '#FFF8F0',
        'bg_secondary': '#F5F1EB',
        'surface': '#FFFFFF',
        'card': '#FEFEFE',
        'accent': '#D4A574',
        'accent_hover': '#B89558',
        'text_primary': '#2F1B14',
        'text_secondary': '#5D4E37',
        'text_muted': '#9B8D82',
        'success': '#7B9A5A',
        'success_hover': '#5A7A50',
        'border': '#E6D7C3',
        'border_light': '#F0E8DD',
        'hover': '#E8D5B7',
        'button_primary': '#D4A574',
        'button_secondary': '#C8B99C',
        'select_bg': '#D3E4CD',
        'shadow': '#00000008',
        'image_placeholder': '#E8DFD4'
        }

        self.dark = {
        'bg_primary': '#1A1611',
        'bg_secondary': '#2A241F',
        'surface': '#332B26',
        'card': '#3D342A',
        'accent': '#E6C08A',
        'accent_hover': '#CBA66F',
        'text_primary': '#F5F1EB',
        'text_secondary': '#D2B48C',
        'text_muted': "#F3E6CD",
        'success': '#8FAA6F',
        'success_hover': '#6F8F57',
        'border': '#4A3F35',
        'border_light': '#5D4E37',
        'hover': '#3D342A',
        'button_primary': '#B8956F',
        'button_secondary': '#9A8269',
        'select_bg': '#4A5D47',
        'shadow': '#00000020',
        'image_placeholder': '#3D362F'
        }
        #Default to light mode
        self.dark_mode = False
        self.colors = self.light

    def set_mode(self, dark_mode):
        self.dark_mode = dark_mode
        self.colors = self.dark if dark_mode else self.light

    def get(self, key, default=None):
        return self.colors.get(key, default)