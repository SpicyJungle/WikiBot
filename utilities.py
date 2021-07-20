import discord
import random
import bs4

colors = ["5dfdcb", "90d7ff", "ffb8d1", "2667FF", "F4D06F"]

def genpage0():
    page0 = discord.Embed(title="WikiBot Help Menu: Page 1, Supported Wikis", description="""
    <:terrariaTree:818161799421624352> [Terraria Gamepedia](https://terraria.gamepedia.com/) - Selection code: T
    <:SDVChicken:818197512795979776> [Stardew Valley Wiki](https://stardewvalleywiki.com/Stardew_Valley_Wiki) - Selection code: SDV
    <:MCGrassblock:818198637908983839> [Minecraft Gamepedia](https://minecraft.gamepedia.com/Minecraft_Wiki) - Selection code: MC
    <:WPlogo:818845968237330472>[Wikipedia](https://en.wikipedia.org/wiki/) - Selection code: WP
    <:SoTIcon:818966654163746896>[Sea Of Thieves](https://seaofthieves.gamepedia.com/) - Selection code: SOT
    
    **[Bot Invite link](https://bit.ly/3qtEunv) | [Support Server](https://discord.gg/Zvt4cesG)**
    """, color=int("2f3136", 16))
    page0.set_footer(text="Wiki suggestions? DM SpicyJungle#1111")
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
    page1.set_footer(text="Command suggestions? DM SpicyJungle#1111")
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
    page1.set_footer(text="Bug reports? DM SpicyJungle#1111")
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
            print(images[0].get("alt"))
            if images[0].parent.name == "td":
                print(True)
        except AttributeError:
            return None

    return finalProduct