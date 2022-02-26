from cgi import test
import discord, datetime, pytz

from discord.ext import commands, tasks
def test(ctx):
   return ctx.id == 941567353672589322
 
class TCGAdvert(commands.Cog):


    def __init__(self, bot):
        print("tcgAdvert constructor function running")
        self.bot = bot
        self.send_message.start()
        
    @tasks.loop(seconds=7)
    async def send_message(self):
        TCG = self.bot.get_guild(371817692199518240)
        general = self.bot.get_channel(941567353672589322)
        await general.send("<@621516858205405197>")


    @tasks.loop(seconds = 5)
    async def wait_until_4pm(self): 
        print("runs every 5 seconds")
        now = datetime.datetime.now(pytz.timezone("US/Eastern"))
        print("now variable has run, ", now)
        next_run = now.replace(hour=0, minute=0, second=0)
        _12AM = now.replace(hour=0, minute=0, second=0)
        _4AM = now.replace(hour=4, minute=0, second=0)
        _8AM = now.replace(hour=8, minute=0, second=0)
        _12PM = now.replace(hour=12, minute=0, second=0)
        _4PM = now.replace(hour=16, minute=0, second=0)
        _8PM = now.replace(hour=20, minute=0, second=0)

        if _8PM == now:
            next_run += datetime.timedelta(days=1)
            self.send_message()
            
        elif _4PM == now:
            next_run = _8PM
            self.send_message()
            
        elif _12PM == now:
            next_run = _4PM 
            self.send_message()
            
        elif _8AM == now:
            next_run = _12PM 
            self.send_message()
            
        elif _4AM == now:
            next_run = _8AM 
            self.send_message()
            
        elif _12AM == now:
            next_run = _4AM 
            self.send_message()
            
        await discord.utils.sleep_until(next_run)

def setup(bot):
    print("tcgAdvert setup starting")
    bot.add_cog(TCGAdvert(bot))
    print("tcgAdvert setup complete")