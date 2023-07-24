import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands
from .informationEmbeds.parentTournamentView import ParentTournamentInformationViews

class ParentClanInformationViews(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Clan Creation/Management", style=discord.ButtonStyle.blurple, custom_id="persistent_view:clan_creation", emoji='💼')
    async def info_clan_creation_management(self, interaction: discord.Interaction, button: discord.ui.Button):

        command_name = "> ``/clan application`` ``Clan_Name:`` ``Clan_Color:`` ``Clan_Leader:`` ``Clan_Co_Leader:`` ``Clan_Member_1:`` ``Clan_Member_2:`` ``Clan_Member_3:`` ``Clan_Member_4:``"

        sign_up_instructions_embed = discord.Embed(
            title=f"Clan Information - Clan Creation/Management",
            color=0x00ffff
        )

        sign_up_instructions_embed.add_field(
            name=f"__How do I Create a clan?__",
            value=f"> 1. Have you and your clan members verify your Roblox account by going to <#351057167706619914> and running the ``/verify`` slash command.\n\n> 2. Submit a clan application by going to <#351057167706619914> and running the {command_name} slash command.",
            inline=False
        )

        command_name = "> ``/clan change`` ``New_Clan_Hex_Color`` ``New_Clan_Leader:`` ``New_Clan_Co_Leader:`` ``New_Clan_Member:`` ``Remove_Clan_Member:``"

        sign_up_instructions_embed.add_field(
            name=f"__How do I remove/add a member to a clan?__",
            value=f"> 1. Have you and your clan members verify your Roblox account by going to <#351057167706619914> and running the ``/verify`` slash command.\n\n> 2. Submit a clan change by going to <#351057167706619914> and running the {command_name} slash command.",
            inline=False
        )

        sign_up_instructions_embed.add_field(
            name=f"__How do I leave a clan?__",
            value=f"> 1. Go to <#351057167706619914> and run the ``/clan leave`` command.",
            inline=False
        )

        await interaction.response.send_message(embed=sign_up_instructions_embed, ephemeral=True)

    @discord.ui.button(label="Joining a Clan", style=discord.ButtonStyle.blurple, custom_id="persistent_view:Joining_A_Clan", emoji='🤝')
    async def info_clan_joining(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"Clan Information - Joining a Clan",
            color=0x00ffff
        )

        information_embed.add_field(
            name="**__How to Join a clan?__**",
            value="> To join a clan, direct message a Clan Leader or Co Leader that is looking for new members! You can find clan advertisements under <#1121271059761602722>."
        )
        await interaction.response.send_message(embed=information_embed, ephemeral=True)

    @discord.ui.button(label="Clan Point Submissions", style=discord.ButtonStyle.blurple, custom_id="persistent_view:Clan_Point_Submissions", emoji='📝')
    async def info_cp_subs(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"Clan Information - Clan Point Submissions",
            color=0x00ffff
        )

        information_embed.add_field(
            name="**__What are clan points?__**",
            value="> Clan points are the coins awarded at the end of round bonus of each TC3 match. Upon submission to the Event Committee, the clan points are totalled and added to the leaderboards.",
            inline=False
        )

        information_embed.add_field(
            name="**__How do I submit clan points?__**",
            value="> Clan points can be submitted via the slash command: ``/submit clan point`` ``Damage_Dealt_Bonus:`` ``Damaged_Healed_Bonus:`` ``Victory_Bonus:`` ``Game_Mode:`` ``Image_Link:`` ``Clan_Member``\n\n> This Command will then notify a staff member to review your clan point submission.",
            inline=False
        )

        information_embed.add_field(
            name="**__Are there any multipliers or clan point caps?__**",
            value="> Yes, there are game mode multipliers and clan point caps. Their multipliers and clan point caps can be found below.",
            inline=False
        )

        information_embed.add_field(
            name="**__Is there a weekly clan point quota?__**",
            value="> Yes, the weekly clan point quota is 1, 000 clan points. Not meeting this quota for 3 weeks will result in a clan disbandment.",
            inline=False
        )

        information_embed.add_field(
            name="**__Conquest:__**",
            value="> ``Clan Point Game Mode Multiplier: 2``\n> ``Clan Point Cap: 125``\n> ``Damaged Healed Bonus Cap: 15``\n> ``Time Required: 20 minutes``",
            inline=False
        )

        information_embed.add_field(
            name="**__Survival:__**",
            value="> ``Clan Point Game Mode Multiplier: 1``\n> ``Clan Point Cap: No cap``\n> ``Damaged Healed Bonus Cap: No Cap``\n> ``Time Required: 20 minutes``",
            inline=False
        )

        information_embed.add_field(
            name="**__Free For All:__**",
            value="> ``Clan Point Game Mode Multiplier: 2``\n> ``Clan Point Cap: 300``\n> ``Damaged Healed Bonus Cap: No Cap``\n> ``Time Required: 60 minutes``",
            inline=False
        )
        
        information_embed.add_field(
            name="**__King Of The Hill:__**",
            value="> ``Clan Point Game Mode Multiplier: 1.5``\n> ``Clan Point Cap: 90``\n> ``Damaged Healed Bonus Cap: No Cap``\n> ``Time Required: Objective Must Be Completed``",
            inline=False
        )

        information_embed.add_field(
            name="**__Tournamnet Scrimmage/Match:__**",
            value="> ``Clan Point Game Mode Multiplier: 3``\n> ``Clan Point Cap: 255``\n> ``Damaged Healed Bonus Cap: 15``\n> ``Time Required: 20 minutes``",
            inline=False
        )
        
        
        information_embed.add_field(
            name="**__Clan Scrimmage:__**",
            value="> ``Clan Point Game Mode Multiplier: 3``\n> ``Clan Point Cap: 255``\n> ``Damaged Healed Bonus Cap: 15``\n> ``Time Required: 20 minutes``",
            inline=False
        )
        
        information_embed.add_field(
            name="**__Note:__**",
            value="> __All__ Clan Point submissions must consist of the end of round bonus image link with a taskbar showing the date and time and the game timer. Clan point submissions expire every 7 days and the leaderboard is rest every week at 12pm EST on Sundays.",
            inline=False
        )

        await interaction.response.send_message(embed=information_embed, ephemeral=True)

    @discord.ui.button(label="Clan Leaderboard Prizes", style=discord.ButtonStyle.blurple, custom_id="persistent_view:Clan_LB_Prizes", emoji='🏆')
    async def info_lb_prizes(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"Clan Information - Leaderboard Prizes",
            color=0x00ffff
        )
        
        information_embed.add_field(
            name=f"**__Note:__**",
            value="Clan Leaders distribute total coins",
            inline=False
        )

        information_embed.add_field(
            name=f"__Clan Prize List (Base Prizes):__",
            value=f"**1st Place:** ``15, 000 coins``\n**2nd Place:** ``10, 000 coins``\n**3rd Place:** ``7, 500 coins``",
            inline=False
        )

        information_embed.add_field(
            name=f"__Multiplier Buff:__",
            value=f"In addition to the base prizes, a buff of ``2 clan points/1 coin prize`` will be applied *on top* of the clan's base prize.",
            inline=False
        )

        await interaction.response.send_message(embed=information_embed, ephemeral=True)


class InformationEmbeds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def tournament_embed_info(
        self, 
        interaction
    ):
        information_embed = discord.Embed(
            title=f"Tournament Information",
            description=f"This section will cover everything there is to know about tournaments for The Conquerors 3.",
            color=0x00ffff
        )

        information_embed.set_image(
            url="https://media.discordapp.net/attachments/350068992045744142/1047732656508510299/IMG_3001.png?width=1193&height=671"
        )
        
        await interaction.channel.send(
            embed=information_embed, 
            view=ParentTournamentInformationViews()
        )

    @app_commands.command(
        name="clan_information",
        description="Get Information On Clans!"
    )
    async def clan_embed_info(
        self, 
        interaction
    ):
        information_embed = discord.Embed(
            title=f"Clan Information",
            description=f"This section will cover everything there is to know about Clans for The Conquerors 3.\n\nClans are a group of 4-6 people that compete competitively for rewards and leaderboard positions. These groups of people advance themselves up the leaderboards by earning clan/conquering points from submitting end of round bonuses via a command. There are 2 types of leaderboards weekly and yearly, clans will be rewarded based on weekly leaderboards.",
            color=0x00ffff
        )

        information_embed.set_image(
            url="https://media.discordapp.net/attachments/389874452227293214/1036035317347647569/tc3_background-1.png?width=1193&height=671"
        )
        
        await interaction.channel.send(
            embed=information_embed, 
            view=ParentClanInformationViews()
        )


async def setup(bot):
    await bot.add_cog(InformationEmbeds(bot))