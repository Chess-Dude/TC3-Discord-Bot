import discord 

class DisbandClansClass(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Disband Clan", style=discord.ButtonStyle.red, emoji='🎮', custom_id="persistent_view:disband_clan")
    async def disband_clans_button(
        self, 
        interaction: discord.Interaction, 
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            content="loading..."
        )

        log_embed_message =  interaction.message
        log_embed = log_embed_message.embeds[0].to_dict()
        log_embed_fields = log_embed['fields']
        create_role_field = log_embed_fields[-1]
        clan_id = create_role_field["value"]

        clan_role = interaction.guild.get_role(int(clan_id))
        clan_leader_role = interaction.guild.get_role(1054999374993817700)
        clan_co_leader_role = interaction.guild.get_role(1054999381029429349)

        for member in clan_role.members:
            if clan_leader_role in member.roles: 
                await member.remove_roles(clan_leader_role)
            
            elif clan_co_leader_role in member.roles:
                await member.remove_roles(clan_co_leader_role)

            await member.remove_roles(clan_role)
        
        await clan_role.delete(reason=f"clan disbanded by {interaction.user.id}")

        await interaction.channel.send(
            content="Disbanded"
        )
