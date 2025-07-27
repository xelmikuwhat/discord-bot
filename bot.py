from aiohttp import web
import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class PaymentView(discord.ui.View):
    def __init__(self, gamepass_link: str):
        super().__init__(timeout=None)
        self.gamepass_link = gamepass_link

    @discord.ui.button(
        label="payment", 
        style=discord.ButtonStyle.secondary, 
        emoji="<:pink_cards:1399059854316015688>"
    )
    async def payment_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(self.gamepass_link, ephemeral=False)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("Slash commands synced!")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="payment", description="Send payment info with button")
@app_commands.describe(gamepass_link="The link to the gamepass")
async def payment(interaction: discord.Interaction, gamepass_link: str):
    message_text = (
        "⋆ ｡ ˚  send **ss + user** once bought <a:000:1398827227348733982> 　\n"
        "-# .   　   <a:3whitearrow:1398827311671017535> refunds aren't provided <a:038:1398827882465464382>"
    )
    view = PaymentView(gamepass_link)
    await interaction.response.send_message(content=message_text, view=view)

async def handle(request):
    return web.Response(text="Bot is running")

port = int(os.getenv("PORT", 8080))
app = web.Application()
app.add_routes([web.get('/', handle)])

async def main():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server running on port {port}")

    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())