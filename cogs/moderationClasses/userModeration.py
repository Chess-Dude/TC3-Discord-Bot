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
            
            if staff_role in self.member.roles:
                response_embed = discord.Embed(
                    description=f"✅ {self.user.display_name} is a staff member! | Failed to mute.", 
                    colour=0x00ffff
                )
                self.success_message = await self.interaction.channel.send(embed=response_embed)
                return True
        
        return False
    
    def create_new_modlog(
        self
    ):
        pass

    def update_total_modlogs(
        self
    ):
        pass

    def get_current_user_ban(
        self
    ):
        pass

    def check_user_record(
        self
    ):
        pass

    def create_user_main_record(
        self
    ):
        pass

    async def send_log_embed(
        self
    ):
        """
        sends log embed to log channel and user.
        """
        pass

    def check_damage_cap(
        self
    ):
        return False
