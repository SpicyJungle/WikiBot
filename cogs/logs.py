import discord
from discord.embeds import Embed
from discord.ext import commands
from datetime import datetime

class logCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logs = self.bot.get_channel(863379605246312488)
        embed = discord.Embed(description=f'Joined **{guild.name}** with {guild.member_count} members.',
         color=int("a5ffa5", 16),
         )
        embed.set_footer(text=f'I am now in {len(self.bot.guilds)} servers!')
        embed.set_author(name='I have joined a new server!', icon_url=guild.icon_url)
        embed.time
        await logs.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        logs = self.bot.get_channel(863379605246312488)
        embed = discord.Embed(description=f'Left **{guild.name}** with {guild.member_count} members.',
         color=int("ffa5a5", 16),
         )
        embed.set_footer(text=f'I am now in {len(self.bot.guilds)} servers!')
        embed.set_author(name='I have been removed from a server', icon_url=guild.icon_url)
        embed.time
        await logs.send(embed=embed)
        
def setup(bot):
    bot.add_cog(logCog(bot))