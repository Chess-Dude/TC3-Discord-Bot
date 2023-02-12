import discord, datetime
from discord import app_commands
from discord.ext import commands

class ReviewStrategies(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, emoji='✅', custom_id="persistent_view:approve_strategy")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        featured_strategies_channel = interaction.guild.get_channel_or_thread(1048729826871230484)
        strategy_embed = interaction.message.embeds[0].to_dict()
        footer_dictionary = dict(strategy_embed["footer"])
        thumbnail_dictionary = dict(strategy_embed["thumbnail"])
        author_dictionary = dict(strategy_embed["author"])

        new_strategy_embed = discord.Embed(
            title=strategy_embed["title"], 
            colour=strategy_embed["color"], 
            timestamp=interaction.created_at
        )

        try:
            image_dictionary = dict(strategy_embed["image"])                
            new_strategy_embed.set_image(url=image_dictionary["url"])
        except:
            pass
        
        new_strategy_embed.description = (f"{strategy_embed['description']}")
        new_strategy_embed.set_author(name=author_dictionary["name"], icon_url=author_dictionary["icon_url"])
        new_strategy_embed.set_thumbnail(url=thumbnail_dictionary["url"])
        new_strategy_embed.set_footer(text=footer_dictionary["text"], icon_url=footer_dictionary["icon_url"])
        await featured_strategies_channel.send(embed=new_strategy_embed)

        await interaction.message.delete()

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji='❌', custom_id="persistent_view:reject_strategy")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()

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
            url=interaction.user.avatar.url
        )

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
        
class StrategyCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def bots_channels(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 351057167706619914

    is_bots = app_commands.check(bots_channels)

    @is_bots
    @app_commands.guilds(350068992045744141)
    @app_commands.command(
        name="strategize",
        description="A Command that allows you to submit a strategy for TC3!")
    async def strategize(
        self,
        interaction:discord.Interaction
    ):
        await interaction.response.send_modal(StrategyModal())
        
async def setup(bot):
    await bot.add_cog(StrategyCommands(bot))
