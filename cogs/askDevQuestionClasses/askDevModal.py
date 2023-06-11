import discord

class AskQuestionsModal(discord.ui.Modal, title="Ask Brokenbone!"):
    question = discord.ui.TextInput(
        label="Question to ask BrokenBone:",
        style=discord.TextStyle.long,
        placeholder="Question Here...",
        required=True,
        min_length=10,
        max_length=100
    )

    async def on_submit(
        self, 
        interaction: discord.Interaction
        ):

            log_channel = interaction.guild.get_channel(1087582528883392553)
            server_name = "The Conquerors 3"

            log_embed = discord.Embed(
                title=f"Question:",
                description=f"{self.question.value}",
                color=0x00ffff
                )
            
            log_embed.set_author(
                name=f"Submitted by: {interaction.user.display_name}", 
                icon_url=interaction.user.display_avatar.url)
            
            log_embed.timestamp = interaction.created_at
        
            log_embed.set_footer(
                text=f"Ask BrokenBone a Question!",
                icon_url=interaction.guild.icon
            )

            log_embed.set_thumbnail(
                url=interaction.user.display_avatar.url
            )

            msg = await log_channel.send(embed=log_embed)

            thumbs_up = '\U0001F44D'
            thumbs_down = '\U0001f44e'

            await msg.add_reaction(thumbs_up)
            await msg.add_reaction(thumbs_down)

            success_embed=discord.Embed(
                title="Question Submitted", 
                description=f"{interaction.user.mention} Thanks for submitting your question!", 
                color=0x00ffff
                )

            await interaction.response.send_message(embed=success_embed)
