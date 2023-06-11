import discord
from .reviewStrategies import ReviewStrategies

class StrategyModal(discord.ui.Modal, title="TC3 Strategy Form"):
    game_mode = discord.ui.TextInput(
        label="What game mode is your strategy for?",
        style=discord.TextStyle.short,
        placeholder="Game mode Here (1v1/2v2/3v3)...",
        required=True,
        min_length=3,
        max_length=3
    )
    
    map_name = discord.ui.TextInput(
        label="What map is your strategy for?",
        style=discord.TextStyle.short,
        placeholder="Map Name here...",
        required=True,
        min_length=3,
        max_length=50
    )

    explanation = discord.ui.TextInput(
        label="Explanation of Strategy",
        style=discord.TextStyle.long,
        placeholder="Explanation Here...",
        required=True,
        min_length=50,
        max_length=4000
    )

    links_1 = discord.ui.TextInput(
        label="Image of plan/path (link)",
        style=discord.TextStyle.short,
        placeholder="Insert Link Here...",
        required=True,
        min_length=0,
        max_length=200
    )

    async def on_submit(
        self, 
        interaction: discord.Interaction
    ):

        all_strategies_thread = interaction.guild.get_channel_or_thread(1048729690866724956)
        strategy_review = interaction.guild.get_channel(1048772041232371802)

        strategy_embed = discord.Embed(
            title=f"{interaction.user.display_name}'s {self.game_mode.value} {self.map_name.value} strategy",
            description=f"{self.explanation.value}",
            color=0x00ffff
        )
        
        strategy_embed.set_author(
            name=f"Strategized by: {interaction.user.display_name}", 
            icon_url=interaction.user.display_avatar.url
        )

        strategy_embed.timestamp = interaction.created_at

        strategy_embed.add_field(
            name="Links",
            value=f"{self.links_1.value}",
            inline=False
        )

        strategy_embed.set_image(
            url=self.links_1.value
        )
              
        strategy_embed.set_footer(
            text=f"The Conquerors 3 Strategies",
            icon_url=interaction.guild.icon
        )

        strategy_embed.set_thumbnail(
            url=interaction.user.display_avatar.url
        )

        await all_strategies_thread.edit(archived=False)
        msg = await all_strategies_thread.send(embed=strategy_embed)

        view = ReviewStrategies()

        await strategy_review.send(embed=strategy_embed, view=view)
        thumbs_up = '\U0001F44D'
        thumbs_down = '\U0001f44e'

        await msg.add_reaction(thumbs_up)
        await msg.add_reaction(thumbs_down)

        success_embed=discord.Embed(
            title="Strategy Submitted", 
            description=f"{interaction.user.mention} Thanks for submitting your strategy!", 
            color=0x00ffff
        )

        await interaction.response.send_message(embed=success_embed)
        