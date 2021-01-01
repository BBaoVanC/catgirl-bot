#!/usr/bin/env python3
# owouwu.py
# gives random weeb thing to add to messaages
import random

uwu = ['UwU', 'OwO', ':3', '<3', 'Nyaa~', 'meow']

def gen() -> str:
    return random.choice(uwu)
    