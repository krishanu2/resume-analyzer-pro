import re
import spacy
import language_tool_python

# Load English model and grammar checker
nlp = spacy.load("en_core_web_sm")
tool = language_tool_python.LanguageTool('en-US')

# Resume sections to search for
SECTION_HEADERS = ["education", "experience", "projects", "skills", "certifications"]

def extract_basic_info(text):
    """Extracts name, email, and phone number from resume text."""
    email = re.findall(r"[\w\.-]+@[\w\.-]+", text)
    phone = re.findall(r"\+?\d[\d\s\-]{8,}\d", text)
    name = text.split("\n")[0] if text else "Unknown"
    return {
        "name": name.strip(),
        "email": email[0] if email else "Not found",
        "phone": phone[0] if phone else "Not found"
    }

def detect_sections(text):
    """Checks presence of key resume sections."""
    found_sections = {}
    for header in SECTION_HEADERS:
        if re.search(rf"\b{header}\b", text.lower()):
            found_sections[header.capitalize()] = "✅ Present"
        else:
            found_sections[header.capitalize()] = "❌ Missing"
    return found_sections

def check_grammar(text):
    """Finds grammar and formatting issues using LanguageTool."""
    matches = tool.check(text)
    suggestions = []
    for match in matches[:10]:  # Limit to top 10 grammar suggestions
        suggestions.append(f"⚠️ {match.context.strip()} → {match.message}")
    return suggestions

def analyze_resume(text):
    """Main function to analyze a resume and return all feedback."""
    basic_info = extract_basic_info(text)
    structure_feedback = detect_sections(text)
    grammar_feedback = check_grammar(text)

    return {
        "basic_info": basic_info,
        "structure": structure_feedback,
        "grammar": grammar_feedback
    }

# Optional testing block
if __name__ == "__main__":
    sample = """
    John Doe
    Email: john.doe@example.com
    Phone: +91 98765 43210

    Education
    B.Tech in Computer Science from XYZ University

    Experience
    Worked on Python development and ML projects.
    """
    report = analyze_resume(sample)

    print("\n📄 Basic Info:")
    for key, val in report["basic_info"].items():
        print(f"  {key.capitalize()}: {val}")

    print("\n📌 Section Check:")
    for section, status in report["structure"].items():
        print(f"  - {section}: {status}")

    print("\n🔍 Grammar Issues:")
    for issue in report["grammar"]:
        print(" ", issue)
