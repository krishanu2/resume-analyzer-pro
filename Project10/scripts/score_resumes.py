import pandas as pd
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CsK@12345",  # Update this if needed
    database="resume_analytics"
)
cursor = conn.cursor(dictionary=True)

# 2. Fetch resumes
cursor.execute("SELECT applicant_id, resume_text FROM applicants")
resumes = cursor.fetchall()

# 3. Fetch job descriptions
cursor.execute("SELECT job_id, description FROM job_descriptions")
jobs = cursor.fetchall()

# 4. Build list of (applicant_id, job_id, resume_text, jd_text)
pairs = []
for job in jobs:
    for resume in resumes:
        pairs.append({
            'applicant_id': resume['applicant_id'],
            'job_id': job['job_id'],
            'resume_text': resume['resume_text'],
            'jd_text': job['description']
        })

# 5. Score each resume–JD pair using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')

match_results = []
for pair in pairs:
    tfidf_matrix = vectorizer.fit_transform([pair['resume_text'], pair['jd_text']])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    match_results.append({
        'applicant_id': pair['applicant_id'],
        'job_id': pair['job_id'],
        'score': round(float(score), 4)
    })

# 6. Insert scores into match_scores table
for result in match_results:
    cursor.execute("""
        INSERT INTO match_scores (applicant_id, job_id, score)
        VALUES (%s, %s, %s)
    """, (result['applicant_id'], result['job_id'], result['score']))

conn.commit()
cursor.close()
conn.close()

print("✅ All match scores inserted into match_scores table!")
