from cgi import test
import discord, datetime, pytz

from discord.ext import commands, tasks

 
class TCGAdvert(commands.Cog):
    start_up_iteration = True

    def __init__(self, bot):
        self.bot = bot
        self.wait_until_4pm()
    
    @tasks.loop(seconds=1)
    async def wait_until_4pm(self):
        print("tcgAdvert loop running sucessfully")
        now = datetime.datetime.now(pytz.timezone('UTC'))
            
        time_stamps = []
        time_stamps.append(now.replace(hour=0, minute=0, second=0))
        time_stamps.append(now.replace(hour=4, minute=0, second=0))
        time_stamps.append(now.replace(hour=8, minute=0, second=0))
        time_stamps.append(now.replace(hour=12, minute=6, second=45))
        time_stamps.append(now.replace(hour=16, minute=0, second=0))
        time_stamps.append(now.replace(hour=20, minute=0, second=0))
        
        if now in time_stamps:
            try:
                TCG = self.bot.get_guild(371817692199518240)
                freecookiechannel = discord.utils.get(TCG.channels, id = 941567353672589322)
                await freecookiechannel.send("**The Conquering Games**\n\nAre you interested in getting better at TC3 and earning some sweet rewards (Robux and TC3 Coins)? If so, join The Conquering Games (TCG), __the competitive side of the game__ which is filled with skilled players!\n\nThese true conquerors will be split into various divisions of different skill levels and be able to partake in various activities. Such as, being trained by some of TCG's finest players, scrimmages with other teams/players, tournaments and other competitive events!\n\nEach activity has something new to offer.\n\nMore Info in <#707263554285207552>\nJoin today at:https://discord.gg/kDnxtFxrKG")
            except:
                print("tcgAdvert wait_until_4pm not looped peroperly")
        
        else:
            pass
    
    @wait_until_4pm.before_loop       
    async def before_task(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TCGAdvert(bot))