from tkinter import *
from weather import send_temperature_graph_email

def on_send_email():
    to_email = e1.get()
    if to_email:
        send_temperature_graph_email(to_email)
    else:
        print("Please enter an email address.")

root = Tk()
root.geometry("450x300")
root.title('Weather over email')

Label(root, text="Weather Update over Email !!").pack(pady=10)

frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Enter email").pack(side=LEFT)
e1 = Entry(frame)
e1.pack(side=LEFT, padx=5)

button = Button(root, text='Send email', width=50, command=on_send_email)
button.pack(pady=20)

root.mainloop()