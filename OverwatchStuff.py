import discord
import requests
import random
from discord.ext import commands

class OverwatchStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = 'owlMatch')
    async def owlLiveMatch(self, ctx):
        '''
        Shows the stats for the live OWL match
        '''
        url = 'https://api.overwatchleague.com/live-match'
        response = requests.get(url)

        team_1 = response.json()['data']['liveMatch']['competitors'][0]['name']
        team_2 = response.json()['data']['liveMatch']['competitors'][1]['name']

        score_1 = response.json()['data']['liveMatch']['scores'][0]['value']
        score_2 = response.json()['data']['liveMatch']['scores'][1]['value']

        logo_1 = response.json()['data']['liveMatch']['competitors'][0]['icon']
        logo_2 = response.json()['data']['liveMatch']['competitors'][0]['icon']
        
        owlEmbed = discord.Embed(title = 'Live Match', 
                    description = 'Score of the current OWL match',
                    colour = discord.Colour.orange())

        owlEmbed.set_image(url = logo_1)
        owlEmbed.set_thumbnail(url = logo_2)
        owlEmbed.add_field(name = team_1 ,value = score_1, inline = True)
        owlEmbed.add_field(name = team_2 ,value = score_2, inline = True)

        await ctx.send(embed = owlEmbed)

    @commands.command(name = 'owlStandings', aliases = ['SpillTheTea'])
    async def owlStandings(self, ctx):
        '''
        Standings of all teams in OWL
        '''
        url = 'https://api.overwatchleague.com/standings'
        response = requests.get(url)
        scoreboard = discord.Embed(title = 'Scoreboard', value = '\u200b', 
                    colour = discord.Colour.orange(), description = 'Win - Loss - Draw - Diff')

        for i in range(20):
            team = response.json()['ranks']['content'][str(i)]
            teamName = team['competitor']['name']
            teamWon = team['records'][0]['matchWin']
            teamLost = team['records'][0]['matchLoss']
            teamDraw = team['records'][0]['matchDraw']
            teamDiff = team['records'][0]['gameWin'] - team['records'][0]['gameLoss']
            teamScore = (str(teamWon) + ' - ' + str(teamLost) + 
                        ' - ' + str(teamDraw) + ' - ' + str(teamDiff))
            scoreboard.add_field(name = str(i+1) + '. ' + teamName, value = teamScore, inline = False)

        await ctx.send(embed = scoreboard)

    @commands.command(name = "owlPlayer", aliases = ['owlplayer'])
    async def owlPlayerStats(self, ctx, name):
        '''
        OWL Player stats
        '''
        url = 'https://api.overwatchleague.com/players'
        response = requests.get(url)
        roster = response.json()['content']
        player = ''

        for i in range(len(roster)):
            tempName = roster[i]['name']
            if tempName.lower() == name.lower():
                player = roster[i]
                break
            else:
                continue

        playerName = player['givenName'] + ' ' + player['familyName']
        playerTeam = player['teams'][0]['team']['name']
        playerColour = int(player['teams'][0]['team']['primaryColor'], 16)
        playerRole = player['attributes']['role'].capitalize()
        playerHeroes = player['attributes']['heroes']
        playerHeroesStr = ', '.join(playerHeroes)
        playerLogo = player['teams'][0]['team']['logo']

        playerStats = discord.Embed(title = 'Stats', value = '\u200b', 
            color = discord.Color(playerColour))
            
        playerStats.add_field(name = 'Name', value = playerName)
        playerStats.add_field(name = 'Team', value = playerTeam)
        playerStats.add_field(name = 'Role', value = playerRole)
        playerStats.add_field(name = 'Mains', value = playerHeroesStr)
        playerStats.set_thumbnail(url = playerLogo)

        await ctx.send(embed = playerStats)

def setup(bot):
    bot.add_cog(OverwatchStuff(bot))