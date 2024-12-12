from tkinter import *
from tkinter import messagebox


def login():
    gebruikersnaam = e1.get()
    wachtwoord = e2.get()

    if (gebruikersnaam== "" and wachtwoord == ""):
        messagebox.showinfo("", "Voer geldige gegevens in.")

    elif(gebruikersnaam == "Project" and wachtwoord == "Steam"):

        messagebox.showinfo("","Login succesvol.")
        root.destroy()

    else:
        messagebox.showinfo("","Wachtwoord en gebruikersnaam zijn onjuist.")

root = Tk()
root.title("Login")
root.geometry("400x200")
global e1
global e2

Label(root, text="Login voor project steam").place(x=5, y=10)

Label(root, text="Gebruikersnaam").place(x=10, y=40)
Label(root, text="Wachtwoord").place(x=10, y=60)

e1 = Entry(root)
e1.place(x=140, y=40)

e2 = Entry(root)
e2.place(x=140, y=60)
e2.config(show="*")

Button(root, text="Login", command=login, height = 2, width = 13).place(x=150,y=110)
root.mainloop()