# Aurora

A simple and fun Discord bot with classic Features built with Python.

## Features

- **Memes**: Get random memes directly in your server.
  - `!meme`: Fetches a random meme from the internet.

## Getting Started

### Prerequisites

- Python 3.11+
- A Discord Bot Token

### Setup

1. **Install dependencies:**
    This project uses `uv` and `pyproject.toml` to manage dependencies. Install them using:

    ```bash
    uv pip install -e .
    ```

2. **Configure your bot token:**
    Create a file named `.env` in the root directory and add your Discord bot token:

    ```
    TOKEN="your_discord_bot_token_here"
    ```

3. **Run the bot:**

    ```bash
    python bot.py
    ```

## Built With

- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
