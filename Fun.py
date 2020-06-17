import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send('It\'s ' + left + right)

    @commands.command()
    async def coinflip(self, ctx):
        """Flips a coin"""
        toss = ['Heads', 'Tails']
        await ctx.send('Its a {}'.format(random.choice(toss)))

    @commands.command(name = '8ball')
    async def eight_ball(self, ctx):
        """Gives an eight ball response to a question"""

        possible_responses = ['That is a resounding no',
                            'It is not looking likely',
                            'Too hard to tell',
                            'It is quite possible',
                            'Definitely','It is certain','Without a doubt',
                            'You may rely on it','As I see it, yes',
                            'Signs point to yes','Reply hazy, try again',
                            'Ask again later','Better not tell you now',
                            'Concentrate and ask again','Don\'t count on it',
                            'My reply is no','Never in your entire life',
                            'Ask the all mighty Pixel instead']

        await ctx.send(random.choice(possible_responses))

    @commands.command(name = 'capitalize')
    async def alternate_caps(self, ctx, message : str):
        result = ''
        for c in range(len(message)):
            letter = message[c]
            if((c % 2 == 0) and (letter != ' ')):
                result += letter.capitalize()
            else:
                result += letter

        await ctx.send(result)

def setup(bot):
    bot.add_cog(Fun(bot))