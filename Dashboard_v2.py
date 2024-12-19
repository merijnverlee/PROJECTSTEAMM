import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import steam
from Login_scherm import *
import os
import requests
import re
from bs4 import BeautifulSoup
from steam import GetGames
# from steam_web_api import Steam
import pyodbc
import io
import paramiko
import psycopg


def get_weather_forecast(city="Utrecht", api_key="87cd39ea96d47fb7e5ca0839517cdd13
"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=nl"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract relevante informatie
        forecast = {
            "stad": data["name"],
            "temperatuur": data["main"]["temp"],
            "beschrijving": data["weather"][0]["description"],
            "vochtigheid": data["main"]["humidity"],
            "windsnelheid": data["wind"]["speed"]
        }
        return forecast
    except requests.exceptions.RequestException as e:
        print("Fout bij het ophalen van weergegevens:", e)
        return None


def connect_to_server():
    try:
        # Servergegevens
        hostname = "CSC-Tyler-01"  # Vervang dit met het IP-adres of de hostnaam van je server
        username = "merijn"  # Gebruikersnaam
        password = "Welkom#1"  # Wachtwoord (of gebruik een SSH-sleutel)

        # Maak SSH-verbinding
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        return client
    except Exception as e:
        print(f"Fout bij verbinden met server: {e}")
        return None

def fetch_server_data():
    try:
        client = connect_to_server()
        if not client:
            return []

        # Voer een commando uit (bijv. om systeembestanden te bekijken)
        command = "ls -l /var/log"  # Pas dit aan naar het gewenste commando
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode("utf-8")

        # Verwerk de uitvoer (splits regels in een lijst van tuples)
        rows = []
        for line in output.splitlines()[1:]:  # Sla de headerregel over
            parts = line.split(maxsplit=8)
            if len(parts) == 9:
                rows.append((parts[0], parts[8]))  # Bijvoorbeeld: rechten en bestandsnaam

        client.close()
        return rows
    except Exception as e:
        print(f"Fout bij het ophalen van gegevens: {e}")
        return []

def load_server_data(self):
    data = fetch_server_data()
    self.database_tree.delete(*self.database_tree.get_children())  # Maak bestaande gegevens leeg
    for row in data:
        self.database_tree.insert("", "end", values=row)




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

        # Voeg dynamische labels toe voor de top 25 Steam-games
        steam_y = 245  # Startpositie Y binnen de Steam-box
        game_names = get_steam_names()[:25]  # Haal de top 25 games op

        for i, game in enumerate(game_names):
            # Maak een label voor de naam van de game
            tk.Label(self, text=f"{i + 1}. {game}", font='Montserrat 10', bg='#2a475e', fg='#FFFFFF', anchor="w") \
                .place(x=400, y=steam_y)
            steam_y += 20  # Verplaats Y-positie voor de volgende game






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

        # Voeg dit toe aan het 'weather_box' gedeelte in de main_window-methode
        weather_data = get_weather_forecast()

        if weather_data:
            x_offset = 30
            y_offset = 120
            tk.Label(self, text=f"Stad: {weather_data['stad']}", font='Montserrat 10', bg='#2a475e', fg='#FFFFFF',
                     anchor="w") \
                .place(x=x_offset, y=y_offset)
            tk.Label(self, text=f"Temperatuur: {weather_data['temperatuur']}°C", font='Montserrat 10', bg='#2a475e',
                     fg='#FFFFFF', anchor="w") \
                .place(x=x_offset, y=y_offset + 20)
            tk.Label(self, text=f"Beschrijving: {weather_data['beschrijving']}", font='Montserrat 10', bg='#2a475e',
                     fg='#FFFFFF', anchor="w") \
                .place(x=x_offset, y=y_offset + 40)
            tk.Label(self, text=f"Vochtigheid: {weather_data['vochtigheid']}%", font='Montserrat 10', bg='#2a475e',
                     fg='#FFFFFF', anchor="w") \
                .place(x=x_offset, y=y_offset + 60)
            tk.Label(self, text=f"Windsnelheid: {weather_data['windsnelheid']} m/s", font='Montserrat 10', bg='#2a475e',
                     fg='#FFFFFF', anchor="w") \
                .place(x=x_offset, y=y_offset + 80)
        else:
            tk.Label(self, text="Fout bij het laden van weergegevens.", font='Montserrat 10', bg='#2a475e',
                     fg='#FFFFFF', anchor="w") \
                .place(x=30, y=120)

        #rasberry pi
        pihole_box = tk.Canvas(self, width=350, height=140, bg='#2a475e', highlightthickness=0).place(x=20, y=240)
        pihole_box_top = tk.Canvas(self, width=350, height=20, bg='#1b2838', highlightthickness=0).place(x=20, y=220)
        pihole_box_temp = tk.Canvas(pihole_box, width=350, height=30, bg='#2a475e', highlightthickness=0).place(x=20,
                                                                                                                y=240)
        pihole_box_middle = tk.Canvas(pihole_box, width=350, height=20, bg='#171a21', highlightthickness=0).place(x=20,
                                                                                                                  y=270)
        tk.Label(pihole_box_top, text='Raspberry PI', font='Montserrat 8 bold', bg='#1b2838', fg='#FFFFFF') \
            .place(x=25, y=220)

        #vriendenlijst eventueel
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

        # Treeview voor databasegegevens
        from tkinter import ttk
        self.database_tree = ttk.Treeview(self, columns=("Rechten", "Bestandsnaam"), show="headings", height=6)
        self.database_tree.heading("Rechten", text="Rechten")
        self.database_tree.heading("Bestandsnaam", text="Bestandsnaam")
        self.database_tree.column("Rechten", anchor="center", width=150)
        self.database_tree.column("Bestandsnaam", anchor="center", width=150)
        self.database_tree.place(x=30, y=620)

        tk.Button(self, text="Haal Serverdata Op", command=self.load_server_data).place(x=30, y=760)


def main():
    window = Window()
    window.mainloop()
    games = get_steam_names()
    for num, game in enumerate(games):
        print(str(num + 1) + ". " + game)

if __name__ == "__main__":
    main()

