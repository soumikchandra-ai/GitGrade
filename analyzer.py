import google.generativeai as genai
from github import Github
import json
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 

if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found. Check your .env file.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest') 

def parse_repo_url(url):
    """
    Converts 'https://github.com/owner/project' -> 'owner/project'
    """
    parts = url.rstrip("/").split("/")
    return f"{parts[-2]}/{parts[-1]}"

def get_repo_data(github_url):
    """
    Fetches real data from GitHub, including Commits!
    """
    print(f"--- Fetching data for: {github_url} ---")
    g = Github()
    
    try:
        repo_path = parse_repo_url(github_url)
        repo = g.get_repo(repo_path)
        
        # 1. Get file structure
        contents = repo.get_contents("")
        file_names = [file.name for file in contents]
        
        # 2. Get README
        readme_content = "No README file found."
        try:
            readme = repo.get_readme()
            readme_content = readme.decoded_content.decode("utf-8")
        except:
            pass
            
        # 3. Get Commit Stats
        # I fetch the last 10 commits to check recent activity
        commits = repo.get_commits()
        commit_count = commits.totalCount
        last_commit = commits[0].commit.author.date.strftime("%Y-%m-%d")

        repo_data = {
            "name": repo.name,
            "description": repo.description if repo.description else "No description",
            "files": file_names,
            "readme": readme_content[:4000],
            "commit_count": commit_count,   
            "last_commit": last_commit 
        }
        return repo_data

    except Exception as e:
        return {"error": str(e)}

def analyze_with_ai(repo_data):
    """
    Sends data to AI and expects a JSON response
    """
    print("--- Sending data to AI... ---")
    
    prompt = f"""
    You are a strict Senior Developer Reviewing a student's code.
    Analyze this GitHub Repository:
    
    Project Name: {repo_data['name']}
    Files: {repo_data['files']}
    Description: {repo_data['description']}
    Total Commits: {repo_data['commit_count']}
    Last Commit Date: {repo_data['last_commit']}
    README: {repo_data['readme']}

    Return your response in strictly VALID JSON format with these exact keys:
    {{
        "score": (integer 0-100),
        "summary": (string, 2 sentences. Mention if they commit often or if the project is abandoned),
        "roadmap": (list of strings, actionable steps)
    }}
    
    Do not add markdown formatting like ```json ... ```. Just the raw JSON string.
    """

    try:
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        # Clean up if the AI adds markdown backticks
        if text_response.startswith("```"):
            text_response = text_response.replace("```json", "").replace("```", "")
            
        return json.loads(text_response)
        
    except Exception as e:
        print(f"AI parsing error: {e}")
        return {
            "score": 0,
            "summary": "Error analyzing repo. Please try again.",
            "roadmap": ["Check if the repo is public", "Try again later"]
        }