import pandas as pd
import mysql.connector

# Step 1: Load the CSV file from the absolute path
# Update the file path below if needed.
df = pd.read_csv("C:/Users/Krishanu/Project10/Project10/data/UpdatedResumeDataSet.csv")
df = df.dropna(subset=["Resume"])

# Step 2: Connect to MySQL with your credentials
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CsK@12345",  # Your MySQL root password
    database="resume_analytics"
)
cursor = conn.cursor()

# Step 3: Insert each resume record into the 'applicants' table
for index, row in df.iterrows():
    resume_text = row["Resume"]
    category = row["Category"]
    name = f"Applicant_{index + 1}"  # You can update this to use a proper name if available
    sql = """
        INSERT INTO applicants (name, resume_text, category)
        VALUES (%s, %s, %s)
    """
    values = (name, resume_text, category)
    cursor.execute(sql, values)

conn.commit()
cursor.close()
conn.close()

print("✅ Resumes uploaded successfully!")
