import discord
from .skillDivsionDropdown import SkillDivisionDropdownView
# from .tournamentSignupModalReview import TournamentSignupModalReview
from .errorHandlers import NotFree, FailedToUnderstandGuidelines

class TournamentSignupModal(discord.ui.Modal, title="Tournament Sign-up"):
    rblx_name = discord.ui.TextInput(
        label="What is your ROBLOX Username?",
        style=discord.TextStyle.short,
        placeholder="ROBLOX username Here...",
        required=True,
        min_length=3,
        max_length=20
    )

    available = discord.ui.TextInput(
        label="Free during 2:00pm-4:00pm (EST)? (Y/N)",
        style=discord.TextStyle.short,
        placeholder="Yes/No Here...",
        required=True,
        min_length=1,
        max_length=3
    )

    understand_guideline = discord.ui.TextInput(
        label="Understand the rules of the event? (Y/N)",
        style=discord.TextStyle.short,
        placeholder="Yes/No Here...",
        required=True,
        min_length=1,
        max_length=3
    )

    backup_player = discord.ui.TextInput(
        label="Would you like to be a backup player? (Y/N)",
        style=discord.TextStyle.short,
        placeholder="Yes/No Here...",
        required=True,
        min_length=1,
        max_length=3
    )

    async def on_submit(
        self, 
        interaction: discord.Interaction
    ):
        one_day_tourney_role = interaction.guild.get_role(690624687004319804)
        await interaction.user.add_roles(one_day_tourney_role)

        try:
            if ((self.backup_player.value.lower() == "yes") or 
                (self.backup_player.value.lower() == 'y')):
                backup_role = interaction.guild.get_role(695683985510236220)
                await interaction.user.add_roles(backup_role)

            if ((self.available.value.lower() == "no") or 
                (self.available.value.lower() == 'n')):
                raise NotFree      

            if ((self.understand_guideline.value.lower() == "no") or 
                (self.understand_guideline.value.lower() == 'n')):
                raise FailedToUnderstandGuidelines

            color = 0x00ffff

        except NotFree:
            error_embed = discord.Embed(
                title="Error: Your sign-up was rejected due to you not being available to attend the event.",
                color=0x00ffff
            )
            
            color = 0xFF0000
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )

        
        except FailedToUnderstandGuidelines:
            error_embed = discord.Embed(
                title="Your sign-up was accepted however please clarify the guidelines/rules with a staff member.",
                color=0x00ffff
            )

            color = 0xFF0000            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )

        signup_embed = discord.Embed(
            title=f"{self.rblx_name.value}",
            color=color
        )
        
        signup_embed.set_author(
            name=f"Sign-up For: {interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url
        )
        
        signup_embed.timestamp = interaction.created_at
        
        signup_embed.set_footer(
            text=f"The Conquerors 3",
            icon_url=interaction.guild.icon
        )

        signup_embed.set_thumbnail(
            url=interaction.user.display_avatar.url
        )

        signup_embed.add_field(
            name=f"``What is your ROBLOX username?``",
            value=f"``{self.rblx_name.value}``",
            inline=False
        )

        signup_embed.add_field(
            name="``Are you available during 2:00pm-4:00pm (EST) (Y/N)``",
            value=f"``{self.available.value}``",
            inline=False
        )

        signup_embed.add_field(
            name="``Do you understand the rules for the event? (Y/N)``",
            value=f"``{self.understand_guideline.value}``",
            inline=True
        )

        signup_embed.add_field(
            name="``Are you a backup player? (Y/N)``",
            value=f"``{self.backup_player.value}``",
            inline=False
        )

        signup_channel = interaction.guild.get_channel(1015670142656581742)
        msg = await signup_channel.send(
            content=f"{interaction.user.mention}",
            embed=signup_embed,
            view=SkillDivisionDropdownView()
        )

        if ((self.available.value.lower() == "no") or 
            (self.available.value.lower() == 'n')):
            return      

        if ((self.understand_guideline.value.lower() == "no") or 
            (self.understand_guideline.value.lower() == 'n')):
            return
        
        approved_embed = discord.Embed(
            title=f"Approved Sign-up.",
            description=f"[Jump To Message]({msg.jump_url})",
            color=0x00ffff,
        )

        await interaction.response.send_message(
            embed=approved_embed,
            ephemeral=True
        )
