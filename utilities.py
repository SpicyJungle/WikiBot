import discord
import random
import bs4
import json

colors = ["5dfdcb", "90d7ff", "ffb8d1", "2667FF", "F4D06F"]

def fetchUserName():
    with open('info.json', 'r+') as f:
        data = json.load(f)
        return data['userName']





def genpage0():



    page0 = discord.Embed(title="WikiBot Help Menu: Page 1, Supported Wikis", description="""
    <:terrariaTree:818161799421624352> [Terraria Gamepedia](https://terraria.gamepedia.com/) - Selection code: T
    <:SDVChicken:818197512795979776> [Stardew Valley Wiki](https://stardewvalleywiki.com/Stardew_Valley_Wiki) - Selection code: SDV
    <:MCGrassblock:818198637908983839> [Minecraft Gamepedia](https://minecraft.gamepedia.com/Minecraft_Wiki) - Selection code: MC
    <:WPlogo:818845968237330472>[Wikipedia](https://en.wikipedia.org/wiki/) - Selection code: WP
    <:SoTIcon:818966654163746896>[Sea Of Thieves](https://seaofthieves.gamepedia.com/) - Selection code: SOT
    
    **[Bot Invite link](https://bit.ly/3qtEunv) | [Support Server](https://discord.gg/Zvt4cesG)**
    """, color=int("2f3136", 16))
    page0.set_footer(text=f"Wiki suggestions? DM {fetchUserName()}")
    return page0


def genpage1():
    page1 = discord.Embed(title="WikiBot Help Menu: Page 2, How to use", description="""
    To use this bot, you simply enter the command `wiki [wiki code] [topic]`.
    `wiki` is which wiki you want to search - The selection code you want
    to use is specified on page 1. The `topic` is what you want to search
    the wiki for. An example of using this would be `wiki t slime`, to 
    search the Terraria Gamepedia for information on `slime`.

    **[Bot Invite link](https://bit.ly/3qtEunv) | [Support Server](https://discord.gg/Zvt4cesG)**
    """, color=int("2f3136", 16))
    page1.set_footer(text=f"Command suggestions? DM {fetchUserName()}")
    return page1


def genpage2():
    page1 = discord.Embed(title="WikiBot Help Menu: Page 3, How to use the search function", description="""
    Using the search function is fairly similar to how you'd search 
    normally. Start off by doing `wiki search [wiki code] [keyword]`. 
    The bot will return a list of these topics, and the next step
    is to pick the one you want. To do so, reply with a number and
    it will fetch that page! It's important to write **nothing but 
    the number** in the message. No dots, no nothing. The timeout
    expires in 30 seconds from the list being sent.

    **[Bot Invite link](https://bit.ly/3qtEunv) | [Support Server](https://discord.gg/Zvt4cesG)**
    """, color=int("2f3136", 16))
    page1.set_footer(text=f"Bug reports? DM {fetchUserName()}")
    return page1


def genHyperLinks(item, url):
    try:
        if item.string.startswith('[') and item.string.endswith(']') and len(item.string) <= 4:
            return ""
    except AttributeError:
        return f"{item}"
    try:
        if item.get('href') == None:
            string = f"{item.string}"
        else:
            string = f"[{str(item.string)}]({url}{item.get('href')})"
    except AttributeError:
        string = item
    return string


def findBestImage(pageData, wiki):
    if wiki == "sdv":
        try:
            infoBox = pageData.find(id="infoboxtable")
            images = infoBox.find_all("img")
            finalProduct = images[0]
            if images[0].parent.name == "td":
                print(True)
        except AttributeError:
            return None

    return finalProduct


def findImage(srcs, wiki):

    defaultImages = {
            "wp": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/128px-Wikipedia-logo-v2.svg.png",
            "mc": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/90/Minecraft_Wiki_header.svg/revision/latest/scale-to-width-down/300?cb=20200525174016",
            "sot": "https://static.wikia.nocookie.net/seaofthieves_gamepedia/images/7/76/WikiWhite.png/revision/latest/scale-to-width-down/350?cb=20170927135347",  
            "sdv": "https://stardewvalleywiki.com/mediawiki/images/6/68/Main_Logo.png",
            "t": "https://static.wikia.nocookie.net/terraria_gamepedia/images/e/e6/Site-logo.png/revision/latest?cb=20210601122638",
            "wiip": "https://static.wikia.nocookie.net/w__/images/2/27/GB_Wii_WiiSports%281%29.jpg/revision/latest/scale-to-width-down/650?cb=20090524182626&path-prefix=wiisports",

            "wikipedia": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/128px-Wikipedia-logo-v2.svg.png",
            "minecraft": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/90/Minecraft_Wiki_header.svg/revision/latest/scale-to-width-down/300?cb=20200525174016",
            "seaofthieves": "https://static.wikia.nocookie.net/seaofthieves_gamepedia/images/7/76/WikiWhite.png/revision/latest/scale-to-width-down/350?cb=20170927135347",
            "stardewvalley": "https://stardewvalleywiki.com/mediawiki/images/6/68/Main_Logo.png",
            "terraria": "https://static.wikia.nocookie.net/terraria_gamepedia/images/e/e6/Site-logo.png/revision/latest?cb=20210601122638",
            "wiiparty":    "https://static.wikia.nocookie.net/w__/images/2/27/GB_Wii_WiiSports%281%29.jpg/revision/latest/scale-to-width-down/650?cb=20090524182626&path-prefix=wiisports"
    }


    irrelevantAlts = ["Button See Issues", "Desktop version", "Mobile version", "This page is protected from being edited by unregistered or new users.", "Desktop, Console, and Mobile versions"]
    foundRelevant = False
    imgSrc = ""
    for image in srcs:
        try:
            if image.get("src").startswith("http") or wiki in ["wikipedia"]:
                if int(image.get('width')) > 48 and int(image.get('width')) != 88:
                    if not image.get("alt") in irrelevantAlts:
                        foundRelevant = True
                        if wiki in ["wikipedia"]:
                            imgSrc = "https:"

                        imgSrc += image["src"]
        except:
            pass
        
    if not foundRelevant:
        imgSrc = defaultImages[wiki]
    
    return imgSrc