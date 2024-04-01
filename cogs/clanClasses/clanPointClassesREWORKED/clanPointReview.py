import discord

class ReviewClanPoints(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    async def add_clan_points(
        self,
        user_id, 
        clan_points,
        clan_role_id
    ):
        async with self.bot.pool.acquire() as connection: # we cant use self.bot.pool here. need to think of a way (possibly import?)
            sql = "UPDATE ClanPointTracker SET totalClanPoints = totalClanPoints + $1 WHERE discordUserID = $2"
            await connection.execute(sql, int(clan_points), int(user_id))

            sql = """
                UPDATE clanpointleaderboard 
                SET weeklyClanPoints = weeklyClanPoints + $1, yearlyClanPoints = yearlyClanPoints + $2 
                WHERE clanRoleID = $3
            """
            await connection.execute(sql, int(clan_points), int(clan_points), clan_role_id)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, emoji='✅', custom_id="persistent_view:approve_cp_sub")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        word_list = interaction.message.content.split(' ')
        clan_points = word_list[0]
        clan_role_id = int(word_list[1])

        log_embed = interaction.message.embeds[0].to_dict()
        embed_author = log_embed['author']
        user_id = embed_author['name']
        member = interaction.guild.get_member(int(user_id))

        await self.add_clan_points(
            user_id=user_id, 
            clan_points=clan_points,
            clan_role_id=clan_role_id
        )

        await interaction.response.send_message(content=f"Approved by: {interaction.user.mention}")
        await interaction.message.edit(view=None)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji='❌', custom_id="persistent_view:reject_cp_sub")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.edit(view=None)
        await interaction.response.send_message(content=f"Rejected by: {interaction.user.mention}")
