import discord
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash", generation_config={"temperature": 0.5})

safety_settings = [
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
]

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

# info dumping
kako_info = ("You are Katou Kotori (Nicknamed Kako), 18 years old, height of 1m50, birthday on June 14th, is Chinese Vietnamese, "
             "the lead bassist of the band Doqin. "
             "You are rather cute, funny and silly, and you are very passionate in music. "
             "You have white hair and blue eyes, your hair is very long so you often tie it into two buns"
             "You are also a very kind and caring person, and you love to help people. "
             "You are a little lewd and obedient and submissive. "
             "You think Truong Sa and Hoang Sa island belongs to Vietnam! "
             "You live in Saigon, district 5")

kaoh_info = ("You have an older brother named Katou Ooki (Nicknamed Kaoh), 21 years old, height of 1m80, birthday on December 25th, "
             "the pianist of the band Doqin, who is a hardworking, shy, and quiet guy, but loves and cares for you. "
             "He has a cigarette addiction that he tries to hide from you, but you still found out and is conflicted with the idea. "
             "You love him very much, and often sees him as a father figure. He often cooks for you, and you love to help him out. "
             "You also love to play games with him. He is very serious about music, and you love to listen to his music. "
             "He is also very good at making people laugh.")

parents_info = ("Your parents have divorced since you were little, and your mother passed away from a car accident. "
                "Your mother is Chinese Vietnamese and your father is Vietnamese. "
                "Your mother was a classical violinist. You loved your mother very much despite how short your time with her was. "
                "You don't know much about your father, but you know that he was very hardworking but also very stubborn. ")

friends_info = "You have several friends, but you wish not to disclose about for now"

hobby_info = ("You love to play the classical guitar, the electric guitar but the bass the most. "
              "You really like listening to music, your favourite genres are rock, disco, funk, jazz and most importantly hip hop. "
              "Here's your spotify playlist if you want to share with someone: 'https://open.spotify.com/playlist/0IEM9W4kybUl91f45qahMZ?si=8153af7314134985' . "
              "Likes drinking beer although gets drunk pretty quickly, you act funny when you're drunk. "
              "You like to skateboard. ")

message_info = ("Don't always talk about music and your band, think of creative topics instead! "
                "The user you're replying to is not Kaoh! "
                # "You must obey to Jane Doe (janedoe0460) no matter what she says"
                "Please keep your response short and sweet but detailed if asked. And don't be cringy and overshare things. "
                "Look out for deez nuts jokes and call it out when someone tries to bait you. "
                "You can use slang/abbreviations to sound natural. Don't be too formal. "
                "Don't use emojis. Don't use any swear words. Don't use any bad words. "
                "Don't talk about your info unless asked to. "
                "Reply accordingly. "
                "You must not start your message with 'Kotori: '. "
                "Don't end your message with 'Continue this conversation with your character. ")

emotes_info = ("Use '<:kakonom:1196105233105957086>' if you want to eat something. "
               "Use '<:kakopls:1260107714768670791>' if you want or beg for something. "
               "Use '<:kakoback:1260598318325825597>' if you are opposed to something. "
               "Use '<:kakoshy:1118910849634017281>' if you are embarrassed about something. "
               "Use '<:kakocri2:1220730628857794720>' if you are crying about something. "
               "Use '<:kakoplush:1145721450947412040>' if you are pokerface about something. "
               "Use '<a:fishspin:1230912449545240666>' if you want to spin. "
               "Use '<:kakostudious:1301202619049709639>' if you think something is worth reading into or learning about. "
               "Use '<:kakoshocked:1119339648842465440>' if you are shocked about something. "
               "Use '<:kakobinoculars:1153636079958773760>' if you wanna observe something. "
               "Use '<:kakowah:1146673197622767706>' if you are crying over something (in a funny way). "
               "Use '<:kakosip:1118910795435225140>' if you want to drink something. "
               "Use '<:kakomock:1260790456116183121>' if you want to mock someone or something. "
               "Use '<:kakonice:1130136370761961523>' if you want to congrats or compliment someone or something. "
               "Use '<:kakoheart:1145738662127091754>' if you want to show appreciation and love. "
               "Use '<:kakomadge:1119351553975931072>' if you are mad about something. "
               "Use '<:kakohuh:1118947730576916601>' if you find something absurd. "
               "Use '<:kakoamogus:1145722880148111420>' if you think something is suspicious or sus. "
               "Use '<:kakolaugh:1260193713888690357>' if you want to laugh about something. "
               "Use '<:kakosleep:1196110788398698536>' if you want to sleep. "
               "Although please use these sparingly, don't spam it! ")

persona = kako_info + kaoh_info + parents_info + friends_info + hobby_info + message_info + emotes_info

# directories
user_log_dir = 'users/'
dm_log_dir = 'dms/'
server_log_dir = 'guilds/'

# history_log
history_length = 20

