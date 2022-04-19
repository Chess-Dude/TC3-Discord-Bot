from ntpath import join
import discord, datetime, pytz

from discord.ext import commands, tasks

 
class TCGAdvert(commands.Cog):
    start_up_iteration = True

    def __init__(self, bot):
        self.bot = bot
        self.wait_until_4pm.start()
    
    @tasks.loop(seconds=1.0)
    async def wait_until_4pm(self):
        now = datetime.datetime.now(pytz.timezone('UTC'))
        time_stamps = []
        time_stamps.append(now.replace(hour=0, minute=0, second=0))
        time_stamps.append(now.replace(hour=4, minute=0, second=0))
        time_stamps.append(now.replace(hour=8, minute=0, second=0))
        time_stamps.append(now.replace(hour=12, minute=0, second=0))
        time_stamps.append(now.replace(hour=16, minute=0, second=0))
        time_stamps.append(now.replace(hour=20, minute=0, second=0))
        
        if now in time_stamps:
            try:
                TC3 = self.bot.get_guild(350068992045744141)
                lobby = discord.utils.get(TC3.channels, id = 350068992045744142)
                message = "**The Conquering Games\n\nAre you bored facing noob TC3 players and winning all the time? Fear no more! The Conquering Games (TCG) is holding a "
                await lobby.send("**__Welcome to The Conquerors 3 Discord Server!__**\n\nOur community has multiple activities and channels to suit your needs like __matchmaking, events, tournaments, clans and more!__ Please feel free to ping any staff member if you have any questions.\n\n__Matchmaking__\nIf you wish to find another member to play TC3 with, please run the ``!!rank game`` command in <#351057167706619914> to gain access to the matchmaking channel. Upon gaining access, you may run the ``!play`` command (in the channel) to find a fellow player!\n\n__Events__\nOur beloved event committee also holds weekly game nights that have a vast variety of games. Occasionally the event committee also holds special events announced at the beginning of every month. Partaking in game nights and special events allows you to enter <#959066479947571232>! If you wish to be notified upon every game night, please run the ``!!rank events`` command.\n\n__Tournaments and Clans__\nAre you tired of playing against unskilled players? Or just interested in getting better at TC3 and earning some sweet rewards (Robux and TC3 Coins)? If so, join The Conquering Games (TCG), the competitive side of the game which is filled with skilled players! These true conquerors will be split into various divisions of different skill levels and be able to partake in various activities. Such as, being trained by some of TCG's finest players, scrimmages with other teams/players, tournaments, clans and other competitive events! You can find more info in <#707263554285207552>\nTo Partake you must join today The Conquering Games discord server: https://discord.gg/kDnxtFxrKG\n\n__Upcoming Events__\n\n__The Conquering Games Elimination 1v1 Tournament Sign ups opening!__ \n> Depending on the skill division you are placed on, you can win up to **10, 000 coins** for winning! \n\nSee instructions to join here:\nhttps://discord.gg/Q8JQJ3d9?event=964713982717984838")
            
            except:
                print("tcgAdvert wait_until_4pm not looped peroperly")
        
        else:
            pass
    
    @wait_until_4pm.before_loop       
    async def before_task(self):
        await self.bot.wait_until_ready()

    @commands.is_owner()
    @commands.command(aliases=["joins"])
    async def member_joins(self, ctx):
        now = datetime.datetime.now(pytz.timezone('UTC'))
        hours_24 = datetime.timedelta(hours = 24)
        last_24_hours = now - hours_24
        member = discord.Member
        TCG = self.bot.get_guild(371817692199518240)
        joined_members = []
        for member in TCG.members:
            if member.joined_at <= (member.joined_at - datetime.timedelta(hours = 24)):
                joined_members.append(member.mention)
        print(joined_members)
        print(last_24_hours)
        
async def setup(bot):
    await bot.add_cog(TCGAdvert(bot))