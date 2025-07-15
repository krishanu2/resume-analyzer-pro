import tkinter as tk

window = tk.Tk()
window.title("Test Window")
window.geometry("300x200")
tk.Label(window, text="Tkinter is working!").pack(pady=50)

window.mainloop()
