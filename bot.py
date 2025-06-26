from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
    
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot connecté en tant que {bot.user}")

@bot.event
async def on_member_join(member):
    try:
        print(f"➡️ Nouveau membre : {member}")
        channel = bot.get_channel(1365790616377757768)

        # Télécharger l'avatar
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.display_avatar.url)) as resp:
                avatar_bytes = await resp.read()

        # Image de fond
        background = Image.open("attached_assets/background_1750859627652.png").convert("RGBA")
        background = background.resize((800, 250))

        # Avatar en cercle
        avatar = Image.open(io.BytesIO(avatar_bytes)).resize((180, 180)).convert("RGBA")
        mask = Image.new("L", (180, 180), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 180, 180), fill=255)
        background.paste(avatar, (40, 35), mask)

        draw = ImageDraw.Draw(background)

        # Charger la police (ou fallback)
        def get_font(size):
            try:
                # Utiliser Lilita One
                font = ImageFont.truetype("attached_assets/LilitaOne-Regular_1750861385675.ttf", size)
                return font
            except:
                try:
                    # Fallback vers Arial Bold si disponible
                    return ImageFont.truetype("arialbd.ttf", size)
                except:
                    try:
                        return ImageFont.truetype("arial.ttf", size)
                    except:
                        return ImageFont.load_default()

        font_title = get_font(38)   # Texte principal encore plus petit
        font_small = get_font(26)   # Sous-texte encore plus petit

        # Texte avec ombre douce et estompée
        def draw_text_with_shadow(draw_obj, position, text, font, fill="white", shadow_color=(0, 0, 0, 120)):
            x, y = position
            shadow_offset = 2
            # Ombre plus transparente et décalage plus petit
            draw_obj.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=shadow_color)
            draw_obj.text((x, y), text, font=font, fill=fill)

        draw_text_with_shadow(draw, (250, 50), f"Bienvenue {member.name} !", font_title)
        draw_text_with_shadow(draw, (250, 130), "Sur Les Mains Tendues !", font_small)

        # Envoie l'image
        with io.BytesIO() as image_binary:
            background.save(image_binary, "PNG")
            image_binary.seek(0)

            if channel:
                await channel.send(
                    content=f"🎉 Bienvenue {member.mention} sur **{member.guild.name}** !",
                    file=discord.File(fp=image_binary, filename="welcome.png")
                )
                print("✅ Image envoyée !")
            else:
                print("❌ Salon introuvable")

    except Exception as e:
        print(f"💥 ERREUR : {e}")

keep_alive()

import os

bot.run(os.environ['DISCORD_TOKEN'])