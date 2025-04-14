# 🤖 DiscordStatBot – Discord Bot Module (v2.0)

This module powers the Discord-facing side of DiscordStatBot, allowing admins and players to upload screenshots, parse box scores, and interact with the stats system through chat commands.

---

## 📦 Structure

- `main.py` – Bot launcher and extension loader
- `commands.py` – Public commands (`!parse`, `/leaderboard`)
- `admin.py` – Admin-only commands (`!resend_game`, `!delete_game`)
- `cooldowns.py` – Command rate-limiting logic
- `image_handler.py` – Forwards uploaded images to the OCR API

---

## 🧠 Features

- `!parse` – Upload a screenshot and auto-parse player stats via OCR
- `/leaderboard` – Slash command variant for viewing filtered stats
- 🔐 Admin commands restricted by Discord ID via `.env` (`ADMIN_IDS`)
- 🕒 Cooldowns on high-traffic commands (e.g. `/parse`) to prevent abuse
- ✨ Supports slash and hybrid commands with `@hybrid_command`

---

## 🔧 Setup

1. Configure your `.env` with:
```env
DISCORD_TOKEN=your_bot_token
ADMIN_IDS=1234567890,987654321
OCR_API_URL=http://localhost:8000/ocr
```

2. Run the bot:
```bash
cd bot
python main.py
```

---

## 🔐 Admin Control

- Admin-only commands check `ctx.author.id` against `ADMIN_IDS`
- Unauthorized attempts are logged with warnings

---

## 🔄 Roadmap (v2.1+)

- Add `/mvp`, `/game <id>`, and slash-based filters
- Sync game state back to Discord messages
- Add resync + reparse commands for bulk updates
