import pandas as pd
import mysql.connector
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CsK@12345",
    database="resume_analytics"
)
cursor = conn.cursor(dictionary=True)

# Load resumes
cursor.execute("SELECT applicant_id, resume_text FROM applicants")
resumes = cursor.fetchall()

# Load job descriptions
cursor.execute("SELECT job_id, description FROM job_descriptions")
jds = cursor.fetchall()

# Load SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Score resumes for each job
results = []
for jd in jds:
    jd_emb = model.encode(jd["description"])
    for res in resumes:
        res_emb = model.encode(res["resume_text"])
        score = float(cosine_similarity([res_emb], [jd_emb])[0][0])
        results.append((res["applicant_id"], jd["job_id"], round(score, 4)))

# Insert match scores
for app_id, job_id, score in results:
    cursor.execute("""
        INSERT INTO match_scores (applicant_id, job_id, score)
        VALUES (%s, %s, %s)
    """, (app_id, job_id, score))

conn.commit()
cursor.close()
conn.close()

print("✅ SBERT match scores inserted!")
