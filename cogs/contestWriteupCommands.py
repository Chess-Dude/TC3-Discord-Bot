import discord, typing
from discord.ext import commands
from discord import app_commands

class ContestWriteupCommands(commands.Cog):
    def __init__(
        self, 
        bot):
            self.bot = bot

    async def type_autocomplete(
        self, 
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        type_list = ["start", "end"]
        return [
            app_commands.Choice(name=type, value=type)
            for type in type_list if current.lower() in type.lower()
        ]

    contest_command_group = app_commands.Group(
        name="contest", 
        description="A Group Of Commands That Allows You To Get Write-Ups!")

    @app_commands.checks.has_any_role(475669961990471680, 554152645192056842, 743302990001340559, 743302990001340559)
    @contest_command_group.command(        
        name="writeup",
        description="A Command That Allows You To Generate A Contest Writeup!")
    @app_commands.autocomplete(type=type_autocomplete)
    @app_commands.describe(winner_1="ping the 1st place member of the contest!")
    @app_commands.describe(winner_2="ping the 2nd place member of the contest!")
    @app_commands.describe(winner_3="ping the 3rd place member of the contest!")
    @app_commands.describe(contest_name="mention the contest name here!")
    @app_commands.rename(contest_name="contest_name")
    @app_commands.rename(winner_1="winner_1")
    @app_commands.rename(winner_2="winner_2")
    @app_commands.rename(winner_3="winner_3")
    async def writeup(
        self, 
        interaction: discord.Interaction, 
        type: str,
        contest_name: str,
        winner_1: typing.Optional[discord.Member],
        winner_2: typing.Optional[discord.Member],
        winner_3: typing.Optional[discord.Member]
        ):

        if type == "start":
            await interaction.response.send_message(
                content=f"contest start message. Winners are: {winner_1.mention} {winner_2.mention} {winner_3.mention}"
                )

        elif type == "end":
            if winner_1 != None:
                winner_1 = f"\n\nIn **1st Place** we have {winner_1.mention} who won :coinn: **10,000 Coins** and 3 Entries in lottery!"
            else:
                winner_1 = ''

            if winner_2 != None:
                winner_2 = f"\n\nIn **2nd Place** we have {winner_2.mention} who won :coinn: **8,000 Coins** and 3 Entries in lottery!"
            else:
                winner_2 = ''

            if winner_3 != None:
                winner_3 = f"\n\nIn **3rd Place** we have {winner_3.mention} who won :coinn: **6,000 Coins** and 3 Entries in lottery!"
            else:
                winner_3 = ''

            await interaction.response.send_message(
                content=f"```@Notify @Contest **The time has come to announce the winners of the {contest_name}!**{winner_1}{winner_2}{winner_3}\n\nIn order claim your prize, please join this server: https://discord.gg/dRdSXGCk7d\n\n**IF YOU DID NOT WIN A PRIZE AND YOU ATTEMPT TO CLAIM IT, YOU WILL BE PERMANENTLY BANNED FROM THE SERVER.**```"                )

        else:
            await interaction.response.send_message(
                content=f"Error: You failed to provide the correct writeup type. Please try again."
                )

async def setup(bot):
    await bot.add_cog(ContestWriteupCommands(bot))