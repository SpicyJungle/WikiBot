from discord.ext import commands, tasks, menus
import discord
import utilities
import json
import os
from py_dotenv import read_dotenv

dotEnvPath = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotEnvPath)
TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')

intents = discord.Intents.default()
intents.members = True
intents.typing = False

bot = commands.Bot(command_prefix="wikib ", case_insensitive=True, intents=intents)
bot.remove_command("help")

colors = ["5dfdcb", "90d7ff", "ffb8d1", "2667FF", "F4D06F"]
successColor = int("a5ffa5", 16)
errorColor = int("ffa5a5", 16)

initial_extensions = ['cogs.wikis', 'cogs.logs']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print("WikiBot online!")
    for guild in bot.guilds:
        print(guild.name)
        print(guild.owner.name)


pagesDict = {
    "0": utilities.genpage0(),
    "1": utilities.genpage1(),
    "2": utilities.genpage2()
}


class HelpMenu(menus.Menu):

    def __init__(self):
        super().__init__()
        self.pageNum = 0


    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=utilities.genpage0())

    @menus.button('\N{BLACK LEFT-POINTING TRIANGLE}')
    async def on_thumbs_up(self, payload):
        await self.message.remove_reaction(emoji='\U000025c0', member=self.ctx.author)
        if self.pageNum == 0:
            return
        self.pageNum -= 1
        await self.message.edit(embed=pagesDict[str(self.pageNum)])

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        await self.message.edit(content="This menu has stopped and will not respond.")
        await self.message.remove_reaction(emoji='\U000023f9', member=self.ctx.author)
        self.stop()

    @menus.button('\N{BLACK RIGHT-POINTING TRIANGLE}')
    async def on_thumbs_down(self, payload):
        await self.message.remove_reaction(emoji='\U000025b6', member=self.ctx.author)
        if self.pageNum >= 3:
            return
        await self.message.edit(embed=pagesDict[str(self.pageNum)])
        self.pageNum += 1


@bot.command(name="help", aliases=["h"])
async def helpCMD(ctx):
    m = HelpMenu()
    await m.start(ctx)


@bot.command(aliases=["stats"])
async def botStats(ctx):
    embed=discord.Embed(title="WikiBot Statistics and information!", description=f"""
    Prefix: `wiki `
    Guilds: **{len(bot.guilds)}**
    Supported wikis: **6**
    Dev: **SpicyJungle#1111**

    **[Click to invite bot](https://bit.ly/3qtEunv) | [Click to join support server](https://discord.gg/Zvt4cesG)**
    """, color=int("2f3136", 16))
    embed.set_author(name="Bot stats & information", icon_url="https://cdn.discordapp.com/attachments/819322820177297408/863554216374698015/logoIter2.png")
    await ctx.send(embed=embed)


@bot.command(name="reload")
@commands.is_owner()
async def cogReload(ctx):
    for extension in initial_extensions:
        bot.unload_extension(extension)
    for extension in initial_extensions:
        bot.load_extension(extension)

    embed = discord.Embed(description=":arrows_counterclockwise: Cogs Reloaded!", color=successColor)
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original
    try: 
        if error.code == 50035:
            embed = discord.Embed(title="", description="The page's first paragraph exceeded discord's message length limit. The bot will resolve this issue in the future.", color=errorColor)
            await ctx.send(embed=embed)
            return
    except AttributeError:
        pass

    error = getattr(error, 'original', error)
    responses = {
        "'NoneType' object has no attribute 'find_all'": "Aye bruv that page ain't existing. \n \n Did you capitalise your search query correctly?"
    }

    try: embed = discord.Embed(title="", description=responses[str(error)], color=errorColor)
    except: embed = discord.Embed(title="", description=error, color=errorColor)
    embed.set_author(name="That page couldn't be fetched...")
    await ctx.send(embed=embed)

bot.run(TOKEN)

