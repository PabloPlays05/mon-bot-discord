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
intents.voice_states = True
intents.message_content = True

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
        draw_text_with_shadow(draw, (250, 120), "Sur Les Mains Tendues !", font_small)

        # Envoyer l’image dans le salon
        with io.BytesIO() as image_binary:
            background.save(image_binary, "PNG")
            image_binary.seek(0)
            if channel:
                await channel.send(
                    content=f"🎉 Bienvenue {member.mention} sur **{member.guild.name}** ",
                    file=discord.File(fp=image_binary, filename="welcome.png")
                )
                print("✅ Image envoyée !")
            else:
                print("❌ Salon introuvable")

    except Exception as e:
        print(f"💥 ERREUR : {e}")

# ================= COMMANDES PERSONNALISÉES =================

@bot.command()
async def youtube(ctx):
    await ctx.send("📌Mon YouTube se trouve ici : https://beacons.ai/pablo_plays__")

@bot.command()
async def tiktok(ctx):
    await ctx.send("📌Mon TikTok se trouve ici : https://beacons.ai/pablo_plays__")

@bot.command()
async def lanterne(ctx):
    await ctx.send("Le TikTok pour la lanterne🏮: https://vm.tiktok.com/ZNd64Wuoh/ ")

@bot.command()
async def cabestan(ctx):
    await ctx.send("Le TikTok pour le cabestan ⚓️: https://vm.tiktok.com/ZNdMRmBsf/")

@bot.command()
async def skin(ctx):
    await ctx.send("Le TikTok pour mon skin 🤡: https://vm.tiktok.com/ZNdkoMK9v/")

@bot.command()
async def doublons(ctx):
    await ctx.send("Le TikTok pour farm les doublons 🔵: https://vm.tiktok.com/ZNdjEsU7h/")

@bot.command()
async def tromblon(ctx):
    await ctx.send("Le TikTok pour le tromblon doré 🔫: https://vm.tiktok.com/ZNdMrH4Lr/")

@bot.command()
async def legende(ctx):
    await ctx.send("Tuto pour monter Pirate Légende 🩵: https://vm.tiktok.com/ZNdUTe492/")

@bot.command()
async def ancien(ctx):
    await ctx.send("Le TikTok pour l'opti des squel anciens 🧿: https://vm.tiktok.com/ZNd566mvy/")

@bot.command()
async def miles(ctx):
    await ctx.send("Le TikTok pour les miles 🗺️: https://vm.tiktok.com/ZNdBuRGuL/")

@bot.command()
async def coque(ctx):
    await ctx.send("Le TikTok pour la coque bleue ⛵️: https://vm.tiktok.com/ZNdaraq5q/")

@bot.command()
async def emissaire(ctx):
    await ctx.send("Le TikTok pour les avantages des émissaires 5 🚩: https://vm.tiktok.com/ZNdnKBg4Y/")

@bot.command()
async def rabais(ctx):
    await ctx.send("Le TikTok pour les rabais des SeaPosts 💰: https://vm.tiktok.com/ZNR181weQ/")

@bot.command()
async def blackscreen(ctx):
    await ctx.send("Le TikTok sur les blackscreen 🔳: https://vm.tiktok.com/ZNRL1vwQx/")

@bot.command()
async def capitaine(ctx):
    await ctx.send("Le TikTok pour l'opti capitaine 💀: https://vm.tiktok.com/ZNRjCK3wJ/")

@bot.command()
async def r4(ctx):
    await ctx.send("Le TikTok pour monter R4 en 1 minute 🚩: https://vm.tiktok.com/ZNRry1cVe/")

@bot.command()
async def lmt(ctx):
    await ctx.send("📌Le TikTok LMT se trouve ici : https://www.tiktok.com/@lesmainstendues")

@bot.command()
async def playstv(ctx):
    await ctx.send("📌Mon TikTok de clips se trouve ici : https://www.tiktok.com/@pabloplaystv")

@bot.command()
async def couteaux(ctx):
    await ctx.send("Le TikTok pour l'arme la plus opti en PVE 🔪: https://vm.tiktok.com/ZNRDWEEt8/")

@bot.command()
async def meg(ctx):
    await ctx.send("Le TikTok pour les megalodons 🦈 : https://vm.tiktok.com/ZNRUWm2un/")

# ================= Gestion musique attente =================

@bot.event
async def on_voice_state_update(member, before, after):
    try:
	ATTENTE_CHANNEL_ID = 1369367264587153488  # ← Remplace par l'ID de ton salon vocal "attente move"
	SALON_COMMANDE_ID = 1369266741288636527  # ← ID du salon texte privé où le bot musique écoute les commandes
	MUSIQUE_ATTENTE = "https://www.youtube.com/watch?v=bAVTn14kdyg"  # ← lien de la musique d'attente

        salon_commande = bot.get_channel(SALON_COMMANDE_ID)
        if not salon_commande:
            return

        # --- Quelqu'un rejoint le salon d'attente ---
        if (after.channel and after.channel.id == ATTENTE_CHANNEL_ID and (not before.channel or before.channel.id != ATTENTE_CHANNEL_ID)):
            print(f"➡️ {member} a rejoint le salon attente")
            await salon_commande.send(f"!play {MUSIQUE_ATTENTE}")

        # --- Quelqu'un quitte le salon d'attente ---
        if (before.channel and before.channel.id == ATTENTE_CHANNEL_ID):
            if len(before.channel.members) == 0:
                print("⏹️ Salon attente vide, !leave")
                await salon_commande.send("!leave")

    except Exception as e:
        print(f"💥 ERREUR voiceStateUpdate : {e}")

# ============================================================

# Lancer le bot
bot.run(os.environ['DISCORD_TOKEN'])