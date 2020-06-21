import discord
import asyncio
from discord import Game
from discord.ext import commands

BOT_PREFIX = '?'
TOKEN = "ENTER YOUR TOKEN HERE"

bot = commands.Bot(command_prefix = BOT_PREFIX)

# TODO
# 1. Basic bot functions -- DONE
# 2. LFG and queueing for games
# 3. Overwatch stats for players -- DONE
# 6. Twitch notification
# 7. OWL notification -- DONE
# 8. Assign streaming role if streaming

@bot.event
async def on_ready():
    await bot.change_presence(activity = Game(name = 'with pink fluffy unicorns'))
    print('Logged in as ' + bot.user.name)

extensions = ['Moderation', 'OverwatchStuff', 'Fun']

if __name__ == '__main__':

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))
           
    bot.run(TOKEN)
