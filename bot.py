print("🚀 Démarrage du bot...")

import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import os
from flask import Flask
import threading

# --- Serveur Flask minimal pour Render ---
app = Flask("")

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

keep_alive()
# ------------------------------------------

intents = discord.Intents.default()
intents.member
