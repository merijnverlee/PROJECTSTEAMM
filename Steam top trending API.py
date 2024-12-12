import os
from steam_web_api import Steam

KEY = os.environ.get("steam_key")

steam = Steam(KEY)

user = steam.users.get_user_details("76561198995017863")
print(user['player']['personaname'])