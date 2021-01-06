#!/usr/bin/env python3
# cooldown.py
# a class to manage command cooldown for resource heavy commands
import time

class cooldown(object):
    """An object for handling command cooldowns"""

    def __init__(self, sec: int):
        self.cooldown_time = int(sec)
        self.used_time = {}
    
    def was_used(self, guild_id):
        self.used_time[f'{guild_id}'] = time.time()

    def can_be_used(self, guild_id) -> bool:
        current_tick = time.time()
        cooldown_passed = False

        try:
            if current_tick - self.used_time[f'{guild_id}'] >= self.cooldown_time:
                cooldown_passed = True
        except:
            cooldown_passed = True
            
        return cooldown_passed

    def seconds_left(self, guild_id) -> float:
        tick_time = time.time() - self.used_time[f'{guild_id}']

        return round(self.cooldown_time - tick_time, 1)

    async def check_and_warn_usage(self, channel) -> bool:
        guild_id = channel.guild.id
        if not self.can_be_used(guild_id):
            await channel.send(f'This command is on cooldown, you must wait another {self.seconds_left(guild_id)} seconds!', delete_after=5)
            return False
        return True