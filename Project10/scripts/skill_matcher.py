import re

# ✅ Vast Skill Database
SKILL_DB = {
    "Data Scientist": [
        "python", "r", "java", "sql", "scala", "c++",
        "tensorflow", "keras", "pytorch", "scikit-learn", "xgboost", "lightgbm",
        "pandas", "numpy", "matplotlib", "seaborn", "statsmodels", "scipy",
        "nltk", "spacy", "transformers", "textblob", "bert", "gpt",
        "hadoop", "spark", "hive", "airflow", "databricks",
        "excel", "tableau", "power bi", "jupyter", "colab", "sql server",
        "machine learning", "deep learning", "data wrangling", "model deployment",
        "feature engineering", "classification", "regression", "clustering",
        "time series", "dimensionality reduction", "a/b testing", "data visualization"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react", "redux", "bootstrap", "tailwind",
        "material ui", "jquery", "sass", "node.js", "express", "django", "flask",
        "php", "java", "spring", "asp.net", "mongodb", "mysql", "postgresql",
        "sqlite", "redis", "firebase", "git", "github", "npm", "webpack",
        "docker", "nginx", "rest api", "graphql", "jwt", "oauth", "api integration",
        "aws", "azure", "gcp", "vercel", "netlify",
        "jest", "mocha", "chai", "cypress", "selenium",
        "responsive design", "web security", "cross-browser testing", "unit testing"
    ],
    "Business Analyst": [
        "excel", "power bi", "tableau", "sql", "python", "google sheets",
        "looker", "qlik", "sas", "data visualization", "dashboarding",
        "data modeling", "reporting", "kpis", "forecasting", "trend analysis",
        "root cause analysis", "variance analysis", "what-if analysis",
        "pivot tables", "business strategy", "market research", "gap analysis",
        "requirement gathering", "stakeholder management", "crm systems",
        "agile", "scrum", "waterfall", "user stories", "process mapping",
        "bpmn", "sdlc", "erp", "communication", "problem solving",
        "presentation", "time management", "collaboration", "storytelling"
    ]
}

def extract_skills(resume_text, job_role):
    """
    Extract matched and missing skills from a resume for a specific job role.
    """
    text = resume_text.lower()
    required_skills = SKILL_DB.get(job_role, [])
    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        # Simple regex match to ensure full word match
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    total_skills = len(required_skills)
    match_score = (len(matched_skills) / total_skills * 100) if total_skills else 0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score_percent": round(match_score, 2)
    }

# Example (For testing only)
if __name__ == "__main__":
    sample_resume = """
    Experienced Data Scientist skilled in Python, machine learning, pandas, numpy, and Tableau.
    Have worked with TensorFlow and deployed models using Flask.
    """
    job = "Data Scientist"
    result = extract_skills(sample_resume, job)
    print("Matched:", result["matched_skills"])
    print("Missing:", result["missing_skills"])
    print("Score:", result["score_percent"], "%")
