import discord, datetime, pytz, asyncio

class AdvertiseMessage():
    def __init__(self):
        self.update_timestamps()

    def update_timestamps(self):
        """Update all timestamps to today's date"""
        now = datetime.datetime.now(pytz.timezone('UTC'))
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Tournament message times (every 4 hours)
        self.tourney_message_time_stamps = [
            today.replace(hour=h) for h in [0, 4, 8, 12, 16, 20]
        ]
        self.tourney_message_time_stamps.append(today.replace(hour=10, minute=20, second=35))

        # Matchmaking message times
        self.matchmaking_message_time_stamps = [
            today.replace(hour=h) for h in [1, 5, 9, 13, 17, 21]
        ]

        # Events message times
        self.events_message_time_stamps = [
            today.replace(hour=h) for h in [2, 6, 10, 14, 18, 22]
        ]

        # One day tournament times (commented out for now)
        self.one_day_tournament_time_stamps = []

    def is_time_to_send(self, target_time, window_minutes=1):
        """Check if current time is within window_minutes of target_time"""
        now = datetime.datetime.now(pytz.timezone('UTC'))
        
        # If we've passed midnight, update all timestamps
        if now.date() > target_time.date():
            self.update_timestamps()
            return False
            
        return target_time <= now < (target_time + datetime.timedelta(minutes=window_minutes))

    async def advertise_message(self, lobby):
        try:
            # Tournament messages
            for timestamp in self.tourney_message_time_stamps:
                if self.is_time_to_send(timestamp):
                    try:
                        embed = discord.Embed(
                            title="**``TC3 Tournaments!``**",
                            description="Are you tired of playing against unskilled players? If so, join official tournaments with __huge coin and robux prizes__! Check out <#1047726075221901383> to see how to join!",
                            color=0x00ffff
                        )
                        await lobby.send(embed=embed)
                        await asyncio.sleep(60)
                        break
                    except Exception as e:
                        print(f"Error sending tournament message: {e}")

            # Matchmaking messages
            for timestamp in self.matchmaking_message_time_stamps:
                if self.is_time_to_send(timestamp):
                    try:
                        embed = discord.Embed(
                            title="**``TC3 Looking For Game!``**",
                            description="If you wish to find another member to play TC3 with, please run the ``!!rank game`` command in <#351057167706619914> to gain access to the matchmaking channel. Upon gaining access, you may run the ``/play`` command (in the channel) to find a fellow player!",
                            color=0x00ffff
                        )
                        await lobby.send(embed=embed)
                        await asyncio.sleep(60)
                        break
                    except Exception as e:
                        print(f"Error sending matchmaking message: {e}")

            # Events messages
            for timestamp in self.events_message_time_stamps:
                if self.is_time_to_send(timestamp):
                    try:
                        embed = discord.Embed(
                            title="**``Server Events!``**",
                            description="Our beloved event committee also holds weekly game nights that have a vast variety of games. Occasionally the event committee also holds special events announced at the beginning of every month. Partaking in game nights and special events allows you to enter <#959066479947571232>! If you wish to be notified upon every game night, please run the ``!!rank events`` command.",
                            color=0x00ffff
                        )
                        await lobby.send(embed=embed)
                        await asyncio.sleep(60)
                        break
                    except Exception as e:
                        print(f"Error sending events message: {e}")

            # One day tournament messages
            for timestamp in self.one_day_tournament_time_stamps:
                if self.is_time_to_send(timestamp):
                    try:
                        await lobby.send("__One-Day Tournament__\nThe Event Comittee will be hosting the 25th One-Day Tournament on Saturday, February the 18th. Sign-ups will open at 2:00pm EST. Visit the below document on further details:\nhttps://docs.google.com/document/d/1e0JkxBFhv55TkJxCLWxVVBxQByblbZV7Ryw95ILqpCE/edit\n\nhttps://discord.gg/tc3?event=1075956129802244176")
                        await asyncio.sleep(60)
                        break
                    except Exception as e:
                        print(f"Error sending tournament message: {e}")

        except Exception as e:
            print(f"Error in advertise_message: {e}")
