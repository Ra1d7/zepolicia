import discord
import requests

ban_words = ["VAC ban on record","game ban on record"]
token = "NzU1MDgzNjQwNTMwMDEwMjAy.X1-IcA.DmCiXGHhBR7jN2qh4gRK3icvgHs"
client_secret = "geLbkU_ZHNyh8tyEzIER8Nz46MfGAJQr"
client_id = "755083640530010202"
client = discord.Client()
def checkit(profile):
    try:
        url=""
        prof = profile[7:]
        if "https://" in profile:
            url=prof
        else:
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
    except:
        return "Invalid Profile ID or URL"
@client.event
async def on_message(message):
    if message.content.find("!help") != -1:
        embed = discord.Embed(title="CSGO ban checker",description=":information_source: Helpful commands to use! :information_source: ")
        embed.add_field(name="!help",value="Shows this message")
        embed.add_field(name="!check <steam id or URL>",value="Checks the given profile's ban status :no_entry:")
        embed.add_field(name="feedback",value="More features will be added soon! :poop:")
        embed.add_field(name="Made by Raid7#1158",value="Version 1.1")
        await message.channel.send(content=None,embed=embed)
    if message.content.find("!check") != -1:
        await message.add_reaction('\N{THUMBS UP SIGN}')
        await message.channel.send(checkit(message.content))
print("[+] build successful [+]")
client.run(token)
