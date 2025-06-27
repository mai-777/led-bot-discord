import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from mqtt_client import MQTTClient

# Configuracion
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MQTT_BROKER = os.getenv('MQTT_BROKER')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC_CONTROL = os.getenv('MQTT_TOPIC_CONTROL')

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Cliente MQTT
mqtt_client = MQTTClient(MQTT_BROKER, MQTT_PORT)

# Comandos
GUILD_ID = discord.Object(id=1388247807680450690)

@bot.tree.command(name="led", description="Controla el LED del ESP32", guild=GUILD_ID)
@app_commands.choices(accion=[
    app_commands.Choice(name="Encender", value="on"),
    app_commands.Choice(name="Apagar", value="off")
])
async def control_led(interaction: discord.Interaction, accion: app_commands.Choice[str]):
    """Control remoto del LED via MQTT"""
    estado = accion.value
    mqtt_client.publish(MQTT_TOPIC_CONTROL, estado.upper())
    
    embed = discord.Embed(
        title=f"LED {estado.upper()}",
        color=discord.Color.green() if estado == "on" else discord.Color.red()
    )
    await interaction.response.send_message(embed=embed)

# Evento on_ready
@bot.event
async def on_ready():
    print(f'✅ Bot listo como {bot.user}')
    await bot.tree.sync(guild=GUILD_ID)

# Ejecucion
if __name__ == "__main__":
    mqtt_client.connect()
    bot.run(TOKEN)