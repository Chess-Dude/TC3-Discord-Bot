import discord

class TournamentSignupModalReview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, emoji='✅', custom_id="persistent_view:approve_sign_up")
    async def approve_sign_up(
        self, 
        interaction: discord.Interaction, 
        button: discord.ui.Button
    ):
        ec_role = interaction.guild.get_role(475669961990471680)
        if ec_role in interaction.user.roles:
            signup_embed = interaction.message.embeds[0].to_dict()
            user_signingup = interaction.message.content
            signup_values = signup_embed['fields']
            roblox_username_field = signup_values[0]
            roblox_username = roblox_username_field['value']

            user = interaction.guild.get_member(int(user_signingup.replace("<@", "").replace(">", "")))
            roblox_username = roblox_username.replace('`', '')

            finalized_signups = interaction.guild.get_channel(1088641192331329628)
            competitor_role = interaction.guild.get_role(690624687004319804)
            normal_tournament_role = interaction.guild.get_role(1047716260185653298)

            await user.add_roles(competitor_role)
            await user.add_roles(normal_tournament_role)
            await finalized_signups.send(
                content=f"{user.name}{user.discriminator}"
            )

            finalized_embed = discord.Embed(
                title=f"Your sign-up was accepted by {interaction.user.name}",
                color=0x00ffff
            )

            await user.send(
                embed=finalized_embed
            )       

            await interaction.response.send_message(
                "Added to finalized-signups", 
                ephemeral=True
            )
            
            await interaction.message.edit(
                view=None
                )

        else:
            error_embed = discord.Embed(
                title="Error: You do not have the Event Committee Role.",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
                    
    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji='🛑', custom_id="persistent_view:reject_sign_up")
    async def reject_signup(
        self, 
        interaction: 
        discord.Interaction, 
        button: discord.ui.Button
    ):
        ec_role = interaction.guild.get_role(475669961990471680)
        if ec_role in interaction.user.roles:

            user_redeeming = interaction.message.content
            user = interaction.guild.get_member(int(user_redeeming.replace("<@", "").replace(">", "")))

            rejection_embed = discord.Embed(
                title=f"Your sign-up was denied by {interaction.user.name}",
                color=0x00ffff
            )

            await user.send(
                embed=rejection_embed
            )       

            await interaction.message.edit(
                view=None
            )

        else:
            error_embed = discord.Embed(
                title="Error: You do not have the Event Committee Role. Please try again.",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
