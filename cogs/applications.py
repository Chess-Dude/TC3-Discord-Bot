from email.mime import application
import discord, datetime

from discord.ext import commands

class Applications(commands.Cog):


    def __init__(self, bot):
        self.bot = bot        
        self.matchStaffPing = '<@&935698898251567124> <@&896440653406433310>'
        self.thumbsUp = '\U0001F44D'
        self.thumbsDown = '\U0001f44e'

    
    def botsOrWorkChannel(ctx):
        return ctx.channel.id == 408820459279220736 or ctx.channel.id == 896440473659519057

    isBotsOrWorkChannel = commands.check(botsOrWorkChannel)

    def createInfoEmbed(infoMessage : discord.Message):

        embed = discord.Embed(description = infoMessage.content, color = 0xff0000)
        embed.add_field(name = '**Jump**', value = f'[Go to message!]({infoMessage.jump_url})')
        embed.set_footer(text = f'#{infoMessage.channel.name}')
        embed.timestamp = infoMessage.created_at
        embed.set_author(name = infoMessage.author.display_name, icon_url = infoMessage.author.avatar.url) 
        return embed

    @isBotsOrWorkChannel
    @commands.command(aliases = ["1v1app"])
    async def _1v1app(self, ctx, *, args = None):

        if args == None:
            _1v1info = discord.utils.get(ctx.guild.channels, id = 886952755367903233)
            infoMessage = await _1v1info.fetch_message(886969424463134730)

            embed = self.createInfoEmbed(infoMessage)
            await ctx.message.reply(content = "Missing information, please read:", embed = embed, mention_author = False)
            return

        tournamentApplications = discord.utils.get(ctx.guild.channels, id = 896444200432861237)
        
        logEmbed = discord.Embed(title = f"The Conquering Games 1v1 Application",description=f"**Application**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        logEmbed.timestamp = datetime.datetime.utcnow()
        msg = await tournamentApplications.send(self.matchStaffPing, embed = logEmbed)

        await msg.add_reaction(self.thumbsUp)
        await msg.add_reaction(self.thumbsDown)

        successEmbed = discord.Embed(title='Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your 1v1 application!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = False)



    @isBotsOrWorkChannel
    @commands.command(aliases = ["2v2app"])
    async def _2v2app(self, ctx, *, args = None):
        
        if args == None:
            _2v2info = discord.utils.get(ctx.guild.channels, id = 886962032753131560)
            infoMessage = await _2v2info.fetch_message(886971602141585508)
            
            embed = self.createInfoEmbed(infoMessage)
            await ctx.message.reply(content = "Missing information, please read:", embed = embed, mention_author = False)
            return

        tournamentApplications = discord.utils.get(ctx.guild.channels, id = 896444200432861237)
        
        logEmbed = discord.Embed(title = f"The Conquering Games 2v2 Application",description=f"**Application**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        logEmbed.timestamp = datetime.datetime.utcnow()
        msg = await tournamentApplications.send(self.matchStaffPing, embed = logEmbed)

        await msg.add_reaction(self.thumbsUp)
        await msg.add_reaction(self.thumbsDown)

        successEmbed = discord.Embed(title='Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your 2v2 application!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = False)


    @isBotsOrWorkChannel
    @commands.command()
    async def teamapp(self, ctx, *, args = None):

        if args == None:
            teaminfo = discord.utils.get(ctx.guild.channels, id = 886972024885481493)
            infoMessage = await teaminfo.fetch_message(886973611221598238)
            
            embed = self.createInfoEmbed(infoMessage)
            await ctx.message.reply(content = "Missing information, please read:", embed = embed, mention_author = False)
            return

        tournamentApplications = discord.utils.get(ctx.guild.channels, id = 896444200432861237)
        
        logEmbed = discord.Embed(title = f"The Conquering Games Team Application",description=f"**Application**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        logEmbed.timestamp = datetime.datetime.utcnow()
        msg = await tournamentApplications.send(self.matchStaffPing, embed = logEmbed)

        await msg.add_reaction(self.thumbsUp)
        await msg.add_reaction(self.thumbsDown)

        successEmbed = discord.Embed(title='Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your Team application!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = False)

def setup(bot):
    bot.add_cog(Applications(bot))
