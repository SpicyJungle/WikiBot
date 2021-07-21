from discord.ext import commands, tasks, menus
import discord
import bs4
import requests
import random
import utilities, search, checks
import Levenshtein
import json

colors = ["5dfdcb", "90d7ff", "ffb8d1", "2667FF", "F4D06F"]
successColor = int("a5ffa5", 16)
errorColor = int("ffa5a5", 16)
nsfwKeywords = [
    "cock", "vagina", "porn", "nude", "sex", "testicle", "breast", "penis", "anus", "anal", "sexual", "kink", "horny", "dick", "cock", "pornography", "masturbate", "orgasm", "tits"
    ]

class WikiCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="terraria", aliases=['t'])
    async def fetchTerrariaWiki(self, ctx, *, args):
        embed = discord.Embed(title="Loading...", description="Please wait while I load the page...", color=successColor)
        msg = await ctx.send(embed=embed)

        wikiItem = ""
        for word in args: wikiItem += word
        wikiItem = wikiItem.replace(" ", '_')

        pageData = requests.get(f"https://terraria.gamepedia.com/{wikiItem}")
        cleanPageData = bs4.BeautifulSoup(pageData.text, 'html.parser')

        paraTag = cleanPageData.find(class_="mw-parser-output")
        paragraphs = paraTag.find_all("p")

        irrelevantAlts = ["Rarity level: " ,"Switch version", "Xbox One", "PS4", "Desktop, Console, Old-gen console, and Mobile versions", "CC BY-NC-SA 3.0", "Powered by MediaWiki", "Button See Issues", "Desktop version", "Mobile version", "This page is protected from being edited by unregistered or new users.", "Desktop, Console, and Mobile versions"]
        allDecentImages = []
        mostRelevant = None
        highestRelevancy = 100
        imgSrc = paraTag.find_all("img")
        
        '''
        for image in imgSrc:
            if image.get("alt") in irrelevantAlts: continue
            relevancy = Levenshtein.distance(str(image.get("alt")), str(cleanPageData.title.contents[0].replace(" - The Official Terraria Wiki", "")))
            if relevancy < 5:
                allDecentImages.append(image)

            if relevancy < highestRelevancy:
                mostRelevant = image
                highestRelevancy = relevancy

        if len(allDecentImages) == 0:
            chosenImage = mostRelevant
        else:
            chosenImage = random.choice(allDecentImages)
        imgSrc = "" + chosenImage["src"]
        '''

        imgSrc = imgSrc[0]["src"]
        intro = ""
        for p in paragraphs:

            if p.parent["class"] != ['mw-parser-output']:
                continue

            else:
                for tag in p.children:
                    if tag.name == "big":
                        continue 

                for item in p.contents:
                    if type(item) == bs4.NavigableString:
                        intro = intro + str(item)
                    else:
                        
                        if item.get("class") == ["eil"]:
                            thingToBeAdded = ""
                            for thing in item:

                                if thing.name == "a":
                                    thingToBeAdded += utilities.genHyperLinks(thing, "https://terraria.gamepedia.com")
                                elif thing.name == "span" and thing.get("class") == ["eico"]:
                                    continue

                            intro += thingToBeAdded
                            continue
                        

                        try:
                            if item.get("class")[0] == "eico":
                                continue
                        except TypeError:
                            pass
                        intro += utilities.genHyperLinks(item, "https://terraria.gamepedia.com")
                break

        embed = discord.Embed(title=cleanPageData.title.contents[0], description=intro,
                            color=int(random.choice(colors), 16), url=f"https://terraria.gamepedia.com/{wikiItem}")
        embed.set_image(url=imgSrc)
        await msg.edit(embed=embed)

    @commands.command(name='minecraft', aliases=['mc'])
    async def fetchMinecraftWiki(self, ctx, *, args):
        embed = discord.Embed(title="Loading...", description="Please wait while I load the page...", color=successColor)
        msg = await ctx.send(embed=embed)

        wikiItem = ""
        for word in args: wikiItem += word
        wikiItem = wikiItem.replace(" ", '_')

        pageData = requests.get(f"https://minecraft.fandom.com/{wikiItem}")
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
            except:
                pass
            
        if not foundRelevantImage:
            imgSrc = None

        intro = ""
        for p in paragraphs:

            if p.parent.get("class") != ['mw-parser-output']:
                continue

            else:
                isBig = False
                for tag in p.children:
                    if tag.name == "big":
                        isBig = True

                if isBig: continue

                for item in p.contents:
                    if type(item) == bs4.NavigableString:
                        intro = intro + str(item)
                    else:
                        try:
                            if "nowrap" in item.get("class"): continue
                        except TypeError:
                            pass
                        intro = intro + utilities.genHyperLinks(item, "https://minecraft.fandom.com")

                break

        embed = discord.Embed(title=cleanPageData.title.contents[0], description=intro,
                            color=int(random.choice(colors), 16), url=f"https://minecraft.fandom.com/{wikiItem}")
        embed.set_image(url=imgSrc)
        await msg.edit(embed=embed)

    @commands.command(name='sdv', aliases=["stardewvalley"])
    async def fetchSdvWiki(self, ctx, *, args):
        embed = discord.Embed(title="Loading...", description="Please wait while I load the page...", color=successColor)
        msg = await ctx.send(embed=embed)


        wikiItem = ""
        for word in args: wikiItem += word
        wikiItem = wikiItem.replace(" ", '_')

        pageData = requests.get(f"https://stardewvalleywiki.com/{wikiItem}")
        cleanPageData = bs4.BeautifulSoup(pageData.text, 'html.parser')

        paraTag = cleanPageData.find(class_="mw-parser-output")
        paragraphs = paraTag.find_all("p")

        irrelevantAlts = ["Gold.png", "Map.png", "Map", "Maplocation", "Jinxed", "Powered by MediaWiki", "Creative Commons Attribution-NonCommercial-ShareAlike"]
        allDecent = []
        mostRelevant = None
        highestRelevancy = 100

        bestImage = utilities.findBestImage(cleanPageData, "sdv")
        if not bestImage:

            imgSrc = paraTag.find_all("img")
            for image in imgSrc:
                if image.get("alt") in irrelevantAlts: continue
                if image.parent.get("class") == ["nametemplate"]: continue
                relevancy = Levenshtein.distance(str(image.get("alt")), str(cleanPageData.title.contents[0].replace(" - Stardew Valley Wiki", "")))
                if relevancy < 5:
                    if len(image.get("alt")) == 0: continue 
                    allDecent.append(image)
                if relevancy < highestRelevancy:
                    if len(image.get("alt")) == 0: continue 
                    mostRelevant = image
                    highestRelevancy = relevancy


            if len(allDecent) == 0:
                chosenImage = mostRelevant
            else:
                chosenImage = random.choice(allDecent)
            imgSrc = "https://stardewvalleywiki.com" + chosenImage["src"]

        else: imgSrc = "https://stardewvalleywiki.com" + bestImage["src"]


        intro = ""
        for p in paragraphs:

            if p.parent.get("class") != ['mw-parser-output']:
                continue

            else:
                for tag in p.children:
                    if tag.name == "big":
                        continue

                for item in p.contents:
                    
                    skip = False
                    if type(item) == bs4.element.Tag:
                        if item.has_attr("style") or item.get("class") == ["no-wrap"]:
                            skip = True
                            for obj in item.children:
                                if type(obj) == bs4.element.Tag:
                                    if obj.has_attr("srcset"):
                                        continue
                                    elif obj.has_attr("href"):
                                        intro += utilities.genHyperLinks(obj, "https://stardewvalleywiki.com")
                                elif type(obj) == bs4.NavigableString:
                                    intro += str(obj)


                    if type(item) == bs4.NavigableString:
                        intro = intro + str(item)
                    elif skip or item.has_attr("srcset"):
                        continue
                    else:
                        intro += utilities.genHyperLinks(item, "https://stardewvalleywiki.com")

                break

        embed = discord.Embed(title=cleanPageData.title.contents[0], description=intro,
                            color=int(random.choice(colors), 16), url=f"https://stardewvalleywiki.com/{wikiItem}")
        embed.set_image(url=imgSrc)
        await msg.edit(embed=embed)

    @commands.command(name='wikipedia', aliases=["wp"])
    async def fetchWikipedia(self, ctx, *, args):
        embed = discord.Embed(title="Loading...", description="Please wait while I load the page...", color=successColor)
        msg = await ctx.send(embed=embed)

        wikiItem = ""
        for word in args: wikiItem += word
        wikiItem = wikiItem.replace(" ", '_')

        pageData = requests.get(f"https://en.wikipedia.org/wiki/{wikiItem}")
        cleanPageData = bs4.BeautifulSoup(pageData.text, 'html.parser')

        paraTag = cleanPageData.find(class_="mw-parser-output")
        paragraphs = paraTag.find_all("p")

        imgSrc = paraTag.find("img")
        imgSrc = "https://en.wikipedia.org/wiki/" + imgSrc["src"]

        intro = ""
        for p in paragraphs:

            if p.parent.get("class") != ['mw-parser-output'] or p.contents == ['\n']:
                continue
            if p.find("span", {"id": "coordinates"}):
                continue
            else:
                
                parserOutput = p.parent
                '''
                if " refer to:" in str(list(p.descendants)[-1]):
                    unorderedLists = parserOutput.find_all("ul")
                    for ulist in unorderedLists:
                        try:
                            title = list(ulist.previous_sibling.descendants)[0].string
                        except AttributeError as es: 
                            print(ulist.previous_sibling)
                            print(es)
                            continue
                        listItems = ""
                        for li in ulist.descendants:
                            listItems+= f"\n {li.string}"
                        await ctx.send(f"{title}, {listItems}")
                    return
                '''

                for tag in p.children:
                    if tag.name == "big":
                        continue

                for item in p.contents:
                    
                    try:
                        if "rt-commentedText" in item.get("class"):
                            pronounciation = ""
                            pronounciationSpan = item.find("span", {"style": "border-bottom:1px dotted"})
                            for IPASpan in pronounciationSpan: # Iterate over the IPA-key-spans in the formatting span
                                pronounciation += IPASpan.string
                            intro += pronounciation
                            continue
                    except (TypeError, AttributeError) as es:
                        pass
                    
                    

                    if type(item) == bs4.NavigableString:
                        intro = intro + str(item)
                    elif item.string != None: # Check if the tag is "Useless"
                        intro = intro + utilities.genHyperLinks(item, "https://en.wikipedia.org")
                break

        nsfw = False
        for word in nsfwKeywords:
            if word in cleanPageData.title.contents[0]:
                nsfw = True
            else: continue
        
        if nsfw:
            if ctx.channel.is_nsfw():
                embed = discord.Embed(title=cleanPageData.title.contents[0], description=intro,
                                    color=int(random.choice(colors), 16), url=f"https://en.wikipedia.org/wiki/{wikiItem}")
                embed.set_image(url=imgSrc)
                await msg.edit(embed=embed)
                return
            else:
                embed = discord.Embed(description="This page looks like it is NSFW... Please be in a NSFW channel!",
                                    color=int(random.choice(colors), 16))            
                await msg.edit(embed=embed)
                return

        embed = discord.Embed(title=cleanPageData.title.contents[0], description=intro,
                            color=int(random.choice(colors), 16), url=f"https://en.wikipedia.org/wiki/{wikiItem}")
        embed.set_image(url=imgSrc)
        await msg.edit(embed=embed)



    @commands.command(name="seaofthieves", aliases=['sot'])
    async def fetchSeaOfThieves(self, ctx, *, args):
        embed = discord.Embed(title="Loading...", description="Please wait while I load the page...", color=successColor)
        msg = await ctx.send(embed=embed)

        wikiItem = ""
        for word in args: wikiItem += word
        wikiItem = wikiItem.replace(" ", '_')
        
        pageData = requests.get(f"https://seaofthieves.gamepedia.com/{wikiItem}")
        cleanPageData = bs4.BeautifulSoup(pageData.text, 'html.parser')

        paraTag = cleanPageData.find(class_="mw-parser-output")    
        paragraphs = paraTag.find_all("p")

        imgSrc = paraTag.find("img")["src"]

        intro = ""
        for p in paragraphs:

            
            if p.parent.get("class") != ['mw-parser-output'] or p.contents == ['\n']:
                continue

            else:
                for tag in p.children:
                    if tag.name == "big":
                        continue


                for item in p.contents:
                    if type(item) == bs4.NavigableString:
                        intro = intro + str(item)
                    else:
                        intro = intro + utilities.genHyperLinks(item, "https://seaofthieves.gamepedia.com")
                break

        embed = discord.Embed(title=cleanPageData.title.contents[0], description=intro,
                            color=int(random.choice(colors), 16), url=f"https://seaofthieves.gamepedia.com/{wikiItem}")
        embed.set_image(url=imgSrc)
        await msg.edit(embed=embed)
    

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
                print("Image had no width")

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
        

    @commands.command(name="search", aliases=["s"])
    async def searchWikis(self, ctx, wiki, *args):
        
        wiki = wiki.lower()
        
        def searchNumberCheck(m): #Check if message is a valid number.
            if m.author == ctx.author:
                if len(m.content) <= 2:
                    try:
                        int(m.content)
                        return True
                    except ValueError:
                        return False

            return False
                        

        wikiItem = ""
        for word in args: wikiItem += word+" "
        
        searching = await search.search(wiki=wiki, args=args)
        links = searching[0]
        texts = searching[1]

        desc = ""
        loops = 0
        for item in texts:
            loops += 1
            desc += f"\n `{loops}.` {item}"

        if len(links) == 0:

            embed = discord.Embed(description="No search results found.", color=errorColor)
            await ctx.send(embed=embed)
            return 
            
        embed=discord.Embed(title="Results fetched!", description=f"{desc}", color=int(random.choice(colors), 16))
        embed.set_author(name=f"Search results for {wikiItem}", icon_url="https://cdn.discordapp.com/attachments/819322820177297408/819322964435795989/wikiIcon.png")
        embed.set_footer(text=f"Reply with a number (excluding the .) within 30 seconds to go to that page!")
        await ctx.send(embed=embed)
        msg = await self.bot.wait_for("message",  check=searchNumberCheck, timeout=30)
        thisLink = links[int(msg.content)-1]
        

        if wiki == "wp" or wiki == "wikipedia":
            await self.fetchWikipedia(ctx=ctx, args=thisLink)
        elif wiki == "mc" or wiki == "minecraft":
            await self.fetchMinecraftWiki(ctx=ctx, args=thisLink)
        elif wiki == "sot" or wiki == "seaofthieves":
            await self.fetchSeaOfThieves(ctx=ctx, args=thisLink)
        elif wiki == "sdv" or wiki == "stardewvalley":
            await self.fetchSdvWiki(ctx=ctx, args=thisLink)
        elif wiki == "t" or wiki == "terraria":
            await self.fetchTerrariaWiki(ctx, args=thisLink)
        elif wiki == "wiip" or wiki == "wiiparty":
            await self.fetchWiiParty(ctx, args=thisLink)      

def setup(bot):
    bot.add_cog(WikiCog(bot))