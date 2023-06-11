import discord


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