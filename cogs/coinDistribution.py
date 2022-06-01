import discord, datetime
import discord.reaction
from discord.ext import commands
from discord import Interaction, ui

class Yes(discord.ui.View):
    @discord.ui.button(label="yes", style=discord.ButtonStyle.green)
    async def count(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Make sure to update the message with our updated selves
        await interaction.response.send_message("yes")

    @discord.ui.button(label="no", style=discord.ButtonStyle.red)
    async def count(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Make sure to update the message with our updated selves
        await interaction.response.send_message("no")


class PrizeDistribution(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.hmsPing = '<@&665951855888826369> <@&908145456171855912>'

    def bots(ctx):
        return ctx.channel.id == 941567353672589322 or ctx.channel.id == 408820459279220736 or ctx.channel.id == 896440473659519057 

    def createInfoEmbed(self, infoMessage : discord.Message):

        embed = discord.Embed(description = infoMessage.content, color = 0xff0000)
        embed.add_field(name = '**Jump**', value = f'[Go to message!]({infoMessage.jump_url})')
        embed.set_footer(text = f'#{infoMessage.channel.name}')
        embed.timestamp = infoMessage.created_at
        embed.set_author(name = infoMessage.author.display_name, icon_url = infoMessage.author.avatar.url)
        return embed

    isTcgBots = commands.check(bots)

    @isTcgBots
    @commands.has_any_role(896542577296306217, 896550746475077672, 716290546519244850, 649683977241886730)
    @commands.command(aliases = ["cd"])
    async def coindistribution(self, ctx, *, args = None):

        if args == None:
            instructions = discord.utils.get(ctx.guild.channels, id = 408820459279220736)
            infoMessage = await instructions.fetch_message(949151674323337286)

            embed = self.createInfoEmbed(infoMessage)
            await ctx.message.reply(content = "Missing information, please read:", embed = embed, mention_author = True)
            return

        successEmbed = discord.Embed(title='Head And Vice Head Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your coin distribution!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = True)
        
        coinDistribtuionChannel = discord.utils.get(ctx.guild.channels, id = 945447870243422299)
        
        # approveButton = discord.ui.Button(label="Approve", style=discord.ButtonStyle.green)
        # rejectButton = discord.ui.Button(label="Reject", style=discord.ButtonStyle.red);

        # view = ui.View()
        # view.add_item(approveButton)
        # view.add_item(rejectButton)
        
        logEmbed = discord.Embed(title = f"The Conquering Games Coin Distribution",description=f"**Distribution**\n{args}", color=0xff0000)
        logEmbed.set_author(name=f"Submitted by: {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        logEmbed.timestamp = ctx.message.created_at
        msg = await coinDistribtuionChannel.send(self.hmsPing, embed = logEmbed) #, view=view)

        # interaction = await self.bot.wait_for("button_click", check = lambda i: i.custom_id == "button1")
        # if approveButton.callback:
        #     print("approve message")
        
        # if rejectButton.callback:
        #     print("reject message")
        
        # await msg.add_reaction('✅')
        # await msg.add_reaction('❌')

        # Should later be made into a lambda function
        def check(r, u):
            return str(r.emoji) in "✅❌"
        
        reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=None)
        
        if str(reaction.emoji) == '✅':
            coinsApprovedEmbed = discord.Embed(title='Your Coins Are Now Validated!', description=f"{ctx.author.mention} Direct message the <@!731872828474916934> to recieve your prize!", color=0xff0000)
            await ctx.message.reply(embed = coinsApprovedEmbed, mention_author = True)
            
            TC3RC = self.bot.get_guild(676112926918049813)
            latestPrizes = discord.utils.get(TC3RC.channels, id = 732411044886216715)
            await latestPrizes.send(embed = logEmbed, mention_author = True)

        if str(reaction.emoji) == '❌': 
            coinsRejectedEmbed = discord.Embed(title='Your Coins Were Rejected!', description=f"{ctx.author.mention} Please recheck your total coin distribution and or format. Then resubmit your coin distribution again.", color=0xff0000)
            await ctx.message.reply(embed = coinsRejectedEmbed, mention_author = True)
    
    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
    #     TCG = self.bot.get_guild(371817692199518240)
    #     coin_distribution_channel = discord.utils.get(TCG.channels, id=945447870243422299)
    #     tc3_bot = self.bot.get_user(953017055236456448)
    #     if payload.channel_id == coin_distribution_channel.id:
    #         coin_distribution_log = await coin_distribution_channel.fetch_message(payload.message_id)
    #         if coin_distribution_log.author.id == tc3_bot.id: 
    #             for reaction in coin_distribution_log.reactions:
    #                 if str(reaction.emoji) == '✅':
    #                     user_upvote_list = [user async for user in reaction.users()]
                    
    #                 elif str(reaction.emoji) == '❌': 
    #                     user_downvote_list = [user async for user in reaction.users()]
    #             user_upvote_list, user_downvote_list = list(set(user_upvote_list).difference(user_downvote_list)), list(set(user_downvote_list).difference(user_upvote_list))

    #             suggestion_embed = coin_distribution_log.embeds[0].to_dict()
    #             author_dictionary = dict(suggestion_embed["author"])
    #             new_suggestion_embed = discord.Embed(title=suggestion_embed["title"], colour=suggestion_embed["color"], timestamp=datetime.datetime.utcnow())
            
    #             new_suggestion_embed.description = (f"{suggestion_embed['description']}")
    #             new_suggestion_embed.add_field(name="**Votes**", value=f"Upvotes: {total_thumbs_up} ``{total_upvote_percentage}%``\nDownvotes: {total_thumbs_down} ``{total_downvote_percentage}%``")
    #             # new_suggestion_embed.set_author(name="TheM1ndGamer | HMS", icon_url="https://images-ext-2.discordapp.net/external/H66Y2mHl-1Ui4ReJRH1wruRy5ZrKUah1KTaF4JWGMUc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/621516858205405197/e34d486c4b1e10ed2df889085eb631be.png?width=473&height=473")
    #             new_suggestion_embed.set_author(name=author_dictionary["name"], icon_url=author_dictionary["icon_url"])
    #             await coin_distribution_log.edit(embed=new_suggestion_embed)
    
    @commands.command()
    async def buttons(self, ctx: commands.Context):
        """Starts a counter for pressing."""
        await ctx.send('Press!', view=Yes())

async def setup(bot):
    await bot.add_cog(PrizeDistribution(bot))