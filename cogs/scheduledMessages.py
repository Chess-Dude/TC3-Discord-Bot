import discord
from discord.ext import commands, tasks
from .scheduledTaskClasses.advertMessages import AdvertiseMessage

class ScheduledTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.advertise_message_obj = AdvertiseMessage()
        self.looped_advert_message.start()
        self.LOBBY_CHANNEL = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.LOBBY_CHANNEL = self.bot.get_channel(350068992045744142)
    
    @commands.Cog.listener()    
    async def on_thread_create(
        self, 
        thread
    ):
        tags = thread.applied_tags
        for index, item in enumerate(tags):
            if item.name == 'Event Suggestion':
                await thread.send(
                    content="<@898392058077802496>"
                )       

    @tasks.loop(seconds=1.0)
    async def looped_advert_message(self):
        await self.advertise_message_obj.advertise_message(self.LOBBY_CHANNEL)

    @looped_advert_message.before_loop       
    async def before_task(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(ScheduledTasks(bot))