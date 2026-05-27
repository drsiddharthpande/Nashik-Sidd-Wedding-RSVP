# INFO_HOW_TO_RUN.md — Launch Instructions

## Purpose
Step-by-step instructions for running this project locally. Written for a non-coder who can follow explicit steps.

> **Fill this in** when you clone this template. Delete this instruction block when done.

---

## Prerequisites

| Requirement | Version | Install Link |
|-------------|---------|--------------|
| Python | 3.10+ | https://python.org |
| pip | latest | bundled with Python |
| _[Other]_ | _[x.x]_ | _[URL]_ |

---

## Environment Setup

1. **Clone the repo** (or open it if already cloned):
   ```
   cd C:\path\to\your-project
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables** — copy the example file and fill in your keys:
   ```
   copy .env.example .env
   ```
   Then open `.env` and add your API keys.

---

## Running the App

```
[FILL IN — e.g. streamlit run src/app.py]
```

The app will open at: **http://localhost:[PORT]**

---

## Common Errors

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| `KeyError: OPENAI_API_KEY` | Check `.env` file has the key set |
| _[Other error]_ | _[Fix]_ |

---

_Last updated: [YYYY-MM-DD]_
