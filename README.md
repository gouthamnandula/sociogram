<div align="center">

# 📡 Sociogram

**A lightweight, full-stack social media app built with FastAPI & Streamlit.**

Upload moments. Browse feeds. Own your posts.

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![ImageKit](https://img.shields.io/badge/ImageKit-blue?style=flat-square)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **JWT Authentication** | Register and log in securely with `fastapi-users` |
| 📸 **Media Uploads** | Share images and videos with optional captions |
| 🌊 **Shared Feed** | Browse all posts, newest first |
| 🗑️ **Post Ownership** | Delete only your own posts — enforced server-side |
| ⚡ **Async Backend** | Non-blocking DB access with SQLAlchemy async + aiosqlite |
| 📄 **Auto API Docs** | Swagger UI auto-generated at `/docs` |

---

## 🛠️ Tech Stack

**Backend** — FastAPI · fastapi-users · SQLAlchemy async · aiosqlite · Uvicorn

**Frontend** — Streamlit

**Storage** — SQLite (posts & users) · ImageKit (media files)

**Tooling** — `uv` · python-dotenv · Python 3.13+

---

## 📁 Project Structure

```
sm_app/
├── app/
│   ├── app.py        # FastAPI app and API routes
│   ├── db.py         # Database models, engine, sessions
│   ├── images.py     # ImageKit client setup
│   ├── schemas.py    # Pydantic and FastAPI Users schemas
│   └── users.py      # Auth backend and user manager
├── frontend.py       # Streamlit UI
├── main.py           # Backend entry point
├── pyproject.toml    # Project metadata and dependencies
└── uv.lock           # Locked dependencies
```

---

## ⚙️ Setup

### 1. Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
IMAGEKIT_PUBLIC_KEY=your-imagekit-public-key
IMAGEKIT_PRIVATE_KEY=your-imagekit-private-key
IMAGEKIT_URL=https://ik.imagekit.io/your_imagekit_id
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Run the Backend

```bash
uv run python main.py
```

> API → `http://localhost:8000`  
> Swagger docs → `http://localhost:8000/docs`

### 4. Run the Frontend

```bash
uv run streamlit run frontend.py
```

> UI → `http://localhost:8501`

---

## 🔄 How It Works

1. **Sign up or log in** via the Streamlit UI
2. **JWT token** is stored in session state and sent with every protected request
3. **Upload media** → backend sends it to ImageKit, stores metadata in SQLite
4. **Feed** returns all posts in reverse chronological order with ownership info
5. **Delete** your own posts directly from the feed

---

## 🌐 API Routes

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Create a new user |
| `POST` | `/auth/jwt/login` | Log in and receive JWT |
| `POST` | `/auth/forgot-password` | Request password reset |
| `POST` | `/auth/reset-password` | Reset password |
| `POST` | `/auth/verify` | Verify account |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/users/me` | Get current authenticated user |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload image or video with caption |
| `GET` | `/feed` | Fetch all posts |
| `DELETE` | `/posts/{post_id}` | Delete a post you own |

---

## 🚀 Quick Workflow

```
Start backend → Sign up → Log in → Upload media → View feed → Delete posts
```

---

## 🗺️ Roadmap

- [ ] Likes, comments, and user profiles
- [ ] Edit post functionality
- [ ] Feed pagination
- [ ] Improved frontend styling
- [ ] Tests for auth and post routes
- [ ] Docker support
- [ ] Full environment variable configuration

---

## 📝 Notes

- SQLite tables are created automatically on startup
- The frontend is hardcoded to talk to `http://localhost:8000`
- Auth is required for uploading, reading the feed, and deleting posts

---

## 📜 License

No license is currently defined. Add one before sharing or distributing publicly.

---

<div align="center">
  Built with ❤️ using FastAPI + Streamlit
</div>