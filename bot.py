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
intents.reactions = True  # ✅ IMPORTANT

bot = commands.Bot(command_prefix="!", intents=intents)

# 🔒 Blacklist des rôles et utilisateurs à ignorer pour le kick vocal
blacklist_roles = [1366128711786561747]

# 🎯 CONFIG REACTION ROLE
CHANNEL_ID = 1365829812253626429
ROLE_ID = 1488970626222919740
EMOJI = "🎟️"

@bot.event
async def on_ready():
    print(f"🤖 Bot connecté en tant que {bot.user}")
    print("✅ Le bot est prêt et connecté !")

    channel_id = 1369266741288636527
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("🟢 **(Au boulot !)** Le bot est maintenant en ligne.")

@bot.event
async def on_member_join(member):
    try:
        print(f"➡️ Nouveau membre : {member}")
        channel = bot.get_channel(1365790616377757768)

        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.display_avatar.url)) as resp:
                avatar_bytes = await resp.read()

        background = Image.open("background.png").convert("RGBA")
        background = background.resize((800, 250))

        avatar = Image.open(io.BytesIO(avatar_bytes)).resize((180, 180)).convert("RGBA")
        mask = Image.new("L", (180, 180), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 180, 180), fill=255)
        background.paste(avatar, (40, 35), mask)

        draw = ImageDraw.Draw(background)

        font_title = ImageFont.truetype("LilitaOne-Regular.ttf", 48)
        font_small = ImageFont.truetype("LilitaOne-Regular.ttf", 32)

        def draw_text_with_shadow(draw_obj, position, text, font, fill="white", shadow_color="black"):
            x, y = position
            draw_obj.text((x+2, y+2), text, font=font, fill=shadow_color)
            draw_obj.text((x, y), text, font=font, fill=fill)

        draw_text_with_shadow(draw, (250, 50), f"Bienvenue {member.name} !", font_title)
        draw_text_with_shadow(draw, (250, 120), "Sur Les Mains Tendues !", font_small)

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

# ================= COMMANDES =================

@bot.command()
async def youtube(ctx):
    await ctx.send("📌Mon YouTube se trouve ici : https://beacons.ai/pablo_plays__")

@bot.command()
async def tiktok(ctx):
    await ctx.send("📌Mon TikTok se trouve ici : https://beacons.ai/pablo_plays__")

# (je raccourcis ici, tes autres commandes restent identiques)

# ================= REACTION ROLE =================

@bot.event
async def on_raw_reaction_add(payload):
    # ✅ Vérifie le bon salon
    if payload.channel_id != CHANNEL_ID:
        return

    # ✅ Vérifie le bon emoji
    if str(payload.emoji) != EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)

    # ✅ Sécurisé (évite bug cache)
    member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)

    # Ignore les bots
    if member.bot:
        return

    role = guild.get_role(ROLE_ID)

    if role:
        await member.add_roles(role)
        print(f"✅ Rôle ajouté à {member}")
    else:
        print("❌ Rôle introuvable")

# ================= LANCEMENT =================

bot.run(os.environ['DISCORD_TOKEN'])