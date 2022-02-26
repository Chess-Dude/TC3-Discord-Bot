import discord 
from discord.ext import commands

def TestingChannel(ctx):
    return ctx.channel.id == 941567353672589322

isFreeCookieChannel = commands.check(TestingChannel)

class AutoMod(commands.Cog):
    """
    """

    def __init__(self, bot):
        """
        constructor function
        """
        self.bot = bot
        self.blacklisted_words = ["1984"]

    @isFreeCookieChannel
    async def on_message(self, message, ctx):
        """
        automod
        """
        for word in self.blacklisted_words:
            if word in str.lower(message.content):
                await message.delete()
                print("1984")


def setup(bot):
    bot.add_cog(AutoMod(bot))
