import discord, datetime, pytz, asyncio

class AdvertiseMessage():
    def __init__(self):
        now = datetime.datetime.now(pytz.timezone('UTC'))
        self.tourney_message_time_stamps = []
        self.tourney_message_time_stamps.append(now.replace(hour=0, minute=0, second=0))
        self.tourney_message_time_stamps.append(now.replace(hour=4, minute=0, second=0))
        self.tourney_message_time_stamps.append(now.replace(hour=8, minute=0, second=0))
        self.tourney_message_time_stamps.append(now.replace(hour=12, minute=0, second=0))
        self.tourney_message_time_stamps.append(now.replace(hour=16, minute=0, second=0))
        self.tourney_message_time_stamps.append(now.replace(hour=20, minute=0, second=0))
        self.tourney_message_time_stamps.append(now.replace(hour=10, minute=20, second=35))

        self.matchmaking_message_time_stamps = []
        self.matchmaking_message_time_stamps.append(now.replace(hour=1, minute=0, second=0))
        self.matchmaking_message_time_stamps.append(now.replace(hour=9, minute=0, second=0))
        self.matchmaking_message_time_stamps.append(now.replace(hour=5, minute=0, second=0))
        self.matchmaking_message_time_stamps.append(now.replace(hour=21, minute=0, second=0))
        self.matchmaking_message_time_stamps.append(now.replace(hour=13, minute=0, second=0))
        self.matchmaking_message_time_stamps.append(now.replace(hour=17, minute=0, second=0))

        self.events_message_time_stamps = []
        self.events_message_time_stamps.append(now.replace(hour=2, minute=0, second=0))
        self.events_message_time_stamps.append(now.replace(hour=6, minute=0, second=0))
        self.events_message_time_stamps.append(now.replace(hour=10, minute=0, second=0))
        self.events_message_time_stamps.append(now.replace(hour=14, minute=0, second=0))
        self.events_message_time_stamps.append(now.replace(hour=18, minute=0, second=0))
        self.events_message_time_stamps.append(now.replace(hour=22, minute=0, second=0))

        self.one_day_tournament_time_stamps = []
        # one_day_tournament_time_stamps.append(now.replace(hour=3, minute=0, second=0))
        # one_day_tournament_time_stamps.append(now.replace(hour=7, minute=0, second=0))
        # one_day_tournament_time_stamps.append(now.replace(hour=11, minute=0, second=0))
        # one_day_tournament_time_stamps.append(now.replace(hour=15, minute=0, second=0))
        # one_day_tournament_time_stamps.append(now.replace(hour=19, minute=0, second=0))
        # one_day_tournament_time_stamps.append(now.replace(hour=23, minute=0, second=0))


    async def advertise_message(self, lobby):
        now = datetime.datetime.now(pytz.timezone('UTC'))
        
        for timestamp in self.tourney_message_time_stamps:
            if timestamp <= now and now < (timestamp + datetime.timedelta(minutes=1)):
                try: 
                    embed = discord.Embed(
                        title="**``TC3 Tournaments!``**",
                        description="Are you tired of playing against unskilled players? If so, join official tournaments with __huge coin and robux prizes__! Check out <#1047726075221901383> to see how to join!",
                        color=0x00ffff
                    )
                    await lobby.send(embed=embed)
                    await asyncio.sleep(60)
                    break
                except:
                    print("tourney_message_time_stamps wait_until_4pm not looped properly")
        
        if now in self.matchmaking_message_time_stamps:
            try: 
                embed = discord.Embed(
                    title="**``TC3 Looking For Game!``**",
                    description="If you wish to find another member to play TC3 with, please run the ``!!rank game`` command in <#351057167706619914> to gain access to the matchmaking channel. Upon gaining access, you may run the ``/play`` command (in the channel) to find a fellow player!",
                    color=0x00ffff
                )
                await lobby.send(embed=embed)
                await asyncio.sleep(60)

            except:
                print("matchmaking_message_time_stamps wait_until_4pm not looped peroperly")

        if now in self.events_message_time_stamps:
            try: 
                embed = discord.Embed(
                    title="**``Server Events!``**",
                    description="Our beloved event committee also holds weekly game nights that have a vast variety of games. Occasionally the event committee also holds special events announced at the beginning of every month. Partaking in game nights and special events allows you to enter <#959066479947571232>! If you wish to be notified upon every game night, please run the ``!!rank events`` command.",
                    color=0x00ffff
                )
                await lobby.send(embed=embed)
                await asyncio.sleep(60)

            except:
                print("events_message_time_stamps wait_until_4pm not looped peroperly")

        if now in self.one_day_tournament_time_stamps:
            try: 
                await lobby.send("__One-Day Tournament__\nThe Event Comittee will be hosting the 25th One-Day Tournament on Saturday, February the 18th. Sign-ups will open at 2:00pm EST. Visit the below document on further details:\nhttps://docs.google.com/document/d/1e0JkxBFhv55TkJxCLWxVVBxQByblbZV7Ryw95ILqpCE/edit\n\nhttps://discord.gg/tc3?event=1075956129802244176")
                await asyncio.sleep(60)

            except:
                print("events_message_time_stamps wait_until_4pm not looped peroperly")
