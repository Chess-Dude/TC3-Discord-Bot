import discord

class SkillDivisionDropdown(discord.ui.Select):
    def __init__(self):
        division_list = [
            discord.SelectOption(
                label="1v1 Tournaments Scout Division",
                description="The Players's Division is Scout",
                ),
            discord.SelectOption(
                label="1v1 Tournaments Light Soldier Division",
                description="The Players's Division is Light Soldier",
                emoji=None
                ),
            discord.SelectOption(
                label="1v1 Tournaments Heavy Soldier Division",
                description="The Players's Division is Heavy Soldier",
                emoji=None
                ),
            discord.SelectOption(
                label="1v1 Tournaments Juggernaut Division",
                description="The Players's Division is Juggernaut",
                emoji=None
                ), 
            discord.SelectOption(
                label="Reject Application",
                description="Reject The Application",
                emoji=None
                )                
            ]

        super().__init__(placeholder="Choose the player's division...", options=division_list, custom_id="one_day_tourney_signups_dropdown", min_values=1, max_values=1)

    async def callback(
        self, 
        interaction: discord.Interaction,
    ):
        ec_role = interaction.guild.get_role(475669961990471680)
        if ec_role in interaction.user.roles:
            await interaction.response.send_message(f"loading...")
            if self.values[0] != "Reject Application":
                signup_embed = interaction.message.embeds[0].to_dict()
                user_signingup = interaction.message.content
                signup_values = signup_embed['fields']
                roblox_username_field = signup_values[0]
                roblox_username = roblox_username_field['value']

                user = interaction.guild.get_member(int(user_signingup.replace("<@", "").replace(">", "")))
                roblox_username = roblox_username.replace('`', '')

                if self.values[0] == "1v1 Tournaments Scout Division":
                    division_role_id = 1047716452599353435
                
                elif self.values[0] == "1v1 Tournaments Light Soldier Division":
                    division_role_id = 1047716972298772490
                
                elif self.values[0] == "1v1 Tournaments Heavy Soldier Division":
                    division_role_id = 1047716743138787378

                elif self.values[0] == "1v1 Tournaments Juggernaut Division":
                    division_role_id = 1047716977772335174

                else:
                    interaction.response.send_message("Error Occured in Skill DivisionDropdown @Mind Gamer")
                    return
            
                finalized_signups = interaction.guild.get_channel(1088641192331329628)
                competitor_role = interaction.guild.get_role(690624687004319804)
                normal_tournament_role = interaction.guild.get_role(1047716260185653298)
                division_role = interaction.guild.get_role(division_role_id)

                await user.add_roles(competitor_role)
                await user.add_roles(normal_tournament_role)
                await user.add_roles(division_role)

                await finalized_signups.send(content=str(user))

                finalized_embed = discord.Embed(
                    title=f"Your sign-up was accepted by {interaction.user.name}",
                    description=f"You were placed in: ``{division_role.name}``",
                    color=0x00ffff
                )

                await user.send(
                    embed=finalized_embed
                )       

                await interaction.channel.send(
                    f"{interaction.user.mention} placed {user.name} in: ``{division_role.name}``.", 
                )
                await interaction.message.edit(view=None)

            else:
                await interaction.channel.send(f"{interaction.user.mention} rejected the application")

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

class SkillDivisionDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SkillDivisionDropdown())
