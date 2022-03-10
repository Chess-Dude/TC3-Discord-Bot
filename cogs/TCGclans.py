import discord, datetime
from discord import ui
from discord.ext import commands
from discord import Embed

def WorkChannel(ctx):
    return ctx.channel.id == 896440473659519057 or ctx.channel.id == 941567353672589322

isWorkChannel = commands.check(WorkChannel)

class TCGClans(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
    
    @isWorkChannel
    @commands.command(aliases = ["c"])
    async def calculate(self, ctx, operation, *nums):
        
        if operation not in ['+', '-', '*', '/']:
            await ctx.send('Please type a valid operation type.')
            pass
        
        var = f' {operation} '.join(nums)
        await ctx.send(f'{var} = {eval(var)}')    

    @isWorkChannel
    @commands.command(aliases=["uatl"])
    async def updatealltimeleaderboard(self, ctx, *, args):
        
        clanLeaderboardChannel = discord.utils.get(ctx.guild.channels, id = 707218944217579541)
        
        # oldAllTimeEmbed=discord.Embed(title="All Time Clan Leaderboard", description="", color=0xff0000)
        # oldAllTimeEmbed.timestamp = datetime.datetime.utcnow()
        # oldAllTimeEmbed.set_thumbnail(url="https://cdn.discordapp.com/icons/371817692199518240/a_e004ffa8a16aa25643914ca5d4436694.gif?size=4096")
        # await clanLeaderboardChannel.send(embed = oldAllTimeEmbed)
        
        clanAllTimeLeaderboard = await clanLeaderboardChannel.fetch_message(950978987285418014)
        newAllTimeLB = discord.Embed(title = "Weekly Clan Leaderboard", description = args, color=0xff0000)
        newAllTimeLB.timestamp = datetime.datetime.utcnow()
        newAllTimeLB.set_thumbnail(url="https://cdn.discordapp.com/icons/371817692199518240/a_e004ffa8a16aa25643914ca5d4436694.gif?size=4096")
        await ctx.message.reply("updated: https://discord.com/channels/371817692199518240/707218944217579541/950978987285418014")
        await clanAllTimeLeaderboard.edit(embed=newAllTimeLB)
        
    @isWorkChannel
    @commands.command(aliases=["uwl"])
    async def updateweeklyleaderboard(self, ctx, *, args):
        
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
        
def setup(bot):
    bot.add_cog(TCGClans(bot))