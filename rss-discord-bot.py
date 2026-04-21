import discord
from fastapi import FastAPI
import uvicorn
import os
from threading import Thread

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

app = FastAPI()
intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")


@app.post("/post-article")
async def post_article(data: dict):
    channel = client.get_channel(CHANNEL_ID)

    if not channel:
        return {"status": "channel not found"}

    title = data.get("title")
    link = data.get("link")
    timestamp = data.get("timestamp")
    role_id = data.get("role_id")
    tag_id = data.get("tag_id")

    content = f"{timestamp}\n{link}"

    if role_id:
        content = f"<@&{role_id}>\n" + content

    await channel.send(content)

    return {"status": "sent"}


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    Thread(target=run_api).start()
    client.run(TOKEN)
