# Our Little New Beginning ♡
> A dreamy blue-themed personal apology & new beginning website.

Built with Python Flask, SQLite, HTML5, and CSS3 animations.
Designed strictly with a **100% Blue Theme** (Midnight Navy, Deep Ocean Blue, Royal Blue, Sky Blue, Ice Blue, Soft Silver, White) with **zero JavaScript**.

---

## ✨ Features
- **Page 1: Welcome (`/`)** – Midnight blue starry ambiance, glowing moon, blue teddy bear, floating hearts & butterflies.
- **Page 2: Apology (`/apology`)** – Sincere handwritten apology letter card with a no-pressure response form saved to SQLite.
- **Page 3: The Magical Gate (`/gate`)** – Pure CSS 3D opening garden gates revealing a peaceful courtyard and heartfelt message.
- **Page 4: A New Beginning (`/beginning`)** – Polaroid starlit frame and inspirational message about respect, patience, and honesty.
- **Page 5: Little Things For You (`/little-things`)** – 4 glassmorphism cards:
  1. *Virtual Gift Box* (Interactive CSS unwrap)
  2. *Our Memories* (Veiled polaroid revealed only on click)
  3. *Reasons to Smile* (Appreciation star cards)
  4. *Secret Letter* (Pure CSS animated envelope with heart wax seal)
- **Page 6: Final Message (`/final`)** – Giant glowing blue heart, lanterns, and blue roses.

---

## 🚀 Running Locally

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application:**
   ```bash
   python app.py
   ```
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## 🌐 Deploy to Render

This repository includes a `render.yaml` Blueprint for fast, zero-hassle deployment on [Render](https://render.com).

### Option 1: Automatic Blueprint (Recommended)
1. Push this repository to your GitHub account.
2. Go to your [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** &rarr; **Blueprint**.
4. Connect this GitHub repository.
5. Render will automatically detect `render.yaml`, configure the environment, and deploy!

### Option 2: Manual Web Service Setup
1. On Render, click **New +** &rarr; **Web Service**.
2. Connect your GitHub repository.
3. Configure settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Click **Deploy Web Service**.

---

## 🎨 Technology Stack
- **Backend:** Python Flask 3.x, SQLite
- **Production Server:** Gunicorn
- **Frontend:** Pure HTML5, CSS3 Keyframes & 3D Perspective Transforms (Zero JS)
