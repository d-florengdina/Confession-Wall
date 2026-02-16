import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox
from datetime import datetime
import time
from turtle import update 
import os

window = tk.Tk()
window.title("Confession Wall")
window.geometry("750x500")

frame = tk.Frame(window)
frame.pack(padx=10, pady=10, fill='both', expand=True)

#placing the time label beofre declaring the function
time_label = tk.Label(frame, text='', font=('Helvetica', 16), bg='white', fg='black')
time_label.grid(row=1, column=2, sticky='nsew')

#placing the date label
date_label = tk.Label(frame, text='', font=('Helvetica', 16), bg='white', fg='black')
date_label.grid(row=0, column=2, sticky='nsew')

def real_time():
    current_time = time.strftime('%I:%M %p') #12-hour time with am/pm 
    time_label.config(text=current_time)
    current_date = time.strftime('%d %B %Y') #day month year
    date_label.config(text=current_date)
    time_label.after(1000, real_time) #Updates every second

real_time()

bubble_color = ['light pink'] #default bubble color; using a list to make it mutable in nested functions   

#changes the bubble that you sent to d ifferent color
#i leave it like taht for now
def change_heartNBubble_color():
    color = colorchooser.askcolor()[1]
    if color:
        heartbtn.config(fg=color)
        bubble_color[0] = color

#button to change heart color as well as message bubble color
heartbtn = tk.Button(frame, text="💖", font=("Arial", 30), 
                     command=change_heartNBubble_color, bg='white')  #this triggers the color changer
heartbtn.grid(row=0, rowspan=2, column=0, sticky='nsew') #this is to make the heart button take up the first two rows and be on the left side of the frame

#the title of the board
title_label = tk.Label(frame, text="Confession Wall",
                            font=('Helvetica', 30, 'bold'), bg='Hot Pink', fg='white')
title_label.grid(row=0, rowspan=2, column=1, sticky='nsew')

#this is to let users get an idea of what they're using
authorsNote_label = tk.Label(frame, text='Don\'t be afraid to confess your feelings. This is your safe space.',
                             font=('Helvetica', 12, 'italic'), bg='hot pink', fg='black')
authorsNote_label.grid(row=2, column=0, columnspan=3, sticky='ew')

#creating the section for the messages/confessions to pop up
message_frame = tk.Frame(frame, bg='white', width=600, height=300)
message_frame.grid(row=3, column=0, columnspan=3, sticky='nsew')

#creating a scrollbar for the message frame
msgScrollbar= tk.Scrollbar(message_frame)
msgScrollbar.pack(side='right', fill='y')

#creating a canvasto hold the messages and scrollbar
msgCanvas = tk.Canvas(message_frame, bg='white', width=600, height=300, 
                      yscrollcommand=msgScrollbar.set) #setting the y command to the scrollbar
msgCanvas.pack(side='left', fill='both', expand=True)
msgScrollbar.config(command=msgCanvas.yview) #making the scrollbar controll the canvas so one can scroll up & down

#creating another frame inside the canvass that is in the message frame within the main frame to hold the actuall bubbles
bubble_container = tk.Frame(msgCanvas, bg='white')
msgCanvas.create_window((0,0), window=bubble_container, anchor='nw') #this is to make sure the canvas scroll with the bubbles

#saving existing messages to a file to be updated and loaded each time a new message is added or app is used
CONFESSIONS_FILE = 'confessions.txt'

#saving existing messages
def save_confessions(text, timestamp, color):
    with open(CONFESSIONS_FILE, 'a', encoding='utf-8') as f:
        #saving as: text|||timestamp|||color
        # Replace newlines in text to avoid breaking the format
        safe_text = text.replace('\n', '\\n')
        f.write(f'{safe_text}|||{timestamp}|||{color}\n')

#load messages from txt file when app is open
def load_confessions():
    if not os.path.exists(CONFESSIONS_FILE):
        return
    with open(CONFESSIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.rstrip('\n').split('|||')
            if len(parts) == 3:
                text, timestamp, color = parts
                #adding back the newlines
                text = text.replace('\n', '\\n')
                display_confessions(text, timestamp, color)

#display messages in the app
def display_confessions(text, timestamp, color):
    # creating the bubble frame to hold text and its timestamp
    bubble_frame = tk.Frame(bubble_container, bg='white')
    bubble_frame.pack(padx=20, pady=10, anchor='e')

    # main confession text (inside the bubble frame)
    new_bubble = tk.Label(bubble_frame, text=text,
                          font=('Helvetica', 12, 'italic'), bg=color, fg='black',
                          wraplength=500, justify='center', pady=10, padx=10)
    new_bubble.pack(fill='both', expand=True)
    ts_label = tk.Label(bubble_frame, text=timestamp,
                        font=('Helvetica', 9, 'italic'), bg='white', fg='grey')
    ts_label.pack(anchor='e', padx=8, pady=(4,0))

    bubble_container.update_idletasks()
    msgCanvas.config(scrollregion=msgCanvas.bbox('all')) #this is to update the scroll region of the canvas to include the new bubble

def addConfession():
    confession_text = input_entry.get("1.0", "end-1c")
    if confession_text.strip() == '':
        messagebox.showwarning(message="Empty. Please enter a confession before sending.")
        return
    
    # adding a timestamp inside the same frame, below the bubble text
    raw_date = datetime.now().strftime('%m/%d/%y')
    clean_date = raw_date.replace('/0', '/').lstrip('0')
    bubble_timestamp = datetime.now().strftime('%I:%M %p · ') + clean_date

    #saving messages & display
    save_confessions(confession_text, bubble_timestamp, bubble_color[0])
    display_confessions(confession_text, bubble_timestamp, bubble_color[0])

    input_entry.delete("1.0", 'end') #this is to clear the input entry after sending the confession


#input area in the main frame
input_entry = tk.Text(frame, font=('Helvetica', 12), bg='white', wrap='word', width=20, height=3)
input_entry.grid(row=4, column=0, columnspan=2, sticky='nsew')

def on_enter(event):
    addConfession()
    return 'break'

input_entry.bind('<Return>', on_enter) #this bind the enter key to sending the input into the messag frame

send_btn = tk.Button(frame, text='Send', font=('Helvetica', 12, 'bold'), bg='hot pink',
                      fg='white',borderwidth=2, relief='raised', command=lambda: addConfession())
send_btn.grid(row=4, column=2, sticky='nsew') #this is to make the send button be on the right side of the input entry and take up the last column of the grid


# Configure grid weights for resizing
frame.grid_rowconfigure(3, weight=1)
frame.grid_columnconfigure(1, weight=1)

load_confessions()

window.mainloop()


