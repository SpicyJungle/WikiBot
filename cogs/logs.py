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
        await logs.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        logs = self.bot.get_channel(863379605246312488)
        embed = discord.Embed(description=f'Left **{guild.name}** with {guild.member_count} members.',
         color=int("ffa5a5", 16),
         )
        embed.set_footer(text=f'I am now in {len(self.bot.guilds)} servers!')
        embed.set_author(name='I have been removed from a server', icon_url=guild.icon_url)
        await logs.send(embed=embed)
    

    @commands.Cog.listener()
    async def on_command(self, ctx):
        logs = self.bot.get_channel(863379605246312488)
        embed = discord.Embed(description=f'Command used: `{ctx.message.content}`',
         color=int("a5a5ff", 16),
         )
        embed.set_author(name=f'{ctx.author.name}', icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'In guild {ctx.guild.name}', icon_url=ctx.guild.icon_url)
        await logs.send(embed=embed)



def setup(bot):
    bot.add_cog(logCog(bot))