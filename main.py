import tkinter as tk
from ui.main_window import ToDoApp

def main():
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop() 

if __name__ == "__main__":
    main()

    