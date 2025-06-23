import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Enable message content intent
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content

# Create the bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

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


bot.run(TOKEN)

