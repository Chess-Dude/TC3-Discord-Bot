import discord, datetime, pytz

from discord.ext import commands, tasks

class TCGAdvert(commands.Cog):


    def init(self, bot):
        self.bot = bot
        self.send_message.start()

    @tasks.loop(hours = 4)
    async def send_message(self):
        TC3 = self.bot.get_guild(350068992045744141)
        general = discord.utils.get(TC3.channels, id = 350068992045744142)
        await general.send("(insert message here)")


    @send_message.before_loop
    async def wait_until_4pm(self): 
        now = datetime.datetime.now(pytz.timezone("US/Eastern"))
        next_run = now.replace(hour=0, minute=0, second=0)
        _12AM= now.replace(hour=0, minute=0, second=0)
        _4AM = now.replace(hour=4, minute=0, second=0)
        _8AM = now.replace(hour=8, minute=0, second=0)
        _12PM = now.replace(hour=12, minute=0, second=0)
        _4PM = now.replace(hour=16, minute=0, second=0)
        _8PM = now.replace(hour=20, minute=0, second=0)

        if _8PM < now:
            next_run += datetime.timedelta(days=1)
            self.send_message()
            
        elif _4PM < now:
            next_run = _8PM
            self.send_message()
            
        elif _12PM < now:
            next_run = _4PM 
            self.send_message()
            
        elif _8AM < now:
            next_run = _12PM 
            self.send_message()
            
        elif _4AM < now:
            next_run = _8AM 
            self.send_message()
            
        elif _12AM < now:
            next_run = _4AM 
            self.send_message()
            
        await discord.utils.sleep_until(next_run)

def setup(bot):
    bot.add_cog(TCGAdvert(bot))