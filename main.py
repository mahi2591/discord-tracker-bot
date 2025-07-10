import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# 🔑 Your bot token here
import os
TOKEN = os.getenv("TOKEN")


# 🎯 IDs to track
TRACKED_USER_IDS = [
    1377990591656366110,  # Target Bot
    735623291989131336    # You
]

# 💬 Channel ID to send messages in
CHANNEL_ID = 1392740406554525706

# ✅ Enable necessary intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.guilds = True

# 🤖 Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_presence_update(before, after):
    if after.id in TRACKED_USER_IDS:
        print(f"🔍 {after.name}: {before.status} → {after.status}")
        channel = bot.get_channel(CHANNEL_ID)

        # 🟢 Online notification
        if before.status != discord.Status.online and after.status == discord.Status.online:
            if channel:
                await channel.send(f"🟢 <@{after.id}> is now **online!**")

        # 🔴 Offline notification
        elif before.status != discord.Status.offline and after.status == discord.Status.offline:
            if channel:
                await channel.send(f"🔴 <@{after.id}> just went **offline!**")

# 🌐 Keep-alive web server for Replit
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# 🚀 Start bot
bot.run(TOKEN)
