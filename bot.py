import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta, timezone
import pytz
import json
import os
from keep_alive import keep_alive
from slash_tracker import update_slash_usage, get_last_slash_usage

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ⏰ Short timezone names (aliases)
timezone_aliases = {
    "IST": "Asia/Kolkata",
    "PST": "US/Pacific",
    "EST": "US/Eastern",
    "CST": "US/Central",
    "MST": "US/Mountain",
    "GMT": "Europe/London",
    "UTC": "UTC",
    "BST": "Europe/London",
}

TIMEZONE_FILE = "timezones.json"

# Load saved timezones
if os.path.exists(TIMEZONE_FILE):
    with open(TIMEZONE_FILE, "r") as f:
        user_timezones = json.load(f)
else:
    user_timezones = {}

# Helper to save timezones to file
def save_timezones():
    with open(TIMEZONE_FILE, "w") as f:
        json.dump(user_timezones, f)

# Enable message content intent
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

# Create the bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    bot.loop.create_task(monthly_reminder())

async def monthly_reminder():
    notified = False
    while True:
        now = datetime.now(pytz.timezone("Asia/Kolkata"))
        if now.day == 1 and not notified:
            user = await bot.fetch_user(0) #YOUR_USER_ID_HERE
            await user.send("📅 Hey! It's a new month. Run any `/command` to keep your Active Developer badge.")
            notified = True
        elif now.day != 1:
            notified = False
        await asyncio.sleep(3600)  # check every hour

# Simple hello command
@bot.command()
async def hello(ctx):
    await ctx.send("Hey there! 👋")

# DM a mentioned user with a custom message
@bot.command()
async def dm(ctx, user: discord.User, *, message):
    try:
        await user.send(message)
        await ctx.send(f"✅ Sent your message to {user.name}.")
    except discord.Forbidden:
        await ctx.send("❌ Could not send DM. They may have DMs off or blocked the bot.")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

# DM a specific user ID with a hardcoded message
@bot.command()
async def msg(ctx):
    user_id = 0  # friend's user ID
    try:
        user = await bot.fetch_user(user_id)
        await user.send("Hey! 👋 This is a message from Coffins bot.")
        await ctx.send("✅ Message sent!")
    except discord.NotFound:
        await ctx.send("❌ User not found.")
    except discord.Forbidden:
        await ctx.send("❌ Cannot DM this user. DMs may be disabled.")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

#Display the UserInfo

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author  # Use the person who ran the command if no one is mentioned

    embed = discord.Embed(
        title="🧾 User Info",
        description=f"Info about {member.mention}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)

    embed.add_field(name="👤 Username", value=f"{member.name}#{member.discriminator}", inline=True)
    embed.add_field(name="🆔 User ID", value=member.id, inline=True)
    embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime('%Y-%m-%d %H:%M'), inline=False)
    embed.add_field(name="🗓️ Account Created", value=member.created_at.strftime('%Y-%m-%d %H:%M'), inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def settz(ctx, tz_input: str):
    tz_name = timezone_aliases.get(tz_input.upper(), tz_input)

    try:
        pytz.timezone(tz_name)
        user_timezones[str(ctx.author.id)] = tz_name
        save_timezones()
        await ctx.send(f"✅ Your timezone is set to `{tz_name}`.")
    except pytz.UnknownTimeZoneError:
        await ctx.send("❌ Invalid timezone. Example: `Asia/Kolkata`, `US/Eastern`, `PST`")


@bot.command()
async def at(ctx, *args):
    try:
        user_id = str(ctx.author.id)

        if user_id not in user_timezones:
            await ctx.send("⚠️ Please set your timezone first using `!settz Your/Timezone`")
            return

        tz_name = user_timezones[user_id]
        user_tz = pytz.timezone(tz_name)

        # Parse args like: "tomorrow", "5:00", "PM"
        day = "today"
        if args[0].lower() in ["today", "tomorrow"]:
            day = args[0].lower()
            time_str = f"{args[1]} {args[2]}"
        else:
            time_str = f"{args[0]} {args[1]}"

        dt_naive = datetime.strptime(time_str, "%I:%M %p")
        now = datetime.now(user_tz)
        dt_local = user_tz.localize(datetime.combine(now.date(), dt_naive.time()))

        if day == "tomorrow" or dt_local < now:
            dt_local += timedelta(days=1)

        unix_ts = int(dt_local.timestamp())

        await ctx.send(f"🕒 <t:{unix_ts}:t> (<t:{unix_ts}:f>) — your time auto-adjusted for everyone")
    except Exception as e:
        await ctx.send("❌ Format: `!at 5:00 PM` or `!at tomorrow 5:00 PM` — and set your timezone first.")


@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"⚠️ Slash sync failed: {e}")

@bot.tree.command(name="ping", description="Replies with Pong!")
async def ping(interaction: discord.Interaction):
    update_slash_usage()
    await interaction.response.send_message("🏓 Pong!")

@bot.tree.command(name="creator", description="Replies with Coffin!")
async def creator(interaction: discord.Interaction):
    update_slash_usage()
    await interaction.response.send_message("_mr_coffin created me as a Python learning project. Check it out on GitHub: https://github.com/devan19ct/Basic-Discord-Bot")

@bot.tree.command(name="help", description="List all available commands")
async def show_commands(interaction: discord.Interaction):
    update_slash_usage()
    content = (
        "**🤖 Available Commands:**\n\n"
        "📨 `/ping` – Replies with Pong!\n"
        "👤 `!userinfo` – Shows user info\n"
        "📬 `!dm @user <msg>` – DM a user with a message\n"
        "📥 `!msg` – Send a hardcoded DM to a specific user\n"
        "🌍 `!settz <timezone>` – Set your timezone (e.g. IST, US/Eastern)\n"
        "🕒 `!at <time>` – Convert time to everyone’s local time\n"
        "👨‍💻 `/creator` – Info about the bot creator\n"
        "📜 `/help` – You’re looking at it 😄"
    )

    await interaction.response.send_message(content)

@bot.tree.command(name="lastused", description="Shows when a slash command was last used.")
async def lastused(interaction: discord.Interaction):
    last = get_last_slash_usage()
    if last:
        days_ago = (datetime.now(timezone.utc) - last).days
        formatted_time = last.astimezone(pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S %Z')
        await interaction.response.send_message(
            f"📆 Last slash command used: `{formatted_time}` ({days_ago} days ago)"
        )
    else:
        await interaction.response.send_message("⚠️ No slash command usage recorded yet.")

keep_alive()
bot.run(TOKEN)