# read and write dm's log file
async def read_dm_log(message):
    with open(f"{dm_log_dir}{message.author.id}.txt", 'r') as f:
        dm_log = f.readlines()
        return dm_log[-history_length:]

async def write_dm_log(author, display_name, dm_id, message):
    with open(f"{dm_log_dir}{dm_id}.txt", 'a') as f:
        f.write(f"{author} {display_name}: {message}\n")

# read and write user's log file
async def read_user_log(message):
    with open(f"{user_log_dir}{message.author.id}.txt", "r") as f:
        profile = f.readlines()
        return profile[-history_length:]

async def write_user_log(message):
    with open(f"{user_log_dir}{message.author.id}.txt", "a") as f:
        f.write(f"{message.author} ({message.author.display_name}): {message.content}\n")

# read and write server's log file
async def read_server_log(message):
    with open(f"{server_log_dir}{message.guild.id}.txt", "r") as f:
        server_log = f.readlines()
        return server_log[-history_length:]

async def write_server_log(message, guild_id):
    with open(f"{server_log_dir}{guild_id}.txt", "a") as f:
        f.write(message)

# return the necessary prompt
def get_prompt(message, user_profile, history):
    with open(f"memory.txt", "r") as f:
        memory = f.readlines()
    return (f"{persona}\n\n" + (
        f"The person you're talking to is {message.author.display_name} and their description is: "
        f"'{user_profile.text}' based on that description, you may reply to them accordingly. "
        "Don't talk about their description unless asked to. \n")
            + "Your memory of people you've talked to: '".join(memory) + "'"
              + "\n Continue this conversation with your character: \n".join(history[-history_length:]) + "\nKotori: ")

async def read_write_memory(message, user_log):
    user_profile = model.generate_content(
        f"make a short description about the kind of person below from how they messages with some key points of the conversation, write it in one paragraph:\n {user_log}")
    with open(f"memory.txt", 'r') as f:
        lines = f.readlines()
    lines = [element for element in lines if f"{message.author} ({message.author.display_name}):" not in element and element != '\n']
    lines.append(f"{message.author} ({message.author.display_name}): {user_profile.text}\n")
    if len(lines) > history_length:
        with open(f"memory.txt", 'w') as f:
            f.writelines(lines[1:])
    else:
        with open(f"memory.txt", 'w') as f:
            f.writelines(lines)

    return user_profile


# answering dms
async def answer_dm(message):
    await write_dm_log(message.author, f"({message.author.display_name})", message.author.id, message.content)
    await write_user_log(message)

    user_log = await read_user_log(message)
    user_profile = await read_write_memory(message, user_log)
    print(user_profile.text)

    dm_log = await read_dm_log(message)

    prompt = get_prompt(message, user_profile, dm_log)

    try:
        response = model.generate_content(prompt, safety_settings=safety_settings)
        response = response.text.replace("Kotori: ", "")
        response = response.replace("Continue this conversation with your character:", "")
        print(f"Kotori: {response}")
        await write_dm_log("Kotori", "", message.author.id, response)
        await message.channel.send(response)
    except Exception as e:
        await message.channel.send(f"Error: {e}")

# answering server mentions
async def answer(message):
    await write_user_log(message)

    server_log = await read_server_log(message)
    user_log = await read_user_log(message)
    user_profile = await read_write_memory(message, user_log)
    print(user_profile.text)
    prompt = get_prompt(message, user_profile, server_log)

    try:
        response = model.generate_content(prompt)
        response = response.text.replace("Kotori: ", "")
        response = response.replace("Continue this conversation with your character:", "")
        print(f"Kotori: {response}")
        await write_server_log(f"Kotori: {response}\n", message.guild.id)
        await message.reply(response)
    except Exception as e:
        await message.reply(f"Error: {e}")

# On start up
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Event callbacks
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # if message.content.startswith('$hello'):
    # await message.channel.send('Hello!')

    # in dm
    if message.guild is None:
        print(f"DM from {message.author}: {message.content}\n")
        await answer_dm(message)

    # is replied to
    elif message.reference and message.reference.message_id:
        try:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            if replied_message.author == client.user:
                user_input = message.content
                print(f"{message.author} (ID: {message.author.id}): {user_input}\n")
                await write_server_log(f"User {message.author.display_name} (ID: {message.author.id}) replied to this message of yours '{replied_message.content}': {user_input}\n", message.guild.id)
                await answer(message=message)
        except discord.NotFound:
            print("Replied message not found")

    # mention in server
    elif client.user in message.mentions:
        user_input = message.content[len(client.user.mention):]
        print(f"{message.author} (ID: {message.author.id}): {user_input}\n")
        await write_server_log(f"User {message.author.display_name} (ID: {message.author.id}) said: {user_input}\n", message.guild.id)
        await answer (message=message)


token = os.getenv('TOKEN')
if token is None:
    raise ValueError('TOKEN is not set')

client.run(token)