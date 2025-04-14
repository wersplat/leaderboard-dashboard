# Leaderboard Dashboard — Bodega Cats GC Edition

A simple Flask web app for displaying team wins/losses in a stylized leaderboard using SQLite.

---

## 🚀 Quick Start (Render)

1. **Create a new Web Service** on [Render](https://render.com)
2. Connect your GitHub repo or upload this project
3. Render will detect `render.yaml` and auto-deploy
4. Set custom domain: `dashboard.bodegacatsgc.gg`
5. Done — your leaderboard is live!

---

## 🐳 Quick Start (Docker)

### Build and run locally:

```bash
git clone https://github.com/YOUR_USERNAME/leaderboard_dashboard.git
cd leaderboard_dashboard

# Build Docker image
docker build -t leaderboard-dashboard .

# Run container
docker run -p 5000:5000 leaderboard-dashboard
```

Then open `http://localhost:5000`

---

## 🧱 Database

Uses `SQLite` with schema defined in `schema.sql`.  
You can re-init the DB by running:

```bash
sqlite3 leaderboard.db < schema.sql
```

---

## 🌐 Customization

- Dashboard style matches **bodegacatsgc.gg**
- Add new teams or update scores in the `teams` table