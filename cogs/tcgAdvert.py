from cgi import test
import discord, datetime, pytz

from discord.ext import commands, tasks

 
class TCGAdvert(commands.Cog):
    start_up_iteration = True

    def __init__(self, bot):
        self.bot = bot
        for guild in self.bot.guilds:
            for channel in guild.channels:
                print(channel)
        self.wait_until_4pm.start()
        
    def send_message(self):
        pass


    @tasks.loop(seconds = 1)
    async def wait_until_4pm(self): 
        print("runs every 5 seconds")   
        now = datetime.datetime.now(pytz.timezone("US/Eastern"))
        print("now variable has run, ", now)
        next_run = now.replace(hour=0, minute=0, second=0)
        time_stamps = []
        time_stamps.append(now.replace(hour=0, minute=0, second=0))
        time_stamps.append(now.replace(hour=4, minute=0, second=0))
        time_stamps.append(now.replace(hour=8, minute=0, second=0))
        time_stamps.append(now.replace(hour=12, minute=0, second=0))
        time_stamps.append(now.replace(hour=16, minute=0, second=0))
        time_stamps.append(now.replace(hour=20, minute=0, second=0))
        
        if now in time_stamps:
            try:
                TCG = self.bot.get_guild(350068992045744141)
                print(TCG)
                general = discord.utils.get(TCG.channels, id = 350068992045744142)
                await general.send("<@621516858205405197>")
            except:
                print("task not looped peroperly")
        else:
            print("not time yet")
            
        await discord.utils.sleep_until(next_run)
        
    @wait_until_4pm.before_loop
    async def before_task(self):
        print('waiting...')
        await self.bot.wait_until_ready()
    

def setup(bot):
    print("tcgAdvert setup starting")
    bot.add_cog(TCGAdvert(bot))
    print("tcgAdvert setup complete")