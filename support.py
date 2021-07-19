from discord.ext import commands, tasks, menus
import discord
import random

TKNS = [
    "ODMxMjc5MTUyMzc5ODU0OTI5.YHS7Cg.KO9pO7Lv_TzfpdjgOYdOlbzV8yI"
    ]
TOKEN = TKNS[0]

intents = discord.Intents.default()
intents.members = True
intents.typing = False

bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)
bot.remove_command("help")

colors = ["5dfdcb", "90d7ff", "ffb8d1", "2667FF", "F4D06F"]


@bot.event
async def on_member_join(member):
    embed = embed=discord.Embed(description=f"{member.mention} has joined!", color=int(random.choice(colors), 16))
    channel = bot.get_channel(817942017858207747)
    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    embed = embed=discord.Embed(description=f"{member.name} has left.", color=int(random.choice(colors), 16))
    channel = bot.get_channel(817942017858207747)
    await channel.send(embed=embed)


bot.run(TOKEN)