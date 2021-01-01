#!/usr/bin/env python3
# context.py
# a class for getting data for a message
from datetime import datetime

class messagecontext(object):
    """An object for message context, used for both logging and filtering"""

    def __init__(self, message):
        self.message = message
    
    def message_words(self) -> list:
        return self.message.content.lower().split()

    def contains_filtered_terms(self, filter) -> bool:
        for word in filter:
            if word.lower() in self.message.content.lower():
                return True

        return False

    def author(self) -> str:
        return self.message.author
    
    def guild(self) -> object:
        try:
            return self.message.guild
        except:
            return None

    def guild_id(self) -> int:
        try:
            return self.guild().id
        except:
            return None

    def readable_author(self) -> str:
        return(f'{self.author().display_name} ({self.author().name})')\

    def log_header(self) -> str:
        return(f'{str(datetime.now())} {self.readable_author()}')

    def readable_log(self) -> str:
        return(f'{self.log_header()}: {self.message.content}')

    def channel(self) -> object:
        return self.message.channel