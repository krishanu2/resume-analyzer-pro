from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util

# Load SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    text = ''
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_ats_score(resume_path, jd_text):
    resume_text = extract_text_from_pdf(resume_path)

    # Create embeddings
    embeddings = model.encode([resume_text, jd_text], convert_to_tensor=True)

    # Calculate cosine similarity
    score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

    # Return score as percentage
    return round(score * 100, 2)

