print("🚀 Démarrage du bot...")

import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot connecté en tant que {bot.user}")
    print("✅ Le bot est prêt et connecté !")

@bot.event
async def on_member_join(member):
    try:
        print(f"➡️ Nouveau membre : {member}")
        channel = bot.get_channel(1365790616377757768)  # ← Remplace cet ID par celui de ton salon

        # Télécharger l'avatar
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.display_avatar.url)) as resp:
                avatar_bytes = await resp.read()

        # Charger l'image de fond
        background = Image.open("background.png").convert("RGBA")
        background = background.resize((800, 250))

        # Avatar en cercle
        avatar = Image.open(io.BytesIO(avatar_bytes)).resize((180, 180)).convert("RGBA")
        mask = Image.new("L", (180, 180), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 180, 180), fill=255)
        background.paste(avatar, (40, 35), mask)

        draw = ImageDraw.Draw(background)

        # Charger la police
        font_title = ImageFont.truetype("LilitaOne-Regular.ttf", 48)
        font_small = ImageFont.truetype("LilitaOne-Regular.ttf", 32)

        def draw_text_with_shadow(draw_obj, position, text, font, fill="white", shadow_color="black"):
            x, y = position
            draw_obj.text((x+2, y+2), text, font=font, fill=shadow_color)
            draw_obj.text((x, y), text, font=font, fill=fill)

        # Texte
        draw_text_with_shadow(draw, (250, 50), f"Bienvenue {member.name} !", font_title)
        draw_text_with_shadow(draw, (250, 120), f"Sur Les Mains Tendues !", font_small)

        # Envoyer l’image
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

# Lancer le bot avec ton token stocké dans une variable d'environnement
bot.run(os.environ['DISCORD_TOKEN'])
