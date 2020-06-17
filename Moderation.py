import discord
from discord.ext import commands
from discord import Member
import random

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''
        Greets the member when they join.
        '''
        GREETINGS = ['I don\'t even care about my boots, but I guess welcome or whatever {0.mention}'.format(member), 
                     'Come walk in this grass with me {0.mention}'.format(member),
                     'My friend told me to wait here, {0.mention} will you wait with me?'.format(member),
                     'Hi {0.mention}, my name\'s Jenna. How can I not help you today?'.format(member)]

        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(random.choice(GREETINGS))

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild
        if guild:
            path = 'chatlogs{}.txt'.format(guild.name)
            with open(path, 'a+') as f:
                print('{0.created_at} : {0.channel} : {0.author.name} : {0.content}'.format(message), file = f)

        if (message.mention_everyone) and (message.author.bot == False):
            await message.channel.send(message.author.mention + ' please refrain from using @ everyone')

    @commands.command()
    async def ping(self, ctx):
        '''
        Pong!
        '''
        await ctx.send('Pong!')

    @commands.command(name = 'recruit')
    @commands.has_role('Squad')
    async def assignToSquad(self, ctx, member):
        '''
        Assign non-mod role to people. Requires admin perms.
        '''
        role = discord.utils.get(member.guild.roles, name = 'Squad')
        await Member.add_roles(member, role)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, number = 10):
        '''
        Clears specified number of messages in a channel. Requires delete message perm.
        '''
        channel = ctx.channel
        msg = []
        async for i in channel.history(limit = number + 1):
            if len(i.attachments) == 0:
                msg.append(i)
        await channel.delete_messages(msg)

    @commands.command(name = 'allClear')
    @commands.has_permissions(manage_messages = True)
    async def all_clear(self, ctx, number = 10):
        '''
        Clears specified number of messages in a channel. Requires delete message perm.
        '''
        channel = ctx.message.channel
        msg = await channel.history(limit = number + 1).flatten()
        await channel.delete_messages(msg)

    @commands.command()
    async def streamingRole(self, ctx):
        '''
        Assigns "Streaming" role to the people who are streaming
        '''
        members = ctx.guild.members
        game = discord.Game(name = 'Visual Studio Code')
        for m in members:
            if m.activity == game:
                print(m.activity.name)
            print(m.activity.name)

    @commands.command(name = 'cr')
    @commands.has_role('Squad')
    async def createNonModRole(self, ctx , name: str, hoist: bool, mentionable: bool):
        '''
        Create a non mod role. The new role won't have any extra permissions.
        '''
        guild = ctx.guild
        await guild.create_role(name = name, hoist = hoist, mentionable = mentionable)
        await ctx.send('Role: {} created'.format(name))

    @commands.command(name = 'changeRegion')
    @commands.has_role('Squad')
    async def changeVoiceRegion(self, ctx, newRegion):
        '''
        Change the server's voice region. Use command 'regions' for valid regions.
        '''
        guild = ctx.guild
        try:
            await guild.edit(region = newRegion)
            await ctx.send('Changed server region to {}'.format(newRegion))
        except:
            await ctx.send('Invalid voice region, use \'regions\' to get a valid list of regions')

    @commands.command(name = 'regions')
    async def voiceRegions(self, ctx):
        await ctx.send('''amsterdam, brazil, eu-central, eu-west, frankfurt, hongkong, japan, 
                        london, russia, singapore, southafrica, sydney, us-central, us-east, 
                        us-south, us-west''')

def setup(bot):
    bot.add_cog(Moderation(bot))