from discord.ext import commands, tasks, menus
import discord
import bs4
import requests
import random
import time
import openpyxl as xl


TOKEN = "ODE3OTQxMzU5MDQxMzE0ODQ2.YEQ1QA.QZXgHYwvg_a8TNF_oeZKpFqK2Ok"


intents = discord.Intents.default()
intents.members = True
intents.typing = False

bot = commands.Bot(command_prefix="wiki ", case_insensitive=True, intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(guild.owner)

bot.run(TOKEN)

