import discord, json

class ReviewClanPoints(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

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

        log_embed = interaction.message.embeds[0].to_dict()
        embed_author = log_embed['author']
        user_id = embed_author['name']
        member = interaction.guild.get_member(int(user_id))

        # ReviewClanPoints.update_data(
        #     self,
        #     user=member
        # )

        # ReviewClanPoints.add_clan_points(
        #     self,
        #     user=member, 
        #     clan_points=clan_points
        #)

        await interaction.response.send_message(content=f"Approved by: {interaction.user.mention}")
        await interaction.message.edit(view=None)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji='❌', custom_id="persistent_view:reject_cp_sub")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.edit(view=None)
        await interaction.response.send_message(content=f"Rejected by: {interaction.user.mention}")

