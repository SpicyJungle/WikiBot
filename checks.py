# Checks.py

import utilities
import bs4

ignoredTags = ["s"]

def wiiPCheck(obj):

    intro = ""

    if type(obj) == bs4.element.Tag:
        if obj.has_attr("srcset"):
            pass
        elif obj.has_attr("href"):
            intro += utilities.genHyperLinks(obj, "https://wiisports.fandom.com")
            pass
        elif obj.name == "b":
            for finalThing in obj:
                if type(finalThing) == bs4.element.NavigableString:
                    intro += f"**{finalThing}**"
                elif type(finalThing) == bs4.element.Tag:
                    if finalThing.has_attr("href"):
                        intro += utilities.genHyperLinks(finalThing, "https://wiisports.fandom.com")
                        continue
    elif type(obj) == bs4.NavigableString:
        intro += str(obj)

    return intro


def terrariaSpanCheck(obj):
    intro = ""

    for item in obj:
        if type(item) == bs4.element.Tag:
            if item.name in ignoredTags:
                continue
        if type(item) == bs4.element.NavigableString:
            intro += item

    return intro


