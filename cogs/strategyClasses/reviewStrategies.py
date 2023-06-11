import discord

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
        await featured_strategies_channel.edit(archived=False)
        await featured_strategies_channel.send(embed=new_strategy_embed)

        await interaction.message.delete()

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji='❌', custom_id="persistent_view:reject_strategy")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
