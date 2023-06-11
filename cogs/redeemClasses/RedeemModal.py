import discord, re
from .InvalidPrizeType import InvalidPrizeType
from .RedeemModalReview import RedeemModalReview

class RedeemModal(discord.ui.Modal, title="The Conquerors 3 Prize Redeem Form"):
    rblx_name = discord.ui.TextInput(
        label="What is your ROBLOX Username?",
        style=discord.TextStyle.short,
        placeholder="ROBLOX username Here...",
        required=True,
        min_length=3,
        max_length=20
    )

    type_of_reward = discord.ui.TextInput(
        label="Are you claiming Coins or Robux?",
        style=discord.TextStyle.short,
        placeholder="Coins/Robux Here...",
        required=True,
        min_length=3,
        max_length=10
    )

    total_prize = discord.ui.TextInput(
        label="Total Coins/Robux being Claimed",
        style=discord.TextStyle.short,
        placeholder="Total Coins/Robux Being Claimed Here...",
        required=True,
        min_length=3,
        max_length=10
    )

    redeem_link = discord.ui.TextInput(
        label="Message link to prize",
        style=discord.TextStyle.short,
        placeholder="Message Link Here...",
        required=True,
        min_length=20,
        max_length=100
    )

    reward_reason = discord.ui.TextInput(
        label="Reason Of Reward (what did you win?)",
        style=discord.TextStyle.short,
        placeholder="Clan Prize/Tournament Prize/Contest Winner...",
        required=True,
        min_length=4,
        max_length=150
    )

    async def on_submit(
        self, 
        interaction: discord.Interaction
    ):

        try:
            total_prize_string = "".join(filter(str.isdigit, self.total_prize.value))
            total_prize_string = total_prize_string.replace(" ", "")

            total_prize = int(total_prize_string)
            
            redeem_link = self.redeem_link.value       
            match = re.search(r'\/(\d+)\/(\d+)\/(\d+)$', redeem_link)
            if match:
                channel_id = int(match.group(2))
                message_id = int(match.group(3))
                server = interaction.client.get_guild(350068992045744141)
                channel = interaction.client.get_channel(channel_id)
                
                message = await channel.fetch_message(message_id)

            else:
                raise TypeError

            type_of_reward = str(self.type_of_reward).lower()
            type_of_reward = type_of_reward.replace(' ', '')

            if ((type_of_reward == "robux") or 
               (type_of_reward == "coins")):
                type_of_reward = type_of_reward.capitalize()

            else:
                raise InvalidPrizeType             

        except ValueError:
            error_embed = discord.Embed(
                title="Error: Your total prize was not a number. Please try again.",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
        
        except TypeError:
            error_embed = discord.Embed(
                title="Error: Your message link was not valid. Please try again.",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return

        except AttributeError:
            error_embed = discord.Embed(
                title="Error: Your message link was not valid. Please try again.",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
                
        except InvalidPrizeType:
            error_embed = discord.Embed(
                title="Error: You did not specify if the prize type was Robux/Coins. Please try again.",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
                    
        ec_role = interaction.guild.get_role(731940681978871948)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ec_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True),
        }

        redeem_category = discord.utils.get(
            interaction.guild.categories, 
            id=815624375792697344
        )

        ticket_channel = await interaction.guild.create_text_channel(
            name=f"{interaction.user.display_name}", 
            overwrites=overwrites, 
            category=redeem_category
        )

        redeem_embed = discord.Embed(
            title=f"{self.rblx_name.value}",
            color=0x00ffff
        )
        
        redeem_embed.set_author(
            name=f"Redeeming Prize For: {self.rblx_name.value}", 
            icon_url=interaction.user.display_avatar.url
        )
        
        redeem_embed.timestamp = interaction.created_at
        
        redeem_embed.set_footer(
            text=f"The Conquerors 3 Redeem Server",
            icon_url=interaction.guild.icon
        )

        redeem_embed.set_thumbnail(
            url=interaction.user.display_avatar.url
        )

        redeem_embed.add_field(
            name=f"Total {type_of_reward} Being Redeemed:",
            value=f"``{total_prize}``",
            inline=False
        )

        redeem_embed.add_field(
            name="Reward Reason:",
            value=f"``{self.reward_reason.value}``",
            inline=False
        )

        redeem_embed.add_field(
            name="Links:",
            value=f"[Jump To URL]({message.jump_url})",
            inline=True
        )

        await ticket_channel.send(
            content=f"{interaction.user.mention}",
            embed=redeem_embed,
            view=RedeemModalReview()
        )

        approved_embed = discord.Embed(
            title=f"Approved: Created {ticket_channel}.",
            color=0x00ffff
        )

        await interaction.response.send_message(
            embed=approved_embed,
            ephemeral=True
        )