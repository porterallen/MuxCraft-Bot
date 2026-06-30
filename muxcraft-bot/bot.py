import os
import discord
from discord.ext import commands
from aiohttp import web
import asyncio
import json

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
OWNER_ID = int(os.environ["OWNER_ID"])
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "muxcraft")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

HOUSE_PRICES = {
    "Oak Cottage": 200,
    "River Shack": 150,
    "Birch Villa": 500,
    "Lakefront Manor": 750,
    "Sky Palace": 1200,
    "Dark Oak Keep": 1000,
}

async def send_claim_dm(ign: str, house: str, price: int):
    owner = await bot.fetch_user(OWNER_ID)
    embed = discord.Embed(
        title="🏠 New house claim!",
        color=0x185FA5
    )
    embed.add_field(name="Player IGN", value=f"`{ign}`", inline=True)
    embed.add_field(name="House", value=house, inline=True)
    embed.add_field(name="Price", value=f"{price} MuxCoins", inline=True)
    embed.add_field(
        name="Commands to run",
        value=(
            f"**1. Check their balance:**\n`/bal {ign}`\n\n"
            f"**2. If they have enough, deduct:**\n`/eco take {ign} {price}`\n\n"
            f"**3. Assign their house in-game and mark it done.**"
        ),
        inline=False
    )
    embed.set_footer(text="MuxCraft Housing Bot")
    await owner.send(embed=embed)

async def handle_claim(request):
    secret = request.headers.get("X-Secret", "")
    if secret != WEBHOOK_SECRET:
        return web.Response(status=403, text="Forbidden")

    try:
        data = await request.json()
        ign = data.get("ign", "").strip()
        house = data.get("house", "").strip()
    except Exception:
        return web.Response(status=400, text="Bad request")

    if not ign or not house:
        return web.Response(status=400, text="Missing ign or house")

    price = HOUSE_PRICES.get(house)
    if not price:
        return web.Response(status=400, text="Unknown house")

    asyncio.create_task(send_claim_dm(ign, house, price))
    return web.json_response({"ok": True})

async def start_web():
    app = web.Application()
    app.router.add_post("/claim", handle_claim)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8080)))
    await site.start()
    print(f"Web server running on port {os.environ.get('PORT', 8080)}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await start_web()

bot.run(DISCORD_TOKEN)
