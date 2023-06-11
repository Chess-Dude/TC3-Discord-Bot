import discord

class SuggestionModal(discord.ui.Modal, title="Suggestion Form"):
    name = discord.ui.TextInput(
        label="What is your suggestion?",
        style=discord.TextStyle.short,
        placeholder="Suggestion Title Here...",
        required=True,
        min_length=10,
        max_length=50
    )

    explanation = discord.ui.TextInput(
        label="Explanation of Suggestion",
        style=discord.TextStyle.long,
        placeholder="Explanation Here...",
        required=True,
        min_length=100,
        max_length=1000
    )

    description = discord.ui.TextInput(
        label="Why should your suggestion be added?",
        style=discord.TextStyle.long,
        placeholder="Suggestion Description Here...",
        required=True,
        min_length=50,
        max_length=500
    )

    links_1 = discord.ui.TextInput(
        label="1st link to media",
        style=discord.TextStyle.short,
        placeholder="Insert Link Here...",
        required=False,
        min_length=0,
        max_length=100
    )

    links_2 = discord.ui.TextInput(
        label="2nd link to media",
        style=discord.TextStyle.short,
        placeholder="Insert Link Here...",
        required=False,
        min_length=0,
        max_length=100
    )

    async def on_submit(
        self, 
        interaction: discord.Interaction
        ):

            if interaction.guild.id == 350068992045744141: 
                suggestion_channel = interaction.guild.get_channel(351057661925654528)
                server_name = "The Conquerors 3"
            else:
                suggestion_channel = interaction.guild.get_channel(724424911791325214)
                server_name = "The Conquerors Games"

            suggestion_embed = discord.Embed(
                title=f"{self.name.value}",
                description=f"**Explanation of Suggestion**\n{self.explanation.value}\n\n**Why should your suggestion be added?**\n{self.description.value}\n\n**Links**\n{self.links_1.value}\n{self.links_2.value}",
                color=0x00ffff
                )
            
            suggestion_embed.set_author(
                name=f"Suggested by: {interaction.user.display_name}", 
                icon_url=interaction.user.display_avatar.url)
            
            suggestion_embed.timestamp = interaction.created_at
            
            try:
                if len(self.links_1.value) == 0:
                    suggestion_embed.set_image(
                        url=self.links_2.value
                    )
                else:
                    suggestion_embed.set_image(
                        url=self.links_1.value
                    )
            
            except:
                await interaction.response.send_message("please ensure that your link is an /http/https.")
                return            

            suggestion_embed.set_footer(
                text=f"{server_name} Suggestions",
                icon_url=interaction.guild.icon
            )

            suggestion_embed.set_thumbnail(
                url=interaction.user.display_avatar.url
            )

            try:
                msg = await suggestion_channel.send(embed=suggestion_embed)

                await msg.create_thread(name=f"{self.name.value}")

                thumbs_up = '\U0001F44D'
                thumbs_down = '\U0001f44e'

                await msg.add_reaction(thumbs_up)
                await msg.add_reaction(thumbs_down)


            except discord.HTTPException:
                failed_embed=discord.Embed(
                    title="Error: Your suggestion is over 1024 characters.", 
                    description=f"{interaction.user.mention} Please shorten your suggestion and try again.", 
                    color=0x00ffff
                    )

                await interaction.response.send_message(
                    embed=failed_embed
                )
                return 
            
            success_embed=discord.Embed(
                title="Suggestion Accepted", 
                description=f"{interaction.user.mention} Thanks for submitting your suggestion!", 
                color=0x00ffff
                )

            await interaction.response.send_message(embed=success_embed)
        