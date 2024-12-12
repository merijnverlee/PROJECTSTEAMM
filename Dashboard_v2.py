import tkinter as tk
from datetime import datetime
from PIL import ImageTk
import steam
from Login_scherm import *
import os
import requests
import re
from bs4 import BeautifulSoup
# from steam import GetGames
# from steam_web_api import Steam

def get_steam_names():
    response = requests.get("https://steamcharts.com/top")
    soup = BeautifulSoup(response.content, 'html.parser')
    contents = soup.findAll('td', {'class', "game-name left"})
    game_names = []
    for content in contents:
        game_names.append(content.get_text().replace('\t','').replace('\n',''))

    return game_names


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.main_window()

    def main_window(self):
        self.geometry("800x700")
        self.resizable(False, False)
        self.geometry('1305x780')
        self.title("Project Steam")
        self.configure(bg='#c7d5e0')
        self.steamgames = []

        #date time
        top_bg = tk.Canvas(self, width=1305, height=60, bg='#1b2838', highlightthickness=0).place(x=0, y=0)
        tk.Label(top_bg, text='Project Steam', font='Montserrat 25', bg='#1b2838', fg='white').place(x=15, y=3)
        tk.Label(top_bg, text=datetime.now().strftime('%A, %d %B %Y'), font='Montserrat 20', bg='#1b2838', fg='white').place(
            x=890, y=8)

        #steam box layout
        steam_box = tk.Canvas(self, width=590, height=520, bg='#2a475e', highlightthickness=0).place(x=390, y=240)
        steam_box_top = tk.Canvas(self, width=590, height=20, bg='#1b2838', highlightthickness=0).place(x=390, y=220)
        steam_box_price = tk.Canvas(self, width=80, height=520, bg='#171a21', highlightthickness=0).place(x=900, y=240)
        tk.Label(steam_box_top, text='Steam Beste reviews', font='Montserrat 7 bold', bg='#1b2838',
                 fg='#FFFFFF').place(x=395, y=220)


        # photo_list = []
        # for i in range(0, 13):
        #     photo_list.append(getimage_steam(self.steam_games[i].imgurl))
        #     tk.Label(root, image=photo_list[i], width=107, height=40, bd=0).place(x=390, y=img_y)
        #     img_y += 40
        #
        # steam_y = 245
        # for i in range(0, 13):
        #     tk.Label(steam_box, text=steam_games[i].title, font='Montserrat 12', bg='#2a475e',
        #              fg='#FFFFFF').place(x=500, y=steam_y)
        #     tk.Label(steam_box, text=steam_games[i].price, font='Montserrat 12', bg='#171a21',
        #              fg='#FFFFFF').place(x=910, y=steam_y)
        #     steam_y += 40

        #weather box
        weather_box = tk.Canvas(self, width=1265, height=100, bg='#2a475e', highlightthickness=0).place(x=20, y=100)
        weather_box_top = tk.Canvas(self, width=1265, height=20, bg='#1b2838', highlightthickness=0).place(x=20, y=80)
        tk.Label(weather_box_top, text='Weersvoorspelling, Utrecht NL.', font='Montserrat 8 bold', bg='#1b2838',
                 fg='#FFFFFF').place(x=25, y=80)

        #rasberry pi
        pihole_box = tk.Canvas(self, width=350, height=140, bg='#2a475e', highlightthickness=0).place(x=20, y=240)
        pihole_box_top = tk.Canvas(self, width=350, height=20, bg='#1b2838', highlightthickness=0).place(x=20, y=220)
        pihole_box_temp = tk.Canvas(pihole_box, width=350, height=30, bg='#2a475e', highlightthickness=0).place(x=20,
                                                                                                                y=240)
        pihole_box_middle = tk.Canvas(pihole_box, width=350, height=20, bg='#171a21', highlightthickness=0).place(x=20,
                                                                                                                  y=270)
        tk.Label(pihole_box_top, text='Raspberry PI', font='Montserrat 8 bold', bg='#1b2838', fg='#FFFFFF') \
            .place(x=25, y=220)

        #not.. sure..
        vriendenlijst = tk.Canvas(self, width=350, height=160, bg='#2a475e', highlightthickness=0).place(x=20, y=420)
        hdd_box_top = tk.Canvas(self, width=350, height=20, bg='#1b2838', highlightthickness=0).place(x=20, y=400)
        tk.Label(hdd_box_top, text='Online vrienden', font='Montserrat 8 bold', bg='#1b2838', fg='#FFFFFF') \
            .place(x=25, y=400)

        # NOS Nieuws
        threshold_box = tk.Canvas(self, width=285, height=520, bg='#2a475e', highlightthickness=0).place(x=1000, y=240)
        threshold_box_top = tk.Canvas(self, width=285, height=20, bg='#1b2838', highlightthickness=0).place(x=1000, y=220)
        tk.Label(threshold_box_top, text='NOS Nieuws', font='Montserrat 8 bold', bg='#1b2838',
                 fg='#FFFFFF').place(x=1005, y=220)

        # DATABASE
        news_box = tk.Canvas(self, width=350, height=140, bg='#2a475e', highlightthickness=0).place(x=20, y=620)
        news_box_top = tk.Canvas(self, width=350, height=20, bg='#1b2838', highlightthickness=0).place(x=20, y=600)
        tk.Label(news_box_top, text='DATABASE', font='Montserrat 8 bold', bg='#1b2838',
                 fg='#FFFFFF').place(x=25, y=600)



def main():
    window = Window()
    window.mainloop()
    games = get_steam_names()
    for num, game in enumerate(games):
        print(str(num + 1) + ". " + game)

if __name__ == "__main__":
    main()
