# GitGrade
### Unfold Success from Untold Experiences

**Theme:** AI + Code Analysis + Developer Profiling

---

## The Problem
We noticed a huge gap in the student developer community: **We write code, push it to GitHub, and... silence.** Most of us don't have a mentor to look at our projects and say, *"Hey, your code works, but your folder structure is messy,"* or *"You need to add a requirements.txt file."*

Recruiters look at our profiles and see "spaghetti code," but we don't even know it's bad.

## The Solution: GitGrade
GitGrade is an AI-powered "Repository Mirror." It acts like a strict but helpful Senior Developer. You paste a GitHub link, and it gives you:
1.  **A Score (0-100)** based on industry standards.
2.  **A Summary** of what's good and what's bad.
3.  **A Personalized Roadmap** with actionable steps to fix the code immediately.

---

## How It Works (The Approach)
We built a pipeline that bridges raw GitHub data with Generative AI.

1.  **Data Extraction (The Eyes):** We use the **GitHub API (`PyGithub`)** to fetch real-time data from the repository:
    * File & Folder structure (to check organization).
    * README content (to check documentation).
    * Commit history (to check consistency).
    * Language usage.

2.  **AI Analysis (The Brain):**
    We feed this metadata into **Google Gemini Flash (Latest)**. We engineered a specific prompt that forces the AI to act as a "Senior Reviewer." It parses the code structure and returns a structured JSON evaluation.

3.  **The Interface (The Face):**
    A clean **Flask** web application takes that JSON and renders a dashboard with a visual score circle and a checklist roadmap.

---

##  Tech Stack
* **Backend:** Python, Flask
* **AI Model:** Google Gemini API (via `google-generativeai`)
* **GitHub Integration:** PyGithub Library
* **Frontend:** HTML5, CSS3 (Custom dashboard design)

---
I kept it simple. No complex environments needed.