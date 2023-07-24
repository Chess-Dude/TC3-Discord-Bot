import discord
from .bugModalReview import BugModalReview

class TC3BugModal(discord.ui.Modal, title="The Conquerors 3 Bug Report"):

    bug_explanation = discord.ui.TextInput(
        label="Explain in detail the bug you encountered.",
        style=discord.TextStyle.long,
        placeholder="Bug Explanation Here...",
        required=True,
        min_length=25,
        max_length=1000
    )

    linked_media = discord.ui.TextInput(
        label="Provide any links to medias (preferred)",
        style=discord.TextStyle.long,
        placeholder="Media link...",
        required=False,
        min_length=25,
        max_length=1000
    )

    async def on_submit(
        self, 
        interaction: discord.Interaction
    ):      
        ws_role = interaction.guild.get_role(351075254912811020)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ws_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True),
        }

        bug_category = discord.utils.get(
            interaction.guild.categories, 
            id=720695144952627251
        )

        ticket_channel = await interaction.guild.create_text_channel(
            name=f"{interaction.user.display_name}", 
            overwrites=overwrites, 
            category=bug_category
        )

        bug_embed = discord.Embed(
            title=f"The Conquerors 3 Bug Report.",
            description=f"{self.bug_explanation.value}",
            color=0x2f3136
        )
        
        bug_embed.set_author(
            name=f"Bug Reported By: {interaction.user.nick}", 
            icon_url=interaction.user.display_avatar.url
        )
        
        bug_embed.timestamp = interaction.created_at
        
        bug_embed.set_footer(
            text=f"The Conquerors 3 Bug Report",
            icon_url=interaction.guild.icon
        )

        bug_embed.set_thumbnail(
            url=interaction.user.display_avatar.url
        )


        link = self.linked_media.value
        if len(self.linked_media.value) == 0: 
            link = "N/A"

        bug_embed.add_field(
            name="Attached Files/Links:",
            value=f"``{link}``",
            inline=False
        )

        await ticket_channel.send(
            content=f"{interaction.user.mention} is reporting a bug {ws_role.mention}!",
            embed=bug_embed,
            view=BugModalReview()
        )
        
        await ticket_channel.send(content=f"{self.linked_media.value}")

        approved_embed = discord.Embed(
            title=f"Approved: Created {ticket_channel}.",
            color=0x2f3136
        )

        await interaction.response.send_message(
            embed=approved_embed,
            ephemeral=True
        )