# Havok Discord Bot 🎮🤖

A beginner-friendly Discord bot built with Python using [discord.py](https://discordpy.readthedocs.io/).  
This bot can respond to commands, send DMs, show user info, and more — and it's designed to grow as I learn Python! 🚀

---

## ✨ Features

- `!hello` – Sends a friendly greeting
- `!userinfo [@user]` – Displays user details like username, join date, and account age
- `!dm @user [message]` – Sends a private message to a mentioned user
- `!msg` – Sends a message to a specific user ID
- More features coming soon: Music, polls, reminders...

---

## 🧰 Requirements

- Python 3.10+ (recommended)
- A Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))
- See [`requirements.txt`](requirements.txt) for needed Python packages

---

## 🚀 Setup

1. **Clone the repo:**

```bash
git clone https://github.com/devan19ct/Basic-Discord-Bot.git
cd Basic-Discord-Bot
```
2. **Create a virtual environment (optional but recommended):**

```bash
python -m venv .venv
```
3. **Activate the virtual environment:**

```bash
.venv\Scripts\activate
```
4.**Install dependencies:**

```bash
pip install -r requirements.txt
```
5.**Set up your .env file -**
**Create a file named .env in the root directory and add:**

```bash
DISCORD_TOKEN=your_bot_token_here
```
6.**Run the bot:**

```bash
python bot.py
```
---
## 🛡️ Security

- Never share your bot token publicly.
- This repo uses a .env file to protect the token (included in .gitignore).

---
## 📦 Todo / Upcoming Features

- 🎶 Music playback from YouTube
- 🗳️ Reaction-based polls
- ⏰ Reminders
- 💬 Chat filters
- 📊 Logging & moderation tools
---
## 🧠 Learning Goals

This project is part of my Python learning journey.
I’m building it step by step

---

## 🤝 Contributing

Not open to contributors yet — just learning and experimenting!

---
## 📜 License
MIT License – feel free to fork and build your own bot!

---