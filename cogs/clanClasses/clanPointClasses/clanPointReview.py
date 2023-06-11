import discord, json

class ReviewClanPoints(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def update_leaderboard(
        self,
        clan_lb_channel,
        clan_lb_message_id,
        clan_points,
        clan_role_name
    ):
        clan_lb_message = await clan_lb_channel.fetch_message(clan_lb_message_id)

        clan_lb_embed = clan_lb_message.embeds[0].to_dict()
        all_clan_points = clan_lb_embed['description']

        # Split the input string into a list of strings
        clan_point_list = all_clan_points.split("\n")

        # Create a list of tuples from the list of strings
        clan_list_list = []
        for clan_item in clan_point_list:
            clan, lb_clan_points = clan_item.split(" - ")
            clan_list_list.append([clan, int(lb_clan_points)])

        for iteration, clan in enumerate(clan_list_list):
            clan_name = clan[0].split(' ')
            clan_name = list(filter(lambda x: x != '', clan_name))
            if clan_name == clan_role_name:
                clan[1] = int(clan[1]) + int(clan_points)
                break

        # Sort the list of lists in ascending order by the number following the clan's name
        sorted_list_list = sorted(clan_list_list, key=lambda x: x[1])

        # Reverse the sorted list of tuples
        reversed_tuple_list = reversed(sorted_list_list)

        # Create a list of strings from the reversed list of tuples
        sorted_strings = []
        for clan, lb_clan_points in reversed_tuple_list:
            sorted_strings.append(f"{clan} - {lb_clan_points}")

        # Join the list of strings into a single string
        result = "\n".join(sorted_strings)

        return result

    def update_data(
        self, 
        users, 
        user
    ):
        if f'{user.id}' not in users:
            users[f'{user.id}'] = {}
            users[f'{user.id}']['clan_points'] = 0

        with open("clanPointsTracker.json", "w") as f:
            json.dump(users, f)

    def add_clan_points(
        self,
        users, 
        user, 
        clan_points
    ):
        current_clan_points = users[f'{user.id}']['clan_points']    
        new_clan_points = int(current_clan_points) + int(clan_points)
    
        users[f'{user.id}']['clan_points'] = new_clan_points

        with open("clanPointsTracker.json", "w") as f:
            json.dump(users, f)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, emoji='✅', custom_id="persistent_view:approve_cp_sub")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        word_list = interaction.message.content.split(' ')
        clan_points = word_list[0]
        clan_role_name = word_list[1:len(word_list)+1]
        clan_lb_channel_1 = interaction.guild.get_channel(1050289500783386655)

        new_weekly_result = await ReviewClanPoints.update_leaderboard(
            self=self,
            clan_lb_channel=clan_lb_channel_1,
            clan_lb_message_id=1056413563209650228,  
            clan_points=clan_points,
            clan_role_name=clan_role_name
        )

        new_weekly_clan_lb = discord.Embed(
            title="Clan Point Weekly Leaderboard",
            description=new_weekly_result,
            color=0x00ffff,
            timestamp=interaction.created_at
        )

        log_embed = interaction.message.embeds[0].to_dict()
        embed_author = log_embed['author']
        user_id = embed_author['name']
        member = interaction.guild.get_member(int(user_id))

        with open('clanPointsTracker.json', 'r') as f:
            users = json.load(f)

        ReviewClanPoints.update_data(
            self,
            users=users, 
            user=member
        )

        ReviewClanPoints.add_clan_points(
            self,
            users=users, 
            user=member, 
            clan_points=clan_points
        )

        clan_weekly_lb_message = await clan_lb_channel_1.fetch_message(1056413563209650228) 
        await interaction.response.send_message(content=f"Approved by: {interaction.user.mention}")
        await clan_weekly_lb_message.edit(embed=new_weekly_clan_lb)
        await interaction.message.edit(view=None)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji='❌', custom_id="persistent_view:reject_cp_sub")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.edit(view=None)
        await interaction.response.send_message(content=f"Rejected by: {interaction.user.mention}")

