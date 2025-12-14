# app.py
from flask import Flask, render_template, request
from analyzer import get_repo_data, analyze_with_ai

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        repo_url = request.form.get('repo_url')
        
        # 1. Fetch Data
        repo_data = get_repo_data(repo_url)
        
        if "error" in repo_data:
            return render_template('index.html', error=repo_data['error'])
            
        # 2. Analyze with AI
        analysis_text = analyze_with_ai(repo_data)
        
        # 3. Show Results
        return render_template('index.html', result=analysis_text, repo=repo_data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)