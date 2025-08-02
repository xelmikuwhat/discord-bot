from aiohttp import web
import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

INFO_PANEL_CHANNEL_ID = 1398822788923392091
EMBED_COLOR = discord.Color(0xFFA8B5)

intents = discord.Intents.default()
intents.guilds = True
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

async def send_info_panel():
    channel = bot.get_channel(INFO_PANEL_CHANNEL_ID)
    if not channel:
        print("Info panel channel not found.")
        return

    try:
        async for msg in channel.history(limit=10):
            if msg.author == bot.user and msg.components:
                await msg.delete()
    except Exception as e:
        print(f"Failed to delete previous panel: {e}")

    embed = discord.Embed(
    description=(
        "﹒make sure to follow **all** of these rules <a:038:1258205221385932993>\n"
        "　<a:000:1325522777977126934>  - general tos   ⋆        ｡        ˚\n"
        "　　　<a:witchy_wand:1399842051788505108>  - middleman tos\n"
        " 　<a:pending:1398831307139584150>  - commission tos\n"
        "-# <a:3whitearrow:1398827311671017535> ask if you're unsure of anything\n"
        "⋆   ｡  ﹒scammers get banned <:B_2:1399841937422291115>\n"
        "-# open a support ticket if you see a scammer in the server <a:000:1325522777977126934>\n\n"
        "<:arrow:1324783744854265888> breaking tos = ban/warn/comm ban/mw ban\n"
        "-# not doing reqs in gws leads to gw ban"
    ),
    color=EMBED_COLOR
)

    view = InfoPanelView()
    await channel.send(embed=embed, view=view)

class InfoPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="<a:000:1398827227348733982>", style=discord.ButtonStyle.secondary, custom_id="tos_general")
    async def general_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
    description=(
        "⋆   ｡  ﹒˚ **general tos <a:000:1398827227348733982>**\n"
        "no blatant racism or rudeness\n"
        "﹒<:arrow:1398832711631765506> respect all staffs <a:038:1398827882465464382>\n\n"
        "no nsfw , gore or threats\n"
        "﹒﹒ no promos\n\n"
        "dont troll <a:pending:1398831307139584150>\n"
        "-# troll gets a ban most likely\n\n"
        "<a:emoji_118:1399839377131307172> use your common sense﹒\n"
        "﹒dont copy embeds/concepts from here\n"
        "-# in doing so is ban or warn"
    ),
    color=EMBED_COLOR
)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji="<a:pink_strawberry:1399844657315319929>", style=discord.ButtonStyle.secondary, custom_id="tos_mm")
    async def mm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
    description=(
        "⋆   ｡  ﹒˚ **middleman tos <a:witchy_wand:1399842051788505108>**\n"
        "use your common sense <a:000:1398827227348733982>\n"
        "﹒dont be rude or ghost the mm <:ttAwkward:1398828101173252228>\n\n"
        "<:arrow:1398832711631765506> not vouching mm in 24hr - ban\n"
        "open a ticket once both are online <a:pending:1398831307139584150>\n"
        "-# in doing so is warn or ban (and mw ban)\n\n"
        "﹒i dont hold money for middlewomen\n"
        "-# <a:3whitearrow:1398827311671017535> more are listed in the req channel\n"
        "﹒﹒tips are appreciated <a:000:1398827227348733982>\n"
        "-# <a:3whitearrow:1398827311671017535> tippers get a role <a:038:1398827882465464382>"
    ),
    color=EMBED_COLOR
)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji="<a:pending:1398831307139584150>", style=discord.ButtonStyle.secondary, custom_id="tos_commission")
    async def comm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
    description=(
        "⋆   ｡  ﹒˚ **commission tos**\n"
        "use your common sense\n"
        "﹒<:arrow:1398832711631765506> you can't ask for a refund <a:000:1398827227348733982>\n"
        "-# <a:3whitearrow:1398827311671017535> you can cancel but no refunds\n\n"
        "not vouching in 24hr - ban\n"
        "﹒dont ghost tickets <a:emoji_118:1399839377131307172>\n\n"
        "payment is always upfront <a:038:1398827882465464382>\n"
        "<:arrow:1398832711631765506> rush / rude = order cancel no refund\n"
        "-# <a:3whitearrow:1398827311671017535> you can ask for updates but not too much\n\n"
        "tips are appreciated\n"
        "-# <a:3whitearrow:1398827311671017535> tippers get a role <a:000:1398827227348733982>"
    ),
    color=EMBED_COLOR
)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("Slash commands synced!")
    except Exception as e:
        print(f"Error syncing commands: {e}")

    await send_info_panel()

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


