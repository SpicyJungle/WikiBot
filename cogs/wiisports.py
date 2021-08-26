from discord.ext import commands, tasks, menus
import discord
import bs4
import requests
import random
import utilities, search, checks
import Levenshtein
import json


class Wiisports(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="wiiparty", aliases=["wiip"])
    async def fetchWiiParty(self, ctx, *, args):
        embed = discord.Embed(title="Loading...", description="Please wait while I load the page...", color=successColor)
        msg = await ctx.send(embed=embed)


        wikiItem = ""
        for word in args: wikiItem += word
        wikiItem = wikiItem.title()
        wikiItem = wikiItem.replace(" ", '_')

        pageData = requests.get(f"https://wiisports.fandom.com/wiki/{wikiItem}")
        cleanPageData = bs4.BeautifulSoup(pageData.text, 'html.parser')

        paraTag = cleanPageData.find(class_="mw-parser-output")
        paragraphs = paraTag.find_all("p")

        irrelevantAlts = ["Button See Issues", "Desktop version", "Mobile version", "This page is protected from being edited by unregistered or new users.", "Desktop, Console, and Mobile versions"]
        foundRelevantImage = False
        imgSrc = cleanPageData.find_all("img")
        for image in imgSrc:
            try: 
                if image.get("alt") in irrelevantAlts or int(image.get("width")) < 48:
                    continue
                else:
                    foundRelevantImage = True
                    imgSrc = "" + image["src"]
            except TypeError:
                pass

        if not foundRelevantImage:
            imgSrc = None

        intro = ""
        for p in paragraphs:

            if p.parent.get("class") != ['mw-parser-output'] or p.get("class") == ["mw-empty-elt"]:
                continue

            else:
                for item in p.contents:
                    if type(item) == bs4.element.Tag:
                        if item.name == "i":
                            for obj in item.children:
                                text = checks.wiiPCheck(obj=obj)
                                intro+=text

                        text = checks.wiiPCheck(obj=item)
                        intro+=text
                    elif type(item) == bs4.NavigableString:
                        intro = intro + str(item)
                    else:
                        try:
                            if "nowrap" in item.get("class"): continue
                        except TypeError:
                            pass
                        intro = intro + utilities.genHyperLinks(item, "https://wiisports.fandom.com")
                break

        embed = discord.Embed(title=cleanPageData.title.contents[0], description=intro,
                            color=int(random.choice(colors), 16), url=f"https://wiisports.fandom.com/wiki/{wikiItem}")
        embed.set_image(url=imgSrc)
        await msg.edit(embed=embed)
    

def setup(bot):
    bot.add_cog(Wiisports(bot))
