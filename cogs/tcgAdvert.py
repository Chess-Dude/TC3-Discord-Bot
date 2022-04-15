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
                await lobby.send("**The Conquering Games**\n\nAre you interested in getting better at TC3 and earning some sweet rewards (Robux and TC3 Coins)? If so, join The Conquering Games (TCG), __the competitive side of the game__ which is filled with skilled players!\n\nThese true conquerors will be split into various divisions of different skill levels and be able to partake in various activities. Such as, being trained by some of TCG's finest players, scrimmages with other teams/players, tournaments and other competitive events!\n\nEach activity has something new to offer.\n\nMore Info in <#707263554285207552>\nJoin today at:https://discord.gg/kDnxtFxrKG\n\nAre you looking for another member to play TC3 with? If so, run the ``!!rank game`` command to gain access to #matchmaking, then run the ``!play`` command to find a friend!")
            
            except:
                print("tcgAdvert wait_until_4pm not looped peroperly")
        
        else:
            pass
    
    @wait_until_4pm.before_loop       
    async def before_task(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TCGAdvert(bot))