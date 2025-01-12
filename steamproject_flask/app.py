import logging
from flask import Flask, render_template
import psycopg2
from psycopg2 import sql
from datetime import datetime
from pydantic_core.core_schema import none_schema
from statistieken import gemiddelde_speeltijd_weergeven
from statistieken import mediaan_prijs_per_genre_weergeven
from flask import request, jsonify

# Flask-app configureren
app = Flask(__name__)

# Logging configureren
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuratie
DB_HOST = '52.178.4.146'
DB_PORT = '5432'
DB_NAME = 'steamdb'
DB_USER = 'merijn'
DB_PASSWORD = 'Welkom#1'

from flask import request, redirect, url_for

@app.route('/search_game', methods=['POST'])
def search_game():
    """Zoek een game op basis van de ingevoerde appid."""
    appid = request.form.get('appid')
    if appid:
        # Controleer of appid geldig is (optioneel)
        return redirect(url_for('game_profile', appid=int(appid)))
    return redirect(url_for('home'))

@app.route('/')
def home():
    """Homepage met een lijst van games"""
    games = [
        {"appid": 2357570, "name": "Overwatch 2"},
        {"appid": 271590, "name": "Grand theft auto v"},
        {"appid": 1593500, "name": "God of war ragnarok"}
    ]
    current_date = datetime.now().strftime('%A, %d %B %Y')
    online_friends = ["King of Death", "King Slayer", "BeastsXSteam", "The Honored One", "Killerbee"]
    top_10_games = get_top_10_games_by_positive_reviews()
    return render_template('home.html', games=games, current_date=current_date, top_10_games=top_10_games, sensor_status=sensor_status)


def get_game_data_from_db(appid):
    """Ophalen van gamegegevens uit de Azure PostgreSQL-database."""
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        query = sql.SQL("SELECT * FROM steam_games WHERE appid::text = %s")
        cursor.execute(query, (str(appid),))
        steam_games = cursor.fetchone()
        cursor.close()
        connection.close()


        if steam_games:
            return {
                "appid": steam_games[0],
                "name": steam_games[2] or "Naam niet beschikbaar",
                "release_date": steam_games[3] or "Onbekend",
                "english": "Ja" if steam_games[4] else "Nee",
                "developer": steam_games[5] or "Geen ontwikkelaar beschikbaar",
                "publisher": steam_games[6] or "Geen uitgever beschikbaar",
                "platforms": steam_games[7],
                "required_age": steam_games[8] if steam_games[8] else "Geen",
                "categories": steam_games[9].split(';') if steam_games[9] else ["Geen categorieën beschikbaar"],
                "genres": steam_games[10].split(';') if steam_games[10] else ["Geen genres beschikbaar"],
                "steamspy_tags": steam_games[11].split(';') if steam_games[11] else ["Geen tags beschikbaar"],
                "achievements": steam_games[12] if steam_games[12] else "Geen",
                "positive_ratings": steam_games[13] if steam_games[13] else 0,
                "negative_ratings": steam_games[14] if steam_games[14] else 0,
                "average_playtime": steam_games[15] if steam_games[15] else "Niet beschikbaar",
                "median_playtime": steam_games[16] if steam_games[16] else "Niet beschikbaar",
                "owners": steam_games[17] if steam_games[17] else "Niet beschikbaar",
                "price": f"€{steam_games[18]}" if steam_games[18] else "Niet beschikbaar"
            }
        else:
            return None

    except psycopg2.Error as e:
        logging.error(f"Database error: {e.pgcode} - {e.pgerror}")
        return None
    except Exception as e:
        logging.error(f"Error fetching data from database: {str(e)}")
        return None

def get_top_10_games_by_positive_reviews():
    """Ophalen van de top 10 games met de meeste positieve reviews."""
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        query = sql.SQL("""
            SELECT name, positive_ratings
            FROM steam_games
            ORDER BY positive_ratings DESC
            LIMIT 10 """)
        cursor.execute(query)
        top_games = cursor.fetchall()
        cursor.close()
        connection.close()
        return [{"name": game[0], "positive_ratings": game[1]} for game in top_games]

    except psycopg2.Error as e:
        logging.error(f"Database error: {e.pgcode} - {e.pgerror}")
        return []
    except Exception as e:
        logging.error(f"Error fetching data from database: {str(e)}")
        return []



@app.route('/game/<int:appid>')
def game_profile(appid):
    """Profielpagina van een game gebaseerd op appid"""
    game = get_game_data_from_db(appid)
    if game:
        return render_template('game_profile.html', game=game)
    else:
        return render_template('game_not_found.html', appid=appid), 404

@app.route('/generate_chart')
def generate_chart():
    gemiddelde_speeltijd_weergeven()
    mediaan_prijs_per_genre_weergeven()
    return "Grafieken gegenereerd"

sensor_status = {"status": "safe", "distance": None}

@app.route('/update_distance', methods=['POST'])
def update_distance():
    global sensor_status
    data = request.get_json()
    if data:
        sensor_status = data
        return jsonify({"message": "Status bijgewerkt"}), 200
    return jsonify({"error": "Ongeldige gegevens"}), 400

@app.route('/get_distance_status', methods=['GET'])
def get_distance_status():
    return jsonify(sensor_status)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

