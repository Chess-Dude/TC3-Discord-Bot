import discord, datetime
from discord import ui
from discord.ext import commands
from discord import Embed

class TCGClans(commands.Cog):
     
    def __init__(self, bot):
        self.bot = bot
        self.matchStaffPing = '<@&935698898251567124> <@&896440653406433310>'
        self.thumbsUp = '\U0001F44D'
        self.thumbsDown = '\U0001f44e'
        
    def WorkChannel(ctx):
        return ctx.channel.id == 896440473659519057 or ctx.channel.id == 941567353672589322

    def bots(ctx):
        return ctx.channel.id == 408820459279220736 or ctx.channel.id == 896440473659519057 or ctx.channel.id == 941567353672589322
    
    def createInfoEmbed(self, infoMessage : discord.Message):
        embed = discord.Embed(description = infoMessage.content, color = 0xff0000)
        embed.add_field(name = '**Jump**', value = f'[Go to message!]({infoMessage.jump_url})')
        embed.set_footer(text = f'#{infoMessage.channel.name}')
        embed.timestamp = infoMessage.created_at
        embed.set_author(name = infoMessage.author.display_name, icon_url = infoMessage.author.avatar.url) 
        return embed
    
    isWorkChannel = commands.check(WorkChannel) 
    isBotsChannel = commands.check(bots)   
    
    @isWorkChannel
    @commands.command(aliases = ["c"])
    async def calculate(self, ctx, operation, *nums):
        
        if operation not in ['+', '-', '*', '/']:
            await ctx.send('Please type a valid operation type.')
            pass
        
        var = f' {operation} '.join(nums)
        await ctx.send(f'{var} = {eval(var)}')    

    @isWorkChannel
    @commands.command(aliases=["uatlb"])
    async def updatealltimelb(self, ctx, *, args):
        
        clanLeaderboardChannel = discord.utils.get(ctx.guild.channels, id = 707218944217579541)
        
        # oldAllTimeEmbed=discord.Embed(title="All Time Clan Leaderboard", description="", color=0xff0000)
        # oldAllTimeEmbed.timestamp = datetime.datetime.utcnow()
        # oldAllTimeEmbed.set_thumbnail(url="https://cdn.discordapp.com/icons/371817692199518240/a_e004ffa8a16aa25643914ca5d4436694.gif?size=4096")
        # await clanLeaderboardChannel.send(embed = oldAllTimeEmbed)
        
        clanAllTimeLeaderboard = await clanLeaderboardChannel.fetch_message(950978987285418014)
        newAllTimeLB = discord.Embed(title = "All Time Clan Leaderboard", description = args, color=0xff0000)
        newAllTimeLB.timestamp = datetime.datetime.utcnow()
        newAllTimeLB.set_thumbnail(url="https://cdn.discordapp.com/icons/371817692199518240/a_e004ffa8a16aa25643914ca5d4436694.gif?size=4096")
        await ctx.message.reply("updated: https://discord.com/channels/371817692199518240/707218944217579541/950978987285418014")
        await clanAllTimeLeaderboard.edit(embed=newAllTimeLB)
        
    @isWorkChannel
    @commands.command(aliases=["uwlb"])
    async def updateweeklylb(self, ctx, *, args):
        
        clanLeaderboardChannel = discord.utils.get(ctx.guild.channels, id = 707218944217579541)
        
        # oldWeeklyEmbed=discord.Embed(title="Weekly Clan Leaderboard", description="", color=0xff0000)
        # oldWeeklyEmbed.timestamp = datetime.datetime.utcnow()
        # oldWeeklyEmbed.set_thumbnail(url="https://cdn.discordapp.com/icons/371817692199518240/a_e004ffa8a16aa25643914ca5d4436694.gif?size=4096")
        # await clanLeaderboardChannel.send(embed = oldWeeklyEmbed)
        
        clanWeeklyLeaderboard = await clanLeaderboardChannel.fetch_message(950979164104716308)
        newWeeklyLB = discord.Embed(title = "Weekly Clan Leaderboard", description = args, color=0xff0000)
        newWeeklyLB.timestamp = datetime.datetime.utcnow()
        newWeeklyLB.set_thumbnail(url="https://cdn.discordapp.com/icons/371817692199518240/a_e004ffa8a16aa25643914ca5d4436694.gif?size=4096")
        await ctx.message.reply("updated https://discord.com/channels/371817692199518240/707218944217579541/950979164104716308")
        await clanWeeklyLeaderboard.edit(embed=newWeeklyLB)

    @isBotsChannel
    @commands.command()
    async def clanapp(self, ctx, *, args = None):
        
        if args == None:
            clanInfo = discord.utils.get(ctx.guild.channels, id = 886988714436354068)
            infoMessage = await clanInfo.fetch_message(887029203457941526)
            
            embed = self.createInfoEmbed(infoMessage)
            await ctx.message.reply(content = "Missing information, please read:", embed = embed, mention_author = False)
            return

        clanApplications = discord.utils.get(ctx.guild.channels, id = 896444227578376192)
        
        logEmbed = discord.Embed(title = f"The Conquering Games Clan Application",description=f"**Application**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        logEmbed.timestamp = datetime.datetime.utcnow()
        msg = await clanApplications.send(self.matchStaffPing, embed = logEmbed)

        await msg.add_reaction(self.thumbsUp)
        await msg.add_reaction(self.thumbsDown)

        successEmbed = discord.Embed(title='Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your clan application!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = True)

    @isBotsChannel
    @commands.command()
    async def clanchange(self, ctx, *, args = None):
        
        if args == None:
            clanInfo = discord.utils.get(ctx.guild.channels, id = 886988714436354068)
            infoMessage = await clanInfo.fetch_message(887029203457941526)
            
            embed = self.createInfoEmbed(infoMessage)
            await ctx.message.reply(content = "Missing information, please read:", embed = embed, mention_author = False)
            return

        clanApplications = discord.utils.get(ctx.guild.channels, id = 896444227578376192)
        
        logEmbed = discord.Embed(title = f"The Conquering Games Clan Change",description=f"**Change**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        logEmbed.timestamp = datetime.datetime.utcnow()
        msg = await clanApplications.send(self.matchStaffPing, embed = logEmbed)

        await msg.add_reaction(self.thumbsUp)
        await msg.add_reaction(self.thumbsDown)

        successEmbed = discord.Embed(title='Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your clan change!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = True)

def setup(bot):
    bot.add_cog(TCGClans(bot))