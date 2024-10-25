import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import openai

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def generate_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user.mention in message.content:
        prompt = message.content.replace(bot.user.mention, "").strip()
        
        response = generate_openai_response(prompt)
        
        await message.channel.send(response)

bot.run(DISCORD_TOKEN)
