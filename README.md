# ✨ Resume Analyzer Pro - AI Powered 🚀

![demo](assets/demo_banner.png) <!-- Optional banner image -->

A powerful AI-based resume analysis tool built with **Tkinter**, **NLP**, and **custom ATS scoring logic**. Instantly analyze resumes, score them against job descriptions, and provide deep structural and grammar feedback.

---

## 🔍 Features

- 📄 **Upload PDF Resumes**
- 🎯 **Match Resume to 30+ Job Roles**
- 📊 **ATS Compatibility Scoring (0-100)**
- ✅ **Strengths & Weaknesses Highlighted**
- 🧠 **AI-Powered Text & Grammar Suggestions**
- 🖥️ **Tkinter GUI for Smooth Experience**

---

## 🚀 Demo

> Upload your resume & paste a job description to get your score!

![demo-screenshot](assets/demo_screenshot.png)

---

## 📦 Installation

### 🛠️ Requirements
- Python 3.9+
- tkinter
- nltk
- pandas
- PyPDF2
- sentence-transformers
- scikit-learn

### 🔧 Setup


git clone https://github.com/krishanu2/resume-analyzer-pro.git
cd resume-analyzer-pro
pip install -r requirements.txt
python scripts/resume_analyzer_app.py


🧠 How It Works
Text Extraction: Extracts raw text from uploaded PDF.

Job Matching: Uses cosine similarity between job desc and resume content.

Resume Parser: Identifies structure issues, missing sections.

Grammar Analysis: Optional NLP-based checks using spaCy or other tools.


📁 Project Structure
scripts/
│
├── resume_analyzer_app.py        # Main GUI
├── score_ats.py                  # ATS scoring logic
├── resume_parser.py              # Structural analysis logic
├── skill_matcher.py              # Role-based keyword match
└── ...

📄 License
This project is licensed under the MIT License. Feel free to use and modify it for personal or educational purposes.

💡 Future Ideas
Integrate ChatGPT-based improvements.

Export detailed reports as PDF.

Deploy as a web app using Flask or Streamlit.

🙌 Credits
Made with ❤️ by Krishanu Mahapatra
