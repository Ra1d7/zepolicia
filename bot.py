import discord
import requests
import asyncio
ban_words = ["VAC ban on record","game ban on record"]
token = "OTQ2MjgzNTQ2ODY2MjMzMzY0.YhcdOg.67lLTM_avqKoE09vpCY-Ph1i59Q"
bot = discord.Bot()
def checkit(profile):
    print(f"checking {profile}")
    try:
        url=""
        if "https://" in profile:
            url=profile
        if profile.isdigit():
            url=f"https://steamcommunity.com/profiles/{profile}"
        else:
            url=f"https://steamcommunity.com/id/{profile}"
        print(url)
        r = requests.get(url)
        for word in ban_words:
            if word in r.text:
                return f"Profile {profile} has {word} :no_entry_sign:"
        else:
            if r.status_code == 200 and "could not be found." not in r.text:
                return f"Profile {profile} is clean! :white_check_mark:"
            else:
                return "Invalid Profile ID or URL"
    except Exception as e:
        return "Invalid Profile ID or URL"
async def getuser(user):
    global bot
    await bot.wait_until_ready()
    return await bot.fetch_user(user)
async def checkfile():
    global bot
    await bot.wait_until_ready()
    print("Running checkfile")
    while(True):
        with open("list.txt",'r') as f:
            for line in f.readlines():
                if line != "\n":
                    steamid = line.split("|")[0]
                    user= line.split("|")[1].strip("\n").strip()
                    result = checkit(steamid)
                    if "clean" in result:
                        pass
                    if "has" in result:
                        await bot.wait_until_ready()
                        userd = await getuser(user)
                        await userd.send(f"{steamid} has been banned!")
                        with open("list.txt", "r+") as f:
                            d = f.readlines()
                            f.seek(0)
                            for i in d:
                                print(i)
                                print("=")
                                print(f"{steamid}|{user}")
                                if i != f"{steamid}|{user}\n":
                                    f.write(i)
                            f.truncate()
        await asyncio.sleep(3600*2)
async def savenotify(steamid,user):
    print(f"Saving Notify with user {user} and steamid {steamid}")
    global bot
    await bot.wait_until_ready()
    with open("list.txt",'a') as f:
        print(f"writing to file {steamid} steamid and user {user}")
        f.write(f"{steamid}|{user}\n")
    print("Saved")
@bot.slash_command(guild_ids=None, name="help", description="Helpful commands to use")
async def helpmsg(ctx):
    embed = discord.Embed(title="CSGO ban checker",description=":information_source: Helpful commands to use? :information_source: ")
    embed.add_field(name="/help",value="Shows this message")
    embed.add_field(name="/check <steam id or URL>",value="Checks the given profile's ban status :no_entry:")
    embed.add_field(name="/notify <steam id or URL>",value="Watch this account and get notified when it gets banned :police_officer:")
    embed.add_field(name="feedback",value="More features will be added soon? :poop:")
    embed.add_field(name="Made by Raid7#3164",value="Version 1.2")
    await ctx.respond(content=None,embed=embed)
@bot.slash_command(guild_ids=None, name="check", description="Checks the given profile's ban status")
async def check(ctx, profile):
    await ctx.respond(checkit(str(profile)))
@bot.slash_command(guild_ids=None, name="notify",description="Watch this account and get notified when it gets banned")
async def notify(ctx, profile):
    user = ctx.author
    check = checkit(str(profile))
    if "clean" in check:
        await ctx.respond("You will be notified when the account gets banned :bell:")
        await bot.loop.create_task(savenotify(str(profile),user.id))
    else:
        await ctx.respond(check)
print("[+] build successful [+]")
bot.loop.create_task(checkfile())
bot.run(token)
