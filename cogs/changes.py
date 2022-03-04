import discord, datetime

from discord.ext import commands

def botsOrWorkChannel(ctx):
    return ctx.channel.id == 408820459279220736 or ctx.channel.id == 896440473659519057

isBotsOrWorkChannel = commands.check(botsOrWorkChannel)

matchStaffPing = '<@&935698898251567124> <@&896440653406433310>'
thumbsUp = '\U0001F44D'
thumbsDown = '\U0001f44e'

class Changes(commands.Cog):


    def __init__(self, bot):
        self.bot = bot


    # @isBotsOrWorkChannel    
    # @commands.command(aliases = ["1v1change"])
    # async def _1v1change(self, ctx, *, args):

    #     tournamentChanges = discord.utils.get(ctx.guild.channels, id = 896479412617359361)

    #     logEmbed = discord.Embed(title = f"The Conquering Games 1v1 Change",description=f"**Change**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
    #     logEmbed.timestamp = datetime.datetime.utcnow()
    #     msg = await tournamentChanges.send(matchStaffPing, embed = logEmbed)

    #     await msg.add_reaction(thumbsUp)
    #     await msg.add_reaction(thumbsDown)
        
    #     successEmbed = discord.Embed(title='Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your 1v1 change!", color=0xff0000)
    #     await ctx.message.reply(embed = successEmbed, mention_author = False)


    @isBotsOrWorkChannel
    @commands.command(aliases = ["2v2change"])
    async def _2v2change(self, ctx, *, args):

        tournamentChanges = discord.utils.get(ctx.guild.channels, id = 896479412617359361)

        logEmbed = discord.Embed(title = f"The Conquering Games 2v2 Change",description=f"**Change**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        logEmbed.timestamp = datetime.datetime.utcnow()
        msg = await tournamentChanges.send(matchStaffPing, embed = logEmbed)

        await msg.add_reaction(thumbsUp)
        await msg.add_reaction(thumbsDown)
        
        successEmbed = discord.Embed(title='Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your 2v2 change!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = False)


    @isBotsOrWorkChannel
    @commands.command()
    async def teamchange(self, ctx, *, args):

        tournamentChanges = discord.utils.get(ctx.guild.channels, id = 896479412617359361)

        logEmbed = discord.Embed(title = f"The Conquering Games Team Change",description=f"**Change**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        logEmbed.timestamp = datetime.datetime.utcnow()
        msg = await tournamentChanges.send(matchStaffPing, embed = logEmbed)

        await msg.add_reaction(thumbsUp)
        await msg.add_reaction(thumbsDown)
        
        successEmbed = discord.Embed(title='Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your team change!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = False)


def setup(bot):
    bot.add_cog(Changes(bot))
