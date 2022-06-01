import discord, datetime, pytz, time 

from discord.ext import commands, tasks

 
class TCGAdvert(commands.Cog):
    start_up_iteration = True

    def __init__(self, bot):
        self.bot = bot
        self.wait_until_4pm.start()
        self.wait_until_12am.start()
    
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
                print(f"timestamp for message sent in before tcgAdvert is: {now}")
                await lobby.send("**__Welcome to The Conquerors 3 Discord Server!__**\n\nOur community has multiple activities and channels to suit your needs like __matchmaking, events, tournaments, clans and more!__ Please feel free to ping any staff member if you have any questions.\n\n__Matchmaking__\nIf you wish to find another member to play TC3 with, please run the ``!!rank game`` command in <#351057167706619914> to gain access to the matchmaking channel. Upon gaining access, you may run the ``!play`` command (in the channel) to find a fellow player!\n\n__Events__\nOur beloved event committee also holds weekly game nights that have a vast variety of games. Occasionally the event committee also holds special events announced at the beginning of every month. Partaking in game nights and special events allows you to enter <#959066479947571232>! If you wish to be notified upon every game night, please run the ``!!rank events`` command.\n\n__Tournaments and Clans__\nAre you tired of playing against unskilled players? Or just interested in getting better at TC3 and earning some sweet rewards (Robux and TC3 Coins)? If so, join The Conquering Games (TCG), the competitive side of the game which is filled with skilled players! These true conquerors will be split into various divisions of different skill levels and be able to partake in various activities. Such as, being trained by some of TCG's finest players, scrimmages with other teams/players, tournaments, clans and other competitive events! You can find more info in <#707263554285207552>\nTo Partake you must join today The Conquering Games discord server: https://discord.gg/kDnxtFxrKG")
                print(f"1st tcgAdvert message sent time: {now}")
                await lobby.send("**__Upcoming Events__**\n\n__2v2 Elimination Tournament Sign Ups Open__\nSign Ups are open until May 22nd 10:00pm EST.\n\n1. Join The Conquering Games Discord Server (https://discord.gg/kDnxtFxrKG)\n2. Go to <#408820459279220736> and have you and your team mates verify (!verify) your roblox account\n3. Ping your and your team mates in <#666966628755570697> to sign up!\n\nKeep in mind that there will be up to 15, 000 in game coins if you win!")
                print(f"2nd tcgAdvert message sent time: {now}")
                time.sleep(100)
                print(f"after 100 sleep: {now}")
            except:
                print("tcgAdvert wait_until_4pm not looped peroperly")

    @tasks.loop(seconds=1)
    async def wait_until_12am(self):
        now = datetime.datetime.now(pytz.timezone("UTC"))
        time_stamps = []
        time_stamps.append(now.replace(hour=4, minute=0, second=0))
        if now in time_stamps:
            try:
                TCG = self.bot.get_guild(371817692199518240)
                joined_members = ""
                general = discord.utils.get(TCG.channels, id = 408819824949592064)
                for member in TCG.members:
                    difference = discord.utils.utcnow() - member.joined_at    
                    if difference.days <= 1:
                        joined_members = joined_members + member.mention
                await general.send(f"**__Welcome to The Conquering Games__** {joined_members}!\n\nIf you wish to partake in tournaments or clans, check out the info channels: <#886952755367903233>, <#886962032753131560>, <#886972024885481493> and <#886988714436354068> to see how to join!\n\n**__Upcoming Events__**\n\n__2v2 Elimination Tournament Sign Ups Open__\nSign Ups are open until May 22nd 10:00pm EST.\n\n1. Join The Conquering Games Discord Server (https://discord.gg/kDnxtFxrKG)\n2. Go to <#408820459279220736> and have you and your team mates verify (!verify) your roblox account\n3. Ping your and your team mates in <#666966628755570697> to sign up!\n\nKeep in mind that there will be up to 15, 000 in game coins if you win!")
                time.sleep(100)
            except:
                print("tcgAdvert wait_until_12am not looped peroperly")
        
    @wait_until_12am.before_loop
    async def welcome_message(self):
        await self.bot.wait_until_ready()

    @wait_until_4pm.before_loop       
    async def before_task(self):
        await self.bot.wait_until_ready()
async def setup(bot):
    await bot.add_cog(TCGAdvert(bot))