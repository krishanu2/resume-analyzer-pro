import tkinter as tk
from tkinter import filedialog, ttk
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util
import mysql.connector

# Load SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CsK@12345",
    database="resume_analytics"
)
cursor = conn.cursor()

# Fetch job descriptions
cursor.execute("SELECT job_id, title, description FROM job_descriptions")
jobs = cursor.fetchall()
job_dict = {title: (job_id, desc) for job_id, title, desc in jobs}

# Tkinter app setup
app = tk.Tk()
app.title("Resume Matcher with ATS Score")
app.geometry("650x500")
app.configure(bg="#f8f8f8")

resume_text = ""
resume_name = ""  # To identify user

# --- Functions ---

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def upload_pdf():
    global resume_text, resume_name
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not path:
        return
    resume_text = extract_text_from_pdf(path)
    resume_name = path.split("/")[-1].split(".")[0]  # Use file name as name
    status_label.config(text=f"📄 Uploaded: {resume_name}")

def calculate_match():
    global resume_text, resume_name

    selected_job = job_combo.get()
    if not selected_job or not resume_text:
        status_label.config(text="⚠️ Upload resume and select job role.")
        return

    job_id, job_desc = job_dict[selected_job]
    job_emb = model.encode(job_desc)
    resume_emb = model.encode(resume_text)
    score = float(util.cos_sim(resume_emb, job_emb)[0][0]) * 100

    # Insert resume into applicants table
    cursor.execute("INSERT INTO applicants (name, resume_text, category) VALUES (%s, %s, %s)", 
                   (resume_name, resume_text, selected_job))
    conn.commit()
    applicant_id = cursor.lastrowid

    # Insert score into match_scores
    cursor.execute("INSERT INTO match_scores (applicant_id, job_id, score) VALUES (%s, %s, %s)",
                   (applicant_id, job_id, score))
    conn.commit()

    # Update treeview
    tree.delete(*tree.get_children())
    tree.insert("", "end", values=(selected_job, f"{score:.2f}%"))

    # Status feedback
    if score > 80:
        status = "✅ Excellent match!"
    elif score > 60:
        status = "⚠️ Good match, minor tweaks needed."
    else:
        status = "❌ Low match. Consider improving your resume."

    status_label.config(text=f"ATS Score: {score:.2f}% — {status}\n✔️ Data saved to database.")

# --- UI Widgets ---

tk.Label(app, text="Upload Resume (PDF):", bg="#f8f8f8", font=("Helvetica", 11)).pack(pady=5)
tk.Button(app, text="Choose PDF", command=upload_pdf, bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=5)

tk.Label(app, text="Select Job Role:", bg="#f8f8f8", font=("Helvetica", 11)).pack(pady=5)
job_combo = ttk.Combobox(app, values=list(job_dict.keys()), width=50, font=("Helvetica", 10))
job_combo.pack(pady=5)

tk.Button(app, text="Check ATS Score", command=calculate_match, bg="#007acc", fg="white", font=("Helvetica", 12)).pack(pady=10)

tree = ttk.Treeview(app, columns=("Job Title", "ATS Score"), show="headings", height=5)
tree.heading("Job Title", text="Job Title")
tree.heading("ATS Score", text="ATS Score")
tree.column("Job Title", width=300)
tree.column("ATS Score", width=100)
tree.pack(pady=10)

status_label = tk.Label(app, text="", bg="#f8f8f8", font=("Helvetica", 11), fg="green")
status_label.pack(pady=10)

app.mainloop()
