import discord
import settings

def emoji_creation(result, difficulty):
    emojis = ''
    for x in result:
        if type(x) == int:
            if x >= difficulty:
                emojis += getattr(settings, ('g' + str(x)))
            if x <= difficulty:
                emojis += getattr(settings, ('r' + str(x)))
        elif type(x) == list:
            emojis += emoji_creation(x, difficulty)
    return emojis
