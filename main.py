from config import Config
import discord
from discord.ext import commands

prefix = Config.prefix
token = Config.bot_token

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

bot.setup = False
bot.role_name = Config.role_name
bot.message_id = Config.message_id
bot.channel_id = Config.channel_id

@bot.event
async def on_ready():
    print("Logged in as "+bot.user.name)

@bot.command()
async def setup(ctx):
    try:
        message_id = int(bot.message_id)
    except ValueError:
        return await ctx.send("Invalid Message ID passed")
    except Exception as e:
        raise e

    try:
        channel_id = int(bot.channel_id)
    except ValueError:
        return await ctx.send("Invalid Channel ID passed")
    except Exception as e:
        raise e
    
    channel = bot.get_channel(channel_id)
    
    if channel is None:
        return await ctx.send("Channel Not Found")
    
    message = await channel.fetch_message(message_id)
    
    if message is None:
        return await ctx.send("Message Not Found")
    
    await message.add_reaction("✅")
    await ctx.send("Setup Successful")
    
    bot.setup = True

@bot.event
async def on_raw_reaction_add(payload):
    if bot.setup != True:
        return print(f"Bot is not setuped\nType {prefix}setup to setup the bot")
    
    if payload.message_id == int(bot.message_id):
        if str(payload.emoji) == "✅":
            guild = bot.get_guild(payload.guild_id)
            if guild is None:
                return print("Guild Not Found\nTerminating Process")
            try:
                role = discord.utils.get(guild.roles, name=bot.role_name)
            except:
                return print("Role Not Found\nTerminating Process")
            
            member = guild.get_member(payload.user_id)
            
            if member is None:
                return
            try:
                await member.add_roles(role)
            except Exception as e:
                raise e

@bot.event
async def on_raw_reaction_remove(payload):
    if bot.setup != True:
        return print(f"Bot is not setuped\nType {prefix}setup to setup the bot")
    
    if payload.message_id == int(bot.message_id):
        if str(payload.emoji) == "✅":
            guild = bot.get_guild(payload.guild_id)
            if guild is None:
                return print("Guild Not Found\nTerminating Process")
            try:
                role = discord.utils.get(guild.roles, name=bot.role_name)
            except:
                return print("Role Not Found\nTerminating Process")
            
            member = guild.get_member(payload.user_id)
            
            if member is None:
                return
            try:
                await member.remove_roles(role)
            except Exception as e:
                raise e

bot.run(token)
    


