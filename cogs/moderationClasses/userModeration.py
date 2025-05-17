import discord
class UserModeration():
    def __init__(
        self,
        bot,
        interaction,
        user,
        modlog_reason,
        damage_taken,
        modlog_type,
        moderator_id
    ):
        self.bot = bot
        self.interaction = interaction
        self.user = user
        self.modlog_reason = modlog_reason
        self.damage_taken = damage_taken
        self.modlog_type = modlog_type
        self.moderator_id = moderator_id

    async def is_staff(
        self
    ):
        """
        Checks if user is staff. Returns true if they are.
        """
        staff_role_id_list = [1072233470606200853,
                              351074813055336458,
                              351166789700550679,
                              363125947635073025,
                              743302990001340559,
                              554152645192056842,
                              743115435821498460,
                              419333829891850250,
                              363500459203231746
                            ]    
        
                
        for role_id in staff_role_id_list:
            staff_role = self.interaction.guild.get_role(role_id)
            
            if staff_role in self.user.roles:
                response_embed = discord.Embed(
                    description=f"✅ {self.user.display_name} is a staff member! | Failed to {self.modlog_type}.", 
                    colour=0x00ffff
                )
                self.success_message = await self.interaction.channel.send(embed=response_embed)
                return True
        
        return False
    
    async def create_new_modlog(
        self, 
        connection
    ):
        """
        Creates a new entry under UserModlogs and records the current ban number.
        """
        # Query the current total bans from UserTotalModlogs for this user in the guild.
        sql_get_bans = """
        SELECT COALESCE(totalBans, 0) FROM UserTotalModlogs 
        WHERE userID = $1 AND guildID = $2;
        """
        current_total_bans = await connection.fetchval(
            sql_get_bans, self.user.id, self.interaction.guild.id
        )
        
        if current_total_bans == None:
            current_total_bans = 0

        # Insert a new modlog entry using the current total bans as the ban number.
        sql_insert_modlog = """
        INSERT INTO UserModlogs (
            guildID, userID, robloxUsername, damageTaken, moderatorID, reason, beforeBan
        ) VALUES ($1, $2, $3, $4, $5, $6, $7);
        """
        await connection.execute(
            sql_insert_modlog,
            self.interaction.guild.id,
            self.user.id,
            self.user.display_name,
            self.damage_taken,
            self.moderator_id,
            f"{self.modlog_type}: {self.modlog_reason}",
            current_total_bans
        )

    async def has_prior_modlogs(
        self, 
        connection    
    ):
        """
        Returns True if a UserTotalModlogs record already exists for this user.
        """
        sql = """
        SELECT EXISTS (
            SELECT 1 FROM UserTotalModlogs WHERE userID = $1 AND guildID = $2
        );
        """
        return await connection.fetchval(sql, self.user.id, self.interaction.guild.id)

    async def create_user_main_record(
        self, 
        connection
    ):
        """
        Creates a new record in UserTotalModlogs for a user without prior mod logs.
        """
        sql = """
        INSERT INTO UserTotalModlogs (
            guildID, userID, robloxUsername, activeDamage, healedDamage, totalDamage, totalBans
        ) VALUES ($1, $2, $3, $4, 0, $4, 0)
        """
        await connection.execute(
            sql,
            self.interaction.guild.id,
            self.user.id,
            self.user.display_name,
            self.damage_taken
        )

    async def update_total_modlogs(
        self, 
        connection
    ):
        """
        Updates the user's damage totals in UserTotalModlogs.
        """
        sql = """
        UPDATE UserTotalModlogs
        SET activeDamage = activeDamage + $1,
            totalDamage = healedDamage + activeDamage + $1
        WHERE userID = $2 AND guildID = $3
        """
        await connection.execute(
            sql,
            self.damage_taken,
            self.user.id,
            self.interaction.guild.id
        )

    async def reached_damage_cap(
        self, 
        connection
    ):
        """
        Checks if the user's active damage has reached or exceeded a set threshold.
        """
        sql = """
        SELECT activeDamage FROM UserTotalModlogs WHERE userID = $1 AND guildID = $2
        """
        active_damage = await connection.fetchval(sql, self.user.id, self.interaction.guild.id)
        return active_damage >= 10  # Example threshold, adjust as needed

    async def notify_to_ban(
        self
    ):
        """
        Notifies moderators to review the user for a ban due to excessive damage.
        """
        embed = discord.Embed(
            title="🚫 Ban Notice",
            description=(
                f"User {self.user.mention} has reached the damage cap and should be reviewed for a ban."
            ),
            color=discord.Color.dark_red()
        )
        alert_channel = discord.utils.get(self.interaction.guild.text_channels, name="tc3-bot-mod-logs")
        if alert_channel:
            await alert_channel.send(embed=embed)

    @staticmethod
    async def get_modlogs(
        user,
        interaction,
        connection
    ):
        # Fetch the mod log history for the user.
        sql_modlogs = """
        SELECT modlogID, damageTaken, moderatorID, reason, beforeBan, date
        FROM UserModlogs
        WHERE userID = $1 AND guildID = $2
        ORDER BY date DESC;
        """
        modlogs = await connection.fetch(sql_modlogs, user.id, interaction.guild.id)

        # Fetch aggregate totals for the user.
        sql_totals = """
        SELECT activeDamage, healedDamage, totalDamage, totalBans
        FROM UserTotalModlogs
        WHERE userID = $1 AND guildID = $2;
        """
        totals = await connection.fetchrow(sql_totals, user.id, interaction.guild.id)

        # Create an embed to display the mod logs.
        embed = discord.Embed(
            title=f"Moderation Logs for {user.display_name}",
            color=discord.Color.blue(),
            timestamp=interaction.created_at,
            description="Below are the aggregated modlog statistics and detailed mod log history."
        )
        # Set the user's avatar as the thumbnail.
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

        # Add aggregate statistics to the embed.
        if totals:
            embed.add_field(
                name="Aggregate Stats",
                value=(
                    f"**🟡 Active Damage:** `{totals['activedamage']:.1f}`\n"
                    f"**🟢 Healed Damage:** `{totals['healeddamage']:.1f}`\n"
                    f"**🔴 Total Damage:** `{totals['totaldamage']:.1f}`\n"
                    f"**🔨 Total Bans:** `{totals['totalbans']:.1f}`"
                ),
                inline=False
            )
        else:
            embed.add_field(
                name="Aggregate Stats",
                value="No aggregate modlog record found.",
                inline=False
            )

        # Build a string with each mod log's details.
        if modlogs:
            logs_str = ""
            for log in modlogs:
                # Calculate the ban number using beforeBan.
                ban_number = log["beforeban"] + 1  
                logs_str += (
                    f"**Modlog ID:** `{log['modlogid']}` (Ban #{ban_number})\n"
                    f"**Damage Taken:** `{log['damagetaken']}`\n"
                    f"**Moderator:** <@{log['moderatorid']}>\n"
                    f"**Reason:** {log['reason']}\n"
                    f"**Date:** {log['date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                    "────────────────────────\n"
                )
            # Truncate if the field exceeds Discord's 1024-character limit.
            if len(logs_str) > 1024:
                logs_str = logs_str[:1020] + "..."
            embed.add_field(
                name="Modlog History",
                value=logs_str,
                inline=False
            )
        else:
            embed.add_field(
                name="Modlog History",
                value="No mod logs found for this user.",
                inline=False
            )

        embed.set_footer(text="The Conquerors 3 Discord")
        return embed