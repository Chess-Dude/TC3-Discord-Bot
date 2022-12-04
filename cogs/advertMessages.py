import discord, datetime, pytz, asyncio
from discord.ext import commands, tasks

class AdvertMessages(commands.Cog):
    start_up_iteration = True

    def __init__(self, bot):
        self.bot = bot
        self.wait_until_4pm.start()
        
    @tasks.loop(seconds=1.0)
    async def wait_until_4pm(self):
        now = datetime.datetime.now(pytz.timezone('UTC'))
        tourney_message_time_stamps = []
        tourney_message_time_stamps.append(now.replace(hour=0, minute=0, second=0))
        tourney_message_time_stamps.append(now.replace(hour=4, minute=0, second=0))
        tourney_message_time_stamps.append(now.replace(hour=8, minute=0, second=0))
        tourney_message_time_stamps.append(now.replace(hour=12, minute=0, second=0))
        tourney_message_time_stamps.append(now.replace(hour=16, minute=0, second=0))
        tourney_message_time_stamps.append(now.replace(hour=20, minute=0, second=0))
        
        matchmaking_message_time_stamps = []
        matchmaking_message_time_stamps.append(now.replace(hour=1, minute=0, second=0))
        matchmaking_message_time_stamps.append(now.replace(hour=5, minute=0, second=0))
        matchmaking_message_time_stamps.append(now.replace(hour=9, minute=0, second=0))
        matchmaking_message_time_stamps.append(now.replace(hour=13, minute=0, second=0))
        matchmaking_message_time_stamps.append(now.replace(hour=17, minute=0, second=0))
        matchmaking_message_time_stamps.append(now.replace(hour=21, minute=0, second=0))

        events_message_time_stamps = []
        events_message_time_stamps.append(now.replace(hour=2, minute=0, second=0))
        events_message_time_stamps.append(now.replace(hour=6, minute=0, second=0))
        events_message_time_stamps.append(now.replace(hour=10, minute=0, second=0))
        events_message_time_stamps.append(now.replace(hour=14, minute=0, second=0))
        events_message_time_stamps.append(now.replace(hour=18, minute=0, second=0))
        events_message_time_stamps.append(now.replace(hour=22, minute=0, second=0))


        if now in tourney_message_time_stamps:
            try: 
                TC3 = self.bot.get_guild(350068992045744141)
                lobby = discord.utils.get(TC3.channels, id = 350068992045744142)
                await lobby.send("__Tournaments__\n\nAre you tired of playing against unskilled players? If so, join official tournaments with __huge coin and robux prizes__!")
                await asyncio.sleep(60)

            except:
                print("tourney_message_time_stamps wait_until_4pm not looped peroperly")

        elif now in matchmaking_message_time_stamps:
            try: 
                TC3 = self.bot.get_guild(350068992045744141)
                lobby = discord.utils.get(TC3.channels, id=350068992045744142)
                await lobby.send("__Matchmaking__\nIf you wish to find another member to play TC3 with, please run the ``!!rank game`` command in <#351057167706619914> to gain access to the matchmaking channel. Upon gaining access, you may run the ``/play`` command (in the channel) to find a fellow player!")
                await asyncio.sleep(60)

            except:
                print("matchmaking_message_time_stamps wait_until_4pm not looped peroperly")

        elif now in events_message_time_stamps:
            try: 
                TC3 = self.bot.get_guild(350068992045744141)
                lobby = discord.utils.get(TC3.channels, id=350068992045744142)
                await lobby.send("__Events__\nOur beloved event committee also holds weekly game nights that have a vast variety of games. Occasionally the event committee also holds special events announced at the beginning of every month. Partaking in game nights and special events allows you to enter <#959066479947571232>! If you wish to be notified upon every game night, please run the ``!!rank events`` command.")
                await asyncio.sleep(60)

            except:
                print("events_message_time_stamps wait_until_4pm not looped peroperly")

    @wait_until_4pm.before_loop       
    async def before_task(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(AdvertMessages(bot))