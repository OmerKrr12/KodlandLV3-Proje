import discord
import os
import requests
import random
from discord.ext import commands
from translate import Translator
from translate import *
from config import TOKEN
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

class PersistentView(discord.ui.View):
    def __init__(self, owner):
        super().__init__(timeout=None)
        self.owner = owner

@bot.event
async def on_ready():
    print(f'{bot.user} olarak online durumdayım yardım için /help')


bot.run(TOKEN)