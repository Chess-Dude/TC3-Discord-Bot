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
            color=0xff0000
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
            
        strategy_embed.add_field(
            name="**Votes**",
            value=f"Upvotes: 0 ``0%``\nDownvotes: 0 ``0%``",
            inline=False
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
            color=0xff0000
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

    async def update_votes(
        self,
        payload
    ):        
        TC3 = self.bot.get_guild(350068992045744141)
        all_strat_thread = TC3.get_thread(1048729690866724956)

        tc3_bot = self.bot.get_user(953017055236456448)
        if payload.user_id != tc3_bot.id:
            if payload.channel_id == all_strat_thread.id:
                strategy_message = await all_strat_thread.fetch_message(payload.message_id)
                if strategy_message.author.id == tc3_bot.id: 
                    for reaction in strategy_message.reactions:
                        if str(reaction.emoji) == '👍':
                            user_upvote_list = [user async for user in reaction.users()]
                        
                        elif str(reaction.emoji) == '👎': 
                            user_downvote_list = [user async for user in reaction.users()]
                    user_upvote_list, user_downvote_list = list(set(user_upvote_list).difference(user_downvote_list)), list(set(user_downvote_list).difference(user_upvote_list))

                    total_thumbs_up = len(user_upvote_list)
                    total_thumbs_down = len(user_downvote_list)
                    total_reactions = total_thumbs_up + total_thumbs_down
                    try:
                        total_upvote_percentage = round((total_thumbs_up / total_reactions) * 100, 2)
                        total_downvote_percentage = round(((total_thumbs_down / total_reactions) * 100), 2)
                    except ZeroDivisionError:
                        return 0
                    
                    strategy_embed = strategy_message.embeds[0].to_dict()
                    footer_dictionary = dict(strategy_embed["footer"])
                    thumbnail_dictionary = dict(strategy_embed["thumbnail"])
                    author_dictionary = dict(strategy_embed["author"])
                    timestamp_dictionary = strategy_embed["timestamp"]

                    new_strategy_embed = discord.Embed(title=strategy_embed["title"], colour=strategy_embed["color"], timestamp=datetime.datetime.utcnow())

                    try:
                        image_dictionary = dict(strategy_embed["image"])                
                        new_strategy_embed.set_image(url=image_dictionary["url"])
                    except:
                        pass
                    
                    new_strategy_embed.description = (f"{strategy_embed['description']}")
                    new_strategy_embed.add_field(name="**Votes**", value=f"Upvotes: {total_thumbs_up} ``{total_upvote_percentage}%``\nDownvotes: {total_thumbs_down} ``{total_downvote_percentage}%``")
                    new_strategy_embed.set_author(name=author_dictionary["name"], icon_url=author_dictionary["icon_url"])
                    new_strategy_embed.set_thumbnail(url=thumbnail_dictionary["url"])
                    new_strategy_embed.set_footer(text=footer_dictionary["text"], icon_url=footer_dictionary["icon_url"])
                    await strategy_message.edit(embed=new_strategy_embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        await StrategyCommands.update_votes(
            self=self,
            payload=payload
        )

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        await StrategyCommands.update_votes(
            self=self,
            payload=payload
        )
        
async def setup(bot):
    await bot.add_cog(StrategyCommands(bot))
