import discord
import requests
import asyncio
import psycopg2

DB_NAME = "depcvpm07c2bsp"
DB_USER = "tndoidyodzvucr"
DB_PASS = "2ed1f9208c62cf219a1a680f99f73baeb92b887770c419f1d05b7082e28f7277"
DB_HOST = "ec2-63-34-223-144.eu-west-1.compute.amazonaws.com"
DB_PORT = "5432"
ban_words = ["VAC ban on record","game ban on record"]
token = "OTQ2MjgzNTQ2ODY2MjMzMzY0.YhcdOg.67lLTM_avqKoE09vpCY-Ph1i59Q"

# FIND A WAY TO USE /PROFILES/ OR /ID/ appropiatly
bot = discord.Bot()
def cleaninput(text):
    txt = text.split('/')
    if "/profiles/" in text:
        return txt[4]
    if "/id/" in text:
        return txt[4]
    else:
        return text
def bancheck(url, prof):
    try:
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
        return "Invalid Profile ID or URL"
def checkit(profile):
    url=f"https://steamcommunity.com/profiles/{profile}"
    if "Invalid" in bancheck(url,profile):
        url=f"https://steamcommunity.com/id/{profile}"
        return bancheck(url,profile)
    else:
        return bancheck(url,profile)
async def getuser(user):
    global bot
    await bot.wait_until_ready()
    return await bot.fetch_user(user)
async def checkfile():
    global bot
    await bot.wait_until_ready()
    while(True):
        conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
        cur = conn.cursor()
        cur.execute("SELECT URL, DUSER FROM profiles")
        profiles = cur.fetchall()
        conn.close()
        for prof in profiles:
                    steamid = prof[0]
                    user= prof[1]
                    result = checkit(steamid)
                    if "clean" in result:
                        pass
                    if "has" in result:
                        await bot.wait_until_ready()
                        userd = await getuser(user)
                        await userd.send(f"{steamid} has been banned!")
                        conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
                        cur = conn.cursor()
                        cur.execute(f"DELETE FROM profiles WHERE URL='{steamid}'")
                        conn.commit()
                        conn.close()
        print('[+] Checking Database [+]')
        await asyncio.sleep(3600*5)
async def savenotify(steamid,user):
    global bot
    await bot.wait_until_ready()
    conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO profiles (URL, DUSER) VALUES('{steamid}','{user}')")
    conn.commit()
    conn.close()
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
    profile = cleaninput(profile)
    await ctx.respond(checkit(str(profile)))
@bot.slash_command(guild_ids=None, name="notify",description="Watch this account and get notified when it gets banned")
async def notify(ctx, profile):
    profile = cleaninput(profile)
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
