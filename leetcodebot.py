import discord
from discord.ext import commands
import asyncio
import Classmate
import time
import pickle
from datetime import datetime

#TOKEN = open("leetcodebottoken.txt", "rt")
TOKEN = "TOKEN HERE"


bot = commands.Bot(command_prefix='.')

try:
    classmates = pickle.load(open("save.p", "rb"))
except:
    classmates = []

#Saving files
async def save():
    pickle.dump(classmates, open("save.p", "wb"))
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Save Created at", current_time)



@bot.event
async def on_ready():

    await bot.change_presence(activity=discord.Game(name="type .info for info"))
    print("LeetCodeBot is ready.")
    print("Logged in as {0.user}".format(bot))
    print(discord.__version__)
    while True:
        await asyncio.sleep(5)
        await save()

    
#used for testing
@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

@bot.command()
async def add_topics(ctx, *, in_text):
    topics = in_text.split(", ")
    user = ctx.message.author.display_name
    id = ctx.message.author.id
    for person in classmates:
        if person.name == user:
            for topic in topics:
                person.topics.append(topic)
            return
    else:
        newClassMate = Classmate.ClassMate(user, id)
        for topic in topics:
            newClassMate.topics.append(topic)
        classmates.append(newClassMate)
        return

@bot.command()
async def users_topics(ctx, *, in_text):
    user = in_text.replace("@!", "") #to remove the @ and ! sign from user pings
    out_string = ""
    for person in classmates:
        if person.name == user or "<" + str(person.id) + ">" == user: #id is returned in pings rather than the name dispite appearing as the name
            if len(person.topics) <= 0:
                await ctx.send("User has any topics currently")
            for topic in person.topics:
                out_string = out_string + topic + ", "
            out_string = out_string[:-2]
            await ctx.send(out_string)
            return
    await ctx.send("User has not added any topics or does not exist")

@bot.command()
async def my_topics(ctx):
    out_string = ""
    for person in classmates:
        if person.id == ctx.message.author.id:
            if len(person.topics) <= 0:
                await ctx.send("You currently do not have any Leetcode Topics Set")
                return
            for topic in person.topics:
                out_string = out_string + topic + ", "
            out_string = out_string[:-2]
            await ctx.send(out_string)
            return
    await ctx.send("You do not have any LeetCode Topics set yet")

@bot.command()
async def clear_topics(ctx):
    for person in classmates:
        if person.id == ctx.message.author.id:
            person.topics = []

@bot.command()
async def remove_topics(ctx, *, in_text):
    topicsToRemove = in_text.split(", ")
    for person in classmates:
        if person.id == ctx.message.author.id:
            for toRemove in topicsToRemove:
                person.topics.remove(toRemove)

@bot.command()
async def find_topics(ctx, *, in_text):
    matches = []
    out_string = ""
    for person in classmates:
        if in_text in person.topics:
            matches.append(person.name)
    if len(matches) <= 0:
        await ctx.send("No matches found.")
        return
    for match in matches:
        out_string = out_string + match + ", "
        out_string = out_string[:-2]
    await ctx.send(out_string)

@bot.command()
async def shared_topics(ctx):
    matches = []
    out_string = ""
    for person in classmates:
        if person.id == ctx.message.author.id:
            user = person
    for person in classmates:
        if user.id != person.id and not set(person.topics).isdisjoint(user.topics):
            matches.append(person.name)
    if len(matches) <= 0:
        await ctx.send("No matches found.")
        return
    for match in matches:
        out_string = out_string + match + ", "
        out_string = out_string[:-2]
    await ctx.send(out_string)

@bot.command()
async def whos_leetcoding(ctx):
    currentlyLeetcoding = []
    out_string = ""
    members = ctx.message.guild.members
    for member in members:
        for activity in member.activities:
            if activity.type == discord.ActivityType.custom and "leetcoding now" in activity.name and member not in currentlyLeetcoding:
                currentlyLeetcoding.append(member.name)
        if len(currentlyLeetcoding) <= 0:
            await ctx.send("Noone is currently Leetcoding")
            return
    for person in currentlyLeetcoding:
        out_string = out_string + person + ", "
        out_string = out_string[:-2]
    await ctx.send(out_string)

@bot.command()
async def info(ctx):
    multiline = """ This is a bot for people to find others to leetcode/study with add a custom status including the words leetcoding now to show that you are available
Commands include:
```.whos_leetcoding: Shows all people currently working on leetcode. 
.add_topics: Type topics you want to leetcode about if multiple use a comma and space seperator , 
.remove_topics: Type topics you wish to remove from you list of topics
.clear_topics: Clear your list of topics
.my_topics: lists all of your topics
.users_topics: lists all of a users topics either by name or by @ ping
.shared_topics: find all users who share a topic with you.
.find_topic: find all users with a particular topic```
    """
    await ctx.send(multiline)
              


    





bot.run(TOKEN)
#bot.run(TOKEN.read())
