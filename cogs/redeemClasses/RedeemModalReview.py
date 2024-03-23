import discord 
import discord, gspread, os 
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

google_sheet = client.open("TC3 Coin Redeem")
temp_coin_redeem_logs = google_sheet.worksheet("CoinRedeemLogs")
perm_coin_redeem_logs = google_sheet.worksheet("PermCoinRedeemLogs")

class RedeemModalReview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    def insert_coin_log(
            self,
            roblox_username,
            total_coins,
            reward_reason
        ):
            temp_coin_redeem_logs.insert_row([f" ", f"{roblox_username}", f"{total_coins}", f"{reward_reason}"], index=4)
            perm_coin_redeem_logs.insert_row([f" ", f"{roblox_username}", f"{total_coins}", f"{reward_reason}"], index=4)

    async def create_embed(
            self,
            interaction,
            user,
            prize_type_name,
            total_prize,
            reward_reason,
            msg
        ):
            redeem_embed = discord.Embed(
                title=f"Prize Redeemed for: {user.display_name}",
                color=0x00ffff
            )
            
            redeem_embed.set_author(
                name=f"{interaction.user.name} Reviewed this redeem:", 
                icon_url=interaction.user.display_avatar.url
            )
            
            redeem_embed.timestamp = interaction.created_at
            
            redeem_embed.set_footer(
                text=f"The Conquerors 3 Redeem Server",
                icon_url=interaction.guild.icon
            )

            redeem_embed.set_thumbnail(
                url=user.display_avatar.url
            )

            redeem_embed.add_field(
                name=f"Total {prize_type_name} Being Redeemed:",
                value=f"{total_prize}",
                inline=False
            )

            redeem_embed.add_field(
                name="Reward Reason:",
                value=f"{reward_reason}",
                inline=False
            )

            if msg != None:
                redeem_embed.add_field(
                    name="Links:",
                    value=f"[Jump To URL]({msg.jump_url})",
                    inline=True
                )

            return redeem_embed

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, emoji='✅', custom_id="persistent_view:approve_redeem")
    async def approve_redeem(self, interaction: discord.Interaction, button: discord.ui.Button):
        ec_role = interaction.guild.get_role(731940681978871948)
        if ec_role in interaction.user.roles:
            redeem_embed = interaction.message.embeds[0].to_dict()
            user_redeeming = interaction.message.content
            redeem_embed_values = redeem_embed['fields']
            total_prize_field = redeem_embed_values[0]
            total_prize = total_prize_field['value']
            prize_type_name = total_prize_field['name']           
            reward_reason_field = redeem_embed_values[1]
            reward_reason = reward_reason_field['value']
            redeem_modal_review_obj = RedeemModalReview()

            user = interaction.guild.get_member(int(user_redeeming.replace("<@", "").replace(">", "")))
            total_prize = total_prize.replace('`', '')
            reward_reason = reward_reason.replace('`', '')

            if "Coins" in prize_type_name:
                prize_type = "Coins"
                prize_channel = interaction.guild.get_channel(1123270001600778312)
                prize_role = interaction.guild.get_role(676116195069657098)
                redeem_modal_review_obj.insert_coin_log(
                    roblox_username=user.display_name,
                    total_coins=total_prize,
                    reward_reason=reward_reason
                )
                
            elif "Robux" in prize_type_name:
                prize_type = "Robux" 
                prize_channel = interaction.guild.get_channel(1123270021037170790)
                prize_role = interaction.guild.get_role(899078081866768414)

            await user.add_roles(prize_role)
            msg = await prize_channel.send(
                content=f"{user.mention} / {user.display_name} / {total_prize} {prize_type} / {reward_reason}"
            )

            redeem_embed = await redeem_modal_review_obj.create_embed(
                interaction=interaction,
                user=user,
                prize_type_name=prize_type_name,
                total_prize=total_prize,
                reward_reason=reward_reason,
                msg=msg
            )

            staff_redeem_log = interaction.guild.get_channel(1088635862159470673)
            await staff_redeem_log.send(
                embed=redeem_embed
            )
            await interaction.channel.delete()

        else:
            error_embed = discord.Embed(
                title="Error: You do not have the Prize Redeem Staff Role. Please try again.",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
                    
    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji='🛑', custom_id="persistent_view:reject_redeem")
    async def reject_redeem(self, interaction: discord.Interaction, button: discord.ui.Button):
        ec_role = interaction.guild.get_role(731940681978871948)
        if ec_role in interaction.user.roles:
            redeem_embed = interaction.message.embeds[0].to_dict()
            user_redeeming = interaction.message.content
            redeem_embed_values = redeem_embed['fields']
            total_prize_field = redeem_embed_values[0]
            total_prize = total_prize_field['value']
            prize_type_name = total_prize_field['name']           
            reward_reason_field = redeem_embed_values[1]
            reward_reason = reward_reason_field['value']

            user_redeeming = interaction.message.content
            user = interaction.guild.get_member(int(user_redeeming.replace("<@", "").replace(">", "")))

            rejection_embed = discord.Embed(
                title=f"Your prize redeem was denied and closed by {interaction.user.mention}",
                color=0x00ffff
            )

            await user.send(
                embed=rejection_embed
            )       
            await interaction.channel.delete()

            redeem_modal_review_obj = RedeemModalReview()
            redeem_embed = await redeem_modal_review_obj.create_embed(
                interaction=interaction,
                user=user,
                prize_type_name=prize_type_name,
                total_prize=total_prize,
                reward_reason=reward_reason,
                msg=None
            )
            staff_redeem_log = interaction.guild.get_channel(1088635862159470673)
            await staff_redeem_log.send(
                embed=redeem_embed
            )

        else:
            error_embed = discord.Embed(
                title="Error: You do not have the Prize Redeem Staff Role. Please try again.",
                color=0x00ffff
            )
            
            await interaction.response.send_message(
                embed=error_embed,
                ephemeral=True
            )
            return
