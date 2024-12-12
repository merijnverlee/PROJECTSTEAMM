import tkinter
import tkinter as tk
from datetime import datetime

from PIL import ImageTk

from Login_scherm import *
import os
import requests
from Steam_test import GetGames
from steam_web_api import Steam

KEY = os.environ.get("steam_key")

steam = Steam(KEY)

print(datetime.now().strftime('%A, %d, %B %Y\n'))

root = tk.Tk()
root.resizable(False, False)
root.geometry('1305x780')
root.title("Project Steam")
root.configure(bg='#c7d5e0')

# DRAW TOP BLUE BAR - DRAW TITLE - DRAW DATETIME
top_bg = tk.Canvas(root, width=1305, height=60, bg='#1b2838', highlightthickness=0).place(x=0, y=0)
tk.Label(top_bg, text='Project Steam', font='Montserrat 25', bg='#1b2838', fg='white').place(x=15, y=3)
tk.Label(top_bg, text=datetime.now().strftime('%A, %d %B %Y'), font='Montserrat 20', bg='#1b2838', fg='white').place(
    x=930, y=8)

# STEAM TOP SELLING
user = steam.users.get_user_details("76561198995017863")
steam_box = tk.Canvas(root, width=590, height=520, bg='#2a475e', highlightthickness=0).place(x=390, y=240)
tk.Label(steam_box, text=user['player']['personaname'], font='Montserrat 8 bold', bg='#1b2838',
         fg='#FFFFFF').place(x=395, y=220)
steam_box_top = tk.Canvas(root, width=590, height=20, bg='#1b2838', highlightthickness=0).place(x=390, y=220)
steam_box_price = tk.Canvas(steam_box, width=80, height=520, bg='#171a21', highlightthickness=0).place(x=900, y=240)
tk.Label(steam_box_top, text='Steam Beste Reviews', font='Montserrat 8 bold', bg='#1b2838',
         fg='#FFFFFF').place(x=395, y=220)

steam_games = GetGames()


def getimage_steam(imgurl):
    url = 'https://steamcdn-a.akamaihd.net/steam/apps/' + imgurl + '/capsule_184x69.jpg'
    response_img = requests.get(url)
    img_data = response_img.content
    img_resize = Image.open(BytesIO(img_data)).resize((107, 40), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img_resize)
    return img


img_y = 240
photo_list = []
for i in range(0, 13):
    photo_list.append(getimage_steam(steam_games[i].imgurl))
    tk.Label(root, image=photo_list[i], width=107, height=40, bd=0).place(x=390, y=img_y)
    img_y += 40

steam_y = 245
for i in range(0, 13):
    tk.Label(steam_box, text=steam_games[i].title, font='Montserrat 12', bg='#2a475e',
             fg='#FFFFFF').place(x=500, y=steam_y)
    tk.Label(steam_box, text=steam_games[i].price, font='Montserrat 12', bg='#171a21',
             fg='#FFFFFF').place(x=910, y=steam_y)
    steam_y += 40

# WEER
weather_box = tk.Canvas(root, width=1265, height=100, bg='#2a475e', highlightthickness=0).place(x=20, y=100)
weather_box_top = tk.Canvas(root, width=1265, height=20, bg='#1b2838', highlightthickness=0).place(x=20, y=80)
tk.Label(weather_box_top, text='Weersvoorspelling, Utrecht NL.', font='Montserrat 8 bold', bg='#1b2838',
         fg='#FFFFFF').place(x=25, y=80)

# PI
pihole_box = tk.Canvas(root, width=350, height=140, bg='#2a475e', highlightthickness=0).place(x=20, y=240)
pihole_box_top = tk.Canvas(root, width=350, height=20, bg='#1b2838', highlightthickness=0).place(x=20, y=220)
pihole_box_temp = tk.Canvas(pihole_box, width=350, height=30, bg='#2a475e', highlightthickness=0).place(x=20, y=240)
pihole_box_middle = tk.Canvas(pihole_box, width=350, height=20, bg='#171a21', highlightthickness=0).place(x=20, y=270)
tk.Label(pihole_box_top, text='Raspberry PI', font='Montserrat 8 bold', bg='#1b2838', fg='#FFFFFF') \
    .place(x=25, y=220)

# Vriendenlijst


vriendenlijst = tk.Canvas(root, width=350, height=160, bg='#2a475e', highlightthickness=0).place(x=20, y=420)
hdd_box_top = tk.Canvas(root, width=350, height=20, bg='#1b2838', highlightthickness=0).place(x=20, y=400)
tk.Label(hdd_box_top, text='Online vrienden', font='Montserrat 8 bold', bg='#1b2838', fg='#FFFFFF') \
    .place(x=25, y=400)

# NOS Nieuws
threshold_box = tk.Canvas(root, width=285, height=520, bg='#2a475e', highlightthickness=0).place(x=1000, y=240)
threshold_box_top = tk.Canvas(root, width=285, height=20, bg='#1b2838', highlightthickness=0).place(x=1000, y=220)
tk.Label(threshold_box_top, text='NOS Nieuws', font='Montserrat 8 bold', bg='#1b2838',
         fg='#FFFFFF').place(x=1005, y=220)

# DATABASE
news_box = tk.Canvas(root, width=350, height=140, bg='#2a475e', highlightthickness=0).place(x=20, y=620)
news_box_top = tk.Canvas(root, width=350, height=20, bg='#1b2838', highlightthickness=0).place(x=20, y=600)
tk.Label(news_box_top, text='DATABASE', font='Montserrat 8 bold', bg='#1b2838',
         fg='#FFFFFF').place(x=25, y=600)

root.mainloop()
