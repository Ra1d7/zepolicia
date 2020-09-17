import discord
import requests
import asyncio
ban_words = ["VAC ban on record","game ban on record"]
token = "NzU1MDgzNjQwNTMwMDEwMjAy.X1-IcA.DmCiXGHhBR7jN2qh4gRK3icvgHs"
client = discord.Client()
def checkit(profile):
    print(f"checking {profile}")
    try:
        prof = profile
        url=""
        print("checking if ?check is in it")
        if "?check" in profile:
            print("its in it")
            prof = profile[7:]
            print(prof)
        if "https://" in profile:
            print("its a url")
            url=prof
        else:
            print("else")
            url="https://steamcommunity.com/id/{}".format(prof)
        r = requests.get(url)
        for word in ban_words:
            if word in r.text:
                return f"Profile {prof} has {word} :no_entry_sign:"
        else:
            if r.status_code == 200 and "could not be found." not in r.text:
                return f"Profile {prof} is clean! :white_check_mark:"
            else:
                return "Invalid Profile ID or URL"
    except Exception as e:
        print(e)
        return "Invalid Profile ID or URL"
async def getuser(user):
    global client
    await client.wait_until_ready()
    return await client.fetch_user(user)
async def checkfile():
    global client
    await client.wait_until_ready()
    print("Running checkfile")
    while(True):
        with open("list.txt",'r') as f:
            for line in f.readlines():
                steamid = line.split("|")[0]
                user= line.split("|")[1].strip("\n").strip()
                if "clean" in checkit(steamid):
                    pass
                if "has" in checkit(steamid):
                    await client.wait_until_ready()
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
            await asyncio.sleep(3600)        #await userd.send(f"{steamid} has been banned?")
async def savenotify(steamid,user):
    print(f"Saving Notify with user {user} and steamid {steamid}")
    global client
    await client.wait_until_ready()
    with open("list.txt",'a') as f:
        f.write(f"{steamid}|{user}\n")
    print("Saved?")
@client.event
async def on_message(message):
    if message.content.find("?help") != -1:
        embed = discord.Embed(title="CSGO ban checker",description=":information_source: Helpful commands to use? :information_source: ")
        embed.add_field(name="?help",value="Shows this message")
        embed.add_field(name="?check <steam id or URL>",value="Checks the given profile's ban status :no_entry:")
        embed.add_field(name="?notify <steam id or URL>",value="Watch this account and get notified when it gets banned :police_officer:")
        embed.add_field(name="feedback",value="More features will be added soon? :poop:")
        embed.add_field(name="Made by Raid7#1158",value="Version 1.1")
        await message.channel.send(content=None,embed=embed)
    if message.content.find("?check") != -1:
        await message.add_reaction('\N{THUMBS UP SIGN}')
        await message.channel.send(checkit(message.content))
    if message.content.find("?notify") != -1:
        user = message.author
        await user.send("You will be notified when the account gets banned :bell:")
        await message.add_reaction('\N{THUMBS UP SIGN}')
        client.loop.create_task(savenotify(str(message.content)[8:],user.id))
print("[+] build successful [+]")
client.loop.create_task(checkfile())
client.run(token)
