import discord
import sqlite3
from discord.ext import commands
from config import TOKEN
from logic import DB_Manager
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
db_manager = DB_Manager('FAQ.db')

@bot.event
async def on_ready():
    print(f'{bot.user} olarak online durumdayım yardım için /help')

@bot.command()
async def about(ctx):
    view = discord.ui.View()

    class LangButton(discord.ui.Button):
        def __init__(self, label, lang):
            super().__init__(label=label, style=discord.ButtonStyle.primary)
            self.lang = lang

        async def callback(self, interaction: discord.Interaction):
            if self.lang == "tr":
                await interaction.response.send_message(
                    "Merhaba! Ben bu site hakkında SSS'i (Sıkça Sorulan Sorular) cevaplayan bir discord botuyum. Eğer sorularınız varsa, bana sorabilirsiniz! :)",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "Hello! I'm a Discord bot that answers FAQs (Frequently Asked Questions) about this site. If you have any questions, you can ask me! :)",
                    ephemeral=True
                )

    view.add_item(LangButton("Türkçe", "tr"))
    view.add_item(LangButton("English", "en"))

    await ctx.send("Lütfen bir dil seçin / Please select a language:", view=view)

@bot.command()
async def selam(ctx):
    await ctx.send('Merhaba!')


bot.run(TOKEN)