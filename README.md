# Enlightening English

> Literature for the curious. Stories for the world.

A beautifully designed literary exploration app for post-A-level adults who want to revisit the joy of English Literature — without the assignments. Explore novels, poetry, and short stories through juicy untold details, author context, literary craft, modern cultural connections, and reflective tasks. Think book club meets premium streaming service.

Built with Python + Streamlit. Styled like a curated editorial magazine.

---

## Running Locally

**Prerequisites:** Python 3.10+

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd enlightening-english

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Adding New Lessons

Drop a `.json` file into `data/lessons/`. It will appear in the gallery automatically on next load.

Every lesson follows this schema:

```json
{
  "id": "unique-slug",
  "title": "Book Title",
  "author": "Author Name",
  "era": "Period / Movement",
  "cover_image_url": "https://...",
  "hero_image_url": "https://...",
  "tagline": "A one-line essence of the work.",
  "themes": ["theme1", "theme2"],
  "juicy_details": ["Surprising fact 1", "Surprising fact 2"],
  "authors_world": {
    "location": "Where they lived / set the work",
    "description": "Context paragraph.",
    "places_to_visit": [
      { "name": "Place name", "why": "Why it matters / what to see." }
    ]
  },
  "literary_techniques": [
    {
      "technique": "Technique name",
      "example": "How it appears in the text.",
      "world_connection": "Where this technique shows up in modern life."
    }
  ],
  "analysis": "## Markdown heading\n\nParagraph text...",
  "modern_connections": [
    { "type": "film", "title": "Film Title (Year)", "connection": "Why it echoes the text." },
    { "type": "tv",   "title": "Show Title",        "connection": "..." },
    { "type": "song", "title": "Song — Artist",     "connection": "..." }
  ],
  "reflective_tasks": [
    "Find a song that captures the feeling of..."
  ],
  "discussion_questions": [
    "Open question with no right answer?"
  ]
}
```

---

## Deploying to Streamlit Community Cloud (Free)

Streamlit Community Cloud lets you deploy this app from a GitHub repo for free, with a public shareable URL.

### Step 1 — Push to GitHub

1. Create a new repository on [github.com](https://github.com) (can be public or private).
2. Push this project:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Step 2 — Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
2. Click **"New app"**.
3. Select your repository, branch (`main`), and set the **Main file path** to `app.py`.
4. Click **"Deploy!"**

Your app will be live at `https://YOUR_USERNAME-YOUR_REPO_NAME-app-XXXXX.streamlit.app` within about 60 seconds.

### Notes
- The `data/lessons/` folder is committed to the repo, so all lessons deploy automatically.
- To add new lessons after deploying: add the JSON file, commit, and push. Streamlit Cloud redeploys on push.
- If you want to keep lessons private, use a **private** GitHub repo (Streamlit Cloud supports private repos).

---

## Project Structure

```
enlightening-english/
├── app.py              # Main Streamlit application
├── utils.py            # JSON content loader
├── requirements.txt    # Python dependencies
└── data/
    └── lessons/
        └── gatsby.json # Sample lesson: The Great Gatsby
```
