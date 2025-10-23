print("🚀 Démarrage du bot...")

import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import os
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True  # Ajout pour suivre les salons vocaux

bot = commands.Bot(command_prefix="!", intents=intents)

# 🔒 Blacklist des rôles et utilisateurs à ignorer pour le kick vocal
blacklist_roles = [1366128711786561747]  # ← Remplace par l'ID de ton rôle "Modérateur" par exemple

@bot.event
async def on_ready():
    print(f"🤖 Bot connecté en tant que {bot.user}")
    print("✅ Le bot est prêt et connecté !")

    # Envoie un message de présence dans un salon spécifique
    channel_id = 1369266741288636527  # ← Remplace avec l'ID de ton salon
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("🟢 **(Au boulot !)** Le bot est maintenant en ligne.")

@bot.event
async def on_member_join(member):
    try:
        print(f"➡️ Nouveau membre : {member}")
        channel = bot.get_channel(1365790616377757768)  # ← Remplace avec l'ID de ton salon

        # Télécharger l'avatar du nouveau membre
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

        # Texte de bienvenue
        draw_text_with_shadow(draw, (250, 50), f"Bienvenue {member.name} !", font_title)
        draw_text_with_shadow(draw, (250, 120), "Sur Les Mains Tendues ", font_small)

        # Envoyer l’image dans le salon
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

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and (before.channel != after.channel):
        await asyncio.sleep(300)  # 5 minutes

        # Vérifie que l'utilisateur est toujours dans le même salon
        if member.voice and member.voice.channel == after.channel:
            # Vérifie qu'il est seul
            if len(after.channel.members) == 1:
                # Vérifie qu'il n'a pas un rôle blacklisté
                if not any(role.id in blacklist_roles for role in member.roles):
                    try:
                        await member.move_to(None)  # Déconnexion du salon vocal
                        await member.send("👋 Tu as été retiré du salon vocal car tu y étais seul pendant 5 minutes.")
                        print(f"🔕 {member.name} déconnecté pour inactivité vocale.")
                    except Exception as e:
                        print(f"⚠️ Erreur lors de la déconnexion vocale : {e}")

# Lancer le bot
bot.run(os.environ['DISCORD_TOKEN'])
