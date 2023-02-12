import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

class ChildTournamentInformationViews(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Tournament Rules", style=discord.ButtonStyle.blurple, emoji='📃', custom_id="persistent_view:tournament_rules")
    async def tournament_rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        tournament_rules_embed = discord.Embed(
            title="Tournament Rules and Guidelines",
            color=0x00ffff
        )

        tournament_rules_embed.add_field(
            name=f"__The Conquerors 3 Community Rules__",
            value=f"All Rules from The Conquerors 3 Discord User and Staff Rules apply to this event.",
            inline=False
        )
        
        tournament_rules_embed.add_field(
            name=f"__Play The Selected Randomized Map__",
            value=f"You will be required to randomize the chosen tournament map from The Conquerors 3 Bot. If you and your opponent both agree to a reroll, you may reroll the map. However, if one player refuses to reroll, you must play the selected map.",
            inline=False
        )

        tournament_rules_embed.add_field(
            name=f"__You Must Screenshot The End Of Round Bonus__",
            value=f"In order to ensure a confirmed match result, a player must screenshot the end of round bonus (or the forfeit message) and send the match result in the dedicated match result channel.",
            inline=False
        )

        tournament_rules_embed.add_field(
            name=f"__Stalling A Match Is Prohibited__",
            value=f"In order to keep the tournament round short, we will be punishing stallers (running with a select few units to delay the end of the match). If you know you have lost, be a good sportsman and forfeit. This saves the staff, yourself and your opponents valuable time.",
            inline=False
        )

        tournament_rules_embed.add_field(
            name=f"__Glitches Are Prohibited__",
            value=f"Any and all game-breaking glitches are prohibited. However, the 'garrison' glitch (to get a land unit onto a higher level of terrain using a garrison unit/building) and the 'wiggle hovercraft' glitch is allowed.",
            inline=False
        )

        tournament_rules_embed.add_field(
            name=f"__Leaving Is Prohibited__",
            value=f"Leaving for any reason is prohibited. The only exception is when you are bugged and need to rejoin to fix it. However if you disconnect mid-game, you must rejoin, but only have two minutes to do so. If you do not rejoin within this timeframe without any indication, this will be counted as a forfeit.",
            inline=False
        )

        tournament_rules_embed.add_field(
            name=f"__Scheduling__",
            value=f"You are required to cooperate with scheduling with your opponent. Meaning if you are unresponsive to scheduling attempts (or make no attempt at all), you put yourself at risk for being disqualified and possibly banned from tournaments. Additionally, you must show up within 40 minutes of the scheduled tournament match. If you fail to do so, your opponent has the right to disqualify you for not showing up.",
            inline=False
        )

        tournament_rules_embed.add_field(
            name=f"__Discord Forfeiting Limits__",
            value=f"Discord forfeiting is when you forfeit a game on discord; meaning when you do not play the match. Having up to two of these forfeits in this tournament will result in a temporary ban from all Tournament activities for upto two months. You will also be pulled out of the tournament.",
            inline=False
        )

        await interaction.response.send_message(
            embed=tournament_rules_embed,
            ephemeral=True
        )
    @discord.ui.button(label="Tournament Schedule", style=discord.ButtonStyle.blurple, emoji='📆', custom_id="persistent_view:tournament_dates")
    async def tournament_schedule(self, interaction: discord.Interaction, button: discord.ui.Button):

        get_information_embed = interaction.message.embeds[0].to_dict()
        get_information_embed_title = get_information_embed['title']
        tournament_type = get_information_embed_title[len("What "):len("What ___")]

        day_number = int
        match_results_channel = None
        if tournament_type == "1v1":
            day_number = 3
            match_results_channel = "<#1045926610328633425>"
        elif tournament_type == "2v2":
            day_number = 4
            match_results_channel = "<#1045926706055221330>"

        elif tournament_type == "3v3":
            day_number = 5
            match_results_channel = "<#1045926787382779984>"

        tournament_schedule_embed = discord.Embed(
            title=f"{tournament_type} Tournmanet Schedule",
            color=0x00ffff
        )

        tournament_schedule_embed.add_field(
            name=f"__When is the next {tournament_type} tournament?__",
            value=f"Tournament sign-ups open once the ongoing tournament finishes. This means {tournament_type} tournament participants are given {day_number} to reach out to their opponent, schedule a match, play their match, and submit a match in {match_results_channel} before the daily deadline of 10:00 pm EST. Failing to do so will result in a disqualification of both players unless your opponent is uncooperative, unavailable, etc. - contact the Head Match Staff to resolve the problem.",
            inline=False
        )

        tournament_schedule_embed.add_field(
            name=f"__What Are some tips to schedule a {tournament_type} tournament match?__",
            value="1. Know you and your team availabilities to schedule a match.\n2. Instead of being the person that asks your opponent for a time, give THEM a __list__ of free times that works for you and your team.",
            inline=False
        )

        await interaction.response.send_message(
            embed=tournament_schedule_embed, 
            ephemeral=True
        )
        
    @discord.ui.button(label="Sign-up Instructions", style=discord.ButtonStyle.blurple, emoji='🔢', custom_id="persistent_view:sign_up_instructions")
    async def sign_up_instructions(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        get_information_embed = interaction.message.embeds[0].to_dict()
        get_information_embed_title = get_information_embed['title']
        tournament_type = get_information_embed_title[len("What "):len("What ___")]

        command_name = ''
        sign_up_channel = ''
        if tournament_type == "1v1":
            command_name = "``/tournament application 1v1``"
            sign_up_channel = "<#1045927249825775647>"
        elif tournament_type == "2v2":
            command_name = "``/tournament application 2v2`` ``Team_Name:`` ``Team Captain:`` ``Team_Member_1:``  ``Team_Member_2: (optional)`` ``Team_Member_3: (optional)``"
            sign_up_channel = "<#1045927311842750486>"
        elif tournament_type == "3v3":
            command_name = "> ``/tournament application 3v3`` ``Team_Name:`` ``Team_Captain:`` ``Team_Co-Captain:`` ``Team_Member_1:`` ``Team_Member_2:`` ``Team_Member_3:`` ``Team_Member_4:``"
            sign_up_channel = "<#1045926787382779984>"

        sign_up_instructions_embed = discord.Embed(
            title=f"{tournament_type} Tournmanet Information",
            color=0x00ffff
        )

        sign_up_instructions_embed.add_field(
            name=f"__How do I sign-up for a {tournament_type} tournament?__",
            value=f"> 1. Have you and your team members verify your Roblox account by going to <#351057167706619914> and running the ``/verify`` slash command.\n\n> 2. Submit a {tournament_type} tournament application by going to <#351057167706619914> and running the {command_name} slash command.\n\n> 3. Ping yourself/your team members in {sign_up_channel} (#{tournament_type} Tournament Sign Ups) once sign-ups open.",
            inline=False
        )
        await interaction.response.send_message(
            embed=sign_up_instructions_embed, 
            ephemeral=True
        )

    @discord.ui.button(label="Map Selection Instructions", style=discord.ButtonStyle.blurple, emoji='🗺', custom_id="persistent_view:map_selection_instructions")
    async def map_selection_instructions(self, interaction: discord.Interaction, button: discord.ui.Button):

        get_information_embed = interaction.message.embeds[0].to_dict()
        get_information_embed_title = get_information_embed['title']
        tournament_type = get_information_embed_title[len("What "):len("What ___")]

        map_selection_instructions_embed = discord.Embed(
            title=f"{tournament_type} Tournmanet Map Selection",
            color=0x00ffff
        )

        map_selection_instructions_embed.add_field(
            name=f"__How do I choose what map to play on?__",
            value=f"Maps are chosen via randomization. This randomization is done by @The Conquerors 3 Bot using the ``/random map {tournament_type}`` slash command in <#351057167706619914>. If both parties agree to reroll the map, they may. However, if one party declines the reroll, that map __must__ be played.",
            inline=False
        )

        await interaction.response.send_message(
            embed=map_selection_instructions_embed,
            ephemeral=True
        )

    @discord.ui.button(label="Skill Divisions", style=discord.ButtonStyle.blurple, emoji='🗂', custom_id="persistent_view:skill_divisions")
    async def skill_divisions_information(self, interaction: discord.Interaction, button: discord.ui.Button):
        get_information_embed = interaction.message.embeds[0].to_dict()
        get_information_embed_title = get_information_embed['title']
        tournament_type = get_information_embed_title[len("What "):len("What ___")]

        skill_divisions = ''
        skill_division_counter = 0
        if tournament_type == "1v1":
            skill_divisions = "Scout, Light Soldier, Heavy Soldier and Juggernaut"
            skill_division_counter = 4
        elif tournament_type == "2v2":
            skill_divisions = "Scout, Middle and Juggernaut"
            skill_division_counter = 3
        elif tournament_type == "3v3":
            skill_divisions = "Scout and Juggernaut"
            skill_division_counter = 2

        skill_divisions_embed = discord.Embed(
            title=f"{tournament_type} Skill Divisions",
            color=0x00ffff
        )

        skill_divisions_embed.add_field(
            name=f"__What are the use of skill divisions?__",
            value=f"Skill divisions are used to separate players into balanced tournament brackets, giving everybody a fair chance to win.",
            inline=False
        )

        skill_divisions_embed.add_field(
            name=f"__How many skill divisions are there in {tournament_type} tournaments?__",
            value=f"{tournament_type} tournaments have {skill_division_counter} skill divisions. These divisions are: {skill_divisions}.",
            inline=False
        )

        skill_divisions_embed.add_field(
            name=f"__How do I move up a division?__",
            value=f"Players with no competitive experience are often placed in Scout Division. The only way to officially progress is by winning a tournament. Depending on your performance, a match staff may move you up a division if they see fit.",
            inline=False
        )

        await interaction.response.send_message(
            embed=skill_divisions_embed,
            ephemeral=True
        )

    @discord.ui.button(label="Prize List", style=discord.ButtonStyle.blurple, emoji='🏆', custom_id="persistent_view:prize_list")
    async def prize_list_information(self, interaction: discord.Interaction, button: discord.ui.Button):
        get_information_embed = interaction.message.embeds[0].to_dict()
        get_information_embed_title = get_information_embed['title']
        tournament_type = get_information_embed_title[len("What "):len("What ___")]

        scout_div_prize = ''
        light_soldier_div_prize = ''
        heavy_soldier_div_prize = ''
        juggernaut_div_prize = ''
        mid_div_prize = ''
        if tournament_type == "1v1":
            scout_div_prize = "**1st Place:** 7, 000 coins\n**2nd Place:** 4, 000 coins\n**3rd Place:** 500 coins"
            light_soldier_div_prize = "**1st Place:** 8, 000 coins\n**2nd Place:** 5, 000 coins\n**3rd Place:** 1, 000 coins"
            heavy_soldier_div_prize = "**1st Place:** 9, 000 coins\n**2nd Place:** 6, 000 coins\n**3rd Place:** 2, 000 coins"
            juggernaut_div_prize = "**1st Place:** 10, 000 coins\n**2nd Place:** 7, 000 coins\n**3rd Place:** 3, 000 coins"

        elif tournament_type == "2v2":
            scout_div_prize = "**1st Place:** 10, 000 coins\n**2nd Place:** 7, 000 coins\n**3rd Place:** 3, 000 coins"
            mid_div_prize = "**1st Place:** 11, 000 coins\n**2nd Place:** 8, 000 coins\n**3rd Place:** 3, 000 coins"
            juggernaut_div_prize = "**1st Place:** 12, 000 coins\n**2nd Place:** 9, 000 coins\n**3rd Place:** 4, 000 coins"

        elif tournament_type == "3v3":
            scout_div_prize = "**1st Place:** 13, 000 coins\n**2nd Place:** 9, 000 coins\n**3rd Place:** 4, 000 coins"
            juggernaut_div_prize = "**1st Place:** 15, 000 coins\n**2nd Place:** 10, 000 coins\n**3rd Place:** 5, 000 coins"

        prize_list_embed = discord.Embed(
            title=f"{tournament_type} Tournaments Prize List",
            color=0x00ffff
        )

        if ((tournament_type == "2v2") or 
        (tournament_type == "3v3")):
            prize_list_embed.add_field(
                name=f"**__Note:__**",
                value="Team captains distribute total coins",
                inline=False
            )

        prize_list_embed.add_field(
            name=f"__{tournament_type} Tournaments Scout Division Prize List:__",
            value=f"{scout_div_prize}",
            inline=False
        )

        if tournament_type == "1v1":
            prize_list_embed.add_field(
                name=f"__{tournament_type} Tournaments Light Soldier Division Prize List:__",
                value=f"{light_soldier_div_prize}",
                inline=False
            )

            prize_list_embed.add_field(
                name=f"__{tournament_type} Tournaments Heavy Soldier Division Prize List:__",
                value=f"{heavy_soldier_div_prize}",
                inline=False
            )
        
        elif tournament_type == "2v2":
            prize_list_embed.add_field(
                name=f"__{tournament_type} Tournaments Middle Division Prize List:__",
                value=f"{mid_div_prize}",
                inline=False
            )

        prize_list_embed.add_field(
            name=f"__{tournament_type} Tournaments Juggernaut Division Prize List:__",
            value=f"{juggernaut_div_prize}",
            inline=False
        )
    
        await interaction.response.send_message(
            embed=prize_list_embed,
            ephemeral=True
        )

class ParentTournamentInformationViews(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="1v1 Tournament Info", style=discord.ButtonStyle.blurple, custom_id="persistent_view:1v1_Tournaments")
    async def info_1v1(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"What 1v1 tournament information would you like to know more about?",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=information_embed, view=ChildTournamentInformationViews(), ephemeral=True)

    @discord.ui.button(label="2v2 Tournament Info", style=discord.ButtonStyle.blurple, custom_id="persistent_view:2v2_Tournaments")
    async def info_2v2(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"What 2v2 tournament information would you like to know more about?",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=information_embed, view=ChildTournamentInformationViews(), ephemeral=True)

    @discord.ui.button(label="3v3 Tournament Info", style=discord.ButtonStyle.blurple, custom_id="persistent_view:3v3_Tournaments")
    async def info_3v3(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"What 3v3 tournament information would you like to know more about?",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=information_embed, view=ChildTournamentInformationViews(), ephemeral=True)

class ParentGeneralInformationViews(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="FAQ", style=discord.ButtonStyle.blurple, custom_id="persistent_view:Discord_FAQ", emoji='❔')
    async def info_faq(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"Game FAQ or Discord FAQ",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=information_embed, view=ChildTournamentInformationViews(), ephemeral=True)

    @discord.ui.button(label="Story Information", style=discord.ButtonStyle.blurple, custom_id="persistent_view:Story_Information", emoji='📖')
    async def info_story(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"Story Information",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=information_embed, view=ChildTournamentInformationViews(), ephemeral=True)

    @discord.ui.button(label="Tournament Information", style=discord.ButtonStyle.blurple, custom_id="persistent_view:Tournament_Information", emoji='🏆')
    async def info_tournament(self, interaction: discord.Interaction, button: discord.ui.Button):
        await InformationEmbeds.tournament_embed_info(
            self, 
            interaction
        )

    @discord.ui.button(label="Suggestion Instructions", style=discord.ButtonStyle.blurple, custom_id="persistent_view:Suggestion_Instructions", emoji='🔢')
    async def info_suggestion(self, interaction: discord.Interaction, button: discord.ui.Button):
        information_embed = discord.Embed(
            title=f"What 3v3 tournament information would you like to know more about?",
            color=0x00ffff
        )
        await interaction.response.send_message(embed=information_embed, view=ChildTournamentInformationViews(), ephemeral=True)


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
            value="> To join a clan, direct message a Clan Leader or Co Leader that is looking for new members! You can find clan advertisements under <#1055586560919216218>."
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

    @commands.is_owner()
    @commands.command()
    async def general_information_embed(
        self, 
        ctx
    ):
        """Starts a persistent view."""
        information_embed = discord.Embed(
            title=f"Information",
            description=f"This section will cover everything there is to know about events at The Conquerors 3.",
            color=0x00ffff
        )

        information_embed.set_image(
            url="https://media.discordapp.net/attachments/501185430751019008/1025972287645691985/unknown.png?width=691&height=389"
        )
        
        await ctx.send(
            embed=information_embed, 
            view=ParentGeneralInformationViews()
        )

async def setup(bot):
    await bot.add_cog(InformationEmbeds(bot))