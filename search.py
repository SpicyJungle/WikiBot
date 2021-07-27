import discord
import random
import requests
import bs4

wikis = {
    "wp": "https://en.wikipedia.org/w/index.php?search=👲&title=Special:Search&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1",   
    "mc": "https://minecraft.gamepedia.com/Special:Search?search=👲&go=Go",
    "sot": "https://seaofthieves.fandom.com/wiki/Special:Search?search=👲&go=Go",
    "sdv": "https://stardewvalleywiki.com/mediawiki/index.php?search=👲&title=Special%3ASearch&profile=default&fulltext=1",
    "t": "https://terraria.fandom.com/wiki/Special:Search?search=👲&go=Go",
    "wiip": "https://wiisports.fandom.com/wiki/Special:Search?query=👲&scope=internal&navigationSearch=true",
}

wikiSearchResultClass = {
    "wp": "mw-search-result-heading",
    "mc": "unified-search__result__title",
    "sot": "unified-search__result__title",
    "sdv": "mw-search-result-heading",
    "t": "unified-search__result__title",
    "wiip": "unified-search__result__title"
}

wikiUrls = {
    "wp": "https://en.wikipedia.org/wiki/",
    "mc": "",
    "sot": "",
    "sdv": "https://stardewvalleywiki.com/",
    "t": "",
    "wiip": "",
}

wikiTitles = {
    "mc": "data-title",
    "wp": "title",
    "sot": "data-title",
    "sdv": "title",
    "t": "data-title",
    "wiip": "data-title",
}


async def search(wiki, args):

    wikiItem = ""
    for word in args: wikiItem += word
    wikiItem = wikiItem.replace(" ", '_')

    url = wikis[wiki].replace("👲", wikiItem)
    pageData = requests.get(url)
    cleanPageData = bs4.BeautifulSoup(pageData.text, 'html.parser')
    urls = []
    matches = cleanPageData.find_all(class_=wikiSearchResultClass[wiki])
    cleanMatches = []
    iterations = 0
    for match in matches:

        iterations += 1
        url = wikiUrls[wiki]
        if wiki == "wp" or wiki == "sdv":
            extractFromThis = match.contents[0]
        else: 
            extractFromThis = match
        text = f"[{extractFromThis.get(wikiTitles[wiki])}]({url+extractFromThis.get('href')})"
        urls.append(extractFromThis.get(wikiTitles[wiki]))
        cleanMatches.append(text)
        if iterations >= 20:
            break
    
    return [urls, cleanMatches]
