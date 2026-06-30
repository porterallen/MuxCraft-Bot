# MuxCraft Housing Bot — Setup Guide

## How it works
1. Player clicks "Claim" on your website and enters their IGN
2. Website sends a request to this bot
3. Bot DMs you on Discord with their IGN, house, price, and the exact commands to run
4. You jump in-game, check their balance, deduct it, and give them the house

---

## Step 1 — Create your Discord bot

1. Go to https://discord.com/developers/applications
2. Click "New Application" → name it "MuxCraft Bot"
3. Go to "Bot" in the left sidebar
4. Click "Reset Token" and copy your token — this is your DISCORD_TOKEN
5. Scroll down and enable "Server Members Intent"
6. Click "Save Changes"

---

## Step 2 — Get your Discord user ID (OWNER_ID)

1. Open Discord
2. Go to Settings → Advanced → turn on "Developer Mode"
3. Right-click your own profile picture anywhere → "Copy User ID"
4. That number is your OWNER_ID

---

## Step 3 — Deploy to Render (free)

1. Go to https://render.com and sign up with GitHub
2. Push this folder to a GitHub repo (github.com → New repo → upload files)
3. On Render: click "New" → "Web Service" → connect your GitHub repo
4. Set these:
   - Runtime: Python
   - Build command: pip install -r requirements.txt
   - Start command: python bot.py
5. Add these Environment Variables (in Render's dashboard):
   - DISCORD_TOKEN = (your bot token from Step 1)
   - OWNER_ID = (your Discord user ID from Step 2)
   - WEBHOOK_SECRET = muxcraft123  (make this something unique)
6. Click Deploy. Render gives you a URL like: https://muxcraft-bot.onrender.com

---

## Step 4 — Update your website

In your index.html, find the Claim button onclick and replace it with:

```javascript
async function claimHouse(houseName, price) {
  const ign = prompt("Enter your Minecraft username:");
  if (!ign) return;
  
  const res = await fetch("https://YOUR-RENDER-URL.onrender.com/claim", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Secret": "muxcraft123"
    },
    body: JSON.stringify({ ign: ign, house: houseName })
  });

  if (res.ok) {
    alert("Claim submitted! A staff member will process it shortly.");
  } else {
    alert("Something went wrong. DM staff in Discord.");
  }
}
```

Then change each house Claim button to:
onclick="claimHouse('Oak Cottage', 200)"
(matching the house name and price)

---

## Step 5 — In-game commands to process a claim

When the bot DMs you, run these in-game:

Check balance:    /bal PlayerName
Deduct coins:     /eco take PlayerName 500
Give coins:       /eco give PlayerName 500

You'll need EssentialsX installed on your Aternos server for these to work.

---

## Installing EssentialsX on Aternos

1. Log into aternos.org
2. Go to your server → Plugins
3. Search "EssentialsX" → Install
4. Search "Vault" → Install
5. Restart the server
6. Done — /bal and /eco commands now work in-game
