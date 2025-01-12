import psycopg2
import matplotlib.pyplot as plt

DB_HOST = '52.178.4.146'
DB_PORT = '5432'
DB_NAME = 'steamdb'
DB_USER = 'merijn'
DB_PASSWORD = 'Welkom#1'

def game_data_ophalen(query):
    # Data ophalen uit de database
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    except psycopg2.Error as e:
        print(f"Database error: {e.pgcode} - {e.pgerror}")
    except Exception as e:
        print(f"Error fetching data from database: {str(e)}")
    return []

def gemiddelde_speeltijd_weergeven():
    query = """
        SELECT name, average_playtime
        FROM steam_games
        WHERE positive_ratings IS NOT NULL
        ORDER BY positive_ratings DESC
        LIMIT 10;
    """
    # berekening gemiddelde speeltijd van de top 10 games
    games = game_data_ophalen(query)
    names = [game[0] for game in games]
    average_playtimes = [game[1] for game in games]

    # Staafdiagram layout
    plt.figure(figsize=(8, 4))
    plt.barh(names, average_playtimes, color='skyblue')
    plt.xlabel("Gemiddelde speeltijd (minuten)")
    plt.ylabel("Games")
    plt.title("Gemiddelde speeltijd per game")
    plt.gca().invert_yaxis()
    plt.tight_layout()

    # code voor het opslaan van de afbeelding in de images map onder static
    plt.savefig("static/gemiddelde_speeltijd_per_game.png")
    plt.close()
    return


def mediaan_prijs_per_genre_weergeven():
    query = """
        SELECT genres, price
        FROM steam_games
        WHERE price IS NOT NULL AND genres IS NOT NULL
        ORDER BY genres;
    """
    games = game_data_ophalen(query)

    # De data van deze 10 genres wil ik weergeven
    gewenste_genres = ["Action", "Adventure", "RPG", "Simulation", "Strategy",
                       "Racing", "Sports", "Education", "Video Production", "Photo Editing"]

    # Sorteren van de data per genre
    genres = {}
    for game in games:
        genre_list = game[0].split(";")  # Verdeel meerdere genres
        price = float(game[1])
        for genre in genre_list:
            genre = genre.strip()  # Hiermee verwijder ik de spaties
            if genre in gewenste_genres:  # Voegt alleen de genres toe die ik wil
                if genre not in genres:
                    genres[genre] = []
                genres[genre].append(price)

    # Berekening mediaanprijs
    median_prices = {}
    for genre, prices in genres.items():
        prices.sort()
        n = len(prices)
        if n % 2 == 1:
            median_price = prices[n // 2]
        else:
            median_price = (prices[n // 2 - 1] + prices[n // 2]) / 2
        median_prices[genre] = median_price

    # Sorteer genres op mediaanprijs
    sorted_genres = sorted(median_prices.items(), key=lambda x: x[1], reverse=True)

    # Data voor de grafiek
    genre_names = [item[0] for item in sorted_genres]
    median_values = [item[1] for item in sorted_genres]

    # ik wil alleen de data van de tien genres
    genre_names = genre_names[:10]
    median_values = median_values[:10]

    # Staafdiagram layout
    plt.figure(figsize=(10, 6))
    plt.barh(genre_names, median_values, color='lightgreen')
    plt.xlabel("Mediaanprijs (€)")
    plt.ylabel("Genres")
    plt.title("Mediaanprijs per genre")
    plt.xlim(0, 9)  # x-as
    plt.gca().invert_yaxis()
    plt.tight_layout()

    # code voor het opslaan van de afbeelding in de images map onder static
    plt.savefig("static/mediaan_prijs_per_genre.png")
    plt.close()
    return

mediaan_prijs_per_genre_weergeven()












