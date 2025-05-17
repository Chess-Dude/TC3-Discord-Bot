from datetime import timedelta
import datetime, re
from .userModeration import UserModeration
import discord

class BanModeration(UserModeration):
    
    def __init__(
        self, 
        bot,
        interaction,
        user, 
        modlog_reason,
        moderator_id,
        ban_length
    ):
        super().__init__(bot, interaction, user, modlog_reason, 0, "Ban", moderator_id)
        self.ban_length = ban_length

    async def ban_user(
        self
    ):
        
        await self.interaction.guild.ban(user=self.user, reason=self.modlog_reason)
        COIN_SERVER = self.bot.get_guild(676112926918049813)
        await COIN_SERVER.ban(user=self.user, reason=self.modlog_reason)        

    async def update_total_bans(self, connection):
        # Parse the self.ban_length string to extract the number of days.
        # Accepts formats like "30d", "30 d", "60d", etc.
        match = re.search(r'(\d+)\s*([smhd])', self.ban_length.lower())
        if match:
            value = int(match.group(1))
            unit = match.group(2)
            if unit == 's':
                kwargs = {'seconds': value}
            elif unit == 'm':
                kwargs = {'minutes': value}
            elif unit == 'h':
                kwargs = {'hours': value}
            else:
                kwargs = {'days': value}
        else:
            kwargs = {'days': 0}

        unban_date = datetime.datetime.utcnow() + datetime.timedelta(**kwargs)

        # Update totalBans in UserTotalModlogs.
        # Check if a record for this user in this guild already exists.
        result = await connection.fetchrow(
            "SELECT record, totalBans FROM UserTotalModlogs WHERE guildID = $1 AND userID = $2",
            self.interaction.guild.id, self.user.id
        )

        if result is not None:
            # If a record exists, increment the totalBans by 1.
            await connection.execute(
                "UPDATE UserTotalModlogs SET totalBans = totalBans + 1 WHERE record = $1",
                result["record"]
            )
        else:
            # If no record exists, create one with totalBans = 1.
            await connection.execute(
                """
                INSERT INTO UserTotalModlogs 
                (guildID, userID, robloxUsername, activeDamage, healedDamage, totalDamage, totalBans)
                VALUES ($1, $2, $3, 0, 0, 0, 1)
                """,
                self.interaction.guild.id, self.user.id, self.user.display_name
            )

        # Insert a new row into ActiveBannedUsers with the computed unban date.
        await connection.execute(
            """
            INSERT INTO ActiveBannedUsers 
            (guildID, userID, robloxUsername, unbanDate)
            VALUES ($1, $2, $3, $4)
            """,
            self.interaction.guild.id, self.user.id, self.user.display_name, unban_date
        )

    async def send_log_embed(
        self,
        connection
    ):
        # Public Success Embed
        response_embed = discord.Embed(
            description=(
                f"✅ **{self.user.display_name}** has been **banned** for **{self.ban_length}**\n"
                f"**Reason:** {self.modlog_reason}"
            ),
            color=0x00ffff
        )

        success_message = await self.interaction.channel.send(embed=response_embed)

        # Initialize appeal message (optional depending on guild)
        appeal_message = ""

        # Modlog Embed
        log_embed = discord.Embed(
            title="🚫 Ban Log",
            color=0x00ffff,
            timestamp=self.interaction.created_at
        )

        log_embed.set_author(
            name=self.interaction.guild.name,
            icon_url=str(self.interaction.guild.icon)
        )

        log_embed.add_field(
            name="👮 Moderator",
            value=f"{self.interaction.user.mention} (`{self.interaction.user.id}`)",
            inline=False
        )

        log_embed.add_field(
            name="🙍‍♂️ User Banned",
            value=f"{self.user.mention} (`{self.user.id}`)",
            inline=False
        )

        log_embed.add_field(
            name="📄 Reason",
            value=f"```{self.modlog_reason}```",
            inline=False
        )

        log_embed.add_field(
            name="⏳ Duration",
            value=f"```{self.ban_length}```",
            inline=False
        )

        log_embed.add_field(
            name="🔗 Jump to Message",
            value=f"[Click to view]({success_message.jump_url})",
            inline=False
        )

        # Send to log channel only if in specific guild
        if self.interaction.guild.id == 350068992045744141:
            log_channel = self.interaction.guild.get_channel(1028869177798295632)
            appeal_message = "You may appeal this ban here: https://discord.gg/YkcvK7P2zt"

            modlogs_embed = await self.get_modlogs(
                user=self.user,
                interaction=self.interaction,
                connection=connection
            )

            self.log_embed_message = await log_channel.send(embeds=[log_embed, modlogs_embed])

        # DM the banned user
        try:
            await self.user.send(
                content=f"You have been **banned** from **{self.interaction.guild.name}**.",
                embeds=[log_embed, modlogs_embed]
            )

            await self.user.send(
                content=f"{appeal_message}"
            )
        except:
            pass
