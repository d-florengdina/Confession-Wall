import tkinter as tk


window = tk.Tk()
window.title("Data Entry Form")
window.geometry("728x460")

frame = tk.Frame(window)

label = tk.Label(text = "Will you be my valentine?",
                 font = ("Arial", 20, "bold"),
                 bg = "hot pink",
                 fg = "white")
label.pack(pady=20, padx=20)

yes_btn = tk.Button(text="Yes!",
                    bg = "white",
                    fg = "hot pink",
                    font = ("Arial", 16, "bold"),
                    relief = tk.RAISED,
                    borderwidth = 5)
yes_btn.pack(side = tk.LEFT, padx = (50, 0))

no_btn = tk.Button(text = "No!",
                   bg = "white",
                   fg = "hot pink",
                   font = ("Arail", 16, "bold"),
                   relief = tk.RAISED,
                   borderwidth =  5)
no_btn.pack(side = tk.RIGHT, padx = (0, 50))

window.mainloop()